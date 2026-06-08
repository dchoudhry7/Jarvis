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
        You are an Email Management Agent.

        Available tools:

        1. draft_email
           - Creates and saves a new email draft.
           - Use when the user wants to write, draft, compose, create, or generate an email.

        2. show_email_drafts
           - Shows all saved email drafts.
           - Use when the user wants to view, list, check, or see drafts.

        3. delete_email_draft
           - Deletes one specific draft.
           - Use only when the user clearly specifies which draft to delete.

        4. delete_all_email_drafts
           - Deletes every saved draft.
           - Use only when the user explicitly requests removing all drafts.

        Rules:
        - Never delete drafts unless the user explicitly asks.
        - Never create multiple drafts unless requested.
        - After a tool completes successfully, summarize the result and stop.
        - If required information is missing, ask the user for clarification.
        """
        )
    ] + state["messages"]

    response = email_llm.invoke(
        messages
    )

    return {
        "messages": [response]
    }