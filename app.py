import os
import tempfile
import streamlit as st
from faster_whisper import WhisperModel
from utils_srt import segments_to_srt

st.set_page_config(page_title="Audio → Text", page_icon="🗣️", layout="centered")
st.title("🗣️ Audio → Text (Whisper)")
st.caption("Upload audio/video → get transcript as TXT or SRT")

# Sidebar
st.sidebar.header("Settings")
model_size = st.sidebar.selectbox("Model", ["large-v3", "medium", "small"], index=0)
device = "cuda" if st.sidebar.checkbox("Use GPU (CUDA)", value=False) else "cpu"

uploaded = st.file_uploader("Upload audio/video file", type=["mp3","wav","m4a","mp4","mkv","mov","aac","flac","ogg","webm"])

if uploaded is not None:
    st.write("**File uploaded:**", uploaded.name)

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded.name)[1]) as tmp:
        tmp.write(uploaded.read())
        input_path = tmp.name

    with st.spinner("Loading model…"):
        model = WhisperModel(model_size, device=device)

    with st.spinner("Transcribing…"):
        segments, info = model.transcribe(input_path)
        segments = list(segments)

    st.success("Transcription complete ✅")
    full_text = "\n".join((seg.text or "").strip() for seg in segments)
    srt_text = segments_to_srt([{"start": seg.start, "end": seg.end, "text": seg.text} for seg in segments])

    st.subheader("Transcript")
    st.text_area("", full_text, height=300)

    st.download_button("⬇️ Download TXT", data=full_text, file_name="transcript.txt")
    st.download_button("⬇️ Download SRT", data=srt_text, file_name="transcript.srt")
