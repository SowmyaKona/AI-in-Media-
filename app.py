## app.py — improved Streamlit frontend for LangChain pipeline

import streamlit as st
from pipeline_langchain import run_pipeline

st.set_page_config(
    page_title="AI Media Automation",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 AI-Powered Media Content Automation")
st.caption("Powered by LangChain + Groq (Llama 3.1)")

# ── Inputs ─────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    topic = st.text_input(
        "💡 Enter a topic",
        placeholder="e.g. AI in healthcare",
        help="The pipeline will generate content from scratch",
    )

with col2:
    content = st.text_area(
        "✍️ Or paste existing content",
        placeholder="Paste your article, blog, or brief here...",
        height=120,
        help="The pipeline will summarize & repurpose this",
    )

# ── Validate before calling ────────────────────────────────────────────────────
generate = st.button("🚀 Generate", use_container_width=True)

if generate:
    if not content and not topic:
        st.error("Please enter a topic OR paste some content.")
    else:
        with st.spinner("Running agents…"):
            result = run_pipeline(content=content or None, topic=topic or None)

        if "error" in result:
            st.error(result["error"])
        else:
            mode_label = "📝 Topic → Content" if result.get("mode") == "generated" else "🔄 Content Repurposing"
            st.success(f"Mode: {mode_label}")

            # ── Tabbed output (cleaner than stacked sections) ──────────────────
            tabs = st.tabs(["📄 Content", "🗒️ Summary", "📰 Headline", "📲 Social Posts", "#️⃣ Hashtags"])

            with tabs[0]:
                st.markdown(result.get("content", ""))

            with tabs[1]:
                st.info(result.get("summary", ""))

            with tabs[2]:
                st.subheader(result.get("headline", ""))

            with tabs[3]:
                raw_social = result.get("social", "")
                # Split LinkedIn / Twitter if both present
                if "LinkedIn" in raw_social and "Twitter" in raw_social:
                    parts = raw_social.split("Twitter", 1)
                    st.markdown("**LinkedIn**")
                    st.write(parts[0].replace("LinkedIn", "").strip().lstrip("1. ").strip())
                    st.markdown("**Twitter / X**")
                    st.write(("Twitter" + parts[1]).replace("Twitter", "").strip().lstrip("2. ").strip())
                else:
                    st.write(raw_social)

            with tabs[4]:
                hashtags = result.get("hashtags", "")
                for tag in hashtags.split():
                    st.badge(tag)

            # ── Download all as text ───────────────────────────────────────────
            export_text = "\n\n".join(
                f"=== {k.upper()} ===\n{v}"
                for k, v in result.items()
                if k not in ("mode", "error")
            )
            st.download_button(
                "⬇️ Download all outputs",
                data=export_text,
                file_name="media_outputs.txt",
                mime="text/plain",
            )
