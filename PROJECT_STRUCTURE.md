# Project Structure - DeepTeam POC

## Overview
This project implements a POC for red teaming LLMs and Agents using the DeepTeam framework for agentic vulnerability testing.

## Directory Structure

```
deep-team/
├── .env                           # API keys (OpenAI, Anthropic, Groq, Tavily, Google)
├── .gitignore                     # Git ignore file
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── IMPLEMENTATION_SUMMARY.md      # Implementation details
├── PROJECT_STRUCTURE.md          # This file
│
├── agent/                         # Travel advisor agent implementation
│   ├── __init__.py                # Package initialization
│   ├── agent.py                   # Main agent with intentional vulnerabilities
│   ├── memory_bank.py             # Memory management system
│   ├── tools.py                   # Travel tools with Tavily API integration
│   ├── llm_backend.py             # LLM integration (Groq, Claude, Gemini)
│   └── main.py                    # Agent demo runner
│
├── test_deepteam_singleturn.py   # Working DeepTeam tests (single-turn attacks only)
│
├── reports/                       # Test results and reports
│   └── [generated reports]        # JSON reports from testing
│
├── agent_memory/                  # Agent persistent memory storage
│   └── [memory files]             # User profiles and conversation history
│
└── deepteam-reference/            # DeepTeam library reference
    └── [reference files]          # Documentation and examples
```

## Key Components

### Agent Implementation (`agent/`)
- **agent.py**: Travel advisor agent with intentional vulnerabilities for testing
  - Goal manipulation vulnerability
  - Memory poisoning vulnerability  
  - Authority escalation paths
  - Google ADK compatibility with root_agent export
  
- **tools.py**: Travel-related tools
  - Tavily API integration for real-time search
  - Flight, hotel, weather, visa services
  - Payment and emergency contact management
  
- **memory_bank.py**: Persistent memory system
  - User profile tracking
  - Conversation history
  - Preference learning

- **llm_backend.py**: Multi-model LLM support
  - Groq (Llama 3.1)
  - Anthropic (Claude)
  - Google (Gemini)

### Testing Framework

- **test_deepteam_singleturn.py**: Main testing script
  - Uses DeepTeam's agentic vulnerabilities
  - Single-turn attacks only (multi-turn has validation issues)
  - Tests 5 vulnerability types:
    - GoalTheft
    - RecursiveHijacking
    - ExcessiveAgency
    - Robustness
    - RBAC (Role-Based Access Control)

### Configuration

- **.env**: API keys configuration
  ```
  ANTHROPIC_API_KEY=your_key
  GROQ_API_KEY=your_key
  OPENAI_API_KEY=your_key
  GOOGLE_API_KEY=your_key
  TAVILY_API_KEY=your_key
  ```

- **requirements.txt**: Dependencies
  - deepteam
  - anthropic
  - groq
  - google-adk
  - tavily-python>=0.3.0
  - python-dotenv

## Usage

### Setup Environment
```bash
conda activate deepteam-poc
pip install -r requirements.txt
```

### Run Agent Demo
```bash
python agent/main.py
```

### Run DeepTeam Tests
```bash
python test_deepteam_singleturn.py
```

### Test with Google ADK
```bash
adk web  # Opens web interface for agent testing
```

## Known Issues

1. **Multi-turn attacks**: DeepTeam's multi-turn attacks (CrescendoJailbreaking, LinearJailbreaking, TreeJailbreaking) have validation errors with the current setup
2. **Telemetry**: Must set `DEEPTEAM_TELEMETRY_OPT_OUT=YES` to avoid telemetry errors
3. **Google ADK**: Requires google-generativeai package for full ADK compatibility

## Test Results

The agent shows good resilience against single-turn attacks:
- Maintains role boundaries
- Doesn't reveal internal objectives
- Resists goal manipulation attempts
- Handles authority escalation attempts appropriately

## Files Removed (Cleanup)

The following obsolete/non-working files were removed:
- deepteam_agent_redteam.py (multi-turn validation errors)
- test_deepteam_working.py (telemetry issues)
- test_deepteam_proper.py (old version)
- deepteam_agentic_test.py (old test)
- simple_agentic_redteam.py (replaced by singleturn)
- final_working_wrapper.py (old wrapper)
- red_team.py (old basic test)
- travel_agent.py (old agent implementation)
- test_deepteam_agent.py (old test)
- archive/ directory (old files)
- examples/ directory (old examples)

## Status

✅ **Working POC for agentic red teaming**
- Single-turn attacks functional
- Agent with intentional vulnerabilities implemented
- Tavily API integration working
- Google ADK compatibility added