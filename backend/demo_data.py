"""
Demo Data for MetaMind
Pre-cached business scenarios for instant demo results.
"""

import time
import uuid

# Demo Scenario 1: Healthcare Patient Monitoring System
DEMO_HEALTHCARE = {
    "run_id": "demo-healthcare-001",
    "request": {
        "business_goal": "Build an AI-powered patient monitoring system that analyzes vital signs in real-time and alerts medical staff of anomalies",
        "domain": "healthcare",
        "modalities": ["text", "tabular"],
        "constraints": {
            "budget": 75000,
            "latency_target_ms": 500,
            "risk_tolerance": "low",
            "compliance_level": "high",
            "expected_users": 5000
        },
        "max_iterations": 3
    },
    "result": {
        "run_id": "demo-healthcare-001",
        "version": 2,
        "score": 87.5,
        "selected_architecture": {
            "architecture_id": "healthcare-monitoring-v2",
            "name": "Healthcare Patient Monitoring System",
            "template": "real_time_analytics",
            "topology": "sequential",
            "modules": [
                {
                    "layer": "ingestion",
                    "component": "Data Ingestion Layer",
                    "config": {
                        "type": "streaming_pipeline",
                        "technology": "Apache Kafka",
                        "purpose": "Real-time vital signs data ingestion from medical devices",
                        "throughput": "10000 events/sec"
                    }
                },
                {
                    "layer": "preprocessing",
                    "component": "Feature Engineering",
                    "config": {
                        "type": "preprocessing",
                        "technology": "Apache Spark",
                        "purpose": "Transform and normalize vital signs data",
                        "features": ["heart_rate", "blood_pressure", "oxygen_saturation"]
                    }
                },
                {
                    "layer": "model",
                    "component": "Anomaly Detection Model",
                    "config": {
                        "type": "ml_model",
                        "technology": "Isolation Forest + LSTM",
                        "purpose": "Detect anomalies in patient vital signs patterns",
                        "accuracy": "94.5%"
                    }
                },
                {
                    "layer": "notification",
                    "component": "Alert Generation System",
                    "config": {
                        "type": "notification_service",
                        "technology": "Redis + WebSocket",
                        "purpose": "Real-time alerts to medical staff",
                        "latency": "<100ms"
                    }
                },
                {
                    "layer": "security",
                    "component": "HIPAA Compliance Layer",
                    "config": {
                        "type": "security",
                        "technology": "Encryption + Audit Logging",
                        "purpose": "Ensure data privacy and regulatory compliance",
                        "encryption": "AES-256"
                    }
                }
            ],
            "estimated_metrics": {
                "latency_ms": 450,
                "throughput": 10000,
                "availability": 99.9
            },
            "final_score": 87.5
        },
        "metrics": {
            "performance": 88.0,
            "cost_efficiency": 82.0,
            "scalability": 90.0,
            "reliability": 92.0,
            "security": 95.0,
            "compliance": 98.0,
            "maintainability": 85.0
        },
        "weights": {
            "performance": 0.15,
            "cost_efficiency": 0.10,
            "scalability": 0.15,
            "reliability": 0.20,
            "security": 0.20,
            "compliance": 0.15,
            "maintainability": 0.05
        },
        "reflection": {
            "confidence": 0.89,
            "strengths": [
                "High compliance score (98%) meets HIPAA requirements",
                "Excellent reliability (92%) for critical healthcare application",
                "Real-time processing with <500ms latency achieved"
            ],
            "weaknesses": [
                "Cost efficiency could be improved with reserved instances",
                "Maintainability score indicates need for better documentation"
            ],
            "improvement_suggestions": [
                "Implement automated testing for ML model drift detection",
                "Add redundancy for alert system to prevent single point of failure",
                "Consider edge computing for remote patient monitoring"
            ],
            "should_iterate": False
        },
        "iterations": [
            {
                "version": 0,
                "score": 78.5,
                "changes": "Initial architecture design"
            },
            {
                "version": 1,
                "score": 83.2,
                "changes": "Enhanced security layer, added HIPAA compliance checks"
            },
            {
                "version": 2,
                "score": 87.5,
                "changes": "Optimized data pipeline, improved alert system reliability"
            }
        ],
        "timestamp": time.time()
    }
}

# Demo Scenario 2: E-commerce Recommendation Engine
DEMO_ECOMMERCE = {
    "run_id": "demo-ecommerce-002",
    "request": {
        "business_goal": "Create a personalized product recommendation system that increases conversion rates and customer engagement",
        "domain": "ecommerce",
        "modalities": ["text", "vision"],
        "constraints": {
            "budget": 50000,
            "latency_target_ms": 200,
            "risk_tolerance": "medium",
            "compliance_level": "medium",
            "expected_users": 100000
        },
        "max_iterations": 3
    },
    "result": {
        "run_id": "demo-ecommerce-002",
        "version": 2,
        "score": 91.3,
        "selected_architecture": {
            "architecture_id": "ecommerce-recommendation-v2",
            "name": "E-Commerce Product Recommendation Engine",
            "template": "recommendation_system",
            "topology": "parallel",
            "modules": [
                {
                    "layer": "tracking",
                    "component": "User Behavior Tracking",
                    "config": {
                        "type": "data_collection",
                        "technology": "Google Analytics + Custom Events",
                        "purpose": "Track user interactions, clicks, and browsing patterns",
                        "events": ["view", "click", "add_to_cart", "purchase"]
                    }
                },
                {
                    "layer": "embedding",
                    "component": "Product Embedding Model",
                    "config": {
                        "type": "ml_model",
                        "technology": "BERT + Vision Transformer",
                        "purpose": "Generate semantic embeddings for products (text + images)",
                        "embedding_dim": 512
                    }
                },
                {
                    "layer": "recommendation",
                    "component": "Collaborative Filtering Engine",
                    "config": {
                        "type": "recommendation_system",
                        "technology": "Matrix Factorization + Neural CF",
                        "purpose": "Generate personalized recommendations based on user similarity",
                        "top_k": 20
                    }
                },
                {
                    "layer": "serving",
                    "component": "Real-time Ranking Service",
                    "config": {
                        "type": "api_service",
                        "technology": "FastAPI + Redis Cache",
                        "purpose": "Serve recommendations with <200ms latency",
                        "cache_ttl": "5min"
                    }
                },
                {
                    "layer": "experimentation",
                    "component": "A/B Testing Framework",
                    "config": {
                        "type": "experimentation",
                        "technology": "Custom Framework + Analytics",
                        "purpose": "Continuously test and optimize recommendation strategies",
                        "variants": ["baseline", "neural_cf", "hybrid"]
                    }
                }
            ],
            "estimated_metrics": {
                "latency_ms": 180,
                "throughput": 50000,
                "availability": 99.95
            },
            "final_score": 91.3
        },
        "metrics": {
            "performance": 94.0,
            "cost_efficiency": 88.0,
            "scalability": 92.0,
            "reliability": 90.0,
            "security": 85.0,
            "compliance": 88.0,
            "maintainability": 90.0
        },
        "weights": {
            "performance": 0.25,
            "cost_efficiency": 0.20,
            "scalability": 0.20,
            "reliability": 0.15,
            "security": 0.05,
            "compliance": 0.05,
            "maintainability": 0.10
        },
        "reflection": {
            "confidence": 0.92,
            "strengths": [
                "Excellent performance (94%) with sub-200ms latency",
                "High scalability (92%) to handle 100K+ users",
                "Strong cost efficiency (88%) within budget constraints"
            ],
            "weaknesses": [
                "Security score (85%) could be improved with additional authentication layers",
                "Compliance score indicates need for better GDPR handling"
            ],
            "improvement_suggestions": [
                "Implement user consent management for GDPR compliance",
                "Add rate limiting to prevent API abuse",
                "Consider multi-armed bandit algorithms for exploration-exploitation balance"
            ],
            "should_iterate": False
        },
        "iterations": [
            {
                "version": 0,
                "score": 82.7,
                "changes": "Initial recommendation system design"
            },
            {
                "version": 1,
                "score": 87.9,
                "changes": "Added vision transformer for image-based recommendations"
            },
            {
                "version": 2,
                "score": 91.3,
                "changes": "Optimized caching strategy, improved ranking algorithm"
            }
        ],
        "timestamp": time.time()
    }
}

# Demo scenarios registry
DEMO_SCENARIOS = {
    "healthcare": DEMO_HEALTHCARE,
    "ecommerce": DEMO_ECOMMERCE
}

def get_demo_scenario(domain: str):
    """Get a demo scenario by domain."""
    return DEMO_SCENARIOS.get(domain)

def get_all_demo_scenarios():
    """Get all available demo scenarios."""
    return list(DEMO_SCENARIOS.keys())

# Made with Bob
