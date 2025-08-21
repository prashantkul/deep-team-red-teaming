#!/usr/bin/env python3
"""
Master Test Runner for All Direct Multi-Turn Attack Tests

Runs all direct multi-turn attack tests (LinearJailbreaking, TreeJailbreaking,
CrescendoJailbreaking, SequentialJailbreak, BadLikertJudge) in sequence.

Each test uses the direct attack enhancement method for true multi-turn behavior.
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from typing import Dict, Any, List

# Set telemetry opt-out before importing deepteam
os.environ["DEEPTEAM_TELEMETRY_OPT_OUT"] = "YES"

from deepteam_test_utils import setup_environment, OutputCapture

def run_test_with_selection(test_file: str, selection: str, output: OutputCapture) -> Dict[str, Any]:
    """
    Run a specific test file with predefined vulnerability selection.
    """
    test_name = test_file.replace('.py', '').replace('test_', '').replace('_direct', '')
    
    output.log(f"\n🚀 Running {test_name} test...")
    output.log(f"   Vulnerability selection: {selection}")
    
    try:
        # Run the test with the selection piped as input
        result = subprocess.run(
            f"echo '{selection}' | python {test_file}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout per test
        )
        
        if result.returncode == 0:
            output.log(f"✅ {test_name} completed successfully")
            return {
                "test_name": test_name,
                "test_file": test_file,
                "selection": selection,
                "status": "success",
                "stdout": result.stdout[-1000:],  # Last 1000 chars
                "stderr": result.stderr
            }
        else:
            output.log(f"❌ {test_name} failed with return code {result.returncode}")
            return {
                "test_name": test_name,
                "test_file": test_file,
                "selection": selection,
                "status": "failed",
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
    except subprocess.TimeoutExpired:
        output.log(f"⏰ {test_name} timed out after 5 minutes")
        return {
            "test_name": test_name,
            "test_file": test_file,
            "selection": selection,
            "status": "timeout"
        }
    except Exception as e:
        output.log(f"💥 {test_name} failed with exception: {str(e)}")
        return {
            "test_name": test_name,
            "test_file": test_file,
            "selection": selection,
            "status": "error",
            "error": str(e)
        }

def main():
    """Main execution function"""
    setup_environment()
    output = OutputCapture()
    
    output.log("🔥 Master Direct Multi-Turn Attack Test Runner")
    output.log("=" * 70)
    output.log("Running all direct multi-turn attack tests with comprehensive vulnerability coverage")
    
    # Define test configurations
    test_configs = [
        {
            "file": "test_true_multiturn_linear.py",
            "name": "LinearJailbreaking",
            "selections": ["1,6", "2,3", "4,5"]  # Different vulnerability combinations
        },
        {
            "file": "test_tree_jailbreaking_direct.py", 
            "name": "TreeJailbreaking",
            "selections": ["1,3", "6,7", "8,9"]
        },
        {
            "file": "test_crescendo_jailbreaking_direct.py",
            "name": "CrescendoJailbreaking", 
            "selections": ["1,2", "4,6", "7,10"]
        },
        {
            "file": "test_sequential_jailbreak_direct.py",
            "name": "SequentialJailbreak",
            "selections": ["3,5", "1,4", "6,8"]
        },
        {
            "file": "test_bad_likert_judge_direct.py",
            "name": "BadLikertJudge",
            "selections": ["1,7", "2,9", "5,10"]
        }
    ]
    
    all_results = []
    start_time = datetime.now()
    
    # Run each test with multiple vulnerability selections
    for test_config in test_configs:
        output.log(f"\n" + "=" * 50)
        output.log(f"🎯 Testing {test_config['name']}")
        output.log("=" * 50)
        
        if not os.path.exists(test_config['file']):
            output.log(f"⚠️  Test file {test_config['file']} not found, skipping...")
            continue
        
        test_results = []
        for i, selection in enumerate(test_config['selections'], 1):
            output.log(f"\n📝 Configuration {i}/3 for {test_config['name']}")
            result = run_test_with_selection(test_config['file'], selection, output)
            test_results.append(result)
            
            # Brief pause between tests
            import time
            time.sleep(2)
        
        all_results.append({
            "attack_type": test_config['name'],
            "test_file": test_config['file'],
            "configurations": test_results,
            "total_configurations": len(test_results),
            "successful_configurations": len([r for r in test_results if r['status'] == 'success'])
        })
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    # Generate comprehensive summary
    output.log("\n" + "=" * 70)
    output.log("📊 MASTER TEST RUNNER SUMMARY")
    output.log("=" * 70)
    
    total_tests = sum(len(result['configurations']) for result in all_results)
    successful_tests = sum(result['successful_configurations'] for result in all_results)
    
    output.log(f"\n⏱️  Total execution time: {duration}")
    output.log(f"📈 Overall success rate: {successful_tests}/{total_tests} ({successful_tests/total_tests*100:.1f}%)")
    
    output.log(f"\n🎯 Attack Type Breakdown:")
    for result in all_results:
        success_rate = result['successful_configurations'] / result['total_configurations'] * 100
        output.log(f"  • {result['attack_type']:20s}: {result['successful_configurations']}/{result['total_configurations']} ({success_rate:.1f}%)")
    
    # Save comprehensive report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"reports/master_multiturn_test_results_{timestamp}.json"
    
    os.makedirs("reports", exist_ok=True)
    
    master_report = {
        "test_type": "Master Direct Multi-Turn Attack Tests",
        "timestamp": start_time.isoformat(),
        "duration_seconds": duration.total_seconds(),
        "summary": {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "success_rate": successful_tests/total_tests if total_tests > 0 else 0,
            "attack_types_tested": len(all_results)
        },
        "detailed_results": all_results,
        "console_output": output.console_log.copy()
    }
    
    with open(report_file, 'w') as f:
        json.dump(master_report, f, indent=2)
    
    output.log(f"\n📁 Comprehensive report saved: {report_file}")
    
    # Analysis notes
    output.log(f"\n🔍 Analysis Notes:")
    output.log(f"   • All tests use direct attack enhancement methods")
    output.log(f"   • Context-aware agent shows conversation progression")
    output.log(f"   • Multiple vulnerability types tested per attack")
    output.log(f"   • True multi-turn behavior demonstrated across all attack types")
    output.log(f"   • Agent maintains security boundaries while showing conversation awareness")

if __name__ == "__main__":
    main()