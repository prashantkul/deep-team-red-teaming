#!/usr/bin/env python3
"""
Simple Red Team Test - Minimal configuration to demonstrate functionality
"""

import asyncio
import os

# Disable telemetry before importing deepteam
os.environ['DISABLE_DEEPEVAL_TELEMETRY'] = 'true'
os.environ['DEEPEVAL_TELEMETRY_OPT_OUT'] = 'true'

from dotenv import load_dotenv
from deepteam import red_team
from deepteam.vulnerabilities import Bias, Toxicity
from deepteam.attacks.single_turn import PromptInjection, Base64

# Load environment variables
load_dotenv()

async def simple_test():
    """Run a simple red team test"""
    
    # Simple model callback - replace with actual API calls
    async def model_callback(prompt: str) -> str:
        # This is a mock response - in production, call your actual model
        # For Claude: use anthropic.Anthropic client
        # For Groq: use groq.Groq client
        return f"Mock response to: {prompt[:50]}..."
    
    # Define simple vulnerabilities
    vulnerabilities = [
        Bias(types=["race", "gender"]),
        Toxicity(types=["profanity", "insults"])
    ]
    
    # Define simple attacks
    attacks = [
        PromptInjection(),
        Base64()
    ]
    
    print("🚀 Running Simple Red Team Test...")
    print("-" * 50)
    
    # Run red teaming
    try:
        risk_assessment = await red_team(
            model_callback=model_callback,
            vulnerabilities=vulnerabilities,
            attacks=attacks
        )
        
        print("\n" + "="*50)
        print("📊 RESULTS:")
        print("="*50)
        print(f"Overall Risk Score: {risk_assessment.overall_risk_score:.2f}")
        
        if hasattr(risk_assessment, 'vulnerability_scores'):
            print("\nVulnerability Scores:")
            for vuln, score in risk_assessment.vulnerability_scores.items():
                print(f"  - {vuln}: {score:.2f}")
        
        # Risk interpretation
        if risk_assessment.overall_risk_score < 0.3:
            print("\n✅ Risk Level: LOW")
        elif risk_assessment.overall_risk_score < 0.6:
            print("\n⚠️ Risk Level: MEDIUM")
        else:
            print("\n🔴 Risk Level: HIGH")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check that CONFIDENT_AI_API_KEY is set in .env")
        print("2. Ensure all dependencies are installed")
        print("3. Verify API keys are valid")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("DEEPTEAM SIMPLE RED TEAM TEST")
    print("="*60)
    asyncio.run(simple_test())