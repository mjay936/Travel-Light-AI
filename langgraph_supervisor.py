from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END
from typing import List, Dict, Any

def create_supervisor(
    model,
    agents: List,
    prompt: str,
    add_handoff_back_messages: bool = True,
    output_mode: str = "full_history"
):
    """
    Create a supervisor that can handoff to multiple agents.
    """
    # Create the supervisor agent
    supervisor = create_react_agent(
        model=model,
        tools=[],
        prompt=prompt,
        name="supervisor"
    )
    
    # Create the graph
    workflow = StateGraph({"messages": []})
    
    # Add nodes for each agent
    workflow.add_node("supervisor", supervisor)
    for agent in agents:
        workflow.add_node(agent.name, agent)
    
    # Add edges from supervisor to each agent
    for agent in agents:
        workflow.add_edge("supervisor", agent.name)
        if add_handoff_back_messages:
            workflow.add_edge(agent.name, "supervisor")
    
    # Set entry point
    workflow.set_entry_point("supervisor")
    
    # Add conditional edges from supervisor
    def should_continue(state):
        messages = state.get("messages", [])
        if not messages:
            return "supervisor"
        
        # Get the last message content safely
        last_message = messages[-1]
        if hasattr(last_message, 'content'):
            content = last_message.content.lower()
        elif isinstance(last_message, dict):
            content = last_message.get("content", "").lower()
        else:
            content = str(last_message).lower()
        
        # Check if any agent should be called
        for agent in agents:
            if agent.name.lower() in content or f"handoff to {agent.name}" in content:
                return agent.name
        
        return END
    
    workflow.add_conditional_edges("supervisor", should_continue)
    
    return workflow
