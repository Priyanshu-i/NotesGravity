import streamlit as st
import requests
import time
from gradio_client import Client

ICON_URL = "https://i.postimg.cc/mrzQQ23m/notes-Gravity.png"

st.set_page_config(
    page_title="NotesGravity AI",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .reportview-container {
        background: #fafafa
    }
    .sidebar .sidebar-content {
        background: #f0f2f6
    }
    .stTextArea textarea {
        font-size: 16px;
    }
    .stButton>button {
        background-color: #534AB7;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background-color: #3C3489;
        color: white;
    }
    .generated-note {
        background-color: #EEEDFE;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #534AB7;
        font-size: 18px;
        line-height: 1.6;
        margin-top: 10px;
    }
</style>
""",
    unsafe_allow_html=True,
)


# @st.cache_resource so the client only initializes ONCE
@st.cache_resource(show_spinner=False)
def load_api_client():
    try:
        # Connects to your specific HF Space
        client = Client("priyanshu-i/notes-gravity-api")
        return client
    except Exception as e:
        st.error(f"Error connecting to Gradio API. Details: {e}")
        return None

with st.spinner("Connecting to Cloud API... (This might take a few seconds)"):
    client = load_api_client()



with st.sidebar:
    st.image(
        "https://i.postimg.cc/mrzQQ23m/notes-Gravity.png", width=210
    )  # Custom logo
    st.title("⚙️ Model Settings")
    st.markdown("Fine-tune how NotesGravity generates your notes.")

    st.divider()

    with st.expander("Advanced Generation Parameters", expanded=False):
        num_beams = st.slider(
            "Beam Search (Quality)",
            min_value=1,
            max_value=8,
            value=5,
            help="Higher = better quality but slower.",
        )
        length_penalty = st.slider(
            "Length Penalty",
            min_value=0.1,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="> 1.0 encourages longer notes; < 1.0 forces extreme brevity.",
        )
        rep_penalty = st.slider(
            "Repetition Penalty",
            min_value=1.0,
            max_value=2.0,
            value=1.1,
            step=0.1,
            help="Prevents the model from repeating the same word.",
        )
        max_tokens = st.number_input(
            "Max Output Tokens", min_value=50, max_value=500, value=150
        )
        min_tokens = st.number_input(
            "Min Output Tokens", min_value=2, max_value=50, value=2
        )

    st.divider()
    st.markdown("### System Status")
    if client:
        st.success("🟢 Connected to Cloud API")
    else:
        st.error("🔴 API Connection Failed")



try:
    response = requests.get(ICON_URL, timeout=5)
    if response.status_code == 200:
        st.markdown(
            f"""
            <h1 style="display:flex; align-items:center;">
                <img src="{ICON_URL}" width="75" style="margin-right:-20px;">
                otesGravity AI
            </h1>
            """,
            unsafe_allow_html=True
        )
    else:
        st.title("📝 NotesGravity AI")
except:
    st.title("📝 NotesGravity AI")

st.markdown(
    "Paste your textbook paragraphs, articles, or lecture transcripts below. NotesGravity will destroy the grammar and compress it into terse, symbolic, bullet-ready notes."
)


col1, col2, col3 = st.columns([1, 10, 1])

with col2:
    input_text = st.text_area(
        "Enter text to terse:",
        height=200,
        placeholder="E.g., Photosynthesis converts sunlight into chemical energy through chlorophyll in plant cells, producing glucose and oxygen.",
    )

    
    button_col1, button_col2 = st.columns([2, 8])
    with button_col1:
        generate_clicked = st.button("⚡ Generate Notes", use_container_width=True)

    st.divider()

    
    if generate_clicked:
        if not input_text.strip():
            st.error("⚠️ Please enter some text first.")
        elif not client:
            st.error("⚠️ API Client failed to load.")
        else:
            start_time = time.time()
            
            with st.spinner("API is chunking and processing your notes..."):
                try:
                    final_notes = client.predict(
                        input_text,          # text
                        max_tokens,          # max_new_tokens
                        min_tokens,          # min_new_tokens
                        num_beams,           # num_beams
                        length_penalty,      # length_penalty
                        rep_penalty,         # rep_penalty
                        api_name="/predict"  # Default API route for Gradio
                    )
                except Exception as e:
                    st.error(f"API Error: {e}")
                    final_notes = ""

            end_time = time.time()

            # Display Results
            if final_notes:
                st.markdown("### ✨ Your Generated Notes:")
                st.markdown(
                    f'<div class="generated-note">{final_notes.replace(chr(10), "<br>")}</div>',
                    unsafe_allow_html=True,
                )

                # Show stats
                input_words = len(input_text.split())
                output_words = len(final_notes.split())
                compression_ratio = output_words / input_words if input_words > 0 else 0

                st.caption(
                    f"⏱️ API Generated in {end_time - start_time:.2f} seconds | 📉 Compression Ratio: **{compression_ratio:.2f}** ({input_words} words → {output_words} words)"
                )