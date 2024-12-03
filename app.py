import streamlit as st
import openai
import time
import re


# Configure OpenAI API
openai.api_key = st.secrets["OPENAI_API_KEY"]


# Function to clean input code
def clean_code(input_code):
    """
    Cleans input code (VBA or WebFOCUS) by:
    - Removing comments and blank lines.
    - Optionally truncating large blocks.
    """
    # Remove comments (lines starting with ' or Rem for VBA, or -* for WebFOCUS)
    code_without_comments = re.sub(r"^\s*('.*|Rem\s+.*|-\*.*)$", "", input_code, flags=re.MULTILINE)
    
    # Remove blank lines
    cleaned_code = "\n".join([line for line in code_without_comments.splitlines() if line.strip()])
    
    # Optional: Limit the length of input
    max_lines = 100  # Keep only the first 100 lines if input is too long
    if len(cleaned_code.splitlines()) > max_lines:
        cleaned_code = "\n".join(cleaned_code.splitlines()[:max_lines]) + "\n'... Truncated for length"
    
    return cleaned_code


# Streamlit app setup
st.title("Code Translator: VBA/WebFOCUS to SQL")
st.markdown("Paste your VBA or WebFOCUS code below to translate it to SQL Server language.")

# Text input area for the code
input_code = st.text_area("Enter Code:", height=300, placeholder="Paste your code here...")

# Button for VBA to SQL translation
if st.button("Translate VBA to SQL"):
    if input_code.strip():
        with st.spinner("Translating VBA to SQL..."):
            for attempt in range(3):  # Retry logic
                try:
                    # Clean the VBA code
                    cleaned_code = clean_code(input_code)
                    
                    # Prepare messages for the OpenAI ChatCompletion API
                    messages = [
                        {"role": "system", "content": "You are an expert in translating VBA code to SQL Server language."},
                        {"role": "user", "content": f"Translate the following VBA code to SQL Server language:\n\n{cleaned_code}"}
                    ]

                    # Call OpenAI API using ChatCompletion
                    response = openai.ChatCompletion.create(
                        model="gpt-4",  # Or "gpt-3.5-turbo"
                        messages=messages,
                        temperature=0.2,
                        max_tokens=3000
                    )

                    # Extract the SQL translation
                    sql_translation = response["choices"][0]["message"]["content"].strip()

                    # Display result
                    st.success("Translation Complete!")
                    st.text_area("SQL Translation:", sql_translation, height=300)
                    break
                except Exception as e:
                    if attempt < 2:
                        st.warning(f"Attempt {attempt + 1} failed. Retrying...")
                        time.sleep(2)  # Wait before retrying
                    else:
                        st.error(f"Error after 3 attempts: {str(e)}")
    else:
        st.warning("Please enter VBA code before translating!")

# Button for WebFOCUS to SQL translation
if st.button("Translate WebFOCUS to SQL"):
    if input_code.strip():
        with st.spinner("Translating WebFOCUS to SQL..."):
            for attempt in range(3):  # Retry logic
                try:
                    # Clean the WebFOCUS code
                    cleaned_code = clean_code(input_code)
                    
                    # Prepare messages for the OpenAI ChatCompletion API
                    messages = [
                        {"role": "system", "content": "You are an expert in translating WebFOCUS code to SQL Server language."},
                        {"role": "user", "content": f"Translate the following WebFOCUS code to SQL Server language:\n\n{cleaned_code}"}
                    ]

                    # Call OpenAI API using ChatCompletion
                    response = openai.ChatCompletion.create(
                        model="gpt-4",  # Or "gpt-3.5-turbo"
                        messages=messages,
                        temperature=0.2,
                        max_tokens=3000
                    )

                    # Extract the SQL translation
                    sql_translation = response["choices"][0]["message"]["content"].strip()

                    # Display result
                    st.success("Translation Complete!")
                    st.text_area("SQL Translation:", sql_translation, height=300)
                    break
                except Exception as e:
                    if attempt < 2:
                        st.warning(f"Attempt {attempt + 1} failed. Retrying...")
                        time.sleep(2)  # Wait before retrying
                    else:
                        st.error(f"Error after 3 attempts: {str(e)}")
    else:
        st.warning("Please enter WebFOCUS code before translating!")

# Footer
st.markdown("---")
st.markdown("Powered by OpenAI")
