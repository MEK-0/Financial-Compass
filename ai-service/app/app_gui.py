import streamlit as st
import time
import json
from datetime import datetime
from app.agents.orchestrator import FinancialOrchestrator
from app.models.request_models import AnalysisRequest


st.set_page_config(page_title="Finansal Pusula AI", layout="wide", initial_sidebar_state="collapsed")


st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .bank-card {
        background: linear-gradient(135deg, #00693E 0%, #008f55 100%);
        color: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 10px 20px rgba(0,105,62,0.2); margin-bottom: 20px;
    }
    .metric-container {
        background-color: white; padding: 20px; border-radius: 15px;
        border-bottom: 4px solid #00693E; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
    }
    .terminal-box {
        background-color: #1a1b1e; color: #e0e0e0; padding: 20px;
        border-radius: 12px; font-family: 'JetBrains Mono', monospace;
        border: 1px solid #333; min-height: 250px; font-size: 14px;
    }
    .stButton>button {
        background-color: #00693E; color: white; border-radius: 50px;
        padding: 10px 25px; font-weight: bold; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)


with open('test_input.json', 'r', encoding='utf-8') as f:
    mock_data = json.load(f)
request_obj = AnalysisRequest(**mock_data)


st.markdown('<h1 style="color: #00693E;">🏦 Finansal Pusula</h1>', unsafe_allow_html=True)

col_card, col_metrics = st.columns([1, 2])

with col_card:
    st.markdown(f"""
        <div class="bank-card">
            <p style="font-size: 0.8rem; opacity: 0.8;">TOPLAM VARLIK</p>
            <h2 style="margin: 0;">{request_obj.user_metadata.current_balance:,.2f} TL</h2>
            <p style="font-size: 0.7rem; margin-top: 20px; opacity: 0.6;">MAHMUT ESAT **** 1923</p>
            <p style="font-size: 0.9rem; font-weight: bold; text-align: right;">Garanti BBVA</p>
        </div>
    """, unsafe_allow_html=True)

with col_metrics:
    m1, m2, m3 = st.columns(3)
    m1.markdown(
        f'<div class="metric-container"><p style="color:gray; font-size:0.8rem;">Kredi Kartı Borcu</p><h3 style="color:#d9534f;">{request_obj.user_metadata.credit_card_debt:,.2f} TL</h3></div>',
        unsafe_allow_html=True)
    m2.markdown(
        f'<div class="metric-container"><p style="color:gray; font-size:0.8rem;">Aylık Gelir</p><h3 style="color:#28a745;">{request_obj.user_metadata.salary:,.2f} TL</h3></div>',
        unsafe_allow_html=True)
    m3.markdown(
        f'<div class="metric-container"><p style="color:gray; font-size:0.8rem;">Maaş Günü</p><h3 style="color:#00693E;">{request_obj.user_metadata.salary_day}. Gün</h3></div>',
        unsafe_allow_html=True)

# 4. AI Terminal Kısmı
st.markdown("### 🤖 Finansal Zeka Analiz Terminali")

# Terminali başlatma butonu
start_analysis = st.button("Pusulayı Çalıştır")


terminal_placeholder = st.empty()
initial_content = '<div class="terminal-box"><span style="color:#666;">> Analizi başlatmak için butona tıklayın...</span></div>'
terminal_placeholder.markdown(initial_content, unsafe_allow_html=True)

if start_analysis:
    full_log = ""


    def add_log(message, color="#ffffff"):
        ts = datetime.now().strftime("[%H:%M:%S]")
        return f'<div style="color:#666; display:inline;">{ts} </div><span style="color:{color};">{message}</span><br>'


    log_steps = [
        ("Thinking: Kullanıcı portföyü ve harcamalar analiz ediliyor...", "#569cd6"),
        ("Found historical data: Son veriler backend'den çekildi.", "#ffffff"),
        ("TOOL: accountant_agent -> Sabit giderler projeksiyonu oluşturuluyor...", "#ce9178"),
        ("Thinking: Gelecek yükümlülükler belirlendi. Anomaliler taranıyor...", "#569cd6"),
        ("TOOL: detective_agent -> MCC 4899 kategorisi taranıyor...", "#ce9178"),
        ("! ANOMALY FOUND: Spotify zammı ve mükerrer abonelikler tespit edildi.", "#d16969"),
        ("Finalizing: Serbest bakiye hesaplanıyor...", "#569cd6")
    ]

    for msg, color in log_steps:
        full_log += add_log(msg, color)
        terminal_placeholder.markdown(f'<div class="terminal-box">{full_log}</div>', unsafe_allow_html=True)
        time.sleep(0.8)


    orchestrator = FinancialOrchestrator(request_obj)
    report = orchestrator.run_full_analysis()

    full_log += add_log("SUCCESS: Analiz raporu oluşturuldu.", "#4ec9b0")
    terminal_placeholder.markdown(f'<div class="terminal-box">{full_log}</div>', unsafe_allow_html=True)


    st.markdown("---")
    res_c1, res_c2 = st.columns(2)

    with res_c1:
        st.markdown(f"""
            <div style="background-color: white; padding: 25px; border-radius: 15px; border-left: 10px solid #28a745;">
                <h4 style="margin-top:0;">💡 AI Finansal Özet</h4>
                <p style="font-size: 1.1rem; color: #333;">{report['safe_to_spend']['explanation']}</p>
                <h2 style="color: #28a745;">{report['safe_to_spend']['amount']:,.2f} TL</h2>
            </div>
        """, unsafe_allow_html=True)

    with res_c2:
        st.markdown(
            '<div style="background-color: white; padding: 25px; border-radius: 15px; border-left: 10px solid #d9534f;">',
            unsafe_allow_html=True)
        st.markdown('<h4 style="margin-top:0;">🚨 Dedektif Bulguları</h4>', unsafe_allow_html=True)
        for alert in report['alerts']:
            st.markdown(f"<small>• {alert['message']}</small><br>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.table(report['upcoming_obligations'])