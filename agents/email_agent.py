from langchain_core.messages import SystemMessage

from config import llm

from tools.email_tools import draft_email, show_email_drafts, delete_email_draft, delete_all_email_drafts

email_llm = llm.bind_tools(
    [
        draft_email,
        show_email_drafts,
        delete_email_draft,
        delete_all_email_drafts
    ]
)


def email_agent(state):

    print("email_agent called")

    messages = [
        SystemMessage(
            content="""
            You are an Email Agent.

            Draft professional emails.

            Use tools whenever required.
            """
        )
    ] + state["messages"]

    response = email_llm.invoke(
        messages
    )

    return {
        "messages": [response]
    }