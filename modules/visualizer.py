import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict
import numpy as np

class DecisionVisualizer:
    """Creates interactive visualizations for decision scenarios using Plotly."""
    
    def create_tradeoff_chart(self, scenarios: List[Dict], analysis: Dict) -> go.Figure:
        """
        Create a radar chart comparing scenarios across key dimensions.
        """
        
        categories = [
            'Financial Upside',
            'Job Security',
            'Learning Growth',
            'Work-Life Balance',
            'Long-term Sustainability'
        ]
        
        fig = go.Figure()
        
        # Add each scenario as a trace
        for i, scenario in enumerate(scenarios[:4]):
            # Generate scores based on scenario content
            scores = self._generate_scenario_scores(scenario, categories)
            
            fig.add_trace(go.Scatterpolar(
                r=scores,
                theta=categories,
                fill='toself',
                name=scenario['title'],
                opacity=0.6,
                line=dict(width=2)
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    tickfont=dict(size=10)
                ),
                bgcolor='rgba(240, 240, 240, 0.5)'
            ),
            showlegend=True,
            title={
                'text': '📊 Scenario Comparison Across Key Dimensions',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18}
            },
            font=dict(size=12),
            height=500,
            hovermode='closest'
        )
        
        return fig
    
    def create_confidence_chart(self, analysis: Dict) -> go.Figure:
        """
        Create a bar chart showing confidence/satisfaction scores for each scenario.
        """
        
        scores = analysis.get('decision_confidence_scores', {})
        
        if not scores:
            return self._create_fallback_confidence_chart()
        
        scenarios = list(scores.keys())
        values = list(scores.values())
        
        # Convert to 1-10 scale if needed
        values = [min(10, max(1, v)) if isinstance(v, (int, float)) else 5 for v in values]
        
        fig = go.Figure(data=[
            go.Bar(
                x=scenarios,
                y=values,
                marker=dict(
                    color=values,
                    colorscale='RdYlGn',
                    showscale=True,
                    colorbar=dict(
                        title="Confidence<br>Score",
                        thickness=15,
                        len=0.7
                    ),
                    line=dict(width=2, color='white')
                ),
                text=[f'{v}/10' for v in values],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Confidence: %{y}/10<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title={
                'text': '🎯 Decision Confidence Scores',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18}
            },
            yaxis_title='Confidence Score (1-10)',
            xaxis_title='Scenario',
            height=400,
            showlegend=False,
            hovermode='x unified',
            yaxis=dict(range=[0, 11])
        )
        
        return fig
    
    def create_risk_timeline(self) -> go.Figure:
        """
        Create a timeline showing potential risks at different time horizons.
        """
        
        risks = {
            '0-6 months': [
                'Adjustment period stress',
                'Learning curve challenges',
                'Initial financial strain'
            ],
            '6-18 months': [
                'Motivation dips',
                'Unexpected obstacles',
                'Relationship impacts'
            ],
            '1-3 years': [
                'Career direction clarity',
                'Financial stability check',
                'Long-term fit assessment'
            ],
            '3+ years': [
                'Compound growth effects',
                'Major life changes',
                'Opportunity costs apparent'
            ]
        }
        
        fig = go.Figure()
        
        for i, (period, items) in enumerate(risks.items()):
            y_pos = list(range(len(items)))
            
            fig.add_trace(go.Scatter(
                x=[i] * len(items),
                y=y_pos,
                mode='markers+text',
                marker=dict(size=15, color='#FF6B6B'),
                text=items,
                textposition='middle right',
                textfont=dict(size=10),
                hoverinfo='text',
                name=period
            ))
        
        fig.update_layout(
            title={
                'text': '⏰ Risk Timeline: What to Watch For',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18}
            },
            xaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=1,
                ticktext=list(risks.keys()),
                showgrid=False
            ),
            yaxis=dict(showticklabels=False, showgrid=False),
            height=400,
            showlegend=False,
            hovermode='closest'
        )
        
        return fig
    
    def _generate_scenario_scores(self, scenario: Dict, categories: List[str]) -> List[int]:
        """
        Generate scores for a scenario based on its description.
        Uses simple keyword analysis for scoring.
        """
        
        text = (scenario.get('description', '') + ' ' + 
                scenario.get('outlook_5yr', '') + ' ' +
                scenario.get('financial_impact', '')).lower()
        
        scores = []
        
        # Financial Upside
        if any(word in text for word in ['high income', 'lucrative', 'profit', 'grow', 'wealthy']):
            scores.append(8)
        elif any(word in text for word in ['salary', 'earnings', 'income']):
            scores.append(6)
        else:
            scores.append(5)
        
        # Job Security
        if any(word in text for word in ['stable', 'secure', 'guaranteed', 'permanent']):
            scores.append(8)
        elif any(word in text for word in ['risk', 'uncertain', 'volatile']):
            scores.append(4)
        else:
            scores.append(6)
        
        # Learning Growth
        if any(word in text for word in ['learn', 'growth', 'develop', 'skill', 'challenge']):
            scores.append(8)
        elif any(word in text for word in ['routine', 'predictable', 'stable']):
            scores.append(4)
        else:
            scores.append(6)
        
        # Work-Life Balance
        if any(word in text for word in ['balance', 'flexible', 'time off', 'leisure']):
            scores.append(7)
        elif any(word in text for word in ['intense', 'demanding', 'stress', 'hours']):
            scores.append(3)
        else:
            scores.append(5)
        
        # Long-term Sustainability
        if any(word in text for word in ['sustainable', 'long-term', 'future', 'retirement']):
            scores.append(8)
        elif any(word in text for word in ['short-term', 'temporary']):
            scores.append(4)
        else:
            scores.append(6)
        
        return scores
    
    def _create_fallback_confidence_chart(self) -> go.Figure:
        """Fallback chart if data is unavailable"""
        
        fig = go.Figure(data=[
            go.Bar(
                x=['Scenario 1', 'Scenario 2', 'Scenario 3'],
                y=[7, 6, 7],
                marker=dict(color=['#4CAF50', '#FFC107', '#4CAF50']),
                text=['7/10', '6/10', '7/10'],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title='🎯 Decision Confidence Scores',
            height=400,
            showlegend=False
        )
        
        return fig