def supervisor(state):

    user_message = state["messages"][-1].content.lower()

    if any(word in user_message for word in [
        "todo",
        "task",
        "add task",
        "show task"
    ]):
        route = "todo"

    elif any(word in user_message for word in [
        "remember",
        "memory",
        "recall"
    ]):
        route = "memory"
    elif any(word in user_message for word in [
        "email",
        "mail",
        "draft"
    ]):
        route = "email"
    elif any(word in user_message for word in [
        "calendar",
        "meeting",
        "schedule",
        "event"
    ]):
        route = "calendar"
    else:
        route = "chat"

    return {
        "route": route
    }


def route_agent(state):
    return state["route"]