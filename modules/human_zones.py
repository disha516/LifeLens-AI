from typing import Dict, List

class HumanDecisionZones:
    """
    Identifies and articulates decision factors that require human judgment.
    Core to responsible AI: showing what AI CANNOT do.
    """
    
    def identify_human_zones(self, decision_text: str) -> Dict:
        """
        Identify critical human decision zones based on the decision.
        Returns zones that require human judgment, not AI optimization.
        """
        
        zones = {
            'emotional_weight': self._analyze_emotional_weight(decision_text),
            'relationship_impact': self._analyze_relationships(decision_text),
            'gut_feeling': self._explain_gut_feeling(),
            'values_alignment': self._analyze_values_alignment(decision_text)
        }
        
        critical_questions = self._generate_critical_questions(decision_text)
        
        return {
            'zones': zones,
            'critical_questions': critical_questions,
            'ai_limitations': self._ai_limitations()
        }
    
    def _analyze_emotional_weight(self, decision_text: str) -> str:
        """
        Explains why emotional weight is a human decision zone.
        """
        return """
**Why AI Can't Measure This:** 
AI can identify decisions are stressful, but cannot feel the actual weight of choosing between 
your dreams and financial security. It cannot understand the specific anxiety YOU would feel 
waking up in a new city, or the specific joy of staying close to family.

**You Must Evaluate:** 
How emotionally heavy is this decision for YOU specifically? Which option would let you sleep 
at night? Which would create persistent anxiety?
        """
    
    def _analyze_relationships(self, decision_text: str) -> str:
        """
        Explains why relationship impacts require human judgment.
        """
        return """
**Why AI Can't Know This:**
AI cannot understand your unique relationships: the parent who depends on you, the partner 
who might relocate with you, the friend group you'd miss. AI has no context for the actual 
people and bonds in your life.

**You Must Evaluate:**
How does each choice affect the people you care about? Which option honors your relationships? 
Are there people you need to consult before deciding? What do you owe them?
        """
    
    def _explain_gut_feeling(self) -> str:
        """
        Explains the role of gut feeling in decisions.
        """
        return """
**Why Gut Feeling Matters:**
Your "gut feeling" is actually your brain processing years of pattern recognition, life 
experience, and subconscious learning that doesn't fit into spreadsheets. It's real data 
that AI cannot access or replicate.

**You Must Evaluate:**
When you imagine each scenario vividly, how do you FEEL? Excited? Dread? Relief? That feeling 
is carrying important information from your deeper self.
        """
    
    def _analyze_values_alignment(self, decision_text: str) -> str:
        """
        Explains why values are a human decision zone.
        """
        return """
**Why AI Cannot Define Your Values:**
AI can identify that a decision involves "freedom" or "stability," but your personal definition 
of these values is unique. Freedom to you might mean flexibility, but to someone else it means 
autonomy from authority. AI cannot rank YOUR values correctly.

**You Must Evaluate:**
What matters most to you? (not what should matter) Does each option align with your actual 
values, or just what you think they should be? Are you compromising on something that truly 
matters to you?
        """
    
    def _generate_critical_questions(self, decision_text: str) -> List[str]:
        """
        Generate personalized critical questions for reflection.
        """
        
        questions = [
            # Emotional questions
            "If you chose each path and checked in with yourself in 1 year, which option would make you most proud?",
            "Which decision would let you sleep peacefully at night without regret?",
            "What does success look like to you in this decision? (Not to anyone else)",
            
            # Relationship questions
            "Who in your life needs to be part of this decision, and have you talked to them honestly?",
            "Which option allows you to show up fully for the people you care about?",
            
            # Values questions
            "What are your TOP 3 personal values? (Not what you think they should be) Does each option honor these?",
            "Are you choosing based on what you actually want, or what you think others expect?",
            "If money and status weren't factors, which option would you choose?",
            
            # Resilience questions
            "If your best-case scenario doesn't happen, could you still be okay with your choice?",
            "Which option gives you the most confidence that you can handle unexpected challenges?",
            
            # Future self questions
            "Imagine yourself at 80 years old looking back. Which choice would older-you be grateful for?",
            "Which option opens doors vs. closes them? Are you okay with that?",
            
            # Gut check questions
            "Without thinking too hard, which option did your gut initially tell you to choose?",
            "What about that option scared you enough to reconsider?"
        ]
        
        return questions
    
    def _ai_limitations(self) -> Dict[str, str]:
        """
        Document what this AI system explicitly CANNOT do.
        Important for responsible AI disclosure.
        """
        
        return {
            'cannot_feel_emotions': 
                'LifeLens cannot experience the emotional weight of your decision or understand how you will emotionally respond to each path.',
            
            'cannot_know_relationships': 
                'LifeLens has no data on your actual relationships, family situation, or social support network. Only you know these.',
            
            'cannot_define_values': 
                'LifeLens cannot know what truly matters to you. It can identify themes in your decision, but your values are uniquely yours.',
            
            'cannot_predict_unknowns': 
                'Major life decisions depend on unpredictable factors: market changes, health, relationships, luck. LifeLens models known scenarios but cannot predict the unknown.',
            
            'cannot_make_your_decision': 
                'LifeLens is a thinking tool, not a decision-maker. The choice must remain 100% yours.',
            
            'cannot_account_for_growth': 
                'People change. The person you become in 2-3 years might value completely different things than you do now. LifeLens cannot predict your personal growth.',
            
            'cannot_guarantee_outcomes': 
                'Even the best-planned scenario can fail due to circumstances beyond your control. Success ultimately depends on your resilience and adaptability.'
        }
    
    def format_ai_limitations_for_display(self) -> str:
        """
        Format limitations in a user-friendly way.
        """
        
        limitations = self._ai_limitations()
        
        formatted = "## 🤖 What LifeLens AI Explicitly CANNOT Do:\n\n"
        
        for i, (key, value) in enumerate(limitations.items(), 1):
            # Convert snake_case to readable text
            readable_key = key.replace('_', ' ').title()
            formatted += f"**{i}. {readable_key}**\n{value}\n\n"
        
        return formatted