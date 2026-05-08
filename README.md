# 🎬 AI-Powered Media Content Automation Pipeline

An intelligent multi-agent pipeline that automatically generates a complete marketing content package from a single topic — using LangChain, Groq, and Llama 3.1.

---

## 🚀 Demo

> Enter a topic like **"AI in Healthcare"** → Get a full content package in seconds

| Output | Description |
|---|---|
| 📄 Blog | 150-200 word marketing blog |
| 🗒️ Summary | 2-3 line summary of the content |
| 📰 Headline | One catchy, engaging headline |
| 📲 Social Posts | LinkedIn + Twitter/X posts |
| #️⃣ Hashtags | 7 trending, relevant hashtags |

---

## 🧠 How It Works

```
You enter a TOPIC
       ↓
Agent 1 (Content Writer)     → Generates blog + ad copy + product description
       ↓
Agent 2 (Summarizer)         → Summarizes content into 2-3 lines
       ↓
Agent 3 (Headline Creator)   → Creates headline using content + summary
       ↓
Agent 4 (Social Media Mgr)   → Writes LinkedIn + Twitter posts
       ↓
Agent 5 (Hashtag Expert)     → Generates 7 hashtags
       ↓
Streamlit UI displays everything in tabs + download option
```

Each agent **passes its output to the next** — so every piece of content is connected and consistent.

---

## 🛠️ Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| LLM | Groq + Llama 3.1 (8B) | Fast, free AI inference |
| Orchestration | LangChain | Agent chaining and management |
| Prompts | PromptTemplate | Structured, reusable prompts |
| Chains | LCEL (`\|` pipe) | Modern agent wiring |
| UI | Streamlit | Interactive web application |
| Config | python-dotenv | Secure API key management |

---

## 📁 Project Structure

```
Langchain_media/
├── pipeline_langchain.py   # All 5 agents + pipeline logic
├── app.py                  # Streamlit web UI
├── .env                    # Your API key (never push this)
├── .gitignore              # Ignores .env
└── requirements.txt        # Dependencies
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ai-media-automation.git
cd ai-media-automation
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file
```bash
# Create a .env file in the project root
GROQ_API_KEY=your_groq_api_key_here
```

> Get your free Groq API key at: https://console.groq.com

### 4. Run the pipeline (terminal test)
```bash
python pipeline_langchain.py
```

### 5. Run the Streamlit app
```bash
streamlit run app.py
```

---

## 🔑 Getting Your Groq API Key

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to **API Keys**
4. Click **Create API Key**
5. Copy and paste into your `.env` file

---

## 📦 Requirements

```
langchain
langchain-groq
langchain-core
langchain-community
streamlit
python-dotenv
```

---

## 💡 Two Modes

### Mode 1 — Topic Mode
Enter a topic → Pipeline generates content from scratch
```
Input:  "Electric Vehicles in India"
Output: Blog + Summary + Headline + LinkedIn + Twitter + Hashtags
```

### Mode 2 — Content Mode
Paste existing content → Pipeline repurposes it
```
Input:  Your existing article or blog
Output: Summary + Headline + LinkedIn + Twitter + Hashtags
```

---

## 🏗️ Agent Architecture

```python
# Each agent is a clean 3-step chain
content_chain  = content_gen_prompt | llm | parser   # Agent 1
summary_chain  = summary_prompt     | llm | parser   # Agent 2
headline_chain = headline_prompt    | llm | parser   # Agent 3
social_chain   = social_prompt      | llm | parser   # Agent 4
hashtag_chain  = hashtag_prompt     | llm | parser   # Agent 5
```

Agents share context:
- **Agent 3** receives output from Agent 1 + Agent 2
- **Agent 4** receives output from Agent 1 + Agent 3
- **Agent 5** receives output from Agent 1 + Agent 4

---

## ✅ Features

- 🤖 5 specialized AI agents working in sequence
- 🔗 Context sharing between agents (not isolated)
- ✔️ Output validation layer — catches bad responses
- 📱 Dual input modes — topic or existing content
- 🎨 Clean tabbed UI with download option
- 🔒 Secure API key management
- ⚡ Fast inference via Groq hardware

---

## 🗺️ Future Improvements

- [ ] Add memory so agents remember previous generations
- [ ] Connect to Gmail to auto-send content
- [ ] Add image generation for social posts
- [ ] Support multiple LLM providers (OpenAI, Gemini)
- [ ] Deploy on Streamlit Cloud

---

> ⭐ If you found this useful, give it a star on GitHub!
