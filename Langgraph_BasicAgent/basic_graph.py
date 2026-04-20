from langgraph.graph import StateGraph, START,END
from typing import TypedDict

# Define the state shared across nodes
class ArticleState(TypedDict):
    status: str     #  "draft, review", "published "

# define nodes
   
def draft_node(state: ArticleState):
    print(f"Article status: {state['status']}")
    return {"status": "draft"}

def reviewer_node(state: ArticleState):
    print(f"Article status: {state['status']}")
    return {"status": "review"}

def publisher_node(state: ArticleState):
    print(f"Article status: {state['status']}")
    return {"status": "published"}





# Build Graph
graph = StateGraph(ArticleState)

graph.add_node("draft_node", draft_node)
graph.add_node("reviewer_node", reviewer_node)
graph.add_node("publisher_node", publisher_node)

# Add edges
graph.add_edge(START, "draft_node")
graph.add_edge("draft_node", "reviewer_node")
graph.add_edge("reviewer_node", "publisher_node")
graph.add_edge("publisher_node", END)

# Compile graph
app = graph.compile()

# Run workflow
result = app.invoke({ "status": "draft"})
print("\nFinal State:")
print(result)