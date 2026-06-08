from langchain_core.messages import SystemMessage

from config import llm

from tools.email_tools import draft_email, show_email_drafts, delete_email_draft, delete_all_email_drafts, send_email, send_pending_email

email_llm = llm.bind_tools(
    [
        draft_email,
        show_email_drafts,
        delete_email_draft,
        delete_all_email_drafts,
        send_email,
        send_pending_email
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
          - Create an email draft.

       2. send_pending_email
          - Send the most recently drafted email.

       3. show_email_drafts
          - Show saved drafts.

       4. delete_email_draft
          - Delete one draft.

       5. delete_all_email_drafts
          - Delete all drafts.

       Rules:

       - You ARE capable of sending emails.
       - Never claim that you cannot send emails.
       - When a user says:
         - send it
         - send this email
         - send this mail
         - yes send it
         - approve
         then use send_pending_email.

       - After an email is drafted, ask for confirmation.

       - Once the user confirms, send the pending email.
       """
        )
    ] + state["messages"]

    response = email_llm.invoke(
        messages
    )

    return {
        "messages": [response]
    }