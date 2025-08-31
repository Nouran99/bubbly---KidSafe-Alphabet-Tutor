# 🤖 AI Configuration Guide

## Complete Guide to Setting Up AI-Powered Intelligence

### Overview

The KidSafe Alphabet Tutor now supports real AI models for intelligent conversation, moving beyond simple pattern matching to true natural language understanding.

## 🎯 Quick Start

### Fastest Setup (Local AI with Ollama)
```bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Download a model
ollama pull llama2

# 3. Start Ollama
ollama serve

# 4. Run AI app
python app/ai_app.py
```

## 📊 AI Model Comparison

| Model | Provider | Cost | Privacy | Quality | Speed | Setup |
|-------|----------|------|---------|---------|-------|--------|
| **Llama 2** | Ollama | Free | 100% Private | Good | Fast | Easy |
| **Mistral** | Ollama | Free | 100% Private | Very Good | Fast | Easy |
| **GPT-3.5** | OpenAI | ~$0.002/1K tokens | Cloud | Excellent | Fast | API Key |
| **GPT-4** | OpenAI | ~$0.03/1K tokens | Cloud | Best | Slower | API Key |
| **Phi-2** | Ollama | Free | 100% Private | Good | Very Fast | Easy |

## 🔧 Detailed Setup Instructions

### Option 1: Ollama (Recommended - Free & Private)

#### Installation

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from [ollama.ai/download](https://ollama.ai/download)

#### Model Selection

```bash
# Small & Fast (3GB)
ollama pull phi

# Balanced (4GB)
ollama pull llama2

# Best Quality (4GB)
ollama pull mistral

# Coding-focused
ollama pull codellama
```

#### Configuration
```env
# .env file
USE_OLLAMA=true
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434
```

#### Running
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Run app
python app/ai_app.py
```

### Option 2: OpenAI GPT

#### Setup
1. Get API key from [platform.openai.com](https://platform.openai.com)
2. Add to `.env`:
```env
OPENAI_API_KEY=sk-...
USE_OLLAMA=false
OPENAI_MODEL=gpt-3.5-turbo
```

#### Cost Optimization
```python
# In .env for cost control
MAX_TOKENS=150  # Limit response length
TEMPERATURE=0.7  # Balance creativity/consistency
```

### Option 3: Hybrid (Fallback)

```env
# Try Ollama first, fallback to OpenAI
USE_OLLAMA=true
OPENAI_API_KEY=sk-...  # Backup
FALLBACK_TO_OPENAI=true
```

## 🧠 AI Agent Configuration

### Understanding Agent
```python
# Controls intent detection and entity extraction
UNDERSTANDING_MODEL=llama2
UNDERSTANDING_TEMPERATURE=0.3  # Lower = more precise
```

### Lesson Agent
```python
# Controls teaching content generation
LESSON_MODEL=mistral
LESSON_TEMPERATURE=0.7  # Balanced creativity
LESSON_MAX_TOKENS=200
```

### Feedback Agent
```python
# Controls encouragement and corrections
FEEDBACK_MODEL=llama2
FEEDBACK_TEMPERATURE=0.8  # Higher = more varied
```

### Safety Agent
```python
# Controls content filtering
SAFETY_MODEL=llama2
SAFETY_TEMPERATURE=0.1  # Very low = strict
```

## 📈 Performance Optimization

### Memory Management
```python
# Limit conversation history (COPPA compliance)
CONVERSATION_BUFFER_SIZE=3  # Keep last 3 exchanges
CLEAR_MEMORY_AFTER_MINUTES=30
```

### Response Speed
```python
# Optimize for speed
USE_STREAMING=true  # Show response as it generates
CACHE_RESPONSES=true  # Cache common questions
PREFETCH_NEXT_LETTER=true  # Prepare next lesson
```

### Resource Usage
```python
# For limited hardware
USE_QUANTIZED_MODELS=true  # Smaller model files
MAX_MEMORY_GB=4  # Limit RAM usage
USE_GPU=false  # CPU-only mode
```

## 🔍 Monitoring & Debugging

### Enable Detailed Logging
```python
# In .env
AI_DEBUG=true
LOG_LEVEL=DEBUG
LOG_EXTRACTED_DATA=true
LOG_RESPONSE_TIME=true
```

### View AI Decisions
```python
# The AI panel shows:
- Extracted entities (name, age, letter)
- Detected intent
- Confidence scores
- Emotion detection
- Response generation time
```

### Test AI Understanding
```python
# Test sentences to verify AI is working:
"My name is Emma and I'm 6 years old"
# Should extract: name=Emma, age=6

"I want to learn the letter B please"
# Should extract: letter=B, intent=learn_letter

"This is too hard, can we try something easier?"
# Should detect: emotion=frustrated, intent=difficulty_adjustment
```

## 🚀 Advanced Features

### Custom Prompts
```python
# Customize AI personality in crew_ai_powered.py
SYSTEM_PROMPT = """
You are Bubbly, a cheerful alphabet tutor.
Always be encouraging and use simple language.
Limit responses to 2-3 sentences.
"""
```

### Multi-Language Support
```env
# Configure language
AI_LANGUAGE=english  # or spanish, french, etc.
TRANSLATE_RESPONSES=true
```

### Voice Integration
```env
# Enable AI-powered speech
ENABLE_VOICE_INPUT=true
VOICE_TO_TEXT_MODEL=whisper
TEXT_TO_VOICE_MODEL=elevenlabs
```

## 📊 Data Extraction Examples

### What AI Extracts from Conversations:

| User Says | AI Extracts |
|-----------|-------------|
| "Hi I'm Alex" | name: "Alex", intent: "introduction" |
| "I'm 5" | age: 5, age_range: "3-5" |
| "Teach me B" | letter: "B", intent: "learn_letter" |
| "Next one" | intent: "next_letter" |
| "I don't get it" | emotion: "confused", intent: "help" |
| "Yay!" | emotion: "excited" |
| "My mom is here" | relationship: "parent_present" |

## 🔒 Privacy & Safety

### COPPA Compliance
```python
# AI is configured to:
- Never store personal data
- Clear memory after each session
- Reject requests for personal info
- Filter inappropriate content
```

### Local-Only Mode
```env
# Complete privacy - no external APIs
USE_OLLAMA=true
DISABLE_TELEMETRY=true
OFFLINE_MODE=true
```

## 🆘 Troubleshooting

### AI Not Responding?
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Check model is loaded
ollama list

# Test model directly
ollama run llama2 "Hello"
```

### Slow Responses?
```bash
# Use smaller model
ollama pull phi

# Reduce token limit
echo "MAX_TOKENS=100" >> .env

# Enable GPU if available
echo "OLLAMA_GPU=true" >> .env
```

### Fallback to Rule-Based?
```bash
# AI will automatically fallback if:
- No models available
- API key invalid
- Network issues
- Resource constraints

# Force rule-based mode:
python app/simple_app.py
```

## 📚 Additional Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [LangChain Docs](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Model Comparison](https://artificialanalysis.ai/)

## 💡 Pro Tips

1. **Start with Ollama + Llama2** - Free, private, good quality
2. **Use GPT-3.5 for production** - Best quality/cost ratio
3. **Enable caching** - Reduces API calls and costs
4. **Monitor extraction accuracy** - Check the AI panel regularly
5. **Adjust temperature** - Lower for consistency, higher for creativity

---

*Need help? Check the main [README](../README.md) or [Troubleshooting Guide](TROUBLESHOOTING.md)*