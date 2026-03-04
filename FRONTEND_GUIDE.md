# MetaMind Frontend Guide

## 🎨 Full-Featured Web Interface

MetaMind now includes a beautiful Streamlit-based frontend with:

- ✅ Interactive design creation form
- ✅ Real-time progress tracking
- ✅ Visual metrics dashboard with radar charts
- ✅ Design history browser
- ✅ Complete architecture visualization
- ✅ Downloadable specifications

## 🚀 Quick Start

### 1. Install Frontend Dependencies

```bash
cd ~/Documents/github/Personal_Project/MetaMind
pip install -r frontend/requirements.txt
```

This installs:
- `streamlit` - Web framework
- `plotly` - Interactive charts
- `pandas` - Data handling
- `requests` - API communication

### 2. Start the Backend (if not running)

**Terminal 1:**
```bash
cd ~/Documents/github/Personal_Project/MetaMind
python run_backend.py
```

Keep this running. You should see:
```
🚀 Starting MetaMind Backend Server...
📍 API Documentation: http://localhost:8000/docs
INFO: Uvicorn running on http://0.0.0.0:8000
```

### 3. Start Ollama (Required!)

**Terminal 2:**
```bash
ollama serve
```

Keep this running. Without Ollama, the AI agents won't work.

### 4. Start the Frontend

**Terminal 3:**
```bash
cd ~/Documents/github/Personal_Project/MetaMind
python run_frontend.py
```

You should see:
```
🎨 Starting MetaMind Frontend...
📍 Frontend URL: http://localhost:8501

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### 5. Open in Browser

Visit: **http://localhost:8501**

The frontend will automatically open in your default browser!

## 🎯 Using the Frontend

### Page 1: New Design

1. **Fill in the form:**
   - Business Goal: Describe what you want to build
   - Domain: Select your industry (ecommerce, healthcare, etc.)
   - Modalities: Choose data types (text, vision, etc.)
   - Constraints: Set budget, latency, users, risk, compliance
   - Max Iterations: How many improvement cycles (1-10)

2. **Click "🚀 Design Architecture"**

3. **Watch the progress:**
   - Real-time status updates
   - Progress bar showing completion
   - Automatic result display when done

4. **View the results:**
   - Architecture type and version
   - Confidence score
   - Interactive radar chart of metrics
   - Detailed component breakdown
   - Design justification
   - Reflection analysis (strengths, weaknesses, improvements)
   - Download complete specification

### Page 2: Design History

1. **View all past designs** in a table
2. **Select any design** to view details
3. **Compare different versions**

### Page 3: About

- Learn about MetaMind
- Understand the architecture
- See available templates
- Review metrics evaluated

## 📊 Features

### Interactive Design Form
- Intuitive input fields
- Helpful tooltips
- Real-time validation
- Domain-specific defaults

### Real-Time Progress
- Live status updates every 5 seconds
- Progress bar visualization
- Automatic result display
- Error handling with clear messages

### Visual Metrics Dashboard
- **Radar Chart**: 6-dimensional metric visualization
- **Metric Cards**: Raw and normalized scores
- **Color-coded**: Easy to understand at a glance

### Architecture Visualization
- Component breakdown
- Module descriptions
- Design justification
- Reflection analysis

### Design History
- Browse all past designs
- Filter and search
- View detailed results
- Compare versions

### Documentation Export
- Download complete specifications
- JSON format
- Includes all details
- Ready for implementation

## 🎨 UI Features

### Modern Design
- Clean, professional interface
- Responsive layout
- Custom styling
- Intuitive navigation

### Status Indicators
- ✅ Success boxes (green)
- ⚠️ Warning boxes (yellow)
- ❌ Error boxes (red)
- ℹ️ Info boxes (blue)

### Interactive Elements
- Expandable sections
- Collapsible details
- Hover tooltips
- Click-to-copy

## 🔧 Configuration

### Change Ports

**Backend Port** (default: 8000):
Edit `run_backend.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change 8000
```

**Frontend Port** (default: 8501):
Edit `run_frontend.py`:
```python
"--server.port=8501",  # Change 8501
```

### API URL

If backend is on a different machine, edit `frontend/app.py`:
```python
API_BASE_URL = "http://localhost:8000"  # Change to your backend URL
```

## 🐛 Troubleshooting

### Frontend won't start

**Error**: `ModuleNotFoundError: No module named 'streamlit'`

**Solution**:
```bash
pip install -r frontend/requirements.txt
```

### "Backend Not Running" message

**Cause**: Backend is not accessible

**Solution**:
1. Check backend is running: `curl http://localhost:8000/health`
2. Start backend: `python run_backend.py`
3. Check firewall settings

### Design fails with 500 error

**Cause**: Ollama is not running

**Solution**:
1. Start Ollama: `ollama serve`
2. Verify: `curl http://localhost:11434/api/tags`
3. Pull model: `ollama pull llama3`

### Progress stuck at 0%

**Cause**: Backend is processing but not responding

**Solution**:
1. Check backend terminal for errors
2. Verify Ollama is running
3. Check system resources (CPU, RAM)
4. Reduce max_iterations to 1-2

### Charts not displaying

**Cause**: Plotly not installed

**Solution**:
```bash
pip install plotly==5.24.0
```

## 📱 Mobile Support

The frontend is responsive and works on:
- ✅ Desktop browsers
- ✅ Tablets
- ✅ Mobile phones (limited)

For best experience, use desktop with screen width > 1024px.

## 🎯 Tips for Best Results

1. **Be specific** in business goals
2. **Choose appropriate domain** for better weight tuning
3. **Set realistic constraints** based on your needs
4. **Start with 2-3 iterations** for faster results
5. **Review reflection feedback** for insights
6. **Download specifications** for implementation

## 🔄 Workflow

```
1. Fill form → 2. Submit → 3. Watch progress → 4. View results → 5. Download spec
                                    ↓
                            6. Review history
                                    ↓
                            7. Compare versions
                                    ↓
                            8. Iterate if needed
```

## 📚 Next Steps

After getting your architecture design:

1. **Review the specification** - Understand all components
2. **Check the deployment plan** - Follow implementation steps
3. **Set up monitoring** - Use the monitoring strategy
4. **Iterate if needed** - Refine based on feedback
5. **Implement** - Build according to the design

## 🎉 You're Ready!

Your MetaMind frontend is now running with:
- ✅ Beautiful web interface
- ✅ Real-time progress tracking
- ✅ Visual metrics dashboard
- ✅ Complete design history
- ✅ Downloadable specifications

**Visit http://localhost:8501 and start designing!** 🚀

---

**Need help?** Check the main [QUICKSTART.md](QUICKSTART.md) or [README.md](README.md)