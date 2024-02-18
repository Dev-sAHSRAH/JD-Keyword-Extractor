import streamlit as st
import PyPDF2 as pdf
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(text1,text2):
    
    #Prompt template

    input_prompt = f"""
    Act like a very experienced ATS(Application Tracking System). You're task is to evaluate the resume based on 
    the given Job Description only. You must extract all the techinal skills,technologies,tools,frameworks mentioned in the Job description word by word, make sure to extract only these
    and then extract the same things from the resume. 
    Make sure to parse the Job Description and Resume to collect only the technology/tool/framework/skillset from every line, by which I mean to say,
    if you see something mentioned like - "versioning tools such as Git", capture only Git. 
    if you see a line like - "Relational database backends using ORMs and plain SQL interfaces" - capture only ORMs and SQL.
    Be very sure of not taking in stop words and other less important words next to them, focus only on keywords.

    Based on the Job description and the missing skillset in the resume, output the response as shown below:

    Skills required as per JD: return a single list
    Skills presents in the resume: return a single list
    Skills missing in the resume: return a single list
    
    Example:
    JD :
    Relevant experience in designing and implementing React JS applications. 
    Extensive experience in catering to developing for modern browsers like Chrome, Edge, etc.
    Good to have: type script + Angular JS combination Experience 
    Must know HTML, CSS, Boot Strap.
    Conduct software analysis, testing, programming, and debugging Implement web services and standards.

    Resume:
    Harsha
    • Operating Systems
    • Computer Networks
    • Database Management Systems (ongoing)
    +91 9019300696 c.harshaofficial@gmail.com Harsha Github://Harsha
    C HARSHA
    Education
    Year Degree/Certificate Institute CGPA/%
    2025 B.Tech PES UNIVERSITY 9.85*
    2021 Intermediate(XII) BASE PU COLLEGE 100%
    2019 Matriculation(X) NARAYANA e-TECHNO SCHOOL 97%
    Projects
    Namma Shaale | An EdTech Platform (Presently working on it)
    Fullstack WebApp
    • Fullstack web application where students can take up courses on multiple domains.
    • Completely Mobile responsive with light and dark mode.
    • Detailed report of views, sales, etc. represented by visually appealing charts
    • Implemented using ChakraUI for UI, Chart.js for charts, Redux for state management, RazorPay
    payment gateway, MongoDB, ExpressJS.
    AI Movie Pitch Generator
    • A movie pitch generator that responds to your thoughts.
    • Suggest the movie pitch along with the suitable cast, title and poster.
    • Implemented using HTML, CSS, JS, OpenAI API.
    Snipify | Blogging App
    • A social publishing platform for people who want to share their learnings or thoughts .
    • User login/logout and comment features are available to make it more interactive among
    community.
    • Implemented using ReactJS, Tailwind CSS, FireBase, react-hot-toast.
    Technical Skills
    Programming Languages: C, C++, JavaScript
    Web development and Databases: HTML5, CSS3, React JS, Redux, Node JS, Express JS, MongoDB, MySQL
    Developer Tools and Technologies: VS Code, Git, GitHub, Bootstrap, Tailwind CSS, MUI
    Relevant Coursework
    • Data Structures and its Applications
    • Design of Algorithms and Analysis
    • Web Technologies
    Achievements
    • Recipient of Prof.C N R Rao Merit Scholarship - 4 times for having CGPA among top 5% of the students
    in the university.
    • HackerRank certified and 5 star in C programming
    • Academics: Department rank – 2.
    Skills required as per JD: ["React JS,"Type Script","Angular JS","HTML","CSS","Boot Starp"]
    Skills in resume:["C, C++, JavaScript,HTML5, CSS3, React JS, Redux, Node JS, Express JS, MongoDB, MySQL,VS Code, Git, GitHub, Bootstrap, Tailwind CSS, MUI,FireBase,Chakra UI"]
    
    Now you compare both the lists and print the missing skills from the resume smtg like below:
    Skills missing: ["Angular JS","Type Script"]
    While comparing, consider everything to be case insensitive and if substring is found do not add it to missing.

    Make sure you don't bring in huge sentences as skills and to parse the whole document word by word.

    The resume and Job description is given below:
    resume:{text1}
    description:{text2}
    """

    model = genai.GenerativeModel("gemini-pro")
    res = model.generate_content(input_prompt)

    return (res.text)

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

resume = st.file_uploader("Upload Resume",type="pdf",help="Please upload the PDF")
JD = st.file_uploader("Upload Job Description",type="pdf")

submit = st.button("Submit")

if submit:
    if (resume is not None) and (JD is not None):
        text1 = input_pdf_text(resume)
        text2 = input_pdf_text(JD)

        response = get_gemini_response(text1,text2)

        st.subheader(response)