import streamlit as st
import requests
import json

# API endpoints
TEXT_API_URL = "https://pranav1908-codereviewautomation.hf.space/AutomateReview/"
FILE_API_URL = "https://pranav1908-codereviewautomation.hf.space/loadFile/"

# Function to generate review for text input
def generate_code_review_text(code_snippet):
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(TEXT_API_URL, json={"code": code_snippet}, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

# Function to generate review for file input
def generate_code_review_file(file):
    try:
        files = {"file": file}
        response = requests.post(FILE_API_URL, files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

# Streamlit App UI
st.title('Code Review Automation')

# Option to choose between text input or file upload
input_option = st.radio("Choose your input method:", ("Enter Text", "Upload File"))

if input_option == "Enter Text":
    text_code = st.text_area("Enter your code here...")
    if st.button("Generate Code Review", type="primary", key="text_review"):
        if text_code.strip():
            # Call API for text input
            review = generate_code_review_text(text_code)
            
            if review:
                # Decode escaped characters in the response
                response_text = json.loads(json.dumps(review.get("answer", "")))
                st.write("### Code Review")
                st.write(response_text)
            else:
                st.error("Failed to generate code review. Please try again.")
        else:
            st.warning("Please enter some code before generating a review.")

elif input_option == "Upload File":
    uploaded_file = st.file_uploader("Upload your code file", type=["py", "java", "txt", "cpp", "js"])
    if uploaded_file and st.button("Generate Code Review", type="primary", key="file_review"):
        # Call API for file input
        review = generate_code_review_file(uploaded_file)
        
        if review:
            # Decode escaped characters in the response
            response_text = json.loads(json.dumps(review.get("answer", "")))
            st.write("### Code Review")
            st.write(response_text)
        else:
            st.error("Failed to generate code review. Please try again.")
