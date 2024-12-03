import streamlit as st
import openai
import time

# Configure OpenAI API
openai.api_base = "https://api.openai.com/v1"
openai.api_key = st.secrets["OPENAI_API_KEY"] 

# Streamlit app setup
st.title("VBA to SQL Translator")
st.markdown("Paste VBA code below to translate it to SQL Server language.")

# Text input area for VBA code
vba_code = st.text_area("Enter VBA Code:", height=300, placeholder="Paste your VBA code here...")

# Button to trigger translation
if st.button("Translate to SQL"):
    if vba_code.strip():
        with st.spinner("Translating VBA to SQL..."):
            for attempt in range(3):  # Retry logic
                try:
                    # Prepare prompt for the OpenAI model
                    prompt = f"Translate the following VBA code to SQL Server language:\n\n{vba_code}"

                    # Call OpenAI API
                    response = openai.Completion.create(
                        model="gpt-4",  # Update model as needed
                        prompt=prompt,
                        temperature=0.2,
                        max_tokens=1500
                    )

                    # Extract the SQL translation
                    sql_translation = response.get("choices", [])[0].get("text", "").strip()

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

# Footer
st.markdown("---")
st.markdown("Powered by OpenAI")
