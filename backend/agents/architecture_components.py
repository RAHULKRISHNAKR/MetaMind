"""
Architecture Component Definitions

This module defines the allowed components for each architecture layer
to prevent hallucinated or invalid components.
"""

from typing import Dict, List

ALLOWED_COMPONENTS: Dict[str, List[str]] = {
    "Data Layer": [
        "PostgreSQL","MongoDB","S3","MinIO","Redis","ChromaDB","Pinecone","Weaviate","SQLite","MySQL","Cassandra","DynamoDB","Kafka","RabbitMQ",
        ],
    
    "Preprocessing Layer": [
        "Data Validation","Data Cleaning","Feature Engineering","Data Augmentation","Normalization","Tokenization","Text Preprocessing",
    ],

    "Embedding Layer": [
        "Sentence Transformers","OpenAI Embeddings","CLIP","BERT","Custom Embeddings","Word2Vec","FastText","Universal Sentence Encoder",
    ],

    "Model Layer": [
        "Llama 3 8B","Llama 3 70B","Llama 3","GPT-4","GPT-3.5","Claude-3","Claude-2","Claude","Gemini Pro","Gemini","Fine-tuned","BERT","T5","Mistral","Mixtral",
    ],

    "Tool Layer": [
        "Web Search","Tavily","SerpAPI","Code Execution","Python Sandbox","Database Query","SQL Generator","API Integration","REST Client","GraphQL Client",
    ],

    "Agent Orchestration Layer": [
        "LangGraph","CrewAI","AutoGen","Custom","LangChain","Semantic Kernel",
    ],

    "Validation & Safety Layer": [
        "Input Sanitization","Output Validation","Content Filtering","Hallucination Detection","Schema Validation","XSS Protection","SQL Injection Protection",
    ],

    "Monitoring Layer": [
        "Prometheus","Grafana","OpenTelemetry","Logging","Structured Logging","Audit Logging","Datadog","New Relic","CloudWatch",
    ],

    "Deployment Layer": [
        "Docker","Kubernetes","API Gateway","Kong","Nginx","Load Balancer","HAProxy","AWS ALB","CI/CD","GitHub Actions","GitLab CI",
    ],
}


def is_component_allowed(layer: str, component: str) -> bool:
    """
    Check if a component is allowed for a given layer.
    
    Args:
        layer: The architecture layer
        component: The component name
        
    Returns:
        bool: True if component is allowed, False otherwise
    """
    if layer not in ALLOWED_COMPONENTS:
        return False
    
    allowed = ALLOWED_COMPONENTS[layer]
    component_lower = component.lower()
    
    for allowed_comp in allowed:
        if allowed_comp.lower() in component_lower:
            return True
    
    return False


def get_default_component(layer: str) -> str:
    """
    Get a default component for a layer.
    
    Args:
        layer: The architecture layer
        
    Returns:
        str: Default component name
    """
    defaults = {
        "Data Layer": "PostgreSQL",
        "Preprocessing Layer": "Data Validation",
        "Embedding Layer": "Sentence Transformers",
        "Model Layer": "Llama 3 8B",
        "Tool Layer": "Web Search",
        "Agent Orchestration Layer": "LangGraph",
        "Validation & Safety Layer": "Input Sanitization",
        "Monitoring Layer": "Prometheus",
        "Deployment Layer": "Docker",
    }
    
    return defaults.get(layer, "Unknown")


def validate_component(layer: str, component: str) -> tuple[bool, str]:
    """
    Validate a component and return validation result with message.
    
    Args:
        layer: The architecture layer
        component: The component name
        
    Returns:
        tuple: (is_valid, message)
    """
    if layer not in ALLOWED_COMPONENTS:
        return False, f"Unknown layer: {layer}"
    
    if is_component_allowed(layer, component):
        return True, "Component is valid"
    
    default = get_default_component(layer)
    return False, f"Invalid component '{component}' for {layer}. Using default: {default}"

