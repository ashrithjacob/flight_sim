import streamlit as st
import json
from flight_sim import graph
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage

st.title("multi agent collab in flight simulation")
st.write(
    "Agents are: mission commander, flight operator, auto pilot system, systems analyst"
)

title = st.text_input(
    "Task to complete",
    "Begin the mission to deliver the package to the specified coordinates: 37.7749, -122.4194",
)


if st.button("Run", type="primary"):
    events = graph.stream(
        {
            "messages": [
                HumanMessage(
                    content=title,
                )
            ],
        },
        # Maximum number of steps to take in the graph
        {"recursion_limit": 150},
    )

    for i, s in enumerate(events, 1):
        key = list(s.keys())[0]
        if key == "call_tool":
            st.markdown(f"Step{i/2}:\n {s[key]['messages'][0].name}:")
            content = json.loads(s[key]["messages"][0].content)
            description = ""
            for m in content.keys():
                description += f":green[{m}] ->[{content[m]}] &nbsp;&nbsp;&nbsp;"
            st.markdown(description)
