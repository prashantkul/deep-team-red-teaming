#!/usr/bin/env python3
"""
Red Team Testing Tool
Main interface for running LLM red team assessments
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from final_working_wrapper import run_comprehensive_red_team_test

def print_banner():
    """Print banner"""
    print("\n" + "="*80)
    print("🛡️  DEEPTEAM LLM RED TEAM ASSESSMENT TOOL")
    print("="*80)
    print("Target Model: Claude 3.5 Sonnet")
    print("Evaluator Model: Groq Llama 3.1-8b")
    print("Framework: DeepTeam-compatible implementation")
    print("="*80)

async def run_assessment():
    """Run the assessment"""
    try:
        print("🚀 Starting comprehensive red team assessment...")
        print("This will test 15 different attack scenarios across 5 vulnerability categories")
        print("\nPress Ctrl+C to interrupt at any time\n")
        
        assessment = await run_comprehensive_red_team_test()
        
        if assessment:
            print("\n✅ Assessment completed successfully!")
            print(f"\nResults saved in the 'reports/' directory")
            print("Check the JSON file for detailed analysis")
        else:
            print("\n❌ Assessment failed")
            
    except KeyboardInterrupt:
        print("\n⚠️ Assessment interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure API keys are set in .env file")
        print("2. Check that conda environment is activated: conda activate deepteam-poc")
        print("3. Verify network connectivity")

def check_prerequisites():
    """Check if prerequisites are met"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ Error: .env file not found")
        print("Please create .env file with your API keys")
        return False
    
    # Check if reports directory exists, create if not
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Red Team Testing Tool for LLMs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python red_team.py                    # Run comprehensive assessment
  python red_team.py --help            # Show this help message

The tool will:
1. Test Claude 3.5 Sonnet with 15 different attack scenarios
2. Evaluate responses using Groq Llama 3.1-8b
3. Generate detailed risk assessment report
4. Save results to reports/ directory
        """
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version='DeepTeam Red Team Tool v1.0'
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    if not check_prerequisites():
        sys.exit(1)
    
    # Run the assessment
    asyncio.run(run_assessment())

if __name__ == "__main__":
    main()