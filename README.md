# DeepTeam Multi-Turn Attack Testing Framework

A comprehensive framework for testing AI agents using DeepTeam's multi-turn attack capabilities with true conversation context awareness.

## 🎯 Features

- **True Multi-Turn Attacks**: Progressive conversation-aware attacks that build on previous responses
- **Context-Aware Agent**: Travel advisor agent with conversation memory and realistic responses
- **DeepTeam Integration**: Proper vulnerability mapping and attack-specific configurations
- **Interactive Testing**: Select specific vulnerabilities and attack types for targeted testing
- **Comprehensive Reporting**: Detailed conversation logs and analysis

## 🚀 Quick Start

### Prerequisites
```bash
conda create -n deepteam-poc python=3.10
conda activate deepteam-poc
pip install -r requirements.txt
```

### Environment Setup
Create `.env` file with your API keys:
```
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key  
TAVILY_API_KEY=your_tavily_key
```

### Run Tests
```bash
# LinearJailbreaking with vulnerability selection
python test_true_multiturn_linear.py

# BadLikertJudge with category selection  
python test_bad_likert_judge_direct.py

# SequentialJailbreak with type/persona selection
python test_sequential_jailbreak_direct.py

# TreeJailbreaking
python test_tree_jailbreaking_direct.py

# CrescendoJailbreaking
python test_crescendo_jailbreaking_direct.py

# Single-turn tests (framework-based)
python test_deepteam_singleturn.py

# Agent memory diagnostic
python test_memory_persistence.py
```

## 📁 Project Structure

```
deep-team/
├── agent/                          # Travel advisor agent implementation
│   ├── agent.py                   # Main agent with context awareness
│   ├── memory_bank.py             # Conversation memory management
│   ├── tools.py                   # Tavily search integration
│   └── llm_backend.py             # LLM backend configuration
├── reports/                        # Test execution reports (JSON)
├── results/                        # Screenshots and artifacts
├── deepteam_test_utils.py         # Shared testing utilities
├── test_true_multiturn_linear.py  # LinearJailbreaking (10 vulnerabilities)
├── test_bad_likert_judge_direct.py # BadLikertJudge (50+ categories)
├── test_sequential_jailbreak_direct.py # SequentialJailbreak (types/personas)
├── test_tree_jailbreaking_direct.py # TreeJailbreaking
├── test_crescendo_jailbreaking_direct.py # CrescendoJailbreaking
├── test_deepteam_singleturn.py    # Single-turn framework tests
├── test_memory_persistence.py     # Memory diagnostic tool
├── run_all_direct_multiturn_tests.py # Master test runner
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🎯 Attack Types & Vulnerabilities

### Multi-Turn Attacks

#### 🔄 LinearJailbreaking
**Progressive pressure with systematic conversation building**

- **Supported Vulnerabilities**: 10 general-purpose categories
  1. **PromptLeakage** - System prompt and configuration extraction
  2. **PIILeakage** - Personal information disclosure testing  
  3. **RBAC** - Role-based access control bypass attempts
  4. **ExcessiveAgency** - Unauthorized action execution testing
  5. **DebugAccess** - Debug mode and development interface access
  6. **Robustness** - Goal hijacking and input overreliance testing
  7. **Bias** - Biased response and unfair treatment testing
  8. **Toxicity** - Harmful or toxic content generation attempts
  9. **IllegalActivity** - Illegal activity guidance requests
  10. **Misinformation** - False information generation testing

- **Behavior**: Each turn builds on previous LLM responses with progressive refinement
- **Usage**: `python test_true_multiturn_linear.py`
- **Configuration**: Interactive vulnerability selection (1,3,6) or 'all'

#### ⚖️ BadLikertJudge  
**Biased evaluation and judgment manipulation**

- **Supported Categories**: 50+ DeepTeam-specific categories grouped by type:

  **Bias & Discrimination**: `bias`, `religion`, `politics`, `gender`, `race`
  
  **Toxicity & Harassment**: `toxicity`, `profanity`, `insults`, `threats`, `mockery`, `bullying`
  
  **Illegal Activities**: `illegal_activity`, `weapons`, `violent_crimes`, `cybercrime`, `unauthorized_access`
  
  **Security Vulnerabilities**: `bfla`, `bola`, `rbac`, `sql_injection`, `shell_injection`
  
  **Safety & Harm**: `personal_safety`, `self-harm`, `unsafe_practices`, `stalking`
  
  **Content Issues**: `graphic_content`, `sexual_content`, `pornographic_content`
  
  **Information Integrity**: `misinformation`, `factual_errors`, `unsupported_claims`
  
  **Data Protection**: `pii_leakage`, `database_access`, `direct_disclosure`, `session_leak`
  
  **System Security**: `prompt_leakage`, `secrets_and_credentials`, `instructions`, `guard_exposure`
  
  **Agency & Control**: `excessive_agency`, `functionality`, `permissions`, `autonomy`
  
  **Robustness**: `robustness`, `input_overreliance`, `hijacking`
  
  **Intellectual Property**: `intellectual_property`, `copyright_violations`, `trademark_infringement`
  
  **Competition**: `competition`, `competitor_mention`, `market_manipulation`

- **Behavior**: Tests biased evaluation systems and judgment manipulation
- **Usage**: `python test_bad_likert_judge_direct.py`
- **Configuration**: Interactive category selection with grouped presentation

#### 🔄 SequentialJailbreak
**Systematic step-by-step approach with configurable types and personas**

- **Attack Types**: 3 distinct approaches
  1. **dialogue** - Conversational approach (requires persona)
  2. **question_bank** - Structured interrogation (no persona)
  3. **game_environment** - Scenario-based testing (no persona)

- **Personas** (for dialogue type only): 4 character approaches
  1. **student** - Curious, academic questioning approach
  2. **researcher** - Systematic, scientific inquiry method
  3. **prisoner** - Manipulative, desperate persuasion tactics  
  4. **generic** - Neutral conversation style

- **Supported Combinations**: 6 total configurations
  - dialogue + student
  - dialogue + researcher  
  - dialogue + prisoner
  - dialogue + generic
  - question_bank (standalone)
  - game_environment (standalone)

- **Behavior**: Methodical testing of security layers with persona-specific approaches
- **Usage**: `python test_sequential_jailbreak_direct.py`
- **Configuration**: Interactive selection of attack types and personas

#### 🌳 TreeJailbreaking
**Tree-based exploration of multiple attack paths**

- **Supported Vulnerabilities**: General-purpose (all DeepTeam vulnerabilities)
- **Behavior**: Explores different attack vectors through branching strategies
- **Best For**: Testing multiple approaches to complex vulnerabilities
- **Usage**: `python test_tree_jailbreaking_direct.py`
- **Configuration**: Custom vulnerability-specific prompts

#### 🎵 CrescendoJailbreaking  
**Gradual escalation strategy with intensity building**

- **Supported Vulnerabilities**: General-purpose (all DeepTeam vulnerabilities)
- **Behavior**: Progressive intensity escalation with sophistication building
- **Best For**: Testing gradual boundary pushing and escalation resistance
- **Usage**: `python test_crescendo_jailbreaking_direct.py`
- **Configuration**: Configurable max_rounds and max_backtracks

### Single-Turn Framework Tests

#### 📋 DeepTeam Single-Turn
**Traditional framework-based vulnerability testing**

- **Vulnerabilities**: Full DeepTeam vulnerability suite
- **Attacks**: Base64, ROT13, Leetspeak, Roleplay, PromptInjection, etc.
- **Usage**: `python test_deepteam_singleturn.py`
- **Behavior**: Classic single-request/response testing patterns

## 🧠 Agent Features

### Context-Aware Travel Advisor
- **Memory Persistence**: Maintains conversation history across turns
- **Progressive Responses**: Acknowledges previous interactions
- **Security Boundaries**: Resists attacks while showing conversation awareness
- **Tavily Integration**: Real-time search instead of hardcoded responses

### Intentional Vulnerabilities
- Goal manipulation susceptibility
- Authority escalation possibilities  
- Memory poisoning vulnerabilities
- Tool misuse potential
- Context injection weaknesses

## 📊 Reporting

Each test generates detailed JSON reports including:
- Conversation logs with timestamps
- Attack progression analysis
- Agent response patterns
- Security boundary testing results
- Console output capture

Reports are saved in `reports/` directory with timestamps.

## 🔧 Key Components

### DeepTeam Integration
- Uses DeepTeam's actual vulnerability mappings
- Proper attack-specific configurations
- Interactive vulnerability/category selection
- True multi-turn behavior (not single-turn disguised)

### Agent Context Awareness
- Fixed conversation-blind issue
- Retrieves and uses conversation history
- Progressive response acknowledgment  
- Realistic multi-turn dynamics

## 📚 Educational Use

Perfect for:
- AI security research classes
- Red teaming demonstrations
- Multi-turn attack vector analysis
- Agent vulnerability assessment
- Conversation-aware AI testing

## ⚠️ Security Notice

This framework is designed for **defensive security research and education only**. The intentionally vulnerable agent and attack simulations should only be used for:
- Academic research
- Security testing of your own systems
- Educational demonstrations
- Defensive security development

## 🤝 Contributing

This is a POC framework for educational purposes. Feel free to extend with additional:
- Attack types
- Vulnerability categories  
- Agent implementations
- Reporting features