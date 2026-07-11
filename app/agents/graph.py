from langgraph.graph import StateGraph, END,START
from langgraph.checkpoint.memory import MemorySaver
from app.agents.state import AgentState
from app.agents.nodes.planner import planner_node
from app.agents.nodes.retriever import retreiver_node
from app.agents.nodes.responder import generate_state

workflow = StateGraph(AgentState)


# 2. Define the Nodes
workflow.add_node("planner", planner_node)
workflow.add_node("retriever", retreiver_node)
workflow.add_node("responder", generate_state)

def route_planner(state:AgentState):
    route=state['current_query']
    if route == 'no_retrieval' : 
        return  "responder"
    else : 
        return "retriever"

workflow.add_edge(START,"planner")
workflow.add_conditional_edges(
    "planner",
    route_planner,
    {
        "responder":"responder",
        "retriever":"retriever",
    }
)

workflow.add_edge('retriever','responder')
workflow.add_edge('responder',END)

checkpointer = MemorySaver()
rag_agent = workflow.compile(checkpointer=checkpointer)