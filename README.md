# ✦ Unmess

> **Turn the chaos in your head into a plan.**

Unmess is a **local-first AI life-admin assistant** that transforms messy, unstructured thoughts into actionable tasks.

Instead of opening a traditional to-do app and manually figuring out what needs to be done, you simply write down what's on your mind.

Unmess uses an **open-weight language model running locally through Ollama** to understand the brain dump, extract individual tasks, identify deadlines, assign priorities, detect blockers, and store the resulting tasks for later use.

---

## ✨ The Problem

Most productivity tools assume that the user already knows how to organize their thoughts.

Real life doesn't work that way.

A person might think:

> "I have to finish my homework tomorrow, submit my exam form by midnight, study for my test on October 6th, send flowers to my friend, and buy groceries today."

That's not a clean task list.

It's a **brain dump**.

Turning that paragraph into a useful plan requires the user to manually:

- identify separate tasks
- find deadlines
- determine urgency
- remember dependencies
- create individual tasks
- prioritize everything

Unmess moves that work to the AI.

---

# 💡 The Idea

Instead of asking:

> **"What tasks do you want to create?"**

Unmess asks:

> **"What's on your mind?"**

The user writes naturally.

The AI turns that messy input into structured tasks.

### Example

Input:

```text
I need to finish my homework tomorrow,
submit my exam form by midnight,
study for my test on October 6th,
send flowers to my friend,
and buy groceries today.

Output:
🔥 Homework Assignment
Deadline: Tomorrow
Priority: Critical

⚠️ Submit Exam Form
Deadline: Midnight
Priority: High

📚 Study for Test
Deadline: October 6
Priority: High

🌸 Send Flowers
Priority: Low

🛒 Buy Groceries
Deadline: Today
Priority: Low


🧠 Core Features
1. Brain Dump
Write naturally instead of manually creating tasks.
I have too much going on...

The AI extracts actionable items automatically.
2. AI Task Extraction
Unmess uses a local open-weight language model to identify individual tasks from unstructured text.
It separates:
One messy paragraph
        ↓
Multiple actionable tasks

3. Deadline Detection
The agent attempts to recognize deadlines expressed in natural language.
Examples:
tomorrow
today
October 6th
by midnight
Thursday

These are converted into structured task data.
4. Priority Classification
Tasks are assigned a priority:
- critical
- high
- normal
- low
This allows the application to surface urgent work first.
5. Blocker Detection
Unmess can represent task dependencies.
For example:
Get passport photo
        ↓
Submit internship application

The application can represent the second task as being blocked by the first.
6. Persistent Task Storage
Tasks are stored in a local SQLite database using SQLAlchemy.
This means the task list can persist beyond a single browser request.
7. Local AI
The application is designed around local inference through Ollama.
The AI model currently used during development is:
Gemma 3 1B

This means the core AI workflow does not require a proprietary AI API key.

**🏗️ Architecture**

                         USER
                           │
                           ▼
                 ┌──────────────────┐
                 │     Next.js      │
                 │    Frontend      │
                 └────────┬─────────┘
                          │
                          │ HTTP
                          ▼
                 ┌──────────────────┐
                 │     FastAPI      │
                 │     Backend      │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │    AI Agent      │
                 │                  │
                 │  Gemma + Ollama  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │  Task / Planner  │
                 │  / Memory Tools  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │      SQLite      │
                 │    Database      │
                 └──────────────────┘

**🔄 How the Request Flows**
When a user submits a brain dump:
User
 ↓
Next.js frontend
 ↓
POST /brain-dump
 ↓
FastAPI
 ↓
Gemma via Ollama
 ↓
Structured JSON
 ↓
Task validation / normalization
 ↓
Task creation tools
 ↓
SQLite
 ↓
FastAPI response
 ↓
Next.js task cards

🛠️ Tech Stack
Frontend
- Next.js
- React
- TypeScript
- Tailwind CSS
Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic
AI
- Gemma 3
- Ollama
- Local inference
Storage
- SQLite
📁 Project



⚙️ Getting Started
Prerequisites
Make sure you have:
- Python 3.11+
- Node.js
- npm
- Git
- Ollama

cmd-
git clone https://github.com/YOUR_USERNAME/unmess.git
cd unmess
ollama pull gemma3:1b

in backend-
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

The backend should now be available at:
http://127.0.0.1:8000

Set up the frontend-
in frontend-
npm install
npm run dev

the frontend should be available at:
http://localhost:3000

🤝 Contributing
Contributions are welcome.
A typical contribution workflow:
git clone https://github.com/YOUR_USERNAME/unmess.git
cd unmess
git checkout -b feature/your-feature

Make your changes, test them locally, then:
git add .
git commit -m "feat: describe your change"
git push origin feature/your-feature

Open a pull request on GitHub.


🔮 Vision
Unmess is built around a simple idea:
Your productivity tool shouldn't require you to be productive before it can help you.

Real thoughts are messy.
Deadlines overlap.
Responsibilities are scattered across conversations, notes, memory, and random thoughts.
The goal of Unmess is to build an AI layer that can understand that mess and gradually turn it into something actionable.

👩‍💻 Built By
Gauri Mishra
Computer Science & Engineering student exploring:
- AI agents
- Generative AI
- local AI
- developer tools
- intelligent productivity systems
⭐ Support the Project
If Unmess is useful or interesting:
- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Open feature requests
- 🔧 Submit pull requests
- 📣 Share it with someone who has too much going on