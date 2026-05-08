## pipeline_langchain.py
## AI Media Automation Pipeline — LangChain version (fixed imports for LangChain v0.3+)

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

# ── LLM setup ──────────────────────────────────────────────────────────────────
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",
    temperature=0.7,
)

parser = StrOutputParser()

# ── Prompt Templates ───────────────────────────────────────────────────────────

content_gen_prompt = PromptTemplate(
    input_variables=["topic"],
    template="""
You are a marketing content expert.

Generate content in this exact format:

Blog:
(150-200 words)

Product Description:
(3 bullet points)

Ad Copy:
Headline:
Body:
Call to Action:

Topic: {topic}
"""
)

summary_prompt = PromptTemplate(
    input_variables=["content"],
    template="""
You are a media assistant.
Summarize the following content in 5-10 lines clearly.
If the content is very short (under 50 words), reply with: "Content is short, no summary needed."

CONTENT:
{content}
"""
)

headline_prompt = PromptTemplate(
    input_variables=["content", "summary"],
    template="""
You are a media expert.
Using the content and its summary below, generate ONE catchy, engaging headline.
Keep it under 15 words.

CONTENT:
{content}

SUMMARY:
{summary}
"""
)

social_prompt = PromptTemplate(
    input_variables=["content", "headline"],
    template="""
You are a social media manager.

Based on the headline and content below, generate:

1. A professional LinkedIn post (max 150 words)
2. A short Twitter/X post (max 280 characters)

HEADLINE: {headline}
CONTENT:
{content}

Rules:
- LinkedIn: professional tone, add a question at the end
- Twitter/X: punchy, conversational, ends with 1-2 emojis
"""
)

hashtag_prompt = PromptTemplate(
    input_variables=["content", "social"],
    template="""
You are a social media expert.
Generate exactly 7 relevant, trending hashtags.
Base them on the content and social posts below.
Return hashtags in one line, separated by spaces.

CONTENT:
{content}

SOCIAL POSTS:
{social}
"""
)

# ── Chains using LCEL (LangChain Expression Language) ─────────────────────────
content_chain = content_gen_prompt | llm | parser
summary_chain = summary_prompt | llm | parser
headline_chain = headline_prompt | llm | parser
social_chain = social_prompt | llm | parser
hashtag_chain = hashtag_prompt | llm | parser

# ── Output Validator ───────────────────────────────────────────────────────────

def validate_output(result: dict) -> dict:
    required_keys = ["content", "summary", "headline", "social", "hashtags"]
    for key in required_keys:
        val = result.get(key, "").strip()
        if not val or len(val) < 5:
            result[key] = f"⚠️ Agent '{key}' returned no usable output. Try rephrasing your input."
    return result

# ── Public entry point ─────────────────────────────────────────────────────────

def run_pipeline(content: str = None, topic: str = None) -> dict:
    if not content and not topic:
        return {"error": "Please provide content or a topic."}

    try:
        if topic and not content:
            print("Generating content...")
            content = content_chain.invoke({"topic": topic})
            mode = "generated"
        else:
            mode = "processed"

        print("Summarizing...")
        summary = summary_chain.invoke({"content": content})

        print("Generating headline...")
        headline = headline_chain.invoke({"content": content, "summary": summary})

        print("Generating social posts...")
        social = social_chain.invoke({"content": content, "headline": headline})

        print("Generating hashtags...")
        hashtags = hashtag_chain.invoke({"content": content, "social": social})

        result = {
            "mode": mode,
            "content": content,
            "summary": summary,
            "headline": headline,
            "social": social,
            "hashtags": hashtags,
        }

        return validate_output(result)

    except Exception as e:
        return {"error": f"Pipeline failed: {str(e)}"}


# ── CLI test ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    topic = input("Enter topic: ")
    result = run_pipeline(topic=topic)
    for key, value in result.items():
        print(f"\n{'─'*40}\n{key.upper()}\n{'─'*40}\n{value}")
