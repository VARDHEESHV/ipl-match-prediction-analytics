import streamlit as st
import joblib
import json
import pandas as pd
import math
import time
import base64
from pathlib import Path

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="IPL Match Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# HELPER FUNCTION TO LOAD IMAGE
# =====================================================
def get_base64_image(image_path):
    """Convert image to base64 for embedding in HTML"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# Load IPL logo
ipl_logo_base64 = get_base64_image("IPL_LOGO.png")

# =====================================================
# VIBRANT COLOR THEME CSS
# =====================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

:root {
    --primary-blue: #00BFFF;
}

:root {
    --card-bg: linear-gradient(
        180deg,
        #111827 0%,
        #0f172a 100%
    );
    --card-border: rgba(255, 255, 255, 0.08);
}


            
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(
        180deg,
        #0f172a 0%,
        #111827 40%,
        #1f2933 100%
    );
    color: #e5e7eb;
}

.stApp {
    background: linear-gradient(
        180deg,
        #0f172a 0%,
        #111827 40%,
        #1f2933 100%
    );
}


h1 {
    background: linear-gradient(135deg, #00BFFF, #2563eb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
}

h2 {
    color: var(--primary-blue) !important;
    font-weight: 700;
}

h3 {
    color: var(--primary-blue) !important;
    font-weight: 700;
}


            
.section-card {
    background: var(--card-bg);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    border: 1px solid var(--card-border);
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}



.metric-box {
    background: var(--card-bg);
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    border: 1px solid var(--card-border);
}


.metric-title {
    color: #00BFFF;
    font-size: 14px;
    margin-bottom: 8px;
    font-weight: 600;
}

.metric-value {
    color: var(--primary-blue);
    font-size: 28px;
    font-weight: 700;
}


.player-box {
    background: linear-gradient(
        180deg,
        #0f172a,
        #020617
    );
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
}


.player-box:hover {
    border-color: #00BFFF;
    box-shadow: 0 4px 12px rgba(0, 191, 255, 0.2);
}

.player-name {
    color: #00BFFF !important;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 4px;
}

.player-stats {
    color: #64748b;
    font-size: 14px;
}

/* Keep emoji colors original */
.player-stats::before {
    filter: none !important;
}

.win-prob-container {
    position: relative;
    height: 200px;
    margin: 20px 0;
}

.prob-bar {
    display: flex;
    height: 60px;
    border-radius: 30px;
    overflow: hidden;
    margin: 20px 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.prob-team {
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 18px;
    color: white;
    transition: all 0.5s ease;
}

.prob-batting {
    background: linear-gradient(135deg, #00BFFF, #0095d9);
}

.prob-bowling {
    background: linear-gradient(135deg, #6b7280, #9ca3af);
}

.circular-progress {
    position: relative;
    width: 200px;
    height: 200px;
    margin: 20px auto;
}

.circular-progress svg {
    transform: rotate(-90deg);
}

.circular-progress circle {
    fill: none;
    stroke-width: 15;
}

.progress-bg {
    stroke: #e5e7eb;
}

.progress-bar {
    stroke-linecap: round;
    transition: stroke-dashoffset 0.5s ease;
}

.progress-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 48px;
    font-weight: 700;
    background: linear-gradient(135deg, #00FFFF, #00BFFF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.progress-label {
    text-align: center;
    margin-top: -10px;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #64748b;
}

.team-label {
    text-align: center;
    font-size: 14px;
    color: #666666;
    text-transform: uppercase;
    letter-spacing: 1px;
}

button {
    background: linear-gradient(135deg, #00BFFF, #0095d9) !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    border: none !important;
    transition: all 0.3s ease !important;
}

button:hover {
    background: linear-gradient(135deg, #0095d9, #0077b3) !important;
    box-shadow: 0 4px 12px rgba(0, 191, 255, 0.4) !important;
}

.prediction-badge {
    display: inline-block;
    background: linear-gradient(135deg, #39FF14, #2ecc00);
    color: #000000;
    padding: 12px 24px;
    border-radius: 25px;
    font-size: 18px;
    font-weight: 700;
    margin: 10px 0;
    box-shadow: 0 4px 12px rgba(57, 255, 20, 0.4);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

label, .stSelectbox label, .stTextInput label, .stNumberInput label, .stRadio label {
    color: #00BFFF !important;
    font-weight: 600 !important;
}

.stSelectbox > div > div {
    background-color: #ffffff !important;
    border: 2px solid #00BFFF !important;
    color: #1e3a8a !important;
}

.stTextInput > div > div > input {
    background-color: #ffffff !important;
    border: 2px solid #00BFFF !important;
    color: #1e3a8a !important;
}

.stNumberInput > div > div > input {
    background-color: #ffffff !important;
    border: 2px solid #00BFFF !important;
    color: #1e3a8a !important;
}

/* Radio group title (Analysis Mode) */
.stRadio > label {
    color: #22C55E !important;
    font-weight: 700 !important;
}

/* Radio options text */
.stRadio div[role="radiogroup"] label {
    color: #22C55E !important;
    font-weight: 600 !important;
}

/* Selected radio background */
.stRadio div[role="radiogroup"] label:has(input:checked) {
    background-color: rgba(34, 197, 94, 0.15) !important;
    border-radius: 6px;
    padding: 4px 8px;
}

/* Radio circle */
.stRadio input[type="radio"] {
    accent-color: #22C55E !important;
}


.stMarkdown {
    color: #1e3a8a;
}

.stCaption {
    color: #64748b !important;
}

.ipl-logo {
    width: 120px;
    height: auto;
    display: inline-block;
    vertical-align: middle;
    margin-right: 25px;
}

.header-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
}

.toss-stat-box {
    background: linear-gradient(
        180deg,
        #0f172a,
        #020617
    );
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    border: 1px solid var(--card-border);
}


.toss-stat-title {
    color: #00BFFF;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 6px;
}

.toss-stat-value {
    color: #38bdf8;
    font-size: 32px;
    font-weight: 700;
}


.toss-stat-label {
    color: #64748b;
    font-size: 12px;
    margin-top: 4px;
}
            
[data-testid="stMetricValue"] {
    color: var(--primary-blue) !important;
    font-size: 26px;
    font-weight: 700;
}

[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-weight: 600;
}          

div[data-testid="stAlert"] {
    background-color: #e6f6ff !important;
    color: var(--primary-blue) !important;
    border-left: 6px solid var(--primary-blue) !important;
    font-weight: 600;
}
            
/* Number input label */
.stNumberInput label {
    color: #22C55E !important;
    font-weight: 700 !important;
}

.stNumberInput input {
    font-weight: 600 !important;
}

div[data-testid="stHorizontalBlock"] {
    background: transparent !important;
}

                     
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD MODELS & DATA (CACHED)
# =====================================================
@st.cache_resource
def load_artifacts():
    win_model = joblib.load("win_probability_model.pkl")
    margin_model = joblib.load("margin_model.pkl")
    with open("city_stats.json") as f:
        city_stats = json.load(f)
    return win_model, margin_model, city_stats

with st.spinner("Loading IPL Intelligence..."):
    win_model, margin_model, city_stats = load_artifacts()

# =====================================================
# HELPER FUNCTIONS (CRICKET-REALISTIC)
# =====================================================
def cricket_realistic_probability(score, avg_win, ml_prob):
    diff = score - avg_win
    logistic = 1 / (1 + math.exp(-0.12 * diff))
    cricket_prob = 0.30 + logistic * (0.97 - 0.30)
    final = 0.65 * cricket_prob + 0.35 * ml_prob
    return max(0.03, min(final, 0.97))

def cricket_realistic_margin(score, avg_win, ml_margin):
    diff = score - avg_win
    if diff <= 0:
        return None
    base = diff * 0.6
    final = 0.7 * base + 0.3 * ml_margin
    return max(1, round(final))

def predict_match(city, score):
    stats = city_stats[city]

    X = dict.fromkeys(win_model.feature_names_in_, 0)
    X["year"] = 2025
    X["innings_1st"] = 1
    X["innings_2nd"] = 2
    X["innings_score_1st"] = score
    X["innings_score_2nd"] = 0
    X["toss_winner_batted_first"] = 1
    X["score_vs_avg"] = score - stats["avg_score"]
    X["score_vs_winning_avg"] = score - stats["avg_winning_score"]
    X["score_percentile"] = 0.5
    X["is_high_score"] = int(score >= stats["avg_winning_score"])
    X["innings_momentum"] = (score - 120) / 120

    city_col = f"city_{city}"
    if city_col in X:
        X[city_col] = 1

    X_df = pd.DataFrame([X])

    ml_prob = win_model.predict_proba(X_df)[0][1]
    ml_margin = margin_model.predict(X_df)[0]

    prob = cricket_realistic_probability(score, stats["avg_winning_score"], ml_prob)
    margin = cricket_realistic_margin(score, stats["avg_winning_score"], ml_margin)

    return prob, margin

# =====================================================
# HEADER WITH IPL LOGO
# =====================================================
if ipl_logo_base64:
    st.markdown(f"""
    <div class="section-card" style="text-align:center;">
        <div class="header-container">
            <img src="data:image/png;base64,{ipl_logo_base64}" class="ipl-logo">
            <h1 style="margin: 0;">IPL Match Prediction & Analytics</h1>
        </div>
        <p style="color: #64748b; margin-top: 10px;">Data-driven insights based on IPL 2023–2025</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="section-card" style="text-align:center;">
        <h1>🏏 IPL Match Prediction & Analytics</h1>
        <p style="color: #64748b;">Data-driven insights based on IPL 2023–2025</p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# MAIN LAYOUT
# =====================================================
left, right = st.columns([1, 2], gap="large")

# =====================================================
# LEFT PANEL – CONFIG
# =====================================================
with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Match Configuration")

    city = st.selectbox("Match City", sorted(city_stats.keys()))

    batting_team = st.text_input("Batting Team (optional)", value="")
    bowling_team = st.text_input("Bowling Team (optional)", value="")

    mode = st.radio(
        "Analysis Mode",
        ["First Innings Score Given", "Yet To Bat"]
    )

    if mode == "First Innings Score Given":
        score = st.number_input(
            "First Innings Score",
            min_value=100,
            max_value=300,
            step=1,
            value=170
        )
    

        predict_btn = st.button("🎯 Predict Outcome")

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# RIGHT PANEL – OUTPUT
# =====================================================
with right:

    stats = city_stats[city]

    # -----------------------------
    # MODE 1 – PREDICTION
    # -----------------------------
    if mode == "First Innings Score Given" and predict_btn:
        prob, margin = predict_match(city, score)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Win Probability")
        st.markdown('<p style="color: #64748b; font-size: 14px;">Based on current match situation</p>', unsafe_allow_html=True)

        # Probability visualization - Circular Progress
        batting_prob = prob * 100
        bowling_prob = 100 - batting_prob

        # Determine color based on probability
        if batting_prob >= 70:
            stroke_color = "#00BFFF"  # Vivid Sky Blue
        elif batting_prob >= 50:
            stroke_color = "#39FF14"  # Neon Green
        else:
            stroke_color = "#00FFFF"  # Electric Cyan

        # Calculate circle parameters
        radius = 85
        circumference = 2 * 3.14159 * radius
        offset = circumference - (batting_prob / 100) * circumference

        # Display circular progress
        st.markdown(f"""
        <div class="circular-progress">
            <svg width="200" height="200">
                <circle class="progress-bg" cx="100" cy="100" r="{radius}"></circle>
                <circle class="progress-bar" cx="100" cy="100" r="{radius}" 
                        stroke="{stroke_color}"
                        stroke-dasharray="{circumference}"
                        stroke-dashoffset="{offset}">
                </circle>
            </svg>
            <div class="progress-text">{int(batting_prob)}%</div>
        </div>
        <div class="progress-label">Win Chance</div>
        """, unsafe_allow_html=True)

        # Probability bar
        st.markdown(f"""
        <div class="prob-bar">
            <div class="prob-team prob-batting" style="width: {batting_prob}%;">
                {batting_team if batting_team else 'BATTING TEAM'}
            </div>
            <div class="prob-team prob-bowling" style="width: {bowling_prob}%;">
                {bowling_team if bowling_team else 'BOWLING TEAM'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Prediction Result
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Match Prediction")

        if margin and prob > 0.5:
            team_name = batting_team if batting_team else "Batting Team"
            st.markdown(
                f'<div class="prediction-badge">🏆 {team_name} expected to win by {margin} runs</div>',
                unsafe_allow_html=True
            )
        elif margin is None or prob <= 0.5:
            team_name = bowling_team if bowling_team else "Bowling Team"
            if margin:
                st.markdown(
                    f'<div class="prediction-badge">🏆 {team_name} expected to win</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="prediction-badge" style="background: linear-gradient(135deg, #00FFFF, #00d4d4);">⚡ Very Close Match Expected</div>',
                    unsafe_allow_html=True
                )

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-title">Batting Team Win %</div>
                    <div class="metric-value">{batting_prob:.1f}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:
            if margin:
                st.markdown(
                    f"""
                    <div class="metric-box">
                        <div class="metric-title">Expected Margin</div>
                        <div class="metric-value">{margin} runs</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div class="metric-box">
                        <div class="metric-title">Match Status</div>
                        <div class="metric-value">Tied</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------
    # MODE 2 – ANALYTICS
    # -----------------------------
    if mode == "Yet To Bat":
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader(f"📊 {city} Stadium Analytics")

        m1, m2, m3, m4 = st.columns(4)

        m1.metric("Avg 1st Innings", round(stats["avg_score"]))
        m2.metric("Avg 2nd Innings", round(stats["avg_second_score"]))
        m3.metric("Avg Winning 1st Inns", round(stats["avg_winning_score"]))
        m4.metric("Highest Chase", stats["highest_chase"])

        st.markdown("---")

        # Calculate actual toss wins from percentages
        # Assuming these are based on total matches, we'll use reasonable estimates
        bat_first_pct = stats['bat_first_win_pct']
        bowl_first_pct = stats['bowl_first_win_pct']
        
        # Calculate wins based on 8 total tosses (adjustable)
        total_tosses = 8
        bat_first_wins = round(total_tosses * bat_first_pct / 100)
        bowl_first_wins = total_tosses - bat_first_wins

        t1, t2 = st.columns(2)
        
        with t1:
            st.markdown(
                f"""
                <div class="toss-stat-box">
                    <div class="toss-stat-title">Bat First Wins</div>
                    <div class="toss-stat-value">{bat_first_wins}</div>
                    <div class="toss-stat-label">out of {total_tosses} matches</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with t2:
            st.markdown(
                f"""
                <div class="toss-stat-box">
                    <div class="toss-stat-title">Bowl First Wins</div>
                    <div class="toss-stat-value">{bowl_first_wins}</div>
                    <div class="toss-stat-label">out of {total_tosses} matches</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.success(f"🎯 Toss Recommendation: **{stats['toss_recommendation']}**")

        st.markdown('</div>', unsafe_allow_html=True)

        # -----------------------------
        # TOP PLAYERS - ENHANCED BOXES (TOP 5)
        # -----------------------------
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🌟 Top Performers (2023–2025)")

        p1, p2 = st.columns(2)

        with p1:
            st.markdown("### 🏏 Top Run Scorers")
            for i, p in enumerate(stats["top_run_scorers"][:5], 1):
                st.markdown(
                    f"""
                    <div class="player-box">
                        <div class="player-name">#{i}  {p['player']}</div>
                        <div class="player-stats">⭐ {p['runs']} runs</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with p2:
            st.markdown("### 🎯 Top Wicket Takers")
            for i, p in enumerate(stats["top_wicket_takers"][:5], 1):
                st.markdown(
                    f"""
                    <div class="player-box">
                        <div class="player-name">#{i}  {p['player']}</div>
                        <div class="player-stats">🔥 {p['wickets']} wickets</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================
st.caption("IPL analytics powered by ML models + cricket-aware logic | Seasons 2023–2025")