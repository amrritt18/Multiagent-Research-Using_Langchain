import streamlit as st
from datetime import datetime
from src.pipeline.pipeline import run_research_pipeline


# --------------------------------------------------
# 1. Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# 2. Custom Styling
# --------------------------------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 750;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.05rem;
        color: #808080;
        margin-bottom: 1.5rem;
    }

    .stage-card {
        padding: 1rem;
        border: 1px solid rgba(128, 128, 128, 0.3);
        border-radius: 12px;
        margin-bottom: 0.5rem;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        min-height: 2.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# 3. Session State
# --------------------------------------------------
if "research_result" not in st.session_state:
    st.session_state.research_result = None

if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""


# --------------------------------------------------
# 4. Sidebar
# --------------------------------------------------
with st.sidebar:
    st.title("Research Assistant")

    st.markdown(
        """
        Your AI research workflow uses four components:

        1. **Search Agent** — finds relevant web sources.
        2. **Reader Agent** — extracts webpage content.
        3. **Writer Chain** — generates a research report.
        4. **Critic Chain** — evaluates the report.

        ---
        """
    )

    st.subheader("Technology Stack")

    st.markdown(
        """
        - LangChain
        - Groq LLM
        - Tavily Search
        - Trafilatura
        - Streamlit
        """
    )

    st.divider()

    if st.button("Clear Research Results"):
        st.session_state.research_result = None
        st.session_state.last_topic = ""
        st.rerun()

    st.caption("Multi-Agent Research System")


# --------------------------------------------------
# 5. Main Header
# --------------------------------------------------
st.markdown(
    '<div class="main-title">Multi-Agent Research Assistant</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Research a topic, gather web evidence, generate a report, "
    "and evaluate its quality."
    "</div>",
    unsafe_allow_html=True,
)


# --------------------------------------------------
# 6. Research Input
# --------------------------------------------------
with st.form("research_form"):
    topic = st.text_area(
        "Enter your research topic",
        placeholder=(
            "Example: Recent applications of multi-agent AI "
            "systems in healthcare"
        ),
        height=100,
        max_chars=500,
    )

    submitted = st.form_submit_button(
        "Start Research",
        type="primary",
        use_container_width=True,
    )


# --------------------------------------------------
# 7. Execute Research Pipeline
# --------------------------------------------------
if submitted:
    topic = topic.strip()

    if not topic:
        st.warning("Please enter a research topic.")

    else:
        # Clear previous results before starting a new run.
        st.session_state.research_result = None
        st.session_state.last_topic = ""

        try:
            with st.spinner(
                "Research is in progress. Agents are working..."
            ):
                result = run_research_pipeline(topic)

            # Store results only after successful completion.
            st.session_state.research_result = result
            st.session_state.last_topic = topic

            st.success("Research pipeline completed successfully!")

        except Exception as error:
            st.error(
                "The research pipeline failed. "
                "Check your API keys, network connection, "
                "model availability, and terminal traceback."
            )

            with st.expander("Error details"):
                st.code(str(error))


# --------------------------------------------------
# 8. Display Results
# --------------------------------------------------
result = st.session_state.research_result

if result:
    st.divider()

    st.subheader("Research Overview")
    st.write(f"**Topic:** {st.session_state.last_topic}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Search", "Completed")

    with col2:
        st.metric("Reader", "Completed")

    with col3:
        st.metric("Writer", "Completed")

    with col4:
        st.metric("Critic", "Completed")

    # ----------------------------------------------
    # Tabs for Individual Stages
    # ----------------------------------------------
    search_tab, reader_tab, report_tab, critic_tab = st.tabs(
        [
            "Search Results",
            "Extracted Research",
            "Final Report",
            "Critic Feedback",
        ]
    )

    with search_tab:
        st.subheader("Web Search Results")
        st.markdown(
            result.get(
                "search_results",
                "No search results available.",
            )
        )

    with reader_tab:
        st.subheader("Extracted Web Content")
        st.markdown(
            result.get(
                "scraped_content",
                "No scraped content available.",
            )
        )

    with report_tab:
        st.subheader("Generated Research Report")

        report = result.get("report", "")

        st.markdown(report or "No report was generated.")

        if report:
            st.download_button(
                label="Download Research Report",
                data=report,
                file_name="research_report.md",
                mime="text/markdown",
                use_container_width=True,
            )

    with critic_tab:
        st.subheader("Critic Evaluation")

        feedback = result.get("feedback", "")

        st.markdown(feedback or "No critic feedback available.")

        if feedback:
            st.download_button(
                label="Download Critic Feedback",
                data=feedback,
                file_name="critic_feedback.md",
                mime="text/markdown",
                use_container_width=True,
            )

    # ----------------------------------------------
    # Download Complete Results
    # ----------------------------------------------
    st.divider()
    st.subheader("Export Research")

    full_report = f"""# Multi-Agent Research Report

**Topic:** {st.session_state.last_topic}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 1. Search Results

{result.get("search_results", "")}

---

## 2. Extracted Research

{result.get("scraped_content", "")}

---

## 3. Final Report

{result.get("report", "")}

---

## 4. Critic Feedback

{result.get("feedback", "")}
"""

    st.download_button(
        label="Download Complete Research (Markdown)",
        data=full_report,
        file_name="complete_research.md",
        mime="text/markdown",
        type="primary",
        use_container_width=True,
    )

else:
    st.info(
        "Enter a research topic above and click Start Research "
        "to generate your first report."
    )
