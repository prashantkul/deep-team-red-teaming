# Clean Project Structure

## 📁 Final Directory Organization

```
deepteam-poc/
├── red_team.py                       # 🎯 MAIN TOOL - Run this for assessments
├── final_working_wrapper.py          # Core implementation with DeepTeam patterns
├── .env                              # API keys configuration
├── .gitignore                        # Git ignore rules
├── README.md                         # User documentation
├── IMPLEMENTATION_SUMMARY.md         # Technical documentation
├── PROJECT_STRUCTURE.md             # This file
│
├── reports/                          # 📊 Assessment Results
│   ├── red_team_assessment_*.json   # Detailed test results
│   └── direct_test_results.json     # Example results
│
├── examples/                         # 📚 Example Implementations
│   ├── direct_test.py               # Simple API testing example
│   └── red_team_llm.py              # DeepTeam wrapper example
│
├── archive/                          # 📦 Development History
│   ├── basic_red_team_test.py       # Initial basic implementation
│   ├── simple_test.py               # Minimal test example
│   ├── systematic_red_team_framework.py # Complex framework attempt
│   └── run_tests.py                 # CLI interface prototype
│
└── deepteam-reference/              # 📖 Original DeepTeam Repository
    └── [DeepTeam source code]       # Reference implementation
```

## 🎯 Primary Files

### **red_team.py** - Main Tool
- **Purpose**: Single command interface for running assessments
- **Usage**: `python red_team.py`
- **Features**: CLI interface, prerequisite checking, banner display

### **final_working_wrapper.py** - Core Engine
- **Purpose**: Production-ready red teaming implementation
- **Features**: 15 test scenarios, multi-model support, JSON reporting
- **Architecture**: Follows DeepTeam model callback patterns

### **.env** - Configuration
- **Purpose**: API key storage
- **Required**: ANTHROPIC_API_KEY, GROQ_API_KEY
- **Security**: Excluded from git via .gitignore

## 📊 Reports Directory

### Automatic Report Generation
- All assessment results saved to `reports/`
- JSON format with detailed analysis
- Timestamp-based naming: `red_team_assessment_YYYYMMDD_HHMMSS.json`

### Report Contents
```json
{
  "metadata": {
    "timestamp": "20250819_185432",
    "target_model": "anthropic - claude-3-5-sonnet-20241022",
    "evaluator_model": "groq - llama-3.1-8b-instant",
    "total_tests": 15
  },
  "assessment": {
    "overall_risk_score": 0.453,
    "vulnerability_scores": {...},
    "test_cases": [...]
  }
}
```

## 📚 Examples Directory

### **direct_test.py**
- Simple implementation without DeepTeam wrapper
- Direct API calls to Claude and Groq
- Good for understanding basic concepts

### **red_team_llm.py**
- DeepTeam-compliant wrapper implementation
- Demonstrates official patterns
- Educational reference

## 📦 Archive Directory

### Development History
- **basic_red_team_test.py**: Initial POC implementation
- **simple_test.py**: Minimal test case
- **systematic_red_team_framework.py**: Complex framework attempt
- **run_tests.py**: CLI prototype

These files are preserved for:
- Development history
- Alternative approaches
- Learning examples

## 🚀 Usage Workflow

### 1. **Setup** (One time)
```bash
conda create -n deepteam-poc python=3.10 -y
conda activate deepteam-poc
pip install -U deepteam anthropic groq python-dotenv
```

### 2. **Configure** (One time)
```bash
# Edit .env file with your API keys
nano .env
```

### 3. **Run Assessment** (Repeatable)
```bash
python red_team.py
```

### 4. **View Results**
```bash
# Check latest results
ls -la reports/
# View detailed analysis
cat reports/red_team_assessment_*.json | jq .
```

## 🧹 Cleanup Benefits

### Before Cleanup
- 11 Python files scattered in root
- Unclear which file to use
- No organized output structure
- Mixed experimental and production code

### After Cleanup
- ✅ **Single entry point**: `red_team.py`
- ✅ **Organized structure**: reports/, examples/, archive/
- ✅ **Clear documentation**: README.md with quick start
- ✅ **Production ready**: Clean, tested implementation

## 🔄 Maintenance

### Adding New Tests
1. Modify scenarios in `final_working_wrapper.py`
2. Test with `python red_team.py`
3. Results automatically saved to `reports/`

### Updating Documentation
1. User docs: `README.md`
2. Technical docs: `IMPLEMENTATION_SUMMARY.md`
3. Structure docs: This file

### Version Control
```bash
# Track only essential files
git add red_team.py final_working_wrapper.py README.md
git add .env.example  # Template only, not actual .env
git commit -m "Update red teaming implementation"
```

## 🎓 Educational Value

### Learning Path
1. **Start**: Read `README.md` for overview
2. **Quick Test**: Run `python red_team.py`
3. **Understand**: Study `examples/direct_test.py`
4. **Deep Dive**: Examine `final_working_wrapper.py`
5. **Advanced**: Review `examples/red_team_llm.py`
6. **Research**: Explore `deepteam-reference/`

### Key Concepts Demonstrated
- ✅ DeepTeam model callback patterns
- ✅ Multi-model AI evaluation
- ✅ Systematic vulnerability testing
- ✅ Production-ready error handling
- ✅ Structured reporting

---

**Status**: ✅ **PROJECT SUCCESSFULLY ORGANIZED**  
**Entry Point**: `python red_team.py`  
**Documentation**: `README.md`  
**Results**: `reports/` directory