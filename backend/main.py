from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv
import re

load_dotenv()

app = FastAPI(title="ZeroBugAuthority")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Pydantic models
class CodeReviewRequest(BaseModel):
    code: str
    language: str
    focus_areas: list[str]

class CodeRewriteRequest(BaseModel):
    code: str
    language: str

class ReviewResponse(BaseModel):
    review: str
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int

# Helper function to parse review
def parse_review_response(review_text: str) -> dict:
    """Extract issue counts from review"""
    
    critical_section = re.search(r'###.*?Critical Issues.*?\n(.*?)(?=###|\Z)', review_text, re.DOTALL)
    high_section = re.search(r'###.*?High Priority.*?\n(.*?)(?=###|\Z)', review_text, re.DOTALL)
    medium_section = re.search(r'###.*?Medium Priority.*?\n(.*?)(?=###|\Z)', review_text, re.DOTALL)
    low_section = re.search(r'###.*?Low Priority.*?\n(.*?)(?=###|\Z)', review_text, re.DOTALL)
    
    def count_items(section):
        if not section:
            return 0
        text = section.group(1)
        # Count numbered items or bullet points
        items = re.findall(r'^\d+\.|^-|^\*', text, re.MULTILINE)
        return len(items)
    
    return {
        "critical_count": count_items(critical_section),
        "high_count": count_items(high_section),
        "medium_count": count_items(medium_section),
        "low_count": count_items(low_section)
    }

# Endpoints
@app.get("/", response_class=HTMLResponse)
async def serve_login():
    """Serve login page"""
    try:
        with open("../frontend/login.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>❌ login.html not found</h1>")

@app.get("/app", response_class=HTMLResponse)
async def serve_tool():
    """Serve main tool page"""
    try:
        with open("../frontend/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>❌ index.html not found</h1>")

@app.post("/api/review", response_model=ReviewResponse)
async def review_code(request: CodeReviewRequest):
    """Review code and provide suggestions"""
    
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    # Format focus areas
    focus_str = ", ".join(request.focus_areas) if request.focus_areas else "all aspects"
    
    # Build prompt
    prompt = f"""You are an expert code reviewer with 15+ years of experience. Analyze this {request.language} code focusing on: {focus_str}.

Code:
```{request.language}
{request.code}
```

Provide a detailed review in this exact format:

### 🔴 Critical Issues
[List each critical bug or security vulnerability as separate bullet points]
- [Another critical issue if exists]

### 🟠 High Priority
[List high priority items as separate bullet points]

### 🟡 Medium Priority
[List medium priority items as separate bullet points]

### 🟢 Low Priority
[List low priority items as separate bullet points]

Be specific about line numbers and provide clear explanations."""

    try:
        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=2000,
            top_p=0.9
        )
        
        review_text = chat_completion.choices[0].message.content
        counts = parse_review_response(review_text)
        
        return ReviewResponse(
            review=review_text,
            critical_count=counts["critical_count"],
            high_count=counts["high_count"],
            medium_count=counts["medium_count"],
            low_count=counts["low_count"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling Groq API: {str(e)}")

@app.post("/api/rewrite")
async def rewrite_code(request: CodeRewriteRequest):
    """Rewrite and optimize code"""
    
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    prompt = f"""You are an expert {request.language} developer. Rewrite this code to fix all issues, improve performance, enhance security, and follow best practices.

Original Code:
```{request.language}
{request.code}
```

Provide:
1. **Rewritten Code** (clean, optimized, production-ready)
2. **Key Improvements** (list 3-5 main changes)
3. **Explanation** (brief summary of what was improved)

Format your response as:
### ✨ Rewritten Code
```{request.language}
[optimized code here]
```

### 💡 Key Improvements
- Improvement 1
- Improvement 2
- Improvement 3

### 📖 Explanation
[Brief summary]"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=2000,
            top_p=0.9
        )
        
        return {"rewritten_code": chat_completion.choices[0].message.content}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling Groq API: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)