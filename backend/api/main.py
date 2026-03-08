"""
MetaMind FastAPI Backend

REST API for the MetaMind autonomous AI pipeline designer.
"""

import os
import uuid
import time
import threading
import asyncio
import json
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import uvicorn

from ..orchestration.graph import create_orchestrator
from ..agents.versioning_agent import VersioningAgent
from ..agents.code_generator_agent import CodeGeneratorAgent
from ..demo_data import get_demo_scenario, get_all_demo_scenarios
from ..utils.logging_config import AgentLogger


# Status constants
STATUS_STARTING = "starting"
STATUS_PROCESSING = "processing"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"

# Status to exception mapping
STATUS_EXCEPTIONS = {
    STATUS_PROCESSING: (400, "Design is still processing"),
    STATUS_STARTING: (400, "Design is still starting"),
    STATUS_FAILED: (500, "Design failed"),
}


# Pydantic models for request/response
class DesignRequest(BaseModel):
    """Request model for design endpoint."""
    business_goal: str = Field(..., description="Clear description of the system's purpose")
    domain: str = Field(..., description="Application domain (healthcare, finance, ecommerce, education, legal, general)")
    modalities: List[str] = Field(..., description="Data types to handle (text, vision, multimodal, tabular)")
    constraints: Dict[str, Any] = Field(..., description="System constraints")
    max_iterations: int = Field(default=5, ge=1, le=10, description="Maximum improvement iterations")


class DesignResponse(BaseModel):
    """Response model for design endpoint."""
    run_id: str
    status: str
    message: str


class StatusResponse(BaseModel):
    """Response model for status endpoint."""
    run_id: str
    status: str
    version: int
    current_iteration: int
    max_iterations: int
    errors: List[str]
    warnings: List[str]


class ResultResponse(BaseModel):
    """Response model for result endpoint."""
    run_id: str
    version: int
    selected_architecture: Dict[str, Any]
    metrics: Dict[str, float]
    score: float
    reflection: Dict[str, Any]
    executive_report: Optional[str] = None
    technical_specification: Optional[str] = None
    deployment_plan: Optional[str] = None
    monitoring_strategy: Optional[str] = None


class VersionResponse(BaseModel):
    """Response model for version list endpoint."""
    run_id: str
    versions: List[Dict[str, Any]]


class ComparisonResponse(BaseModel):
    """Response model for comparison endpoint."""
    run_id: str
    version_1: int
    version_2: int
    comparison: Dict[str, Any]


class HistoryResponse(BaseModel):
    """Response model for history endpoint."""
    total: int
    runs: List[Dict[str, Any]]


# Initialize FastAPI app
app = FastAPI(
    title="MetaMind API",
    description="Autonomous AI Pipeline Designer & Self-Optimizing Architecture Engine",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include code editor router
from .code_editor_endpoints import router as code_editor_router
app.include_router(code_editor_router)

# Initialize components
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
DB_PATH = os.getenv("DB_PATH", "./metamind.db")

# Global orchestrator (in production, use dependency injection)
orchestrator = None
versioning_agent = VersioningAgent(db_path=DB_PATH)

# Store for active design sessions
active_designs = {}  # {run_id: {"status": str, "result": dict, "error": str, "progress": dict}}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_architecture_blueprint(run_id: str) -> Dict[str, Any]:
    """
    Retrieve architecture blueprint for a given run_id.
    
    Checks active_designs first, then falls back to database.
    
    Args:
        run_id: The run identifier
        
    Returns:
        Dict containing the architecture blueprint
        
    Raises:
        HTTPException: If run not found or not completed
    """
    # Check active designs first
    if run_id in active_designs:
        design_status = active_designs[run_id]
        if design_status["status"] != STATUS_COMPLETED:
            raise HTTPException(
                status_code=400,
                detail="Design must be completed before accessing blueprint"
            )
        result = design_status["result"]
        return result.get("selected_architecture", {})
    
    # Fall back to database
    run = versioning_agent.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    versions = versioning_agent.get_architecture_versions(run_id)
    if not versions:
        raise HTTPException(status_code=404, detail="No versions found")
    
    final_version = versions[-1]
    return json.loads(final_version["architecture_json"])


def parse_json_field(json_string: str) -> Dict[str, Any]:
    """
    Safely parse a JSON string field.
    
    Args:
        json_string: JSON string to parse
        
    Returns:
        Parsed dictionary
        
    Raises:
        HTTPException: If JSON parsing fails
    """
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse JSON data: {str(e)}"
        )


def build_result_response(
    run_id: str,
    version: int,
    architecture: Dict[str, Any],
    metrics: Dict[str, float],
    score: float,
    reflection: Dict[str, Any],
    executive_report: Optional[str] = None,
    technical_specification: Optional[str] = None,
    deployment_plan: Optional[str] = None,
    monitoring_strategy: Optional[str] = None
) -> ResultResponse:
    """
    Build a standardized ResultResponse object.
    
    Args:
        run_id: Run identifier
        version: Architecture version number
        architecture: Selected architecture dictionary
        metrics: Performance metrics
        score: Final score
        reflection: Reflection feedback
        executive_report: Optional executive report
        technical_specification: Optional technical spec
        deployment_plan: Optional deployment plan
        monitoring_strategy: Optional monitoring strategy
        
    Returns:
        ResultResponse object
    """
    return ResultResponse(
        run_id=run_id,
        version=version,
        selected_architecture=architecture,
        metrics=metrics,
        score=score,
        reflection=reflection,
        executive_report=executive_report,
        technical_specification=technical_specification,
        deployment_plan=deployment_plan,
        monitoring_strategy=monitoring_strategy
    )

# Store for log streams (SSE)
log_streams = {}  # {run_id: {"logs": [], "connected": bool}}


def get_orchestrator():
    """Get or create orchestrator instance."""
    global orchestrator
    if orchestrator is None:
        orchestrator = create_orchestrator(
            ollama_base_url=OLLAMA_BASE_URL,
            model_name=OLLAMA_MODEL,
            db_path=DB_PATH
        )
    return orchestrator


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "MetaMind API",
        "version": "1.0.0",
        "description": "Autonomous AI Pipeline Designer & Self-Optimizing Architecture Engine",
        "endpoints": {
            "design": "POST /api/design",
            "status": "GET /api/design/{run_id}/status",
            "result": "GET /api/design/{run_id}/result",
            "versions": "GET /api/design/{run_id}/versions",
            "compare": "GET /api/design/{run_id}/compare/{v1}/{v2}",
            "specification": "GET /api/design/{run_id}/specification",
            "history": "GET /api/history",
            "health": "GET /health",
            "docs": "GET /docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "ollama_url": OLLAMA_BASE_URL,
        "model": OLLAMA_MODEL,
        "database": DB_PATH
    }


def update_progress(run_id: str, stage: str, message: str, details: dict = None):
    """Update progress for a design session."""
    if run_id in active_designs:
        if "progress" not in active_designs[run_id]:
            active_designs[run_id]["progress"] = {
                "stages": [],
                "current_stage": "",
                "current_message": "",
                "details": {}
            }
        
        active_designs[run_id]["progress"]["stages"].append({
            "stage": stage,
            "message": message,
            "timestamp": time.time()
        })
        active_designs[run_id]["progress"]["current_stage"] = stage
        active_designs[run_id]["progress"]["current_message"] = message
        if details:
            active_designs[run_id]["progress"]["details"].update(details)
        
        # Also add to log stream for SSE
        add_log_to_stream(run_id, "INFO", "Progress", message)


def add_log_to_stream(run_id: str, level: str, agent: str, message: str):
    """Add a log entry to the stream for SSE."""
    if run_id not in log_streams:
        log_streams[run_id] = {"logs": [], "connected": False}
    
    log_entry = {
        "timestamp": time.time(),
        "level": level,
        "agent": agent,
        "message": message
    }
    
    log_streams[run_id]["logs"].append(log_entry)
    
    # Keep only last 1000 logs to prevent memory issues
    if len(log_streams[run_id]["logs"]) > 1000:
        log_streams[run_id]["logs"] = log_streams[run_id]["logs"][-1000:]


def stream_callback_factory(run_id: str):
    """Create a streaming callback for a specific run_id."""
    def callback(level: str, agent: str, message: str):
        add_log_to_stream(run_id, level, agent, message)
    return callback


def run_design_pipeline(run_id: str, request: DesignRequest):
    """Run the design pipeline in background with progress tracking and log streaming."""
    try:
        active_designs[run_id]["status"] = "processing"
        update_progress(run_id, "initialization", "🚀 Starting MetaMind pipeline...")
        
        # Register streaming callback for this run
        AgentLogger.register_stream_callback(run_id, stream_callback_factory(run_id))
        
        # Get orchestrator
        orch = get_orchestrator()
        update_progress(run_id, "orchestrator", "✓ Orchestrator initialized")
        
        # Track progress through pipeline
        update_progress(run_id, "requirements", "📋 Analyzing your requirements...", {
            "domain": request.domain,
            "goal": request.business_goal
        })
        
        # Create progress callback
        def progress_callback(stage: str, message: str):
            update_progress(run_id, stage, message)
        
        # Run design pipeline with progress tracking
        result = orch.design(
            business_goal=request.business_goal,
            domain=request.domain,
            modalities=request.modalities,
            constraints=request.constraints,
            max_iterations=request.max_iterations,
            progress_callback=progress_callback
        )
        
        update_progress(run_id, "completed", "✅ Design complete!", {
            "architecture": result.get("selected_architecture", {}).get("name", "Unknown"),
            "score": result.get("score", 0),
            "version": result.get("version", 1)
        })
        
        # Store result
        active_designs[run_id]["status"] = "completed"
        active_designs[run_id]["result"] = result
        
    except Exception as e:
        active_designs[run_id]["status"] = "failed"
        active_designs[run_id]["error"] = str(e)
        update_progress(run_id, "failed", f"❌ Design failed: {str(e)}")
    
    finally:
        # Unregister streaming callback
        AgentLogger.unregister_stream_callback(run_id)
        
        # Mark stream as completed
        if run_id in log_streams:
            add_log_to_stream(run_id, "INFO", "System", "🏁 Pipeline execution completed")


@app.post("/api/design", response_model=DesignResponse)
async def start_design(request: DesignRequest, background_tasks: BackgroundTasks):
    """
    Start a new architecture design session (async).
    
    This endpoint initiates the complete multi-agent pipeline in the background:
    1. Parse requirements
    2. Generate candidate architectures
    3. Simulate and score
    4. Select optimal design
    5. Reflect and iterate if needed
    6. Generate documentation
    
    Returns immediately with a run_id. Use /api/design/{run_id}/status to check progress.
    """
    try:
        # Validate domain
        valid_domains = ["healthcare", "finance", "ecommerce", "education", "legal", "general"]
        if request.domain not in valid_domains:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid domain. Must be one of: {', '.join(valid_domains)}"
            )
        
        # Validate modalities
        valid_modalities = ["text", "vision", "multimodal", "tabular"]
        for modality in request.modalities:
            if modality not in valid_modalities:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid modality '{modality}'. Must be one of: {', '.join(valid_modalities)}"
                )
        
        # Generate run_id
        run_id = str(uuid.uuid4())
        
        # Initialize status with progress tracking
        active_designs[run_id] = {
            "status": "starting",
            "result": None,
            "error": None,
            "progress": {
                "stages": [],
                "current_stage": "initialization",
                "current_message": "Initializing design pipeline...",
                "details": {}
            }
        }
        
        # Start background task
        background_tasks.add_task(run_design_pipeline, run_id, request)
        
        return DesignResponse(
            run_id=run_id,
            status="processing",
            message="Design pipeline started. Use /api/design/{run_id}/status to check progress."
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Design failed: {str(e)}")


@app.post("/api/demo/design", response_model=DesignResponse)
async def start_demo_design(domain: str = Query(..., description="Demo domain (healthcare or ecommerce)")):
    """
    Start a demo design with pre-cached results for instant response.
    
    This endpoint returns immediate results without running the full pipeline,
    perfect for demonstrations and testing the UI.
    """
    try:
        # Get demo scenario
        demo = get_demo_scenario(domain)
        if not demo:
            available = get_all_demo_scenarios()
            raise HTTPException(
                status_code=400,
                detail=f"Invalid demo domain. Available: {', '.join(available)}"
            )
        
        run_id = demo["run_id"]
        
        # Store demo result in active_designs
        active_designs[run_id] = {
            "status": "completed",
            "result": demo["result"],
            "error": None,
            "progress": {
                "stages": [
                    {"stage": "demo", "message": "✨ Demo mode - instant results!", "timestamp": time.time()}
                ],
                "current_stage": "completed",
                "current_message": "Demo design completed instantly",
                "details": {"demo": True, "domain": domain}
            }
        }
        
        return DesignResponse(
            run_id=run_id,
            status="completed",
            message=f"Demo design completed! This is a pre-cached {domain} scenario."
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo failed: {str(e)}")


@app.get("/api/demo/scenarios")
async def get_demo_scenarios():
    """Get list of available demo scenarios."""
    return {
        "scenarios": [
            {
                "domain": "healthcare",
                "title": "Patient Monitoring System",
                "description": "AI-powered real-time patient vital signs monitoring with anomaly detection",
                "features": ["Real-time processing", "HIPAA compliant", "Alert system"]
            },
            {
                "domain": "ecommerce",
                "title": "Product Recommendation Engine",
                "description": "Personalized product recommendations using collaborative filtering and vision AI",
                "features": ["Sub-200ms latency", "Multi-modal", "A/B testing"]
            }
        ]
    }


@app.get("/api/design/{run_id}/status", response_model=StatusResponse)
async def get_design_status(run_id: str):
    """
    Get the current status of a design session.
    
    Returns information about the design progress, current version,
    and any errors or warnings.
    """
    try:
        # Check if design is still processing
        if run_id in active_designs:
            design_status = active_designs[run_id]
            
            if design_status["status"] == "processing" or design_status["status"] == "starting":
                return StatusResponse(
                    run_id=run_id,
                    status="processing",
                    version=0,
                    current_iteration=0,
                    max_iterations=5,
                    errors=[],
                    warnings=[]
                )
            elif design_status["status"] == "failed":
                return StatusResponse(
                    run_id=run_id,
                    status="failed",
                    version=0,
                    current_iteration=0,
                    max_iterations=5,
                    errors=[design_status.get("error", "Unknown error")],
                    warnings=[]
                )
            elif design_status["status"] == "completed" and design_status["result"]:
                # Design completed, return completed status
                result = design_status["result"]
                return StatusResponse(
                    run_id=run_id,
                    status="completed",
                    version=result.get("version", 1),
                    current_iteration=result.get("version", 1),
                    max_iterations=5,
                    errors=[],
                    warnings=[]
                )
        
        # Get run from database (for old runs not in active_designs)
        run = versioning_agent.get_run(run_id)
        
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        
        # Get versions to determine current state
        versions = versioning_agent.get_architecture_versions(run_id)
        
        return StatusResponse(
            run_id=run_id,
            status=run["status"],
            version=len(versions),
            current_iteration=len(versions),
            max_iterations=5,  # Default, should be stored in run
            errors=[],
            warnings=[]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")


@app.get("/api/design/{run_id}/progress")
async def get_design_progress(run_id: str):
    """
    Get real-time progress updates for a design session.
    
    Returns detailed progress information including current stage,
    messages, and execution details.
    """
    try:
        if run_id not in active_designs:
            raise HTTPException(status_code=404, detail="Run not found")
        
        design_status = active_designs[run_id]
        progress = design_status.get("progress", {
            "stages": [],
            "current_stage": "unknown",
            "current_message": "No progress information available",
            "details": {}
        })
        
        return {
            "run_id": run_id,
            "status": design_status["status"],
            "progress": progress
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get progress: {str(e)}")


@app.get("/api/design/{run_id}/logs/stream")
async def stream_logs(run_id: str):
    """
    Stream real-time logs from agents during design execution.
    
    Uses Server-Sent Events (SSE) to push log messages to the frontend
    as they are generated by agents during the design pipeline execution.
    
    Returns:
        StreamingResponse: SSE stream of log messages
    """
    async def event_generator():
        """Generate SSE events from log stream."""
        # Initialize log stream if not exists
        if run_id not in log_streams:
            log_streams[run_id] = {"logs": [], "connected": True}
        else:
            log_streams[run_id]["connected"] = True
        
        # Send initial connection message
        yield f"data: {json.dumps({'type': 'connected', 'run_id': run_id})}\n\n"
        
        # Track last sent log index
        last_index = 0
        
        try:
            # Stream logs until design is complete or client disconnects
            while True:
                # Check if design is still active
                if run_id in active_designs:
                    status = active_designs[run_id]["status"]
                    
                    # Send any new logs
                    if run_id in log_streams:
                        logs = log_streams[run_id]["logs"]
                        
                        # Send new logs since last check
                        for i in range(last_index, len(logs)):
                            log_entry = logs[i]
                            yield f"data: {json.dumps({'type': 'log', **log_entry})}\n\n"
                        
                        last_index = len(logs)
                    
                    # If design is complete or failed, send final message and close
                    if status in ["completed", "failed"]:
                        yield f"data: {json.dumps({'type': 'complete', 'status': status})}\n\n"
                        break
                else:
                    # Design not found in active_designs, might be old run
                    yield f"data: {json.dumps({'type': 'error', 'message': 'Design session not found'})}\n\n"
                    break
                
                # Wait before checking for new logs
                await asyncio.sleep(0.5)
        
        except asyncio.CancelledError:
            # Client disconnected
            if run_id in log_streams:
                log_streams[run_id]["connected"] = False
        
        finally:
            # Cleanup
            if run_id in log_streams:
                log_streams[run_id]["connected"] = False
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )


@app.get("/api/design/{run_id}/result", response_model=ResultResponse)
async def get_design_result(run_id: str) -> ResultResponse:
    """
    Get the final design result.
    
    Returns the selected architecture, metrics, reflection feedback,
    and generated documentation.
    
    Args:
        run_id: The run identifier
        
    Returns:
        ResultResponse with complete design results
        
    Raises:
        HTTPException: If run not found, still processing, or failed
    """
    try:
        # Check active designs first
        if run_id in active_designs:
            design_status = active_designs[run_id]
            status = design_status["status"]
            
            # Check for non-completed statuses
            if status in [STATUS_PROCESSING, STATUS_STARTING]:
                raise HTTPException(status_code=400, detail="Design is still processing")
            elif status == STATUS_FAILED:
                error_msg = design_status.get("error", "Unknown error")
                raise HTTPException(status_code=500, detail=f"Design failed: {error_msg}")
            
            # Handle completed status
            if status == STATUS_COMPLETED and design_status.get("result"):
                result = design_status["result"]
                selected_arch = result.get("selected_architecture", {})
                
                # Extract score (check both locations for backward compatibility)
                score = result.get("score") or selected_arch.get("final_score", 0.0)
                
                # Extract metrics (check both locations for backward compatibility)
                metrics = result.get("metrics") or selected_arch.get("estimated_metrics", {})
                
                return build_result_response(
                    run_id=run_id,
                    version=result.get("version", 1),
                    architecture=selected_arch,
                    metrics=metrics,
                    score=score,
                    reflection=result.get("reflection", {}),
                    executive_report=result.get("executive_report"),
                    technical_specification=result.get("technical_specification"),
                    deployment_plan=result.get("deployment_plan"),
                    monitoring_strategy=result.get("monitoring_strategy")
                )
        
        # Get run from database (for old runs not in active_designs)
        run = versioning_agent.get_run(run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        
        # Get final version
        versions = versioning_agent.get_architecture_versions(run_id)
        if not versions:
            raise HTTPException(status_code=404, detail="No versions found for this run")
        
        final_version = versions[-1]
        
        # Parse JSON fields using helper
        architecture = parse_json_field(final_version["architecture_json"])
        metrics = parse_json_field(final_version["metrics_json"])
        
        # Build response with default reflection (should be stored in future)
        return build_result_response(
            run_id=run_id,
            version=final_version["version"],
            architecture=architecture,
            metrics=metrics,
            score=final_version["score"],
            reflection={
                "confidence_score": 0.85,
                "strengths": [],
                "weaknesses": [],
                "improvement_suggestions": []
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get result: {str(e)}")


@app.get("/api/design/{run_id}/versions", response_model=VersionResponse)
async def get_design_versions(run_id: str):
    """
    Get all architecture versions for a design session.
    
    Returns the complete version history with metrics and changes.
    """
    try:
        # Get versions from database
        versions = versioning_agent.get_architecture_versions(run_id)
        
        if not versions:
            raise HTTPException(status_code=404, detail="No versions found for this run")
        
        return VersionResponse(
            run_id=run_id,
            versions=versions
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get versions: {str(e)}")


@app.get("/api/design/{run_id}/compare/{v1}/{v2}", response_model=ComparisonResponse)
async def compare_versions(run_id: str, v1: int, v2: int):
    """
    Compare two architecture versions.
    
    Returns metric deltas, score improvements, and change summary.
    """
    try:
        # Get versions from database
        version1 = versioning_agent.get_version(run_id, v1)
        version2 = versioning_agent.get_version(run_id, v2)
        
        if not version1 or not version2:
            raise HTTPException(status_code=404, detail="One or both versions not found")
        
        # Calculate comparison
        import json
        metrics1 = json.loads(version1["metrics_json"])
        metrics2 = json.loads(version2["metrics_json"])
        
        metric_deltas = {}
        for metric in metrics1.keys():
            metric_deltas[metric] = metrics2.get(metric, 0) - metrics1.get(metric, 0)
        
        comparison = {
            "score_delta": version2["score"] - version1["score"],
            "metric_deltas": metric_deltas,
            "changes_made": json.loads(version2["changes_made"]) if version2["changes_made"] else [],
            "recommendation": "Improvement" if version2["score"] > version1["score"] else "Regression"
        }
        
        return ComparisonResponse(
            run_id=run_id,
            version_1=v1,
            version_2=v2,
            comparison=comparison
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to compare versions: {str(e)}")

# ============================================================================
# CODE GENERATION ENDPOINTS
# ============================================================================

class CodeGenerationRequest(BaseModel):
    """Request model for code generation."""
    project_name: str = Field(..., description="Name of the project to generate")


class CodeGenerationResponse(BaseModel):
    """Response model for code generation."""
    status: str
    project_id: str
    project_path: str
    files_generated: List[str]
    architecture_type: str
    message: str
    download_url: Optional[str] = None


class CodeFileResponse(BaseModel):
    """Response model for code file listing."""
    files: List[Dict[str, Any]]
    total_files: int


# Store for generated projects (in production, use persistent storage)
generated_projects: Dict[str, Dict[str, Any]] = {}


@app.post("/api/design/{run_id}/generate-code", response_model=CodeGenerationResponse)
async def generate_code(
    run_id: str,
    request: CodeGenerationRequest,
    background_tasks: BackgroundTasks
) -> CodeGenerationResponse:
    """
    Generate production-ready code from architecture blueprint.
    
    This endpoint:
    1. Retrieves the architecture blueprint for the run
    2. Generates complete project files using templates
    3. Creates a downloadable ZIP archive
    4. Returns file listing and download link
    
    Args:
        run_id: The run identifier
        request: Code generation request with project name
        background_tasks: FastAPI background tasks
        
    Returns:
        CodeGenerationResponse with generation results
        
    Raises:
        HTTPException: If generation fails or run not found
    """
    try:
        # Get the architecture blueprint using helper function
        architecture_blueprint = get_architecture_blueprint(run_id)
        
        # Generate code
        generator = CodeGeneratorAgent()
        generation_result = generator.generate_code(
            architecture_blueprint=architecture_blueprint,
            project_name=request.project_name
        )
        
        if generation_result["status"] == "error":
            raise HTTPException(status_code=500, detail=generation_result["message"])
        
        # Create ZIP archive
        project_path = Path(generation_result["project_path"])
        zip_path = generator.create_zip_archive(project_path)
        
        # Store project info
        project_id = f"{run_id}_{request.project_name.lower().replace(' ', '_')}"
        generated_projects[project_id] = {
            "run_id": run_id,
            "project_name": request.project_name,
            "project_path": str(project_path),
            "zip_path": str(zip_path),
            "files_generated": generation_result["files_generated"],
            "architecture_type": generation_result["architecture_type"],
            "timestamp": time.time()
        }
        
        return CodeGenerationResponse(
            status="success",
            project_id=project_id,
            project_path=str(project_path),
            files_generated=generation_result["files_generated"],
            architecture_type=generation_result["architecture_type"],
            message=generation_result["message"],
            download_url=f"/api/design/{run_id}/download/{project_id}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code generation failed: {str(e)}")


@app.get("/api/design/{run_id}/code-files/{project_id}", response_model=CodeFileResponse)
async def get_code_files(run_id: str, project_id: str):
    """
    Get list of generated code files with content preview.
    
    Returns file tree structure with file sizes and preview content.
    """
    try:
        if project_id not in generated_projects:
            raise HTTPException(status_code=404, detail="Generated project not found")
        
        project_info = generated_projects[project_id]
        project_path = Path(project_info["project_path"])
        
        if not project_path.exists():
            raise HTTPException(status_code=404, detail="Project directory not found")
        
        # Build file tree
        files = []
        for file_path in project_path.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(project_path)
                
                # Read file content (limit to 500 chars for preview)
                try:
                    content = file_path.read_text()
                    preview = content[:500] + "..." if len(content) > 500 else content
                except:
                    preview = "[Binary file]"
                
                files.append({
                    "path": str(relative_path),
                    "size": file_path.stat().st_size,
                    "preview": preview,
                    "full_content": content if len(content) < 10000 else None  # Only include full content for small files
                })
        
        return CodeFileResponse(
            files=files,
            total_files=len(files)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get code files: {str(e)}")


@app.get("/api/design/{run_id}/download/{project_id}")
async def download_project(run_id: str, project_id: str):
    """
    Download generated project as ZIP archive.
    
    Returns the ZIP file for download.
    """
    try:
        from fastapi.responses import FileResponse
        
        if project_id not in generated_projects:
            raise HTTPException(status_code=404, detail="Generated project not found")
        
        project_info = generated_projects[project_id]
        zip_path = Path(project_info["zip_path"])
        
        if not zip_path.exists():
            raise HTTPException(status_code=404, detail="ZIP file not found")
        
        return FileResponse(
            path=str(zip_path),
            media_type="application/zip",
            filename=f"{project_info['project_name'].replace(' ', '_')}.zip"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download project: {str(e)}")




@app.get("/api/design/{run_id}/specification")
async def get_specification(run_id: str):
    """
    Get the complete architecture specification.
    
    Returns all generated documentation as a single package.
    """
    try:
        # Get run and final version
        run = versioning_agent.get_run(run_id)
        
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        
        versions = versioning_agent.get_architecture_versions(run_id)
        
        if not versions:
            raise HTTPException(status_code=404, detail="No versions found")
        
        final_version = versions[-1]
        
        import json
        architecture = json.loads(final_version["architecture_json"])
        
        # Generate specification package
        specification = {
            "run_id": run_id,
            "business_goal": run["business_goal"],
            "domain": run["domain"],
            "architecture": architecture,
            "score": final_version["score"],
            "metrics": json.loads(final_version["metrics_json"]),
            "executive_summary": "Generated executive summary...",
            "technical_specification": "Generated technical specification...",
            "deployment_plan": "Generated deployment plan...",
            "monitoring_strategy": "Generated monitoring strategy..."
        }
        
        return specification
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get specification: {str(e)}")


@app.get("/api/history", response_model=HistoryResponse)
async def get_history(
    limit: int = Query(50, ge=1, le=100, description="Maximum number of runs to return"),
    offset: int = Query(0, ge=0, description="Number of runs to skip")
):
    """
    Get design session history.
    
    Returns a paginated list of all design sessions.
    """
    try:
        runs = versioning_agent.get_all_runs(limit=limit, offset=offset)
        
        # Get total count (simplified)
        all_runs = versioning_agent.get_all_runs(limit=1000)
        total = len(all_runs)
        
        return HistoryResponse(
            total=total,
            runs=runs
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")


@app.get("/api/graph")
async def get_graph_visualization():
    """
    Get a visualization of the pipeline graph.
    
    Returns a text representation of the multi-agent workflow.
    """
    orch = get_orchestrator()
    return {
        "graph": orch.get_graph_visualization()
    }


if __name__ == "__main__":
    # Run the server
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)