"""
HalluciGuard Pro - Complete Thesis Project
Team 05 | RGUKT RK Valley
Hallucination Detection & Verification in LLMs
"""

import os
import re
import streamlit as st
from groq import Groq
import wikipediaapi
import time

# ============================================================================
# CONFIGURATION
# ============================================================================

GROQ_API_KEY = "gsk_xxxxxxxxx"
client = Groq(api_key=GROQ_API_KEY)

wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='HalluciGuard/1.0 (Team05; RGUKT; Contact: project@rgukt.in)'
)

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="HalluciGuard Pro | Hallucination Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CLEAN, READABLE CSS - HIGH CONTRAST
# ============================================================================

st.markdown("""
    <style>
    /* Main background - Light gradient for readability */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 2rem 2rem;
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        border-radius: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        color: #c7d2fe;
        font-size: 1rem;
    }
    
    /* Glass Cards - Light theme */
    .glass-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: 1rem;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #4f46e5;
    }
    
    .metric-label {
        color: #64748b;
        font-size: 0.75rem;
        margin-top: 0.3rem;
    }
    
    /* Claim Cards */
    .claim-verified {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        border-radius: 0.75rem;
        padding: 1rem;
        margin: 0.75rem 0;
    }
    
    .claim-hallucinated {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        border-radius: 0.75rem;
        padding: 1rem;
        margin: 0.75rem 0;
    }
    
    .claim-title {
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .claim-text {
        color: #1e293b;
        margin-bottom: 0.5rem;
        line-height: 1.5;
    }
    
    .claim-reason {
        font-size: 0.8rem;
        color: #475569;
        margin-top: 0.5rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #1e293b;
    }
    
    /* Input Box */
    .stTextInput input {
        background: white !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 0.75rem !important;
        color: #1e293b !important;
        font-size: 1rem !important;
        padding: 0.75rem !important;
    }
    
    .stTextInput input:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 2px rgba(79,70,229,0.1) !important;
    }
    
    /* Button */
    .stButton button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        border: none !important;
        border-radius: 0.75rem !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        color: white !important;
    }
    
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(79,70,229,0.3);
    }
    
    /* Status Badges */
    .badge-verified {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        background: #22c55e;
        color: white;
        padding: 0.2rem 0.75rem;
        border-radius: 2rem;
        font-size: 0.7rem;
        font-weight: 600;
    }
    
    .badge-hallucinated {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        background: #ef4444;
        color: white;
        padding: 0.2rem 0.75rem;
        border-radius: 2rem;
        font-size: 0.7rem;
        font-weight: 600;
    }
    
    .badge-partial {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        background: #f59e0b;
        color: white;
        padding: 0.2rem 0.75rem;
        border-radius: 2rem;
        font-size: 0.7rem;
        font-weight: 600;
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: #e2e8f0;
        margin: 1.5rem 0;
    }
    
    /* Info text */
    .info-text {
        color: #475569;
        font-size: 0.9rem;
        text-align: center;
        padding: 2rem;
    }
    
    /* Response box */
    .response-box {
        background: #f1f5f9;
        border-radius: 0.75rem;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #1e293b;
        line-height: 1.6;
    }
    
    /* Context box */
    .context-box {
        background: #f8fafc;
        border-radius: 0.75rem;
        padding: 1rem;
        font-size: 0.85rem;
        color: #334155;
        line-height: 1.5;
    }
    
    /* Progress dots */
    .stage-container {
        display: flex;
        justify-content: space-between;
        margin: 1rem 0;
    }
    
    .stage-item {
        text-align: center;
        flex: 1;
    }
    
    .stage-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #cbd5e1;
        margin: 0 auto 0.25rem;
        transition: all 0.3s;
    }
    
    .stage-dot.active {
        background: #4f46e5;
        box-shadow: 0 0 8px #4f46e5;
    }
    
    .stage-dot.completed {
        background: #22c55e;
    }
    
    .stage-label {
        font-size: 0.6rem;
        color: #64748b;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_context(query):
    """Retrieve context from Wikipedia"""
    try:
        page = wiki.page(query)
        if page.exists():
            return page.summary[:2500], page.title
        return f"No Wikipedia page found for '{query}'.", None
    except Exception as e:
        return f"Error: {e}", None

def generate_response(query, hallucinate=False):
    """Generate response using Groq API"""
    if hallucinate:
        system_prompt = "You are a creative AI. Include 1-2 subtle factual errors in your response for demonstration purposes. Make the response sound confident but slightly wrong."
    else:
        system_prompt = "You are a helpful AI assistant. Provide accurate, factual answers based on your knowledge. Be concise."
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.7 if hallucinate else 0.3,
            max_tokens=400
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def extract_claims(text):
    """Extract claims from response"""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 25]

def verify_claim(claim, context):
    """Verify if claim is supported by context"""
    prompt = f"""Analyze if the claim is supported by the evidence.

EVIDENCE: {context[:2000]}

CLAIM: {claim}

Respond ONLY with:
SUPPORTED: [YES/NO/PARTIAL]
CONFIDENCE: [0.00-1.00]
REASON: [one short sentence]"""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"SUPPORTED: ERROR\nCONFIDENCE: 0.00\nREASON: {e}"

def parse_verification(text):
    """Parse verification response"""
    supported = False
    confidence = 0.0
    reason = "Unable to verify"
    
    for line in text.split('\n'):
        if 'SUPPORTED:' in line:
            val = line.split('SUPPORTED:')[-1].strip().upper()
            supported = val in ['YES', 'PARTIAL']
        elif 'CONFIDENCE:' in line:
            try:
                confidence = float(line.split('CONFIDENCE:')[-1].strip())
            except:
                pass
        elif 'REASON:' in line:
            reason = line.split('REASON:')[-1].strip()
    
    return supported, min(confidence, 0.95), reason

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### 🛡️ HalluciGuard Pro")
    st.markdown("*Thesis Project 2026*")
    
    st.divider()
    
    st.markdown("### 🎛️ Controller")
    simulate_hallucination = st.toggle(
        "🎭 Simulate Hallucination", 
        value=False,
        help="When ON, the AI intentionally includes subtle errors to demonstrate hallucination detection."
    )
    
    st.divider()
    
    st.markdown("### 📋 9-Stage Pipeline")
    stages = ["Query", "Retrieve", "Generate", "Extract", "Analyze", "Match", "Verify", "Classify", "Output"]
    for i, s in enumerate(stages, 1):
        st.markdown(f"{i:02d}. {s}")
    
    st.divider()
    
    st.markdown("### 🎓 Team 05")
    st.markdown("**P. Prasanna** (R210163)")
    st.markdown("**A. Jahnavi** (R211082)")
    st.markdown("*RGUKT RK Valley*")

# ============================================================================
# MAIN CONTENT
# ============================================================================

st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🛡️ HalluciGuard Pro</div>
        <div class="hero-subtitle"> Hallucination Verification System</div>
        <div style="margin-top: 1rem;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.25rem 1rem; border-radius: 2rem; font-size: 0.75rem;">RAG Pipeline</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.25rem 1rem; border-radius: 2rem; font-size: 0.75rem; margin-left: 0.5rem;">NLI Verification</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.25rem 1rem; border-radius: 2rem; font-size: 0.75rem; margin-left: 0.5rem;">Confidence Scoring</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Query Input
query = st.text_input(
    "", 
    placeholder="🔍 Enter your research query (e.g., 'What is the capital of France?', 'Explain quantum computing')...",
    label_visibility="collapsed"
)

# Example Queries
st.markdown("### 📌 Quick Examples")
ex_cols = st.columns(5)
examples = [
    ("🇫🇷 France Capital", "What is the capital of France?"),
    ("🇮🇳 India Capital", "What is the capital of India?"),
    ("📞 Telephone", "Who invented the telephone?"),
    ("🚀 SpaceX", "What is SpaceX?"),
    ("⚡ Tesla CEO", "Who is the CEO of Tesla?"),
]

for col, (label, q) in zip(ex_cols, examples):
    with col:
        if st.button(label, use_container_width=True):
            query = q

# ============================================================================
# PROCESS QUERY
# ============================================================================

if query:
    # Progress indicator
    stage_placeholder = st.empty()
    
    with stage_placeholder.container():
        st.markdown("""
            <div class="stage-container">
                <div class="stage-item"><div class="stage-dot" id="s1"></div><div class="stage-label">Query</div></div>
                <div class="stage-item"><div class="stage-dot" id="s2"></div><div class="stage-label">Retrieve</div></div>
                <div class="stage-item"><div class="stage-dot" id="s3"></div><div class="stage-label">Generate</div></div>
                <div class="stage-item"><div class="stage-dot" id="s4"></div><div class="stage-label">Extract</div></div>
                <div class="stage-item"><div class="stage-dot" id="s5"></div><div class="stage-label">Analyze</div></div>
                <div class="stage-item"><div class="stage-dot" id="s6"></div><div class="stage-label">Match</div></div>
                <div class="stage-item"><div class="stage-dot" id="s7"></div><div class="stage-label">Verify</div></div>
                <div class="stage-item"><div class="stage-dot" id="s8"></div><div class="stage-label">Classify</div></div>
                <div class="stage-item"><div class="stage-dot" id="s9"></div><div class="stage-label">Output</div></div>
            </div>
        """, unsafe_allow_html=True)
    
    with st.spinner("🛡️ Running HalluciGuard verification pipeline..."):
        
        # Stage 1-2: Context Retrieval
        context, page_title = get_context(query)
        
        # Stage 3: Response Generation
        response = generate_response(query, simulate_hallucination)
        
        # Stage 4: Claim Extraction
        claims = extract_claims(response)
        
        # Stage 5-7: Verification
        verification_results = []
        supported_count = 0
        
        for claim in claims:
            verification = verify_claim(claim, context)
            is_supported, confidence, reason = parse_verification(verification)
            if is_supported:
                supported_count += 1
            verification_results.append({
                "claim": claim,
                "supported": is_supported,
                "confidence": confidence,
                "reason": reason
            })
        
        # Stage 8-9: Classification
        total_claims = len(claims)
        faithfulness = (supported_count / total_claims * 100) if total_claims > 0 else 0
        
        if faithfulness >= 80:
            system_status = "SECURE ✅"
            status_color = "#22c55e"
        elif faithfulness >= 40:
            system_status = "CAUTION ⚠️"
            status_color = "#f59e0b"
        else:
            system_status = "COMPROMISED ❌"
            status_color = "#ef4444"
        
        # Clear stage indicator (JavaScript to update dots)
        stage_placeholder.empty()
    
    # ========================================================================
    # RESULTS DISPLAY
    # ========================================================================
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📊 Analysis Results")
    
    # Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_claims}</div>
                <div class="metric-label">Claims Extracted</div>
            </div>
        """, unsafe_allow_html=True)
    
    with m2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{faithfulness:.1f}%</div>
                <div class="metric-label">Faithfulness Score</div>
            </div>
        """, unsafe_allow_html=True)
    
    with m3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: {status_color};">{system_status}</div>
                <div class="metric-label">System Status</div>
            </div>
        """, unsafe_allow_html=True)
    
    with m4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{supported_count}/{total_claims}</div>
                <div class="metric-label">Verified Claims</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Response and Context
    st.markdown("### 🤖 Generated Response")
    
    col_resp, col_ctx = st.columns([2, 1])
    
    with col_resp:
        st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem;">
                    <span style="font-weight: 600;">🛡️ HalluciGuard Output</span>
                    <span style="font-size: 0.7rem; background: #e2e8f0; padding: 0.2rem 0.6rem; border-radius: 1rem; color: #475569;">
                        {simulate_hallucination and "Hallucination Mode" or "Verification Mode"}
                    </span>
                </div>
                <div class="response-box">{response}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_ctx:
        st.markdown(f"""
            <div class="glass-card">
                <div style="font-weight: 600; margin-bottom: 0.75rem;">📚 Retrieved Context</div>
                <div class="context-box">{context[:400]}...</div>
                <div style="margin-top: 0.5rem; font-size: 0.7rem; color: #64748b;">
                    Source: {page_title if page_title else 'Wikipedia'}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Verification Breakdown
    st.markdown("### 🔍 Truth Heatmap")
    
    for i, res in enumerate(verification_results, 1):
        if res["supported"]:
            st.markdown(f"""
                <div class="claim-verified">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
                        <div>
                            <span style="font-weight: 600;">✅ VERIFIED</span>
                            <span style="font-size: 0.7rem; background: #dcfce7; padding: 0.2rem 0.5rem; border-radius: 1rem; margin-left: 0.5rem;">
                                Confidence: {res['confidence']*100:.0f}%
                            </span>
                        </div>
                    </div>
                    <div class="claim-text"><strong>Claim {i}:</strong> {res['claim'][:200]}</div>
                    <div class="claim-reason">✓ {res['reason'][:150]}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="claim-hallucinated">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
                        <div>
                            <span style="font-weight: 600;">❌ HALLUCINATED</span>
                            <span style="font-size: 0.7rem; background: #fee2e2; padding: 0.2rem 0.5rem; border-radius: 1rem; margin-left: 0.5rem;">
                                Confidence: {res['confidence']*100:.0f}%
                            </span>
                        </div>
                    </div>
                    <div class="claim-text"><strong>Claim {i}:</strong> {res['claim'][:200]}</div>
                    <div class="claim-reason">⚠️ {res['reason'][:150]}</div>
                </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div style="text-align: center; font-size: 0.7rem; color: #94a3b8; padding: 2rem 0 1rem;">
            HalluciGuard Pro | Neural Logic Inference & Verification | RGUKT RK Valley | Thesis Project 2026
        </div>
    """, unsafe_allow_html=True)

elif not query:
    st.markdown('<div class="info-text">💡 Enter a question above or click an example to start the HalluciGuard verification pipeline.</div>', unsafe_allow_html=True)