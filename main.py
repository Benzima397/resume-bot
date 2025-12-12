import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

# Initialize the App
app = FastAPI()

# SECURITY: Allow your WordPress site to talk to this API
# In production, replace "*" with your actual domain (e.g., "https://nwaochei.tech")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://bencodes.tech",
        "https://bencodes.tech",
        "http://www.bencodes.tech",
        "https://www.bencodes.tech"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
)

# DATA: Your Resume Context (Populated from your source files)
# This is what the AI "knows" about you.
RESUME_CONTEXT = """
You are the AI Assistant for Benjamin Nwaochei. You answer questions about his career.
Here is Benjamin's professional profile:

SUMMARY:
Senior Software Engineer & AI Architect based in Lagos, Nigeria.
Specializes in bridging Enterprise WordPress with Python Automation.
Focuses on Cybersecurity, Robotics logic, and Database Design.

EXPERIENCE:
1. Seplat Energy Plc (2024–Present):
   - Role: IT Support Engineer & Systems Analyst.
   - [cite_start]Key Work: Diagnoses complex hardware/software issues[cite: 3]. [cite_start]Maintains rigorous cybersecurity standards[cite: 7]. 
   - Environment: Network Infrastructure, System Diagnosis.

2. Cv-HUB 4 Africa (2022–2024):
   - Role: Software Engineer.
   - [cite_start]Key Work: Architected relational databases and data entry systems[cite: 3]. [cite_start]Collaborated on system analysis based on client requirements[cite: 3].
   - Environment: Python, SQL, API Integration.

3. Growatt Integrated Company (2019–2021):
   - Role: Web Developer & Digital Strategy Lead.
   - [cite_start]Key Achievement: Increased web traffic by 80% through technical SEO and content optimization[cite: 3].
   - [cite_start]Managed digital channels (Twitter, LinkedIn) and paid ads[cite: 3].

EDUCATION:
- HND, Lagos City Polytechnic (Completed 2023). [cite_start]Awarded Best Innovative Student[cite: 5].
- [cite_start]Diploma in Cybersecurity Fundamentals[cite: 14].

SKILLS:
- Tech Stack: Python (FastAPI, Django), WordPress (Headless, Custom Plugins), SQL.
- Domain: Robotics (AI), Digital Strategy, Cybersecurity.

INSTRUCTIONS:
- Keep answers professional, concise, and under 3 sentences.
- If asked about contact info, provide: benjaminnwaochei@gmail.com.
- If the answer isn't in this text, say: "I don't have that specific detail, but you can email Benjamin directly."
"""


# The Request Model (What the frontend sends)
class QueryRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"status": "Benjamin's AI is Online"}


@app.post("/ask")
async def ask_resume(request: QueryRequest):
    try:
        # Check for API Key using the new name: GROQ_API_KEY
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            # Update the error message to reflect the correct key name
            raise HTTPException(status_code=500, detail="Groq API Key not found")
        # Initialize the Chat Model (GPT-4o-mini is cheap and fast)
        ChatGroq(model="mixtral-8x7b-32768", temperature=0)

        # Create the conversation
        messages = [
            SystemMessage(content=RESUME_CONTEXT),
            HumanMessage(content=request.question)
        ]

        # Get response
        response = chat.invoke(messages)

        return {"answer": response.content}

    except Exception as e:
        return {"error": str(e)}

# To run locally: uvicorn main:app --reload
