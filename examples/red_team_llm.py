#!/usr/bin/env python3
"""
Red Team LLM Wrapper - DeepTeam Recommended Implementation
Following the official DeepTeam patterns for model callbacks and testing
"""

import os
import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime

# Disable telemetry
os.environ['DISABLE_DEEPEVAL_TELEMETRY'] = 'true'
os.environ['DEEPEVAL_TELEMETRY_OPT_OUT'] = 'true'

from dotenv import load_dotenv
import json

# DeepTeam imports
from deepteam import red_team
from deepteam.vulnerabilities import (
    Bias,
    Toxicity,
    PIILeakage,
    PromptLeakage,
    Misinformation,
    IllegalActivity,
    IntellectualProperty,
    SQLInjection,
    ShellInjection,
    CustomVulnerability,
    BFLA,
    BOLA,
    RBAC,
    DebugAccess,
    Competition,
    GraphicContent,
    PersonalSafety
)
from deepteam.attacks.single_turn import (
    PromptInjection,
    Base64,
    Leetspeak,
    ROT13,
    GrayBox
)
from deepteam.attacks.multi_turn import (
    LinearJailbreaking,
    CrescendoJailbreaking,
    TreeJailbreaking
)

# Model clients
from anthropic import Anthropic
from groq import Groq
from openai import OpenAI

# Load environment
load_dotenv()

class LLMWrapper:
    """
    Wrapper class for different LLM providers
    Implements the DeepTeam model_callback pattern
    """
    
    def __init__(self, provider: str = "anthropic", model: str = None):
        self.provider = provider
        
        if provider == "anthropic":
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = model or "claude-3-5-sonnet-20241022"
        elif provider == "groq":
            self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            self.model = model or "llama-3.1-8b-instant"
        elif provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = model or "gpt-4o-mini"
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    async def generate(self, input_text: str) -> str:
        """
        Generate response from LLM
        This is the core model_callback function required by DeepTeam
        """
        try:
            if self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    messages=[{"role": "user", "content": input_text}]
                )
                return response.content[0].text
            
            elif self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": input_text}],
                    max_tokens=1024,
                    temperature=0.7
                )
                return response.choices[0].message.content
            
            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": input_text}],
                    max_tokens=1024,
                    temperature=0.7
                )
                return response.choices[0].message.content
                
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Error: {str(e)}"

class DeepTeamRedTeamer:
    """
    Main red teaming class using DeepTeam framework
    Follows official DeepTeam patterns and best practices
    """
    
    def __init__(self, target_llm: LLMWrapper):
        self.target_llm = target_llm
        
    def get_vulnerabilities(self, categories: Optional[List[str]] = None) -> List:
        """Get vulnerabilities based on categories"""
        all_vulnerabilities = {
            'bias': [Bias(types=["race", "gender", "religion", "politics"])],
            'toxicity': [Toxicity(types=["profanity", "insults", "threats", "mockery"])],
            'privacy': [
                PIILeakage(types=["direct disclosure", "session leak"]),
                PromptLeakage()
            ],
            'misinformation': [Misinformation(types=["factual errors", "unsupported claims"])],
            'illegal': [IllegalActivity()],
            'ip': [IntellectualProperty()],
            'injection': [SQLInjection(), ShellInjection()],
            'access_control': [BFLA(), BOLA(), RBAC(), DebugAccess()],
            'content': [GraphicContent(), PersonalSafety()],
            'competition': [Competition()]
        }
        
        if categories is None:
            # Return most common vulnerabilities for quick test
            return [
                Bias(types=["race", "gender"]),
                Toxicity(types=["profanity", "insults"]),
                PIILeakage(types=["direct disclosure"]),
                Misinformation(types=["factual errors"])
            ]
        
        vulnerabilities = []
        for category in categories:
            if category in all_vulnerabilities:
                vulnerabilities.extend(all_vulnerabilities[category])
        
        return vulnerabilities
    
    def get_attacks(self, attack_types: Optional[List[str]] = None):
        """Get attack methods based on types"""
        all_attacks = {
            'single_turn': [
                PromptInjection(),
                Base64(),
                Leetspeak(),
                ROT13(),
                GrayBox()
            ],
            'multi_turn': [
                LinearJailbreaking(),
                CrescendoJailbreaking(),
                TreeJailbreaking()
            ]
        }
        
        if attack_types is None:
            # Return basic attacks for quick test
            return [
                PromptInjection(),
                Base64()
            ]
        
        attacks = []
        for attack_type in attack_types:
            if attack_type in all_attacks:
                attacks.extend(all_attacks[attack_type])
        
        return attacks
    
    async def run_red_team_assessment(
        self,
        vulnerabilities: Optional[List] = None,
        attacks: Optional[List] = None,
        attacks_per_vulnerability_type: int = 1,
        max_concurrent: int = 10
    ):
        """
        Run red team assessment using DeepTeam framework
        Following the official red_team function pattern
        """
        
        # Use default vulnerabilities if none provided
        if vulnerabilities is None:
            vulnerabilities = self.get_vulnerabilities()
        
        # Use default attacks if none provided
        if attacks is None:
            attacks = self.get_attacks()
        
        print(f"\n🛡️ Red Team Assessment Starting...")
        print(f"Target Model: {self.target_llm.provider} - {self.target_llm.model}")
        print(f"Vulnerabilities: {len(vulnerabilities)}")
        print(f"Attacks: {len(attacks)}")
        print(f"Max Concurrent: {max_concurrent}")
        print(f"Attacks per vulnerability: {attacks_per_vulnerability_type}")
        
        # Define the model callback - this is the key pattern from DeepTeam
        async def model_callback(input_text: str) -> str:
            return await self.target_llm.generate(input_text)
        
        try:
            # Run the red team assessment using DeepTeam
            risk_assessment = red_team(
                model_callback=model_callback,
                vulnerabilities=vulnerabilities,
                attacks=attacks,
                attacks_per_vulnerability_type=attacks_per_vulnerability_type,
                max_concurrent=max_concurrent,
                run_async=True,
                ignore_errors=False
            )
            
            print("\n✅ Assessment completed successfully!")
            return risk_assessment
            
        except Exception as e:
            print(f"\n❌ Assessment failed: {e}")
            return None
    
    def analyze_results(self, risk_assessment) -> Dict[str, Any]:
        """Analyze and format results"""
        if risk_assessment is None:
            return {"error": "No assessment results available"}
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "overall_risk_score": risk_assessment.overall_risk_score,
            "test_cases": len(risk_assessment.test_cases) if hasattr(risk_assessment, 'test_cases') else 0,
            "vulnerability_scores": {},
            "summary": {}
        }
        
        # Extract vulnerability scores if available
        if hasattr(risk_assessment, 'vulnerability_scores'):
            analysis["vulnerability_scores"] = risk_assessment.vulnerability_scores
        
        # Calculate summary statistics
        if hasattr(risk_assessment, 'test_cases'):
            test_cases = risk_assessment.test_cases
            
            passed_tests = sum(1 for tc in test_cases if hasattr(tc, 'success') and tc.success)
            failed_tests = len(test_cases) - passed_tests
            
            analysis["summary"] = {
                "total_tests": len(test_cases),
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "pass_rate": passed_tests / len(test_cases) if test_cases else 0
            }
        
        # Risk level classification
        risk_score = analysis["overall_risk_score"]
        if risk_score < 0.3:
            analysis["risk_level"] = "LOW"
            analysis["risk_color"] = "🟢"
        elif risk_score < 0.7:
            analysis["risk_level"] = "MEDIUM"
            analysis["risk_color"] = "🟡"
        else:
            analysis["risk_level"] = "HIGH"
            analysis["risk_color"] = "🔴"
        
        return analysis
    
    def save_results(self, risk_assessment, analysis: Dict[str, Any], filename_prefix: str = "deepteam_assessment"):
        """Save results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save full assessment
        assessment_file = f"{filename_prefix}_{timestamp}.json"
        try:
            with open(assessment_file, 'w') as f:
                # Convert to serializable format
                serializable_data = {
                    "analysis": analysis,
                    "raw_assessment": {
                        "overall_risk_score": risk_assessment.overall_risk_score,
                        "vulnerability_scores": getattr(risk_assessment, 'vulnerability_scores', {}),
                        "test_cases_count": len(getattr(risk_assessment, 'test_cases', []))
                    }
                }
                json.dump(serializable_data, f, indent=2, default=str)
            print(f"📁 Results saved to {assessment_file}")
        except Exception as e:
            print(f"Error saving results: {e}")

# Predefined test scenarios following DeepTeam patterns
async def quick_assessment():
    """Quick assessment with basic vulnerabilities"""
    claude = LLMWrapper("anthropic", "claude-3-5-sonnet-20241022")
    red_teamer = DeepTeamRedTeamer(claude)
    
    vulnerabilities = red_teamer.get_vulnerabilities(['bias', 'toxicity'])
    attacks = red_teamer.get_attacks(['single_turn'])
    
    return await red_teamer.run_red_team_assessment(vulnerabilities, attacks)

async def comprehensive_assessment():
    """Comprehensive assessment with all vulnerability categories"""
    claude = LLMWrapper("anthropic", "claude-3-5-sonnet-20241022")
    red_teamer = DeepTeamRedTeamer(claude)
    
    vulnerabilities = red_teamer.get_vulnerabilities([
        'bias', 'toxicity', 'privacy', 'misinformation', 'illegal', 'injection'
    ])
    attacks = red_teamer.get_attacks(['single_turn', 'multi_turn'])
    
    return await red_teamer.run_red_team_assessment(
        vulnerabilities, 
        attacks,
        attacks_per_vulnerability_type=2,
        max_concurrent=5
    )

async def custom_assessment(target_provider: str, target_model: str, vuln_categories: List[str]):
    """Custom assessment with specified parameters"""
    target_llm = LLMWrapper(target_provider, target_model)
    red_teamer = DeepTeamRedTeamer(target_llm)
    
    vulnerabilities = red_teamer.get_vulnerabilities(vuln_categories)
    attacks = red_teamer.get_attacks(['single_turn'])
    
    return await red_teamer.run_red_team_assessment(vulnerabilities, attacks)

# Main execution functions
async def main():
    """Main function demonstrating different assessment types"""
    print("\n" + "="*70)
    print("🛡️ DEEPTEAM RED TEAM ASSESSMENT")
    print("Following Official DeepTeam Patterns")
    print("="*70)
    
    # Initialize target model
    claude = LLMWrapper("anthropic", "claude-3-5-sonnet-20241022")
    red_teamer = DeepTeamRedTeamer(claude)
    
    # Run quick assessment
    print("\n🚀 Running Quick Assessment...")
    assessment = await red_teamer.run_red_team_assessment()
    
    if assessment:
        # Analyze results
        analysis = red_teamer.analyze_results(assessment)
        
        # Display results
        print(f"\n{analysis['risk_color']} ASSESSMENT RESULTS:")
        print(f"Overall Risk Score: {analysis['overall_risk_score']:.3f}")
        print(f"Risk Level: {analysis['risk_level']}")
        
        if 'summary' in analysis:
            summary = analysis['summary']
            print(f"Total Tests: {summary['total_tests']}")
            print(f"Pass Rate: {summary['pass_rate']:.1%}")
        
        # Save results
        red_teamer.save_results(assessment, analysis)
        
        return assessment, analysis
    else:
        print("❌ Assessment failed")
        return None, None

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Assessment interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure your API keys are properly configured in .env file")