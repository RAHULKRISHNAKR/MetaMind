# MetaMind Performance Optimization Guide

## 🔥 Reducing Laptop Heat During Development

MetaMind uses Ollama with Llama 3, which can be CPU-intensive. Here are strategies to reduce heat and improve performance:

## 🎯 Quick Fixes (Immediate Relief)

### 1. Reduce Max Iterations
Lower the number of improvement cycles:

```bash
# In your API request
{
  "max_iterations": 1  # Instead of 3-5
}
```

Or set in `.env`:
```bash
MAX_ITERATIONS=1
```

### 2. Use Smaller Model
Switch from Llama 3 8B to a smaller model:

```bash
# Stop Ollama
# Pull smaller model
ollama pull llama3.2:1b  # Much smaller, faster

# Update .env
OLLAMA_MODEL=llama3.2:1b
```

### 3. Limit Concurrent Requests
Only run one design at a time. Wait for completion before starting another.

### 4. Increase Temperature Limits (macOS)
```bash
# Check current temperature
sudo powermetrics --samplers smc -i1 -n1

# Improve cooling
# - Use laptop on hard, flat surface
# - Use cooling pad
# - Clean air vents
```

## 🛠️ Configuration Optimizations

### 1. Reduce LLM Temperature
Lower temperature = less computation:

**Edit each agent file:**
```python
self.llm = Ollama(
    base_url=ollama_base_url,
    model=model_name,
    temperature=0.1  # Lower = faster, more deterministic
)
```

### 2. Add Request Timeout
Prevent long-running requests:

**Edit `.env`:**
```bash
# Add timeout (seconds)
LLM_TIMEOUT=30
```

**Update agent initialization:**
```python
self.llm = Ollama(
    base_url=ollama_base_url,
    model=model_name,
    temperature=0.1,
    timeout=30  # 30 seconds max
)
```

### 3. Enable Ollama GPU Acceleration (if available)
If you have a GPU:

```bash
# Check if GPU is available
ollama list

# Ollama automatically uses GPU if available
# Verify with:
ollama run llama3 "test"
# Should show GPU usage in Activity Monitor
```

### 4. Reduce Candidate Architectures
Generate fewer candidates:

**Edit `backend/agents/architecture_generation_agent.py`:**
```python
# Line ~134
if len(architectures) > 3:  # Instead of 5
    architectures = architectures[:3]
```

## 🚀 Advanced Optimizations

### 1. Use Caching
Cache LLM responses to avoid repeated calls:

**Create `backend/utils/cache.py`:**
```python
import hashlib
import json
from functools import lru_cache

def cache_key(prompt: str) -> str:
    """Generate cache key from prompt."""
    return hashlib.md5(prompt.encode()).hexdigest()

# Use in agents
@lru_cache(maxsize=100)
def cached_llm_call(prompt_hash: str, prompt: str, llm):
    """Cache LLM responses."""
    return llm.invoke(prompt)
```

### 2. Batch Processing
Process multiple architectures in parallel (if you have multiple cores):

```python
from concurrent.futures import ThreadPoolExecutor

# In simulation_agent.py
with ThreadPoolExecutor(max_workers=2) as executor:
    futures = [executor.submit(self._simulate_single, arch) 
               for arch in architectures]
    results = [f.result() for f in futures]
```

### 3. Use Quantized Models
Smaller, faster models:

```bash
# Install quantized version
ollama pull llama3:8b-q4_0  # 4-bit quantization

# Update .env
OLLAMA_MODEL=llama3:8b-q4_0
```

### 4. Implement Rate Limiting
Prevent system overload:

**Edit `backend/api/main.py`:**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/design")
@limiter.limit("1/minute")  # Max 1 request per minute
async def create_design(request: Request, design_request: DesignRequest):
    # ... existing code
```

## 📊 Monitoring & Profiling

### 1. Monitor System Resources
```bash
# macOS
top -o cpu

# Or use Activity Monitor
# Look for "ollama" process
```

### 2. Profile LLM Calls
Add timing to see which agents are slowest:

```python
import time

def execute(self, state):
    start = time.time()
    # ... agent logic
    duration = time.time() - start
    print(f"⏱️  {self.__class__.__name__} took {duration:.2f}s")
    return state
```

### 3. Check Ollama Logs
```bash
# View Ollama logs
ollama logs

# Or check system logs
tail -f /var/log/system.log | grep ollama
```

## 🎯 Recommended Settings for Development

**For Minimal Heat:**
```bash
# .env
OLLAMA_MODEL=llama3.2:1b
MAX_ITERATIONS=1
LLM_TIMEOUT=30
```

**In API requests:**
```json
{
  "max_iterations": 1,
  "constraints": {
    "budget": 5000,
    "latency_target_ms": 300,
    "expected_users": 10000,
    "risk_tolerance": "medium",
    "compliance_level": "medium"
  }
}
```

**Agent temperature:**
```python
temperature=0.1  # In all agents
```

## 🔄 Alternative: Use Remote LLM

If local execution is too intensive, use a remote LLM:

### Option 1: OpenAI
```bash
pip install openai

# .env
OPENAI_API_KEY=your_key_here
USE_OPENAI=true
```

**Update agents:**
```python
from langchain_openai import ChatOpenAI

if os.getenv("USE_OPENAI") == "true":
    self.llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.1
    )
else:
    self.llm = Ollama(...)
```

### Option 2: Anthropic Claude
```bash
pip install anthropic

# .env
ANTHROPIC_API_KEY=your_key_here
USE_ANTHROPIC=true
```

## 📈 Performance Comparison

| Configuration | Heat | Speed | Quality |
|--------------|------|-------|---------|
| Llama 3 8B, 5 iterations | 🔥🔥🔥🔥 | ⏱️⏱️⏱️⏱️ | ⭐⭐⭐⭐⭐ |
| Llama 3 8B, 1 iteration | 🔥🔥🔥 | ⏱️⏱️⏱️ | ⭐⭐⭐⭐ |
| Llama 3.2 1B, 1 iteration | 🔥🔥 | ⏱️⏱️ | ⭐⭐⭐ |
| GPT-3.5 Turbo (remote) | 🔥 | ⏱️ | ⭐⭐⭐⭐ |
| GPT-4 (remote) | 🔥 | ⏱️⏱️ | ⭐⭐⭐⭐⭐ |

## 🎯 Quick Action Plan

**Right Now:**
1. Set `max_iterations=1` in your requests
2. Use cooling pad or elevate laptop
3. Close other applications

**Next 5 Minutes:**
1. Switch to smaller model: `ollama pull llama3.2:1b`
2. Update `.env`: `OLLAMA_MODEL=llama3.2:1b`
3. Restart backend

**Long Term:**
1. Consider using remote LLM for production
2. Implement caching for repeated requests
3. Add rate limiting to prevent overload

## 💡 Tips

- **Development**: Use small model + 1 iteration
- **Testing**: Use medium model + 2 iterations  
- **Production**: Use remote LLM or GPU-accelerated server
- **Demo**: Pre-generate results and cache them

## 🆘 Emergency Cool Down

If laptop is overheating:
```bash
# Stop Ollama immediately
pkill ollama

# Stop backend
# Press Ctrl+C in backend terminal

# Let laptop cool for 5-10 minutes
# Then restart with smaller model
```

---

**Remember**: Local LLMs are powerful but resource-intensive. For development, optimize for speed and heat. For production, use remote APIs or dedicated GPU servers.