import json
import streamlit as st
from typing import List, Dict

class ScenarioEngine:
    """
    Generates and analyzes decision scenarios using Claude and Gemini.
    Responsible for deep reasoning about tradeoffs.
    """
    
    def __init__(self, claude_client, genai_module):
        self.claude = claude_client
        self.genai = genai_module
    
    def generate_scenarios(self, decision_text: str) -> List[Dict]:
        """
        Generate 3-4 realistic scenarios for the decision using Gemini.
        Gemini is used here for creative scenario generation.
        """
        
        prompt = f"""
        A user is facing this life decision: "{decision_text}"
        
        Generate exactly 3-4 distinct realistic scenarios they could pursue. 
        For each scenario, provide:
        1. A catchy title (e.g., "The Startup Path", "The Safe Route")
        2. A detailed description of what pursuing this option looks like
        3. A 5-year outlook (where they'd be in 5 years)
        4. Financial impact (salary progression, debt, savings)
        5. 3-5 hidden factors (unexpected benefits or costs)
        
        Make scenarios specific, realistic, and moderately different from each other.
        Respond with ONLY a valid JSON array, nothing else. No markdown, no explanation text.
        """
        
        try:
            # FIX: Changed to gemini-pro to prevent 404 error and get real dynamic answers!
            model = self.genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text
            
            # Try to parse JSON
            try:
                start_idx = response_text.find('[')
                end_idx = response_text.rfind(']') + 1
                json_str = response_text[start_idx:end_idx]
                scenarios = json.loads(json_str)
            except Exception as parse_error:
                st.warning("⚠️ Using standard demo scenarios (Offline Mode).")
                scenarios = self._create_fallback_scenarios(decision_text)
            
            # Validate and enhance scenarios
            validated_scenarios = []
            for scenario in scenarios[:4]:  # Max 4 scenarios
                validated = {
                    'title': scenario.get('title', 'Scenario'),
                    'description': scenario.get('description', ''),
                    'outlook_5yr': scenario.get('outlook_5yr', ''),
                    'financial_impact': scenario.get('financial_impact', ''),
                    'hidden_factors': scenario.get('hidden_factors', [])
                }
                validated_scenarios.append(validated)
            
            return validated_scenarios
        
        except Exception as e:
            st.warning("⚠️ Running in offline mode. Loading standard demo scenarios.")
            return self._create_fallback_scenarios(decision_text)
    
    def analyze_tradeoffs(self, decision_text: str, scenarios: List[Dict], play_devils_advocate: bool = False) -> Dict:
        """
        Deep analysis using Claude Sonnet for reasoning about tradeoffs.
        Now includes Regret Minimization, Micro-actions, and optional Devil's Advocate.
        """
        
        scenarios_text = "\n\n".join([
            f"**{s['title']}:** {s['description']}\n"
            f"5-Year: {s['outlook_5yr']}\n"
            f"Financial: {s['financial_impact']}"
            for s in scenarios
        ])

        # Dynamic instruction based on UI toggle
        devils_advocate_instruction = ""
        if play_devils_advocate:
            devils_advocate_instruction = '\n8. "devils_advocate" - Provide the absolute strongest, most brutal argument AGAINST the safest or most appealing scenario here. Shatter confirmation bias.'
        
        prompt = f"""
        A person is deciding: "{decision_text}"
        
        Here are their options:
        {scenarios_text}
        
        Provide deep analysis in JSON format with these exact keys:
        1. "tradeoffs_text" - Detailed paragraph comparing major tradeoffs between scenarios
        2. "key_risks" - Most likely failure points for each approach
        3. "hidden_assumptions" - What each scenario assumes to work out (that might not)
        4. "confidence_factors" - What would make success MORE or LESS likely
        5. "decision_confidence_scores" - Rate each scenario 1-10 on "likelihood of personal satisfaction" (e.g., {{"Scenario 1 Title": 8, "Scenario 2 Title": 5}})
        6. "regret_minimization" - Apply Jeff Bezos' Regret Minimization Framework. Projecting forward to age 80, which path minimizes future regret and why?
        7. "micro_actions" - A list of 3 tiny, 5-minute real-world tasks the user can do right now to validate this decision.{devils_advocate_instruction}
        
        Be realistic and honest about downsides. Avoid generic advice.
        Respond with ONLY a valid JSON object, nothing else. No markdown formatting, no explanation text.
        """
        
        try:
            # FIX: Safely check if Claude is initialized
            if not self.claude:
                raise Exception("Claude client not found.")
                
            message = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = message.content[0].text
            
            # Parse JSON from response
            try:
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                json_str = response_text[start_idx:end_idx]
                analysis = json.loads(json_str)
            except Exception as parse_error:
                st.warning("⚠️ Using standard demo analysis (Offline Mode).")
                analysis = self._create_fallback_analysis()
            
            return analysis
        
        except Exception as e:
            st.warning("⚠️ Running in offline mode. Loading standard demo analysis.")
            return self._create_fallback_analysis()
    
    def _create_fallback_scenarios(self, decision_text: str) -> List[Dict]:
        """Fallback scenarios if APIs fail"""
        return [
            {
                'title': 'Conservative Path',
                'description': 'Take the safe, stable option that minimizes risk.',
                'outlook_5yr': 'Stable position, proven growth, lower stress',
                'financial_impact': 'Steady income, predictable savings',
                'hidden_factors': ['May feel unchallenged over time', 'Less learning and growth', 'Missed opportunities for higher upside']
            },
            {
                'title': 'Aggressive Growth Path',
                'description': 'Pursue high-risk, high-reward option.',
                'outlook_5yr': 'Potentially higher income or skills, greater uncertainty',
                'financial_impact': 'High volatility, potential debt, high upside',
                'hidden_factors': ['Stress and work intensity', 'Faster learning curve', 'Relationships may suffer']
            }
        ]
    
    def _create_fallback_analysis(self) -> Dict:
        """Fallback analysis if Claude API fails, updated with new feature keys"""
        return {
            'tradeoffs_text': 'Each scenario offers different combinations of security, growth, and fulfillment. You must balance immediate comfort with long-term potential.',
            'key_risks': '• Unforeseen market changes\n• Personal circumstances shifting\n• Initial assumptions not panning out',
            'hidden_assumptions': '• That you can handle the stress level\n• That the path aligns with your values\n• That external factors remain stable',
            'confidence_factors': 'Your resilience, support network, and adaptability will matter more than the choice itself.',
            'decision_confidence_scores': {'Conservative Path': 7, 'Aggressive Growth Path': 6},
            'regret_minimization': 'When looking back from age 80, people rarely regret the risks they took to pursue growth, even if they failed. They usually regret the safe choices that led to "what ifs".',
            'micro_actions': [
                'Reach out to one person who chose the risky path on LinkedIn.',
                'Write down your absolute minimum financial requirement for the next 6 months.',
                'Flip a coin to decide; notice if you feel disappointed by the result.'
            ],
            'devils_advocate': 'The conservative path feels safe, but in a rapidly changing world, playing it safe might actually guarantee stagnation and long-term obsolescence.'
        }