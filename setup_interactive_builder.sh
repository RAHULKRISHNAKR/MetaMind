#!/bin/bash

# MetaMind Interactive Builder Setup Script
# This script prepares the system for testing Phase 1 & 2

echo "🚀 MetaMind Interactive Builder Setup"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "run_backend.py" ]; then
    echo -e "${RED}❌ Error: Must run from MetaMind root directory${NC}"
    exit 1
fi

echo "📋 Step 1: Installing Dependencies"
echo "-----------------------------------"

# Install Jinja2
echo "Installing Jinja2..."
pip install jinja2==3.1.4

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Jinja2 installed successfully${NC}"
else
    echo -e "${RED}❌ Failed to install Jinja2${NC}"
    exit 1
fi

echo ""
echo "📁 Step 2: Verifying File Structure"
echo "------------------------------------"

# Check templates directory
if [ -d "backend/code_generation/templates/rag_pipeline/python" ]; then
    echo -e "${GREEN}✅ Templates directory exists${NC}"
    
    # Count template files
    TEMPLATE_COUNT=$(ls backend/code_generation/templates/rag_pipeline/python/*.j2 2>/dev/null | wc -l)
    echo "   Found $TEMPLATE_COUNT template files"
    
    if [ $TEMPLATE_COUNT -eq 6 ]; then
        echo -e "${GREEN}   ✅ All 6 templates present${NC}"
    else
        echo -e "${YELLOW}   ⚠️  Expected 6 templates, found $TEMPLATE_COUNT${NC}"
    fi
else
    echo -e "${RED}❌ Templates directory not found${NC}"
    exit 1
fi

# Check code editor files
if [ -f "backend/api/code_editor_endpoints.py" ]; then
    echo -e "${GREEN}✅ Code editor API endpoints exist${NC}"
else
    echo -e "${RED}❌ Code editor API endpoints not found${NC}"
    exit 1
fi

if [ -f "frontend/code_editor.py" ]; then
    echo -e "${GREEN}✅ Code editor frontend component exists${NC}"
else
    echo -e "${RED}❌ Code editor frontend component not found${NC}"
    exit 1
fi

echo ""
echo "🔧 Step 3: Checking Configuration"
echo "----------------------------------"

# Check .env file
if [ -f ".env" ]; then
    echo -e "${GREEN}✅ .env file exists${NC}"
    
    # Check for required variables
    if grep -q "OLLAMA_BASE_URL" .env || grep -q "XAI_API_KEY" .env || grep -q "OPENAI_API_KEY" .env; then
        echo -e "${GREEN}   ✅ LLM configuration found${NC}"
    else
        echo -e "${YELLOW}   ⚠️  No LLM configuration found in .env${NC}"
        echo "   Please configure at least one LLM provider"
    fi
else
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo "   Creating from .env.example..."
    
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}   ✅ Created .env from template${NC}"
        echo -e "${YELLOW}   ⚠️  Please edit .env and add your API keys${NC}"
    else
        echo -e "${RED}   ❌ .env.example not found${NC}"
    fi
fi

echo ""
echo "🧪 Step 4: Creating Test Directories"
echo "-------------------------------------"

# Create generated_projects directory if it doesn't exist
if [ ! -d "generated_projects" ]; then
    mkdir -p generated_projects
    echo -e "${GREEN}✅ Created generated_projects directory${NC}"
else
    echo -e "${GREEN}✅ generated_projects directory exists${NC}"
fi

echo ""
echo "📊 Step 5: System Check"
echo "-----------------------"

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

if python -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo -e "${GREEN}✅ Python version is 3.11+${NC}"
else
    echo -e "${YELLOW}⚠️  Python 3.11+ recommended${NC}"
fi

# Check if ports are available
echo ""
echo "Checking ports..."

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Port 8000 is in use (backend)${NC}"
    echo "   You may need to stop the existing process"
else
    echo -e "${GREEN}✅ Port 8000 is available (backend)${NC}"
fi

if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Port 8501 is in use (frontend)${NC}"
    echo "   You may need to stop the existing process"
else
    echo -e "${GREEN}✅ Port 8501 is available (frontend)${NC}"
fi

echo ""
echo "✅ Setup Complete!"
echo "=================="
echo ""
echo "📚 Next Steps:"
echo "1. Review TESTING_GUIDE.md for detailed testing instructions"
echo "2. Start backend: python run_backend.py"
echo "3. Start frontend: python run_frontend.py"
echo "4. Open browser: http://localhost:8501"
echo ""
echo "📖 Documentation:"
echo "- TESTING_GUIDE.md - Complete testing procedures"
echo "- PHASE_1_COMPLETION_REPORT.md - Phase 1 details"
echo "- PHASE_2_COMPLETION_REPORT.md - Phase 2 details"
echo "- CODE_GENERATION_QUICKSTART.md - Quick start guide"
echo ""
echo "🎯 Ready to test the Interactive Builder!"

# Made with Bob
