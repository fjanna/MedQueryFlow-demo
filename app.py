import json, yaml, streamlit as st
from core.pipeline import MedQueryFlowPipeline

st.set_page_config(page_title="MedQueryFlow · Final Proper", layout="wide")
st.title("MedQueryFlow · RAG + Qwen2 (Offline)")

with open("config.yaml","r",encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

if "pipeline" not in st.session_state:
    st.session_state["pipeline"] = MedQueryFlowPipeline(cfg)

q = st.text_input("Ask a medical question:", "Does my chest feel tight because I ate something bad?")
show_prompts = st.checkbox("Show raw prompts (debug)", value=True)

if st.button("Run"):
    res = st.session_state["pipeline"].run(q)

    # UI banner: MedQuAD missing
    if not res.get("corpus_ok", True):
        st.warning("MedQuAD subset not found. Using fallback stubs. Put your medquad_subset.json into data/ .")

    tabs = st.tabs(["Intent","Rewrites","Retrieved (local)","Retrieved (web)","Answer / Safety / Logs"])

    with tabs[0]:
        st.subheader("Predicted intent")
        st.code(res["intent"])
        if res.get("intent_probs"):
            st.subheader("Confidence")
            probs = res["intent_probs"]
            st.bar_chart({"probability": probs})
            st.write({k: round(v, 4) for k, v in probs.items()})
        if show_prompts and res.get("intent_raw_prompt"):
            with st.expander("Raw intent prompt"):
                st.text(res["intent_raw_prompt"])

    with tabs[1]:
        st.write(res["rewrites"])
        if res.get("rewrite_prompt_error"):
            st.error(res["rewrite_prompt_error"])

    with tabs[2]:
        st.write(res["retrieved"]["local"])

    with tabs[3]:
        st.write(res["retrieved"]["web"])

    with tabs[4]:
        st.subheader("Answer")
        st.markdown(res["answer"]["text"])
        st.divider()
        st.subheader("Safety")
        trig = res["answer"]["safety_triggered"]
        st.write(f"Triggered: **{trig}**")
        st.write(f"Terms: {res['answer']['safety_terms']}")
        if show_prompts and res["answer"].get("raw_prompt"):
            st.subheader("Raw answer prompt")
            with st.expander("Show prompt"):
                st.text(res["answer"]["raw_prompt"])

        st.divider()
        # Export JSON button
        export_payload = json.dumps(res, indent=2, ensure_ascii=False)
        st.download_button("Export JSON", data=export_payload, file_name="medqueryflow_run.json", mime="application/json")
