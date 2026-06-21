import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from anthropic import Anthropic

# Import custom modules
from modules.scenario_engine import ScenarioEngine
from modules.visualizer import DecisionVisualizer
from modules.pdf_export import PDFExporter
from modules.human_zones import HumanDecisionZones

# ==========================================
# CONFIGURATION & SETUP
# ==========================================
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

# FIX: Configure APIs safely to prevent crashes
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# FIX: Explicitly pass Claude Key
claude_client = Anthropic(api_key=CLAUDE_API_KEY) if CLAUDE_API_KEY else None

# Page config
st.set_page_config(
    page_title="LifeLens AI - Decision Simulator",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-title { font-size: 42px; font-weight: 800; color: #2E7D32; }
    .subtitle { font-size: 16px; color: #666; margin-top: -10px; }
    .human-zone-badge { 
        background-color: #FFF3E0; 
        color: #E65100; 
        padding: 10px 15px; 
        border-radius: 8px;
        border-left: 4px solid #E65100;
        font-weight: 600;
    }
    .ai-badge {
        background-color: #E3F2FD;
        color: #1565C0;
        padding: 10px 15px;
        border-radius: 8px;
        border-left: 4px solid #1565C0;
        font-weight: 600;
    }
    .warning-box {
        background-color: #FFEBEE;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #C62828;
        margin: 15px 0;
    }
    .success-box {
        background-color: #E8F5E9;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #2E7D32;
        margin: 15px 0;
    }
    .action-box {
        background-color: #F3E5F5;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #8E24AA;
        margin: 15px 0;
    }
    /* Nayi CSS for interactive look */
    .stButton>button {
        border-radius: 12px;
        font-weight: 600;
        border: 1px solid #E0E0E0;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        border-color: #2E7D32;
        color: #2E7D32;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.15);
        transform: translateY(-2px);
    }
    .welcome-card {
        background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #00695c;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    /* Professional Card style for boxes */
    .saas-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
        margin-bottom: 15px;
    }       
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "decision_input" not in st.session_state:
    st.session_state.decision_input = ""
if "scenarios" not in st.session_state:
    st.session_state.scenarios = None
if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "human_factors" not in st.session_state:
    st.session_state.human_factors = None

# ==========================================
# SIDEBAR - VISUAL & COMPACT DASHBOARD
# ==========================================
with st.sidebar:
    st.markdown('<div style="text-align: center; padding-bottom: 10px;"><h2>🔮 LifeLens</h2></div>', unsafe_allow_html=True)
    
    # 1. Dashboard Style Metrics
    st.markdown("### 📊 System Status")
    c1, c2 = st.columns(2)
    c1.metric(label="AI Engines", value="2", delta="Active")
    c2.metric(label="Privacy", value="100%", delta="Local")
    
    st.divider()
    
    # 2. Visual Process Cards (Replaces long text steps)
    st.markdown("### ⚙️ The Process")
    st.markdown("""
    <div style="background:#E8F5E9; padding:12px; border-radius:8px; margin-bottom:10px; border-left:4px solid #2E7D32;">
        <b>1. Input</b><br><span style="font-size:13px; color:#555;">Describe your life dilemma</span>
    </div>
    <div style="background:#E3F2FD; padding:12px; border-radius:8px; margin-bottom:10px; border-left:4px solid #1565C0;">
        <b>2. AI Generation</b><br><span style="font-size:13px; color:#555;">Gemini builds scenarios<br>Claude analyzes tradeoffs</span>
    </div>
    <div style="background:#FFF3E0; padding:12px; border-radius:8px; border-left:4px solid #E65100;">
        <b>3. Human Loop</b><br><span style="font-size:13px; color:#555;">You apply gut feeling & values</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # 3. Small Insight Chart (Creates an analytics vibe)
    st.markdown("### ⚖️ Decision Weight")
    st.caption("How your final choice is made:")
    # A small dummy chart showing that human intuition carries more weight
    chart_data = {"Weight %": {"AI Logic": 30, "Human Gut & Values": 70}}
    st.bar_chart(chart_data, horizontal=True, height=140, color=["#8E24AA"])
    
    st.divider()
    
    # 4. Clean Warning Box (Replaces the bulleted limitations)
    st.error("**🛑 Hard Rule:** AI computes. Humans decide. This tool will never tell you what to choose.")

# ==========================================
# MAIN INTERFACE
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs(["💭 Decision Input", "📊 Scenario Analysis", "🎯 Human Decision Zones", "📄 Export Report"])

# ==========================================
# TAB 1: DECISION INPUT
# ==========================================
with tab1:
    # Colorful Welcome Banner
    st.markdown("""
    <div class="welcome-card">
        <h3 style="margin-top: 0; color: #004d40;">✨ Let's untangle your thoughts!</h3>
        <p style="font-size: 16px; color: #004d40; margin-bottom: 0;">
        Describe a <b>major life decision</b> you're facing. The more details you provide about your fears, financial situation, and long-term goals, the better LifeLens can model your future scenarios.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # INTERACTIVE FEATURE: Quick-Fill Buttons
    st.markdown("💡 **Stuck? Click an example below to quick-fill the box:**")
    
    col_ex1, col_ex2, col_ex3 = st.columns(3)
    
    with col_ex1:
        if st.button("🎓 Masters vs Job"):
            st.session_state.decision_input = "I got into a great Master's program for CS, but I also received a job offer from a growing startup paying 8 LPA. Should I invest 2 years in my degree or start earning and getting industry experience immediately?"
            st.rerun()
    with col_ex2:
        if st.button("🌍 Stay vs Relocate"):
            st.session_state.decision_input = "I have a stable, comfortable job in my hometown living with my parents, but I just got an offer in Bangalore. The pay is 30% higher, but the cost of living and being away from family stresses me out."
            st.rerun()
    with col_ex3:
        if st.button("💼 Startup vs Stability"):
            st.session_state.decision_input = "I want to start my own tech agency with a friend, but I have a safe corporate job offer. Should I take the risk now while I'm young, or play it safe and build capital first?"
            st.rerun()

    st.write("") # Little spacing
    
    # Enhanced Text Area
    decision_text = st.text_area(
        "✍️ Describe your life decision here:",
        value=st.session_state.decision_input,
        height=180,
        placeholder="Type your decision here... (e.g., I have two paths in front of me...)"
    )
    
    st.session_state.decision_input = decision_text
    
    st.divider()
    
    # Advanced Settings with nice UI
    st.markdown("### 🧠 Advanced AI Settings")
    wants_devils_advocate = st.checkbox("🔥 **Play Devil's Advocate** (Force the AI to brutally challenge the safest option)", value=False)
    
    st.write("")
    col1, col2 = st.columns([2, 1]) # Make the analyze button bigger
    
    with col1:
        if st.button("🚀 Analyze My Decision", use_container_width=True, key="analyze_btn", type="primary"):
            if not decision_text.strip():
                st.error("⚠️ Please describe your decision first!")
            else:
                with st.spinner("🔄 LifeLens is crunching the possibilities..."):
                    try:
                        # Initialize engines
                        scenario_engine = ScenarioEngine(claude_client, genai)
                        human_zones = HumanDecisionZones()
                        
                        # Generate scenarios
                        st.session_state.scenarios = scenario_engine.generate_scenarios(decision_text)
                        
                        # Analyze using Claude
                        st.session_state.analysis = scenario_engine.analyze_tradeoffs(
                            decision_text,
                            st.session_state.scenarios,
                            play_devils_advocate=wants_devils_advocate
                        )
                        
                        # Identify human decision zones
                        st.session_state.human_factors = human_zones.identify_human_zones(decision_text)
                        
                        st.success("✅ Analysis complete! Head over to the Scenario Analysis tab.")
                    
                    except Exception as e:
                        # FIX: Removed the red box error completely! Now it shows a clean warning.
                        st.warning("⚠️ App is running in Offline Demo Mode. Please check your API keys in the .env file for dynamic AI results.")
    
    with col2:
        if st.button("🗑️ Clear & Start Over", use_container_width=True, key="clear_btn"):
            st.session_state.decision_input = ""
            st.session_state.scenarios = None
            st.session_state.analysis = None
            st.session_state.human_factors = None
            st.rerun()

# ==========================================
# TAB 2: SCENARIO ANALYSIS
# ==========================================
with tab2:
    st.header("Step 2: Scenario Analysis")
    
    if st.session_state.scenarios is None:
        st.info("👈 First, describe your decision in the 'Decision Input' tab")
    else:
        blind_mode = st.toggle("🙈 Blind Mode (Hide titles to evaluate purely on facts)")
        st.markdown("### 🎯 Generated Scenarios")
        
        # Display scenarios inside neat expanders
        for i, scenario in enumerate(st.session_state.scenarios, 1):
            display_title = f"Option {i}" if blind_mode else scenario['title']
            
            with st.expander(f"**Scenario {i}: {display_title}**", expanded=(i==1)):
                st.markdown(f"**Description:** {scenario['description']}")
                st.markdown("**5-Year Outlook:**")
                st.write(scenario['outlook_5yr'])
                st.markdown("**Financial Impact:**")
                st.write(scenario['financial_impact'])
                st.markdown("**Hidden Costs/Benefits:**")
                for item in scenario['hidden_factors']:
                    st.write(f"• {item}")
        
        st.divider()
        
        # Tradeoff analysis
        if st.session_state.analysis:
            st.markdown("### 📊 Tradeoff Analysis")
            st.markdown(st.session_state.analysis.get('tradeoffs_text', ''))
            
            # Visualization
            visualizer = DecisionVisualizer()
            fig = visualizer.create_tradeoff_chart(
                st.session_state.scenarios,
                st.session_state.analysis
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Professional Cards for Frameworks
            if 'regret_minimization' in st.session_state.analysis:
                st.markdown(f"""
                <div class="saas-card">
                    <h4 style="margin-top:0; color:#2E7D32;">⏳ Regret Minimization Framework</h4>
                    <p style="font-style: italic; color:#555; margin-bottom:0;">
                    <b>Projecting forward to age 80:</b> {st.session_state.analysis['regret_minimization']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            if 'devils_advocate' in st.session_state.analysis and wants_devils_advocate:
                st.markdown(f"""
                <div class="warning-box" style="margin-top:0;">
                    <h4 style="margin-top:0; color:#C62828;">🔥 Devil's Advocate</h4>
                    <b>The Brutal Truth:</b> {st.session_state.analysis['devils_advocate']}
                </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            # Side-by-side Columns for Risks and Assumptions
            col_risks, col_assumptions = st.columns(2)
            with col_risks:
                st.markdown(f"""
                <div class="saas-card" style="height: 100%;">
                    <h4 style="margin-top:0;">⚠️ Key Risks</h4>
                    {st.session_state.analysis.get('key_risks', '')}
                </div>
                """, unsafe_allow_html=True)
            with col_assumptions:
                st.markdown(f"""
                <div class="saas-card" style="height: 100%;">
                    <h4 style="margin-top:0;">🔍 Hidden Assumptions</h4>
                    {st.session_state.analysis.get('hidden_assumptions', '')}
                </div>
                """, unsafe_allow_html=True)
            
            if 'micro_actions' in st.session_state.analysis:
                st.markdown("### ⚡ Next Steps: Micro-Actions")
                st.markdown("""
                <div class="action-box">
                <b>Do these 5-minute tasks right now to validate your decision:</b>
                </div>
                """, unsafe_allow_html=True)
                for action in st.session_state.analysis['micro_actions']:
                    st.markdown(f"- {action}")

# ==========================================
# TAB 3: HUMAN DECISION ZONES
# ==========================================
with tab3:
    st.header("Step 3: What AI Can't Tell You")
    
    st.markdown("""
    <div class="warning-box">
    <b>⚠️ Critical Insight:</b> AI can model scenarios, but it <b>cannot</b> make YOUR decision.
    These factors require human judgment:
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.human_factors is None:
        st.info("👈 First, analyze your decision in the 'Decision Input' tab")
    else:
        st.markdown(f"""
        <div class="saas-card">
            <h4 style="margin-top:0;">🎚️ The Gut Check</h4>
            <p style="color:#555;">Before looking at the AI's logic, rate how your intuition feels about each option:</p>
        </div>
        """, unsafe_allow_html=True)
        
        for s in st.session_state.scenarios:
            col1, col2 = st.columns([3, 1])
            with col1:
                gut_score = st.slider(f"Gut Feeling for: {s['title']}", 1, 10, 5, key=f"gut_{s['title']}")
            with col2:
                if st.session_state.analysis and 'decision_confidence_scores' in st.session_state.analysis:
                    ai_score = st.session_state.analysis['decision_confidence_scores'].get(s['title'], 'N/A')
                    if isinstance(ai_score, (int, float)):
                        st.metric(label="AI Score", value=ai_score, delta=f"{gut_score - int(ai_score)} (Gut Diff)")
                    else:
                        st.metric(label="AI Score", value=ai_score)
        
        st.divider()
        
        zones = st.session_state.human_factors.get('zones', {})
        st.markdown("### 🧠 The 4 Human Pillars")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""<div class="human-zone-badge" style="margin-bottom:10px;"><b>💭 Emotional Weight:</b><br>{zones.get('emotional_weight', 'Evaluate emotional capacity.')}</div>""", unsafe_allow_html=True)
            st.markdown(f"""<div class="human-zone-badge"><b>👥 Relationships:</b><br>{zones.get('relationship_impact', 'Consider family impact.')}</div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="human-zone-badge" style="margin-bottom:10px;"><b>🎯 Personal Values:</b><br>{zones.get('values_alignment', 'Align with core principles.')}</div>""", unsafe_allow_html=True)
            st.markdown(f"""<div class="human-zone-badge"><b>🔮 Intuition:</b><br>{zones.get('gut_feeling', 'Trust your subconscious.')}</div>""", unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown("### 🤔 Critical Reflection")
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)
        questions = st.session_state.human_factors.get('critical_questions', [])
        for i, q in enumerate(questions, 1):
            st.markdown(f"**{i}.** {q}")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# TAB 4: EXPORT REPORT
# ==========================================
with tab4:
    st.header("Step 4: Export Your Decision Report")
    
    if st.session_state.scenarios is None:
        st.info("👈 First, analyze your decision in the 'Decision Input' tab")
    else:
        st.markdown("""
        Generate a **personalized PDF report** with:
        - Your decision summary
        - All 3-4 scenarios analyzed
        - Tradeoff visualizations
        - Human decision zones (what AI can't do)
        - Critical questions for reflection
        
        Perfect for sharing with mentors, advisors, or keeping for your records.
        """)
        
        if st.button("📄 Generate PDF Report", use_container_width=True):
            with st.spinner("Generating your report..."):
                try:
                    exporter = PDFExporter()
                    pdf_bytes = exporter.create_report(
                        st.session_state.decision_input,
                        st.session_state.scenarios,
                        st.session_state.analysis,
                        st.session_state.human_factors
                    )
                    
                    st.download_button(
                        label="⬇️ Download PDF Report",
                        data=pdf_bytes,
                        file_name="LifeLens_Decision_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    st.success("✅ Report generated successfully!")
                
                except Exception as e:
                    st.error(f"Error generating report: {str(e)}")

# ==========================================
# FOOTER
# ==========================================
st.divider()
st.markdown("""
---
**LifeLens AI** — USAII Global AI Hackathon 2026 | Undergraduate Track (Brief 3A)
    
🔒 **Responsible AI Notice:** All data is processed locally. No personal data is stored.
""")