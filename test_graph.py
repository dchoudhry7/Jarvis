from langchain_core.messages import HumanMessage

from graph import graph


result = graph.invoke(
    {
        "messages": [
            HumanMessage(
                content="""
Remember my name is Dhairya
and add milk to my todo list
"""
            )
        ]
    },
    config={
        "configurable": {
            "thread_id": "test"
        }
    }
)

print(result)