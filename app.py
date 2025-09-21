import streamlit as st
from resume_parser import extract_keywords, extract_text_from_pdf
import random

st.set_page_config(page_title="Career & Skills Advisor", layout="wide")
st.title("🎯 Personalized Career and Skills Advisor")

menu = st.sidebar.radio("Choose Feature", ["Career Mentor", "Skill Roadmap", "Mock Interview"])

# Define roles with keywords for matching
roles_keywords = {
    "Data Scientist": ["python","machine learning","statistics","data analysis","pandas","numpy","scikit-learn"],
    "Web Developer": ["javascript","html","css","react","node.js","frontend","backend"],
    "AI Engineer": ["deep learning","tensorflow","pytorch","nlp","neural network","python"]
}

# Predefined resources for skills
resources = {
    "python": "https://www.w3schools.com/python/",
    "machine learning": "https://www.coursera.org/learn/machine-learning",
    "statistics": "https://www.khanacademy.org/math/statistics-probability",
    "data analysis": "https://www.datacamp.com/",
    "pandas": "https://pandas.pydata.org/docs/",
    "numpy": "https://numpy.org/",
    "scikit-learn": "https://scikit-learn.org/stable/",
    "javascript": "https://www.w3schools.com/js/",
    "html": "https://www.w3schools.com/html/",
    "css": "https://www.w3schools.com/css/",
    "react": "https://reactjs.org/docs/getting-started.html",
    "node.js": "https://nodejs.org/en/docs/",
    "frontend": "https://developer.mozilla.org/en-US/docs/Learn/Front-end_web_developer",
    "backend": "https://developer.mozilla.org/en-US/docs/Learn/Server-side",
    "deep learning": "https://www.deeplearning.ai/",
    "tensorflow": "https://www.tensorflow.org/",
    "pytorch": "https://pytorch.org/tutorials/",
    "nlp": "https://www.nltk.org/",
    "neural network": "https://www.coursera.org/learn/neural-networks-deep-learning"
}

question_templates = [
    "Explain your experience with {}.",
    "How have you used {} in real projects?",
    "What challenges did you face when working with {}?"
]

# --------- Features ---------
if menu == "Career Mentor":
    uploaded_file = st.file_uploader("Upload your resume PDF", type=["pdf"])
    resume_text = extract_text_from_pdf(uploaded_file) if uploaded_file else ""

    if st.button("Get Career Suggestions"):
        if resume_text.strip() == "":
            st.warning("Please upload your resume PDF!")
        else:
            resume_keywords = extract_keywords(resume_text)
            scores = {}
            for role, role_kw in roles_keywords.items():
                match_count = len(set(resume_keywords) & set(role_kw))
                scores[role] = match_count
            top_roles = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
            st.success("Top Career Matches:")
            for role, score in top_roles:
                st.write(f"**{role}** - {score} keyword matches")

elif menu == "Skill Roadmap":
    uploaded_file = st.file_uploader("Upload your resume PDF", type=["pdf"])
    resume_text = extract_text_from_pdf(uploaded_file) if uploaded_file else ""
    target_role = st.selectbox("Select Target Role", list(roles_keywords.keys()))

    if st.button("Get Skill Gap Analysis"):
        if resume_text.strip() == "":
            st.warning("Please upload your resume PDF!")
        else:
            resume_keywords = extract_keywords(resume_text)
            user_skills = list(set(resume_keywords) & set(roles_keywords[target_role]))
            missing_skills = [skill for skill in roles_keywords[target_role] if skill not in user_skills]
            
            st.info(f"Skills you already have: {', '.join(user_skills) if user_skills else 'None'}")
            
            if missing_skills:
                st.warning("Skills to learn:")
                for skill in missing_skills:
                    link = resources.get(skill, "No resource found")
                    st.write(f"- {skill} → [Learn here]({link})")
            else:
                st.success("You have all key skills for this role!")

elif menu == "Mock Interview":
    target_role = st.selectbox("Select Role", list(roles_keywords.keys()))
    uploaded_file = st.file_uploader("Upload your resume PDF (optional, for dynamic Qs)", type=["pdf"])
    resume_text = extract_text_from_pdf(uploaded_file) if uploaded_file else ""

    if st.button("Generate Interview Question"):
        resume_keywords = extract_keywords(resume_text) if resume_text.strip() else []
        relevant_keywords = list(set(resume_keywords) & set(roles_keywords[target_role]))
        if relevant_keywords:
            keyword = random.choice(relevant_keywords)
        else:
            keyword = random.choice(roles_keywords[target_role])
        question = random.choice(question_templates).format(keyword)
        st.write(f"**Interview Question:** {question}")

    answer = st.text_area("Type your answer here")
    if st.button("Get Feedback"):
        if answer.strip() == "":
            st.warning("Please type your answer!")
        else:
            answer_keywords = extract_keywords(answer)
            match = list(set(answer_keywords) & set(roles_keywords[target_role]))
            if match:
                st.success(f"Good! You mentioned: {', '.join(match)}")
            else:
                st.warning("Try to mention relevant skills from your target role!")
