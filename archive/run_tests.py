#!/usr/bin/env python3
"""
Main script to run red team tests with different configurations
"""

import asyncio
import argparse
from systematic_red_team_framework import SystematicRedTeamer, TestCategory

async def run_quick_test():
    """Run a quick test with limited scenarios"""
    print("\n🚀 Running Quick Red Team Test...")
    print("-" * 50)
    
    tester = SystematicRedTeamer()
    
    # Run only critical categories for quick test
    results, evaluation = await tester.run_systematic_test(
        categories=[TestCategory.JAILBREAK, TestCategory.PRIVACY]
    )
    
    print("\n✅ Quick test completed!")
    return results, evaluation

async def run_full_test():
    """Run comprehensive test across all categories"""
    print("\n🚀 Running Full Red Team Test Suite...")
    print("-" * 50)
    
    tester = SystematicRedTeamer()
    results, evaluation = await tester.run_systematic_test()
    
    print("\n✅ Full test suite completed!")
    return results, evaluation

async def run_category_test(category: str):
    """Run test for a specific category"""
    print(f"\n🚀 Running {category.upper()} Category Test...")
    print("-" * 50)
    
    tester = SystematicRedTeamer()
    
    # Map string to enum
    category_map = {
        "bias": TestCategory.BIAS,
        "toxicity": TestCategory.TOXICITY,
        "privacy": TestCategory.PRIVACY,
        "misinformation": TestCategory.MISINFORMATION,
        "jailbreak": TestCategory.JAILBREAK,
        "injection": TestCategory.INJECTION,
        "custom": TestCategory.CUSTOM
    }
    
    if category.lower() not in category_map:
        print(f"❌ Invalid category: {category}")
        print(f"Available categories: {', '.join(category_map.keys())}")
        return None, None
    
    results, evaluation = await tester.run_systematic_test(
        categories=[category_map[category.lower()]]
    )
    
    print(f"\n✅ {category.upper()} test completed!")
    return results, evaluation

def main():
    parser = argparse.ArgumentParser(
        description="Red Team Testing Framework for LLMs and Agents"
    )
    
    parser.add_argument(
        "--mode",
        choices=["quick", "full", "category"],
        default="quick",
        help="Testing mode: quick (2 categories), full (all categories), or category (specific)"
    )
    
    parser.add_argument(
        "--category",
        type=str,
        help="Specific category to test (bias, toxicity, privacy, misinformation, jailbreak, injection, custom)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("🛡️  RED TEAM TESTING FRAMEWORK")
    print("Target Model: Claude 3.5 Sonnet")
    print("Evaluation Model: Groq Llama 3.1-8b")
    print("="*60)
    
    if args.mode == "quick":
        asyncio.run(run_quick_test())
    elif args.mode == "full":
        asyncio.run(run_full_test())
    elif args.mode == "category":
        if not args.category:
            print("❌ Error: --category argument required for category mode")
            parser.print_help()
        else:
            asyncio.run(run_category_test(args.category))

if __name__ == "__main__":
    main()