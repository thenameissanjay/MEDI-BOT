import streamlit as st
import PyPDF2
from io import BytesIO
from medisearch_client import MediSearchClient
import uuid
import warnings

import pyttsx3

# Title
st.title("Report GPT")

# File upload widget to allow users to upload a PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Function to extract text from a PDF file
def extract_text_from_pdf(uploaded_file):
    if uploaded_file is not None:
        warnings.filterwarnings("ignore", category=PyPDF2.utils.PdfReadWarning)
        pdf_reader = PyPDF2.PdfFileReader(uploaded_file)
        page_content = []
        print(pdf_reader.numPages)

        for page_num in range(pdf_reader.numPages):
            print(pdf_reader.numPages)
            page = pdf_reader.getPage(page_num)
            text = page.extractText()
            page_content.append(text)
            print(text)

        return page_content

# Process the uploaded PDF file and display the extracted text
if uploaded_file:
    st.write("File uploaded successfully!")
    extracted_text = extract_text_from_pdf(uploaded_file)
    for page_num, text in enumerate(extracted_text, start=1):
            st.write(f"Page {page_num}:\n{text}\n")
            api_key = "8590291a-8835-463b-a9e8-c8e1e08535ec"
            conversation_id = str(uuid.uuid4())
            client = MediSearchClient(api_key=api_key)
            responses = client.send_user_message(conversation=[text], 
                                    conversation_id=conversation_id,
                                    should_stream_response=True,
                                    language="English")
            st.write(responses)
            for response in responses:
               if response["event"] == "llm_response":
                 llm_answer = response["text"]
                 print(llm_answer)
            st.write(llm_answer)
            engine = pyttsx3.init()
            st.image('speak.gif', caption="ABU_THE_BOT",use_column_width=True)

            engine.say(llm_answer)
            engine.runAndWait()
            st.image('abu.gif', caption="ABU_THE_BOT",use_column_width=True)
            break