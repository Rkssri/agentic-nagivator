from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------
# LLM
# -------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# -------------------------
# STATE DEFINITION
# -------------------------
class ArticleState(TypedDict):
    messages: List[str]   # timeline of agent actions
    status: str           # draft / review / revise / publish
    topic: str            # topic of article
    content: str          # article content

# -------------------------
# AGENT DEFINITIONS
# -------------------------
def writer_agent(state: ArticleState):
    print("\n📝 Writer Agent: Drafting article...", flush=True)
    
    prompt = f"""
You are the Writer Agent.
Write a well‑structured article on the topic: {state['topic']}.
Return ONLY the article text.
"""
    msg = llm.invoke(prompt)

    print("✔ Writer Agent: Draft completed.", flush=True)

    return {
        "messages": state["messages"] + ["Writer → Draft completed"],
        "content": msg.content,
        "status": "draft"
    }


def reviewer_agent(state: ArticleState):
    print("\n🔍 Reviewer Agent: Reviewing article...", flush=True)

    prompt = f"""
You are the Reviewer Agent.
Review the following article:

{state['content']}

Give 5 bullet‑point critiques.
Also rate the article quality from 1 to 10.
"""
    msg = llm.invoke(prompt)

    print("✔ Reviewer Agent: Review completed.", flush=True)

    return {
        "messages": state["messages"] + ["Reviewer → Review completed"],
        "content": msg.content,
        "status": "review"
    }


def planner_agent(state: ArticleState):
    print("\n🧠 Planner Agent: Deciding next step...", flush=True)

    content = state["content"].lower()

    # Extract rating
    import re
    match = re.search(r"(\d+)/?10", content)
    if match:
        score = int(match.group(1))
        print(f"📊 Planner Agent: Detected rating = {score}/10", flush=True)

        if score < 7:
            print("🔁 Planner Agent: Sending back to Writer for revision.", flush=True)
            return {"status": "revise"}

    print("🚀 Planner Agent: Sending to Publisher.", flush=True)
    return {"status": "publish"}


def publisher_agent(state: ArticleState):
    print("\n📢 Publisher Agent: Publishing final content...", flush=True)

    prompt = f"""
You are the Publisher Agent.
Extract 10 key points from the reviewed content below:

{state['content']}

Return ONLY the final published summary.
"""
    msg = llm.invoke(prompt)

    print("✔ Publisher Agent: Publishing completed.", flush=True)

    return {
        "messages": state["messages"] + ["Publisher → Published"],
        "content": msg.content,
        "status": "published"
    }


# -------------------------
# BUILD GRAPH
# -------------------------
graph = StateGraph(ArticleState)

graph.add_node("writer", writer_agent)
graph.add_node("reviewer", reviewer_agent)
graph.add_node("planner", planner_agent)
graph.add_node("publisher", publisher_agent)

# FLOW:
graph.add_edge(START, "writer")
graph.add_edge("writer", "reviewer")
graph.add_edge("reviewer", "planner")

graph.add_conditional_edges(
    "planner",
    lambda state: state["status"],
    {
        "revise": "writer",
        "publish": "publisher"
    }
)

graph.add_edge("publisher", END)

app = graph.compile()

# -------------------------
# RUN WORKFLOW
# -------------------------
result = app.invoke({
    "topic": "Artificial Intelligence and Machine Learning",
    "status": "draft",
    "content": "",
    "messages": []
})

print("\n==============================", flush=True)
print("📌 FINAL STATUS:", result["status"], flush=True)
print("==============================", flush=True)

print("\n🧵 AGENT TIMELINE:", flush=True)
for m in result["messages"]:
    print("•", m, flush=True)

print("\n📄 FINAL OUTPUT:\n", flush=True)
print(result["content"], flush=True)
