import streamlit as st
import json
import re

# Page configuration
st.set_page_config(page_title="AI Technical Recruiter", page_icon="🤖", layout="wide")

# --- Mock Evaluation Logic (No API Key Required) ---
def evaluate_candidate(jd_text, resume_text):
    """
    Mock evaluation function. 
    In production, replace this with an LLM API call using the system prompt 
    defined in the sidebar to ensure objective, evidence-based evaluation 
    without inferring demographic details.
    """
    if not jd_text or not resume_text:
        return None

    # Simple heuristic to extract a name for the mock response
    name_match = re.search(r'(?:Name|Candidate)[:\s]+([A-Za-z\s]+?)(?:\n|Email|Phone)', resume_text, re.IGNORECASE)
    candidate_name = name_match.group(1).strip() if name_match else "Candidate"
    
    # Mock scoring based on text length/complexity for demonstration
    jd_len = len(jd_text.split())
    res_len = len(resume_text.split())
    base_score = min(10, max(4, int((res_len / max(jd_len, 1)) * 4)))
    
    # Ensure recommendation aligns with score
    if base_score >= 8:
        rec = "Strong Yes"
    elif base_score >= 6:
        rec = "Yes"
    elif base_score >= 4:
        rec = "Maybe"
    else:
        rec = "No"

    return {
        "name": candidate_name,
        "overall_score": base_score,
        "dimension_scores": {
            "technical_skills_match": min(10, base_score + 1),
            "experience_level": base_score,
            "impact_and_achievements": min(10, base_score + 2) if base_score > 2 else 2,
            "education_and_certifications": 8,
            "red_flags_absence": 9 # 10 means no red flags
        },
        "strengths": [
            "Strong alignment with core technical requirements and tech stack.",
            "Demonstrated quantifiable impact and scope in previous roles.",
            "Clear progression in seniority and experience level."
        ],
        "concerns": [
            "Minor gap in specific niche tool mentioned in the job description.",
            "Could elaborate more on cross-functional leadership experience."
        ],
        "recommendation": rec,
        "one_liner_summary": f"{candidate_name} is a solid fit for the role with a strong technical foundation and proven impact, though minor upskilling may be needed for niche tools."
    }

# --- UI Layout ---
st.title("🤖 AI Technical Recruiter")
st.markdown("Evaluate candidates objectively across 5 key dimensions. *Built with Streamlit.*")

# Sidebar with instructions/persona
with st.sidebar:
    st.header("⚙️ Recruiter Persona")
    st.markdown("""
    **Role:** Expert Technical Recruiter (15 years exp)
    **Rules:**
    - Be objective and evidence-based.
    - Do not infer demographic details.
    - Score dimensions 1-10.
    - Output strict JSON format.
    """)
    st.info("💡 **Note:** This demo uses a mock evaluator. In production, connect this UI to an LLM API to process real resumes.")

# Main input area
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Job Description")
    jd_input = st.text_area("Paste the Job Description here...", height=300)

with col2:
    st.subheader("📝 Candidate Resume")
    resume_input = st.text_area("Paste the Candidate's Resume here...", height=300)

# Evaluate Button
if st.button("🚀 Evaluate Candidate", type="primary", use_container_width=True):
    if not jd_input or not resume_input:
        st.warning("Please provide both a Job Description and a Resume.")
    else:
        with st.spinner("Analyzing candidate profile..."):
            # Simulate processing time
            import time
            time.sleep(1.5) 
            
            result = evaluate_candidate(jd_input, resume_input)
            
            if result:
                st.success("Evaluation Complete!")
                st.divider()
                
                # Header
                st.header(f"Evaluation for: {result['name']}")
                st.markdown(f"**Recommendation:** `{result['recommendation']}` | **Overall Score:** `{result['overall_score']}/10`")
                st.markdown(f"*{result['one_liner_summary']}*")
                
                st.divider()
                
                # Dimension Scores
                st.subheader("📊 Dimension Scores")
                dims = result['dimension_scores']
                cols = st.columns(len(dims))
                for i, (key, val) in enumerate(dims.items()):
                    # Format key for display
                    display_key = key.replace('_', ' ').title()
                    cols[i].metric(label=display_key, value=f"{val}/10")
                
                # Strengths and Concerns
                col_s, col_c = st.columns(2)
                with col_s:
                    st.subheader("✅ Strengths")
                    for s in result['strengths']:
                        st.markdown(f"- {s}")
                with col_c:
                    st.subheader("⚠️ Concerns")
                    for c in result['concerns']:
                        st.markdown(f"- {c}")
                
                # Raw JSON Output
                with st.expander("🔍 View Raw JSON Output"):
                    st.json(result)