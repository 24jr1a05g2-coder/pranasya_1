import streamlit as st
import random
import time

# -----------------------------------------------------------------------------
# Configuration & Page Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Pranasya’s Rock Paper Scissors Game",
    page_icon="🎮",
    layout="centered"
)

# Custom Styling
st.markdown("""
    <style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        color: #4B5563;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .choice-box {
        font-size: 3rem;
        text-align: center;
        padding: 10px;
    }
    .result-text {
        font-size: 1.8rem;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Game Constants
CHOICES = {
    "Rock": "🪨",
    "Paper": "📄",
    "Scissors": "✂️"
}

# Initialize Session State Variables
if "user_score" not in st.session_state:
    st.session_state.user_score = 0
if "computer_score" not in st.session_state:
    st.session_state.computer_score = 0
if "ties" not in st.session_state:
    st.session_state.ties = 0
if "last_user_move" not in st.session_state:
    st.session_state.last_user_move = None
if "last_computer_move" not in st.session_state:
    st.session_state.last_computer_move = None
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# Helper Logic
def determine_winner(user: str, computer: str) -> str:
    if user == computer:
        return "Tie"
    winning_combos = {
        "Rock": "Scissors",
        "Paper": "Rock",
        "Scissors": "Paper"
    }
    if winning_combos[user] == computer:
        return "User"
    return "Computer"

def play_round(user_choice: str):
    computer_choice = random.choice(list(CHOICES.keys()))
    result = determine_winner(user_choice, computer_choice)
    
    st.session_state.last_user_move = user_choice
    st.session_state.last_computer_move = computer_choice
    st.session_state.last_result = result
    
    if result == "User":
        st.session_state.user_score += 1
    elif result == "Computer":
        st.session_state.computer_score += 1
    else:
        st.session_state.ties += 1

def reset_game():
    st.session_state.user_score = 0
    st.session_state.computer_score = 0
    st.session_state.ties = 0
    st.session_state.last_user_move = None
    st.session_state.last_computer_move = None
    st.session_state.last_result = None

# -----------------------------------------------------------------------------
# Sidebar
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("🎮 Game Controls")
    st.markdown("---")
    st.write("### 📜 Rules")
    st.markdown("""
    - 🪨 **Rock** beats ✂️ **Scissors**
    - 📄 **Paper** beats 🪨 **Rock**
    - ✂️ **Scissors** beats 📄 **Paper**
    """)
    st.markdown("---")
    if st.button("🔄 Reset Scoreboard", width="stretch"):
        reset_game()
        st.rerun()

    st.markdown("---")
    st.caption("Created with ❤️ by **Pranasya**")

# -----------------------------------------------------------------------------
# Main Header
# -----------------------------------------------------------------------------
st.markdown('<div class="main-title">🎮 Pranasya’s Rock Paper Scissors Game</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Challenge the AI in a classic showdown!</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Scoreboard
# -----------------------------------------------------------------------------
score_col1, score_col2, score_col3 = st.columns(3)
with score_col1:
    st.metric(label="👤 Player Score", value=st.session_state.user_score)
with score_col2:
    st.metric(label="🤝 Ties", value=st.session_state.ties)
with score_col3:
    st.metric(label="🤖 AI Score", value=st.session_state.computer_score)

st.markdown("---")

# -----------------------------------------------------------------------------
# User Move Selection
# -----------------------------------------------------------------------------
st.subheader("Choose your move:")
col_rock, col_paper, col_scissors = st.columns(3)

with col_rock:
    if st.button("🪨 Rock", width="stretch"):
        play_round("Rock")

with col_paper:
    if st.button("📄 Paper", width="stretch"):
        play_round("Paper")

with col_scissors:
    if st.button("✂️ Scissors", width="stretch"):
        play_round("Scissors")

# -----------------------------------------------------------------------------
# Round Outcome Display
# -----------------------------------------------------------------------------
if st.session_state.last_result:
    st.markdown("---")
    disp_col1, disp_col2 = st.columns(2)
    
    with disp_col1:
        st.markdown("<h4 style='text-align: center;'>Your Move</h4>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='choice-box'>{CHOICES[st.session_state.last_user_move]}<br><small>{st.session_state.last_user_move}</small></div>", 
            unsafe_allow_html=True
        )
        
    with disp_col2:
        st.markdown("<h4 style='text-align: center;'>AI Move</h4>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='choice-box'>{CHOICES[st.session_state.last_computer_move]}<br><small>{st.session_state.last_computer_move}</small></div>", 
            unsafe_allow_html=True
        )

    # Outcome Banner
    res = st.session_state.last_result
    if res == "User":
        st.success("🎉 You Win this round!")
        st.balloons()
    elif res == "Computer":
        st.error("💻 Computer Wins this round!")
    else:
        st.warning("🤝 It's a Tie!")