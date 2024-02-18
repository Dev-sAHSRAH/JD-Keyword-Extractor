import streamlit as st
import PyPDF2 as pdf
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(JD):
    
    #Prompt template

    input_prompt =f"""
    Imagine yourself as a seasoned Application Tracking System (ATS), brimming with years of experience deciphering the intricate language of technical expertise. Your singular purpose today is to delve into the depths of the provided job description, acting as a meticulous extractor of all things technical.
    With laser focus, scan every line, sentence, and phrase, leaving no stone unturned in your quest. Seek out and capture every technical skill, technology, tool, framework, software, and platform mentioned within the text. Be mindful, however, to keep your gaze firmly fixed on these specific targets, disregarding any common stop words or extraneous phrases that may linger nearby.
    Remember, your mission is to capture the essence of each technical term, even if it appears embedded within a larger sentence. For instance, should you encounter the phrase "versioning tools such as Git," do not succumb to the allure of capturing the entire sentence. Instead, your discerning eye should focus solely on "Git," focus of the techstack,tools,software or framework only. Similarly, if you stumble upon the statement "Relational database backends using ORMs and plain SQL interfaces," let your expertise guide you toward capturing only the vital elements: "ORMs" and "SQL."

    Do not confine your search to designated sections labeled "Skills" or "Technical Requirements." Remember, valuable technical details can lurk anywhere within the job description, waiting to be unearthed by your keen eye. Treat every line as a potential treasure trove of technical information, meticulously examining each word to ensure no morsel of knowledge escapes your grasp.

    Finally, upon conclusion of your thorough analysis, present your findings in a clear and concise manner. 
    Compile all extracted technical skills into a well-structured JSON format, where each skill is represented as a lowercase string within an array aptly named "skills."
    Return it as a single string as shown below so that I can parse it directly for further processing:

    '{{"skills": ["skill1", "skill2",...]}}'
    Before showing the output check if each of them is a techstack or a tool or a framework or a platform, else omit.
    For more accuracy, do the task 3 times,try to find the missing one's from the previous results(nothing should be out of the JD) and add it ,give me the output of only 3 of them individually.
    make sure to keep the output in the same way as shown: key should always be "skills" and all values must be in  lowercase.

    Here's the Job description: {JD}
    """

    model = genai.GenerativeModel("gemini-pro")
    res = model.generate_content(input_prompt).text
    if(res.startswith("```json")):
        res = res[7:]
        res.rstrip("```")
        
    return (res)

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""

    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text+=str(page.extract_text())

    return text


##streamlit app
st.title("Recruiter Model")
st.text("JD - Resume Matcher")

JD = st.file_uploader("Upload Job Description",type="pdf")

submit = st.button("Submit")

if submit:
    if (JD is not None):
        text = input_pdf_text(JD)

        response = get_gemini_response(text)

        st.text(response)