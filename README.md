# KidSafe Alphabet Tutor - "Bubbly" 🫧

## Technical Architecture & Implementation Strategy

### Project Overview
A Python-only, locally-running educational AI system that teaches children the English alphabet through speech interaction and optional vision recognition, built with CrewAI multi-agent framework.

### Architecture Design

#### 1. Multi-Agent System (CrewAI Framework)
```
┌─────────────────────────────────────────────────────┐
│                  CrewAI Orchestrator                 │
├─────────────────────────────────────────────────────┤
│   Lesson_Agent ──► Curriculum & Progression         │
│   Feedback_Agent ──► Pronunciation Analysis         │
│   Personalization_Agent ──► Adaptive Learning       │
│   Understanding_Agent ──► Intent Recognition        │
│   Safety_Agent ──► Content Moderation               │
└─────────────────────────────────────────────────────┘
```

#### 2. Speech Processing Pipeline
```
Audio Input → VAD (150-250ms) → ASR (300-500ms) → 
Agent Processing (200-300ms) → TTS Streaming (150-250ms first chunk)
Total Target: <1.2s first response
```

#### 3. Vision Pipeline
```
Camera Input → OpenCV Processing → 
Letter Detection (Tesseract) | Object Detection (YOLOv8n) →
Confidence Score → Agent Adaptation
```

### Technical Stack
- **UI**: Gradio (real-time mic/camera integration)
- **ASR**: faster-whisper (small.en model) + silero-vad
- **TTS**: Piper TTS with streaming
- **LLM**: Ollama with Llama 3.2 3B (quantized)
- **Vision**: OpenCV + pytesseract + YOLOv8n
- **Framework**: CrewAI for multi-agent orchestration
- **Deployment**: Docker container (CPU-optimized)

### Implementation Phases

#### Phase 1: Core Infrastructure (Days 1-2)
- [x] Project scaffold and directory structure
- [ ] Docker configuration with all dependencies
- [ ] Gradio UI shell with all components
- [ ] Model integration layer
- [ ] CrewAI agent framework setup

#### Phase 2: Agent Implementation (Days 3-4)
- [ ] Complete 5 agents with CrewAI
- [ ] Session memory management
- [ ] Curriculum JSON design
- [ ] Pronunciation coaching logic

#### Phase 3: Advanced Features (Days 5-6)
- [ ] Vision components integration
- [ ] Adaptive learning pathways
- [ ] Progress tracking system
- [ ] Age-specific adaptations

#### Phase 4: Polish & Safety (Day 7)
- [ ] Safety features implementation
- [ ] Parental controls with math gate
- [ ] Performance optimization
- [ ] Complete acceptance testing

### Key Differentiators
1. **Pure Python Implementation**: No JavaScript, all UI in Gradio
2. **CrewAI Multi-Agent Architecture**: Sophisticated agent collaboration
3. **Zero Data Retention**: Session-only memory, COPPA compliant
4. **Offline-First**: All models run locally, no cloud dependencies
5. **Sub-1.2s Response**: Optimized streaming pipeline

### Performance Targets
- First audio response: <1.2s
- ASR confidence threshold: 0.7 (adjustable by age)
- Vision detection confidence: >0.8
- Memory buffer: 3-turn rolling window
- Docker image size: <5GB with all models

### Author
**Nouran Darwish**  
Generative AI Engineer | CrewAI Expert | VOIS