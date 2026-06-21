from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
from datetime import datetime
from typing import List, Dict
import json

class PDFExporter:
    """
    Generates professional PDF reports of decision analysis.
    """
    
    def __init__(self):
        self.pagesize = letter
        self.margin = 0.5 * inch
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Create custom styles for the report."""
        
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#2E7D32'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHead',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#1565C0'),
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            leading=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='Emphasis',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=HexColor('#D32F2F'),
            fontName='Helvetica-Bold'
        ))
    
    def create_report(self, decision_text: str, scenarios: List[Dict], 
                     analysis: Dict, human_factors: Dict) -> bytes:
        """
        Create a complete PDF report and return as bytes.
        """
        
        # Create PDF in memory
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=self.pagesize,
            rightMargin=self.margin,
            leftMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin
        )
        
        # Build content
        story = []
        
        # Header
        story.extend(self._build_header())
        story.append(Spacer(1, 0.2 * inch))
        
        # Decision Summary
        story.append(Paragraph("Your Decision", self.styles['SectionHead']))
        story.append(Paragraph(decision_text, self.styles['CustomBody']))
        story.append(Spacer(1, 0.2 * inch))
        
        # Scenarios
        story.append(Paragraph("Scenarios Analyzed", self.styles['SectionHead']))
        story.extend(self._build_scenarios_section(scenarios))
        story.append(Spacer(1, 0.2 * inch))
        
        # Analysis
        if analysis:
            story.append(PageBreak())
            story.append(Paragraph("Tradeoff Analysis", self.styles['SectionHead']))
            story.extend(self._build_analysis_section(analysis))
            story.append(Spacer(1, 0.2 * inch))
        
        # Human Decision Zones
        story.append(PageBreak())
        story.append(Paragraph("What AI Cannot Decide For You", self.styles['SectionHead']))
        story.extend(self._build_human_zones_section(human_factors))
        story.append(Spacer(1, 0.2 * inch))
        
        # Critical Questions
        story.append(PageBreak())
        story.append(Paragraph("Critical Reflection Questions", self.styles['SectionHead']))
        story.append(Paragraph(
            "Spend time with these questions. Your honest answers form the foundation for your final decision.",
            self.styles['CustomBody']
        ))
        story.append(Spacer(1, 0.15 * inch))
        
        if human_factors and 'critical_questions' in human_factors:
            for i, question in enumerate(human_factors['critical_questions'][:10], 1):
                story.append(Paragraph(f"{i}. {question}", self.styles['CustomBody']))
                story.append(Spacer(1, 0.1 * inch))
        
        # Footer
        story.append(Spacer(1, 0.3 * inch))
        story.extend(self._build_footer())
        
        # Build PDF
        doc.build(story)
        
        # Get bytes
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
    
    def _build_header(self) -> List:
        """Build the report header."""
        
        content = [
            Paragraph("LifeLens AI", self.styles['CustomTitle']),
            Paragraph("Life Decision Simulator Report", self.styles['SectionHead']),
            Spacer(1, 0.1 * inch),
            Paragraph(
                f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
                self.styles['Normal']
            )
        ]
        
        return content
    
    def _build_scenarios_section(self, scenarios: List[Dict]) -> List:
        """Build scenarios section."""
        
        content = []
        
        for i, scenario in enumerate(scenarios, 1):
            # Scenario title
            content.append(Paragraph(
                f"Scenario {i}: {scenario.get('title', 'Option')}",
                self.styles['Emphasis']
            ))
            
            # Description
            content.append(Paragraph(
                f"<b>Description:</b> {scenario.get('description', '')}",
                self.styles['CustomBody']
            ))
            
            # 5-year outlook
            content.append(Paragraph(
                f"<b>5-Year Outlook:</b> {scenario.get('outlook_5yr', '')}",
                self.styles['CustomBody']
            ))
            
            # Financial impact
            content.append(Paragraph(
                f"<b>Financial Impact:</b> {scenario.get('financial_impact', '')}",
                self.styles['CustomBody']
            ))
            
            # Hidden factors
            if scenario.get('hidden_factors'):
                factors_text = ", ".join(scenario['hidden_factors'][:3])
                content.append(Paragraph(
                    f"<b>Hidden Factors:</b> {factors_text}",
                    self.styles['CustomBody']
                ))
            
            content.append(Spacer(1, 0.15 * inch))
        
        return content
    
    def _build_analysis_section(self, analysis: Dict) -> List:
        """Build analysis section."""
        
        content = []
        
        # Tradeoffs
        if 'tradeoffs_text' in analysis:
            content.append(Paragraph(
                f"<b>Key Tradeoffs:</b> {analysis['tradeoffs_text'][:500]}...",
                self.styles['CustomBody']
            ))
            content.append(Spacer(1, 0.1 * inch))
        
        # Risks
        if 'key_risks' in analysis:
            content.append(Paragraph(
                f"<b>Key Risks:</b> {analysis['key_risks'][:300]}...",
                self.styles['CustomBody']
            ))
            content.append(Spacer(1, 0.1 * inch))
        
        # Hidden assumptions
        if 'hidden_assumptions' in analysis:
            content.append(Paragraph(
                f"<b>Hidden Assumptions:</b> {analysis['hidden_assumptions'][:300]}...",
                self.styles['CustomBody']
            ))
            content.append(Spacer(1, 0.1 * inch))
        
        # Confidence factors
        if 'confidence_factors' in analysis:
            content.append(Paragraph(
                f"<b>What Determines Success:</b> {analysis['confidence_factors'][:300]}...",
                self.styles['CustomBody']
            ))
        
        return content
    
    def _build_human_zones_section(self, human_factors: Dict) -> List:
        """Build human decision zones section."""
        
        content = []
        
        if not human_factors or 'zones' not in human_factors:
            return content
        
        zones = human_factors['zones']
        
        # Emotional weight
        content.append(Paragraph("💭 Emotional Weight", self.styles['Emphasis']))
        content.append(Paragraph(
            zones.get('emotional_weight', '').replace('\n', ' '),
            self.styles['CustomBody']
        ))
        content.append(Spacer(1, 0.15 * inch))
        
        # Relationships
        content.append(Paragraph("👥 Relationship Impact", self.styles['Emphasis']))
        content.append(Paragraph(
            zones.get('relationship_impact', '').replace('\n', ' '),
            self.styles['CustomBody']
        ))
        content.append(Spacer(1, 0.15 * inch))
        
        # Gut feeling
        content.append(Paragraph("🧠 Gut Feeling & Intuition", self.styles['Emphasis']))
        content.append(Paragraph(
            zones.get('gut_feeling', '').replace('\n', ' '),
            self.styles['CustomBody']
        ))
        content.append(Spacer(1, 0.15 * inch))
        
        # Values
        content.append(Paragraph("🎯 Personal Values Alignment", self.styles['Emphasis']))
        content.append(Paragraph(
            zones.get('values_alignment', '').replace('\n', ' '),
            self.styles['CustomBody']
        ))
        
        return content
    
    def _build_footer(self) -> List:
        """Build the report footer."""
        
        content = [
            Paragraph(
                "<b>⚠️ Important Reminder:</b> This report is a tool for thinking, not a recommendation. "
                "LifeLens AI models scenarios and surfaces considerations, but your final decision must reflect "
                "your own values, relationships, and judgment. AI cannot and should not make life decisions for you.",
                self.styles['CustomBody']
            ),
            Spacer(1, 0.15 * inch),
            Paragraph(
                "---",
                self.styles['Normal']
            ),
            Paragraph(
                "Generated by LifeLens AI | USAII Global AI Hackathon 2026",
                self.styles['Normal']
            )
        ]
        
        return content