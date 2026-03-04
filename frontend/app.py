"""
MetaMind Streamlit Frontend

A full-featured web interface for the MetaMind AI Pipeline Designer.
"""

import os
import streamlit as st
import requests
import time
import json
from typing import Dict, Any, Optional
import plotly.graph_objects as go
import pandas as pd

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="MetaMind - AI Pipeline Designer",
    page_icon="```",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with modern design
st.markdown("""
<style>
    /* Main Header Styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .sub-header {
        font-size: 1.3rem;
        text-align: center;
        color: #6c757d;
        margin-bottom: 2.5rem;
        font-weight: 400;
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    /* Card Styling */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Status Boxes */
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 2px solid #28a745;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(40, 167, 69, 0.2);
        animation: fadeInUp 0.5s ease-out;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 2px solid #ffc107;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(255, 193, 7, 0.2);
        animation: fadeInUp 0.5s ease-out;
    }
    
    .error-box {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 2px solid #dc3545;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(220, 53, 69, 0.2);
        animation: fadeInUp 0.5s ease-out;
    }
    
    .info-box {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border: 2px solid #17a2b8;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(23, 162, 184, 0.2);
        animation: fadeInUp 0.5s ease-out;
    }
    
    /* Progress Indicator */
    .progress-container {
        background: #f0f2f6;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .progress-stage {
        display: flex;
        align-items: center;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
        background: white;
        transition: all 0.3s ease;
    }
    
    .progress-stage:hover {
        transform: translateX(5px);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Score Badge */
    .score-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 2rem;
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.4);
        animation: pulse 2s infinite;
    }
    
    /* Component Card */
    .component-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .component-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Button Enhancements */
    .stButton>button {
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Metric Styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 0.5rem;
        font-weight: 600;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        .sub-header {
            font-size: 1.1rem;
        }
    }
</style>
""", unsafe_allow_html=True)


def check_api_health() -> bool:
    """Check if the API is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def create_design(design_request: Dict[str, Any]) -> Optional[str]:
    """Submit a new design request."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/design",
            json=design_request,
            timeout=5  # Just for initial submission, not the whole process
        )
        if response.status_code == 200:
            return response.json()["run_id"]
        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            return None
    except requests.exceptions.Timeout:
        st.error("Request timed out. The backend might be processing. Try checking the design history in a moment.")
        return None
    except Exception as e:
        st.error(f"Failed to connect to API: {str(e)}")
        return None


def get_design_status(run_id: str) -> Optional[Dict[str, Any]]:
    """Get the status of a design session."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/design/{run_id}/status")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def get_design_result(run_id: str) -> Optional[Dict[str, Any]]:
    """Get the final result of a design session."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/design/{run_id}/result")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_design_progress(run_id: str) -> Optional[Dict[str, Any]]:
    """Get real-time progress of a design session."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/design/{run_id}/progress")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None



def get_design_history() -> list:
    """Get all design sessions."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/history")
        if response.status_code == 200:
            data = response.json()
            # Backend returns {"total": int, "runs": list}
            if isinstance(data, dict) and "runs" in data:
                return data["runs"]
            return []
        return []
    except:
        return []


def create_radar_chart(metrics: Dict[str, float]) -> go.Figure:
    """Create a radar chart for metrics visualization."""
    categories = list(metrics.keys())
    values = list(metrics.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Metrics',
        line=dict(color='#1f77b4', width=2),
        fillcolor='rgba(31, 119, 180, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        height=400,
        margin=dict(l=80, r=80, t=40, b=40)
    )
    
    return fig


def main():
    """Main application."""
    
    # Enhanced Header with gradient and animation
    st.markdown('<div class="main-header">🧠 MetaMind</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Autonomous AI Pipeline Designer & Self-Optimizing Architecture Engine</div>', unsafe_allow_html=True)
    
    # Check API health with enhanced styling
    if not check_api_health():
        st.markdown("""
        <div class="error-box">
            <h3>⚠️ Backend Not Running</h3>
            <p><strong>The MetaMind backend is not accessible.</strong></p>
            <p>Please start the backend server:</p>
            <pre style="background: #2d2d2d; color: #f8f8f2; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;">python run_backend.py</pre>
            <p style="margin-top: 1rem;">Then refresh this page.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Show API status with success indicator in sidebar
    with st.sidebar:
        st.markdown("""
        <div class="success-box" style="padding: 0.75rem; margin-bottom: 1rem;">
            <p style="margin: 0; text-align: center;">
                <strong>✅ Backend Connected</strong><br/>
                <small style="color: #155724;">API: http://localhost:8000</small>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sidebar navigation with enhanced styling
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["🎨 New Design", "📊 Design History", "🔍 Pipeline Monitor", "📖 About"]
    )
    
    if page == "🎨 New Design":
        show_new_design_page()
    elif page == "📊 Design History":
        show_history_page()
    elif page == "🔍 Pipeline Monitor":
        show_pipeline_monitor_page()
    else:
        show_about_page()


def show_new_design_page():
    """Show the new design creation page."""
    st.header("Create New AI Architecture Design")
    
    with st.form("design_form"):
        st.subheader("System Requirements")
        
        col1, col2 = st.columns(2)
        
        with col1:
            business_goal = st.text_area(
                "Business Goal",
                placeholder="Describe what you want to build...",
                help="Clear description of the system's purpose"
            )
            
            domain = st.selectbox(
                "Domain",
                ["ecommerce", "healthcare", "finance", "education", "legal", "general"],
                help="Application domain affects optimization priorities"
            )
            
            modalities = st.multiselect(
                "Data Modalities",
                ["text", "vision", "multimodal", "tabular"],
                default=["text"],
                help="Types of data the system will handle"
            )
        
        with col2:
            st.subheader("Constraints")
            
            budget = st.number_input(
                "Budget ($)",
                min_value=100,
                max_value=1000000,
                value=5000,
                step=100,
                help="Maximum budget for the system"
            )
            
            latency_target = st.number_input(
                "Latency Target (ms)",
                min_value=10,
                max_value=10000,
                value=300,
                step=10,
                help="Maximum acceptable response time"
            )
            
            expected_users = st.number_input(
                "Expected Users",
                min_value=1,
                max_value=10000000,
                value=50000,
                step=1000,
                help="Number of expected concurrent users"
            )
            
            risk_tolerance = st.select_slider(
                "Risk Tolerance",
                options=["low", "medium", "high"],
                value="medium",
                help="Acceptable level of risk"
            )
            
            compliance_level = st.select_slider(
                "Compliance Level",
                options=["low", "medium", "high"],
                value="high",
                help="Required compliance level"
            )
        
        max_iterations = st.slider(
            "Maximum Iterations",
            min_value=1,
            max_value=10,
            value=3,
            help="Maximum number of improvement iterations"
        )
        
        submitted = st.form_submit_button("🚀 Design Architecture", use_container_width=True)
        
        if submitted:
            if not business_goal:
                st.error("Please provide a business goal")
                return
            
            if not modalities:
                st.error("Please select at least one data modality")
                return
            
            # Create design request
            design_request = {
                "business_goal": business_goal,
                "domain": domain,
                "modalities": modalities,
                "constraints": {
                    "budget": budget,
                    "latency_target_ms": latency_target,
                    "expected_users": expected_users,
                    "risk_tolerance": risk_tolerance,
                    "compliance_level": compliance_level
                },
                "max_iterations": max_iterations
            }
            
            with st.spinner("Submitting design request..."):
                run_id = create_design(design_request)
            
            if run_id:
                st.success(f"✅ Design session started! Run ID: `{run_id}`")
                st.session_state.current_run_id = run_id
                st.session_state.show_progress = True
                st.rerun()
    
    # Show progress if a design is running
    if st.session_state.get("show_progress") and st.session_state.get("current_run_id"):
        show_design_progress(st.session_state.current_run_id)


def show_design_progress(run_id: str):
    """Show the progress of a design session with real-time updates."""
    st.divider()
    st.header("🔄 Design in Progress")
    
    # Get progress data
    progress_data = get_design_progress(run_id)
    
    if not progress_data:
        st.error("Failed to get progress information")
        return
    
    status = progress_data.get("status", "unknown")
    progress = progress_data.get("progress", {})
    
    # Show current stage in user-friendly way
    current_message = progress.get("current_message", "Processing...")
    st.info(f"**{current_message}**")
    
    # Show progress stages in a nice timeline
    stages = progress.get("stages", [])
    if stages:
        st.subheader("Progress Timeline")
        for stage_info in stages[-5:]:  # Show last 5 stages
            message = stage_info.get("message", "")
            st.markdown(f"✓ {message}")
    
    # Show details if available
    details = progress.get("details", {})
    if details:
        cols = st.columns(len(details))
        for i, (key, value) in enumerate(details.items()):
            with cols[i]:
                st.metric(key.replace("_", " ").title(), value)
    
    # Check if completed
    if status == "completed":
        st.success("✅ Design completed!")
        result = get_design_result(run_id)
        if result:
            show_design_result(result)
        st.session_state.show_progress = False
        
        # Add button to view in Pipeline Monitor
        if st.button("🔍 View Detailed Execution Log"):
            st.session_state['monitor_run_id'] = run_id
            st.rerun()
    elif status == "failed":
        error_msg = progress_data.get("error", "Unknown error")
        st.error(f"❌ Design failed: {error_msg}")
        st.session_state.show_progress = False
    else:
        # Still processing - auto refresh
        st.info("🔄 Refreshing in 5 seconds...")
        time.sleep(5)
        st.rerun()


def show_design_result(result: Dict[str, Any]):
    """Display the design result."""
    st.divider()
    st.header("🎉 Design Result")
    
    # Architecture overview
    architecture = result.get("selected_architecture", {})
    metrics = result.get("metrics", {})
    score = result.get("score", 0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        arch_name = architecture.get("name", architecture.get("type", "Unknown"))
        st.metric("Architecture", arch_name)
    with col2:
        st.metric("Score", f"{score:.1f}/100")
    with col3:
        st.metric("Version", result.get("version", 1))
    
    # Metrics visualization
    st.subheader("📊 Performance Metrics")
    
    if metrics:
        fig = create_radar_chart(metrics)
        st.plotly_chart(fig, use_container_width=True)
        
        # Show metrics in columns
        cols = st.columns(3)
        for i, (key, value) in enumerate(metrics.items()):
            with cols[i % 3]:
                st.metric(key.replace("_", " ").title(), f"{value:.1f}/100")
    else:
        st.warning("No metrics available for this design.")
    
    # Architecture details
    st.subheader("🏗️ Architecture Details")
    
    # Template
    template = architecture.get("template", "Unknown")
    st.info(f"**Template:** {template}")
    
    # Modules
    modules = architecture.get("modules", [])
    if modules:
        st.write("**Components:**")
        for i, module in enumerate(modules, 1):
            # Module structure: {layer, component, config}
            layer = module.get('layer', 'Unknown Layer')
            component = module.get('component', 'Unknown Component')
            config = module.get('config', {})
            
            # Use component as the name, layer as the type
            display_name = f"{layer}: {component}"
            
            with st.expander(f"{i}. {display_name}"):
                st.write(f"**Layer:** {layer}")
                st.write(f"**Component:** {component}")
                if config:
                    st.write(f"**Configuration:**")
                    for key, value in config.items():
                        st.write(f"  - {key}: {value}")
    
    # Selection Rationale & Comparison
    st.subheader("🎯 Why This Architecture Was Selected")
    
    # Get template information
    template = architecture.get("template", "Unknown")
    
    # Template descriptions and characteristics
    template_info = {
        "LLM + RAG Pipeline": {
            "description": "Retrieval-Augmented Generation combining vector search with LLM reasoning",
            "best_for": ["Knowledge-intensive tasks", "Document Q&A", "Customer support", "Research assistance"],
            "tech_stack": ["Vector DB (ChromaDB/Pinecone)", "Embeddings (Sentence Transformers)", "LLM (GPT-4/Llama)", "FastAPI"],
            "strengths": ["High accuracy", "Grounded responses", "Scalable knowledge base", "Cost-effective"],
            "weaknesses": ["Latency overhead", "Embedding costs", "Index maintenance"],
            "use_cases": ["E-commerce product search", "Legal document analysis", "Healthcare knowledge base"],
            "business_impact": "Reduces hallucinations by 80%, improves answer accuracy by 60%, enables 24/7 support"
        },
        "Multi-Agent LLM System": {
            "description": "Specialized agents working together, each handling specific tasks",
            "best_for": ["Complex workflows", "Multi-step reasoning", "Task decomposition", "Collaborative problem-solving"],
            "tech_stack": ["LangGraph", "Multiple LLMs", "Task orchestration", "State management"],
            "strengths": ["Handles complexity", "Parallel processing", "Specialized expertise", "Flexible routing"],
            "weaknesses": ["Higher latency", "Complex debugging", "Coordination overhead"],
            "use_cases": ["Financial analysis", "Code generation", "Research automation", "Business process automation"],
            "business_impact": "Handles 3x more complex tasks, reduces manual work by 70%, improves decision quality by 50%"
        },
        "Fine-Tuned Compact Model": {
            "description": "Custom-trained smaller model optimized for specific domain",
            "best_for": ["High-volume inference", "Low latency requirements", "Domain-specific tasks", "Cost optimization"],
            "tech_stack": ["Fine-tuned Llama/Mistral", "Custom training pipeline", "Model optimization", "Edge deployment"],
            "strengths": ["Ultra-low latency", "Cost-effective at scale", "Domain expertise", "Privacy-friendly"],
            "weaknesses": ["Training overhead", "Less flexible", "Requires data", "Maintenance"],
            "use_cases": ["Real-time chat", "Content moderation", "Sentiment analysis", "Classification tasks"],
            "business_impact": "90% cost reduction at scale, <100ms latency, 95% accuracy on domain tasks"
        },
        "Hybrid RAG + Fine-Tuning": {
            "description": "Combines retrieval with domain-specific fine-tuned model",
            "best_for": ["Enterprise applications", "High accuracy + low latency", "Domain expertise + knowledge", "Production systems"],
            "tech_stack": ["Vector DB", "Fine-tuned model", "Hybrid retrieval", "Caching layer"],
            "strengths": ["Best of both worlds", "High accuracy", "Good latency", "Scalable"],
            "weaknesses": ["Complex setup", "Higher initial cost", "Maintenance overhead"],
            "use_cases": ["Enterprise search", "Medical diagnosis support", "Financial advisory", "Legal research"],
            "business_impact": "85% accuracy improvement, 60% faster than pure RAG, handles 10x more queries"
        },
        "Ensemble Multi-Model": {
            "description": "Multiple models voting on outputs for maximum reliability",
            "best_for": ["Critical decisions", "High-stakes applications", "Consensus-based reasoning", "Error reduction"],
            "tech_stack": ["Multiple LLMs", "Voting mechanism", "Confidence scoring", "Fallback logic"],
            "strengths": ["Highest reliability", "Error detection", "Robust outputs", "Confidence scores"],
            "weaknesses": ["Highest cost", "Highest latency", "Complex orchestration"],
            "use_cases": ["Medical diagnosis", "Financial trading", "Legal contracts", "Safety-critical systems"],
            "business_impact": "99.5% reliability, 95% error reduction, suitable for regulated industries"
        }
    }
    
    # Display selected architecture info
    if template in template_info:
        info = template_info[template]
        
        # Create tabs for different aspects
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "🔧 Tech Stack", "💼 Business Impact", "🎯 Use Cases"])
        
        with tab1:
            st.markdown(f"""
            <div class="info-box">
                <h4>{template}</h4>
                <p><strong>Description:</strong> {info['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**✅ Strengths:**")
                for strength in info['strengths']:
                    st.markdown(f"- {strength}")
            
            with col2:
                st.markdown("**⚠️ Considerations:**")
                for weakness in info['weaknesses']:
                    st.markdown(f"- {weakness}")
        
        with tab2:
            st.markdown("**🔧 Technology Stack:**")
            for tech in info['tech_stack']:
                st.markdown(f"- {tech}")
            
            st.markdown("**📦 Components in This Design:**")
            for i, module in enumerate(modules[:5], 1):  # Show first 5
                layer = module.get('layer', 'Unknown')
                component = module.get('component', 'Unknown')
                st.markdown(f"{i}. **{layer}**: {component}")
        
        with tab3:
            st.markdown(f"""
            <div class="success-box">
                <h4>💼 Business Impact</h4>
                <p>{info['business_impact']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**🎯 Best For:**")
            for use in info['best_for']:
                st.markdown(f"- {use}")
        
        with tab4:
            st.markdown("**🎯 Ideal Use Cases:**")
            for use_case in info['use_cases']:
                st.markdown(f"- {use_case}")
            
            st.markdown("**📊 Expected Performance:**")
            st.markdown(f"- **Score**: {score:.1f}/100")
            st.markdown(f"- **Cost Efficiency**: {metrics.get('cost', 0):.1f}/100")
            st.markdown(f"- **Latency**: {metrics.get('latency', 0):.1f}/100")
            st.markdown(f"- **Scalability**: {metrics.get('scalability', 0):.1f}/100")
    
    # Justification from optimization agent
    justification = architecture.get("justification", "")
    if justification:
        st.markdown(f"""
        <div class="info-box" style="margin-top: 1rem;">
            <h4>🤖 AI Selection Rationale</h4>
            <p>{justification}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Architecture Comparison Table
    st.subheader("📊 Architecture Comparison")
    
    comparison_data = {
        "Template": ["LLM + RAG", "Multi-Agent", "Fine-Tuned", "Hybrid", "Ensemble"],
        "Latency": ["Medium", "High", "Low", "Medium", "High"],
        "Cost": ["Medium", "High", "Low", "Medium", "Very High"],
        "Accuracy": ["High", "Very High", "Medium", "Very High", "Highest"],
        "Complexity": ["Medium", "High", "Low", "High", "Very High"],
        "Best For": [
            "Knowledge Q&A",
            "Complex workflows",
            "High-volume tasks",
            "Enterprise apps",
            "Critical decisions"
        ]
    }
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Highlight selected architecture
    st.info(f"✨ **Selected**: {template} - Optimized for your requirements")
    
    # Reflection feedback
    reflection = result.get("reflection_feedback", {})
    if reflection:
        st.subheader("🔍 Reflection Analysis")
        
        strengths = reflection.get("strengths", [])
        if strengths:
            st.write("**Strengths:**")
            for strength in strengths:
                st.write(f"- {strength}")
        
        weaknesses = reflection.get("weaknesses", [])
        if weaknesses:
            st.write("**Weaknesses:**")
            for weakness in weaknesses:
                st.write(f"- {weakness}")
        
        improvements = reflection.get("improvements", [])
        if improvements:
            st.write("**Suggested Improvements:**")
            for improvement in improvements:
                st.write(f"- {improvement}")
    
    # Download specification
    st.subheader("📄 Documentation")
    if st.button("📥 Download Complete Specification"):
        try:
            response = requests.get(f"{API_BASE_URL}/api/design/{result['run_id']}/specification")
            if response.status_code == 200:
                spec = response.json()
                st.download_button(
                    label="Download JSON",
                    data=json.dumps(spec, indent=2),
                    file_name=f"metamind_spec_{result['run_id']}.json",
                    mime="application/json"
                )
        except Exception as e:
            st.error(f"Failed to download specification: {str(e)}")


def show_history_page():
    """Show the design history page."""
    st.header("📊 Design History")
    
    history = get_design_history()
    
    if not history:
        st.info("No design sessions found. Create your first design!")
        return
    
    # Convert to DataFrame
    df_data = []
    for session in history:
        df_data.append({
            "Run ID": session.get("run_id", "N/A"),
            "Domain": session.get("domain", "N/A"),
            "Status": session.get("status", "N/A"),
            "Version": session.get("version", "N/A"),
            "Created": session.get("created_at", "N/A")
        })
    
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True)
    
    # Select a session to view
    st.subheader("View Design Details")
    
    # Filter valid sessions
    valid_sessions = [s for s in history if s.get("run_id")]
    
    if not valid_sessions:
        st.warning("No valid design sessions found.")
        return
    
    selected_run_id = st.selectbox(
        "Select a design session",
        options=[s.get("run_id") for s in valid_sessions],
        format_func=lambda x: f"{x[:8]}... - {next((s.get('domain', 'Unknown') for s in valid_sessions if s.get('run_id') == x), 'Unknown')}"
    )
    
    if selected_run_id and st.button("View Details"):
        with st.spinner("Loading design details..."):
            result = get_design_result(selected_run_id)
        
        if result:
            show_design_result(result)
        else:
            st.error(f"Failed to load design details for run ID: {selected_run_id[:8]}...")
            st.info("The design may still be processing or the result may not be available yet.")


def show_about_page():
    """Show the about page."""
    st.header("📖 About MetaMind")
    
    st.markdown("""
    ## What is MetaMind?
    
    MetaMind is an **Autonomous AI Pipeline Designer** that uses a multi-agent system to:
    
    - 🎯 Analyze your requirements
    - 🏗️ Generate multiple architecture candidates
    - 📊 Simulate performance metrics
    - 🎖️ Select the optimal design
    - 🔍 Reflect and improve iteratively
    - 📄 Generate complete documentation
    
    ## Key Features
    
    - **Multi-Agent System**: 11 specialized agents working together
    - **Deterministic Scoring**: Reproducible architecture evaluation
    - **Domain-Adaptive**: Optimizes based on your industry
    - **Iterative Improvement**: Self-optimizing through reflection
    - **Version Control**: Track architecture evolution
    - **Complete Documentation**: Executive, technical, deployment, and monitoring specs
    
    ## Architecture Templates
    
    - LLM + RAG Pipeline
    - Multi-Agent LLM System
    - Vision + LLM Multimodal Pipeline
    - Tool-Augmented Agent System
    - Fine-Tuned Compact Model Pipeline
    - Hybrid Multi-Model Arbitration Pipeline
    
    ## Metrics Evaluated
    
    - **Cost**: Infrastructure and operational costs
    - **Latency**: Response time performance
    - **Risk**: Security and reliability risks
    - **Compliance**: Regulatory adherence
    - **Scalability**: Growth capacity
    - **Complexity**: Implementation difficulty
    
    ## How It Works
    
    1. **Requirements Analysis**: Parse natural language into structured constraints
    2. **Weight Tuning**: Adjust optimization priorities based on domain
    3. **Architecture Generation**: Create 3-5 candidate designs
    4. **Simulation**: Estimate all metrics for each candidate
    5. **Scoring**: Normalize and compute weighted scores
    6. **Selection**: Choose the highest-scoring architecture
    7. **Reflection**: Critique and identify improvements
    8. **Iteration**: Refine if confidence < 85%
    9. **Documentation**: Generate complete specifications
    
    ## Tech Stack
    
    - **Backend**: FastAPI + LangGraph
    - **LLM**: Ollama (Llama 3)
    - **Frontend**: Streamlit
    - **Database**: SQLite
    - **Deployment**: Docker
    
    ---
    
    **Version**: 1.0.0  
    **License**: MIT  
    **Repository**: [GitHub](https://github.com/yourusername/metamind)
    """)

def show_pipeline_monitor_page():
    """Show the pipeline monitoring page with real-time progress."""
    st.header("🔍 Pipeline Monitor")
    st.markdown("Monitor active design sessions and view detailed execution logs.")
    
    # Input for run ID
    col1, col2 = st.columns([3, 1])
    with col1:
        run_id = st.text_input("Enter Run ID to monitor:", placeholder="e.g., 7ac19269-c86b-4bec-b2ea-038223416d68")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        monitor_btn = st.button("🔍 Monitor", use_container_width=True)
    
    if not run_id:
        st.info("💡 Enter a Run ID from your design session to see real-time progress and technical details.")
        
        # Show recent sessions
        st.subheader("Recent Design Sessions")
        history = get_design_history()
        if history:
            recent = history[:5]  # Show last 5
            for idx, session in enumerate(recent):
                # Skip sessions without run_id
                if not session.get('run_id'):
                    continue
                    
                run_id = session.get('run_id')
                with st.expander(f"📋 {run_id[:8]}... - {session.get('domain', 'Unknown')}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Status", session.get('status', 'Unknown'))
                    with col2:
                        st.metric("Version", session.get('version', 'N/A'))
                    with col3:
                        st.metric("Domain", session.get('domain', 'Unknown'))
                    
                    # Use index to ensure unique keys
                    if st.button(f"Monitor This Session", key=f"monitor_btn_{idx}_{run_id[:8]}"):
                        st.session_state['monitor_run_id'] = run_id
                        st.rerun()
        else:
            st.info("No design sessions found yet.")
        return
    
    # Use session state if available
    if 'monitor_run_id' in st.session_state:
        run_id = st.session_state['monitor_run_id']
    
    # Get progress data
    progress_data = get_design_progress(run_id)
    
    if not progress_data:
        st.error(f"❌ Could not find design session: {run_id}")
        return
    
    # Display current status
    status = progress_data.get("status", "unknown")
    progress = progress_data.get("progress", {})
    
    # Status banner
    status_colors = {
        "processing": "🟡",
        "completed": "🟢",
        "failed": "🔴",
        "starting": "🟠"
    }
    status_icon = status_colors.get(status, "⚪")
    
    st.markdown(f"""
    <div style="padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color: white; margin: 0;">{status_icon} Status: {status.upper()}</h2>
        <p style="color: white; margin: 5px 0 0 0; opacity: 0.9;">Run ID: {run_id}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Current stage
    current_stage = progress.get("current_stage", "unknown")
    current_message = progress.get("current_message", "No message")
    
    st.subheader("📍 Current Stage")
    st.info(f"**{current_stage.upper()}**: {current_message}")
    
    # Progress timeline
    st.subheader("📊 Execution Timeline")
    stages = progress.get("stages", [])
    
    if stages:
        for i, stage_info in enumerate(stages):
            stage_name = stage_info.get("stage", "unknown")
            message = stage_info.get("message", "")
            timestamp = stage_info.get("timestamp", 0)
            
            # Format timestamp
            from datetime import datetime
            time_str = datetime.fromtimestamp(timestamp).strftime("%H:%M:%S") if timestamp else "N/A"
            
            # Create timeline entry
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"**{time_str}**")
            with col2:
                st.markdown(f"{message}")
            
            if i < len(stages) - 1:
                st.markdown("↓")
    else:
        st.warning("No execution stages recorded yet.")
    
    # Details section
    details = progress.get("details", {})
    if details:
        st.subheader("🔧 Execution Details")
        
        cols = st.columns(len(details))
        for i, (key, value) in enumerate(details.items()):
            with cols[i]:
                st.metric(key.replace("_", " ").title(), value)
    
    # Auto-refresh for active sessions
    if status in ["processing", "starting"]:
        st.markdown("---")
        st.info("🔄 This page will auto-refresh every 3 seconds while the design is processing.")
        time.sleep(3)
        st.rerun()
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    with col2:
        if status == "completed":
            if st.button("📊 View Results", use_container_width=True):
                st.session_state['view_result_run_id'] = run_id
                st.switch_page("pages/results.py") if hasattr(st, 'switch_page') else st.info("Navigate to Design History to view results")
    
    with col3:
        if st.button("🏠 Back to Home", use_container_width=True):
            if 'monitor_run_id' in st.session_state:
                del st.session_state['monitor_run_id']
            st.rerun()



if __name__ == "__main__":
    main()

# Made with Bob
