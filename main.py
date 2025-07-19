import streamlit as st
from langgraph.types import Command
from pathlib import Path
from graphsetup import create_graph 
import uuid

# --- Page Configuration ---
st.set_page_config(
    page_title="Auto News Generator",
    page_icon="📰",
    layout="wide",
)

# --- Graph Initialization ---
graph = create_graph()

# --- Session State Management ---
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())[:8]
if "state" not in st.session_state:
    st.session_state.state = None
if "interrupted" not in st.session_state:
    st.session_state.interrupted = False
if "config" not in st.session_state:
    st.session_state.config = None

# --- UI Rendering ---
st.title("🎬 Auto News Generator")
st.markdown("---")

# --- Main Content Area ---
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Controls")
    st.markdown(f"**Session ID:** `{st.session_state.thread_id}`")

    if st.button("🚀 Start Creation", use_container_width=True):
        st.session_state.interrupted = False
        st.session_state.state = None
        
        with st.spinner("🚀 Kicking off the process... Please wait."):
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            result = graph.invoke({}, config=config)
            
            st.session_state.state = result
            st.session_state.config = config
            st.session_state.interrupted = "__interrupt__" in result
            st.rerun()

with col2:
    st.header("Process Status")

    # --- Interrupt Handling ---
    if st.session_state.interrupted:
        interrupt = st.session_state.state["__interrupt__"][0]
        
        with st.container(border=True):
            st.warning("🛑 Human Approval Required")
            st.markdown(f"**🔔 Prompt:** {interrupt.value}")

            script = st.session_state.state.get("script")
            if script:
                st.text_area("Script for Approval", script, height=200, disabled=True)

            with st.form("resume_form"):
                st.write("Do you approve this step?")
                user_input = st.radio("Your Response:", ["yes", "no"], horizontal=True)
                
                if st.form_submit_button("Submit Response"):
                    with st.spinner("▶️ Resuming process..."):
                        resumed = graph.invoke(
                            Command(resume=user_input),
                            config=st.session_state.config
                        )
                        st.session_state.state = resumed
                        st.session_state.interrupted = "__interrupt__" in resumed
                        st.rerun()

    # --- Completion Handling ---
    elif st.session_state.state:
        final = st.session_state.state
        upload_status = final.get("upload_status")

        if upload_status == "uploaded":
            st.balloons()
            st.success("🎉 Video uploaded successfully!")
            st.markdown(f"🔗 **YouTube URL:** {final.get('youtube_url')}")
        elif upload_status == "no":
            st.error("❌ Upload failed")
            st.markdown(f"**Error:** {final.get('upload_error', 'An unknown error occurred.')}")
        else:
            st.info("✅ Process completed successfully!")

        with st.expander("📦 View Final State", expanded=False):
            st.json({k: v for k, v in final.items() if k != "__interrupt__"})

    else:
        st.info("👋 Welcome! Click 'Start Creation' to begin.")