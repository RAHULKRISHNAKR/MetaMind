"""
MetaMind FastAPI Backend

REST API for the MetaMind autonomous AI pipeline designer.
"""

import os
import uuid
import time
import threading
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from ..orchestration.graph import create_orchestrator
from ..agents.versioning_agent import VersioningAgent


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

# Initialize components
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
DB_PATH = os.getenv("DB_PATH", "./metamind.db")

# Global orchestrator (in production, use dependency injection)
orchestrator = None
versioning_agent = VersioningAgent(db_path=DB_PATH)

# Store for active design sessions
active_designs = {}  # {run_id: {"status": str, "result": dict, "error": str, "progress": dict}}


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


def run_design_pipeline(run_id: str, request: DesignRequest):
    """Run the design pipeline in background with progress tracking."""
    try:
        active_designs[run_id]["status"] = "processing"
        update_progress(run_id, "initialization", "🚀 Starting MetaMind pipeline...")
        
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


@app.get("/api/design/{run_id}/result", response_model=ResultResponse)
async def get_design_result(run_id: str):
    """
    Get the final design result.
    
    Returns the selected architecture, metrics, reflection feedback,
    and generated documentation.
    """
    try:
        # Check if design is in active_designs first
        if run_id in active_designs:
            design_status = active_designs[run_id]
            
            if design_status["status"] == "completed" and design_status["result"]:
                # Return result from active_designs
                result = design_status["result"]
                selected_arch = result.get("selected_architecture", {})
                
                # Extract score from selected_architecture if not at top level
                score = result.get("score", 0.0)
                if score == 0.0 and selected_arch.get("final_score"):
                    score = selected_arch.get("final_score", 0.0)
                
                # Extract metrics from selected_architecture if not at top level
                metrics = result.get("metrics", {})
                if not metrics and selected_arch.get("estimated_metrics"):
                    metrics = selected_arch.get("estimated_metrics", {})
                
                return ResultResponse(
                    run_id=run_id,
                    version=result.get("version", 1),
                    selected_architecture=selected_arch,
                    metrics=metrics,
                    score=score,
                    reflection=result.get("reflection", {}),
                    executive_report=result.get("executive_report"),
                    technical_specification=result.get("technical_specification"),
                    deployment_plan=result.get("deployment_plan"),
                    monitoring_strategy=result.get("monitoring_strategy")
                )
            elif design_status["status"] == "processing" or design_status["status"] == "starting":
                raise HTTPException(status_code=400, detail="Design is still processing")
            elif design_status["status"] == "failed":
                raise HTTPException(status_code=500, detail=f"Design failed: {design_status.get('error', 'Unknown error')}")
        
        # Get run from database (for old runs not in active_designs)
        run = versioning_agent.get_run(run_id)
        
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        
        # Get final version
        versions = versioning_agent.get_architecture_versions(run_id)
        
        if not versions:
            raise HTTPException(status_code=404, detail="No versions found for this run")
        
        final_version = versions[-1]
        
        # Parse JSON fields
        import json
        architecture = json.loads(final_version["architecture_json"])
        metrics = json.loads(final_version["metrics_json"])
        
        return ResultResponse(
            run_id=run_id,
            version=final_version["version"],
            selected_architecture=architecture,
            metrics=metrics,
            score=final_version["score"],
            reflection={
                "confidence_score": 0.85,  # Should be stored
                "strengths": [],
                "weaknesses": [],
                "improvement_suggestions": []
            },
            executive_report=None,  # Should be stored
            technical_specification=None,
            deployment_plan=None,
            monitoring_strategy=None
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

# Made with Bob
