ZeroBug Authority: AI-Powered Code Guardian

*ZeroBug Authority* is an advanced developer tool that leverages the lightning-fast inference of *Llama 3.3 70B* on *Groq* to provide real-time code reviews and automated logic rewrites. It goes beyond simple linting by identifying deep-seated security vulnerabilities and performance bottlenecks, then providing a side-by-side diff of optimized, production-ready code.

Key Features

*Real-Time AI Logs*: Watch the "thought process" of the AI as it analyzes your AST and scans for vulnerabilities.
*Security-First Analysis*: Detects critical flaws like SQL Injection, XSS, and hardcoded credentials.
*Intelligent Rewrites*: Automatically refactors code for better Big O complexity and memory management.
*Visual Diff Viewer*: See exactly what changed with a professional side-by-side comparison (Red/Green highlighting).
*Workflow Integration*: One-click "Apply to Repo" simulation to streamline the Pull Request process.
*Adaptive UI*: Modern glassmorphism design with Dark/Light mode support for accessibility.

Tech Stack

*Model*: Llama 3.3 70B Versatile.
*Inference Engine*: [Groq Cloud](https://groq.com) (Ultra-low latency).
*Backend*: Python / FastAPI.
*Frontend*: Tailwind CSS, Highlight.js, jsdiff.

Installation & Setup

### 1. Clone the Repository

git clone https://github.com/safura-minhaj/ZeroBugAuthorityGenAI.git
cd ZeroBugAuthorityGenAI



### 2. Backend Setup

cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt



### 3. Environment Variables

Create a `.env` file in the `backend` folder:

GROQ_API_KEY=your_groq_api_key_here


*(Note: Never commit your actual API keys to GitHub!)*

### 4. Run the Project

*Start the Backend:*

python main.py

**Start the Frontend:**
Simply open `frontend/login.html` in your browser (or use the "Go Live" extension in VS Code).


## 📖 How it Works

1. *Input*: The user pastes a code snippet (C#, Python, JS, etc.).
2. *Analysis*: The agent performs a multi-step scan:
* *AST Construction*: Parsed via the LLM to understand logic flow.
* *Security Scan*: Checks against OWASP top 10 standards.
* *Optimization*: Identifies redundant loops or inefficient memory usage.


3. *Output*: A structured report showing bolded errors, line numbers, and an optimized "After" version.
