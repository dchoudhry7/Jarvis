def supervisor(state):
    user_message = state["messages"][-1].content.lower()
    route = None
    if any(word in user_message for word in ["todo", "task", "add task", "show task"]):
        route = "todo"
    elif any(word in user_message for word in ["remember", "memory", "recall"]):
        route = "memory"
    elif any(word in user_message for word in ["email", "mail", "draft"]):
        route = "email"
    elif any(word in user_message for word in ["calendar", "meeting", "schedule", "event"]):
        route = "calendar"
    elif any(word in user_message for word in ["playlist", "song", "music", "spotify"]):
        route = "spotify"

    if route is None:
        confirmations = ["yes", "go ahead", "send it", "approve", "do it", "confirm", "yep", "sure", "ok", "okay"]
        if any(c == user_message.strip().lower() or user_message.startswith(c) for c in confirmations):
            for msg in reversed(state["messages"][:-1]):
                if msg.type == "ai":
                    content = msg.content.lower()
                    if "calendar" in content or "📅" in content or "schedule" in content:
                        route = "calendar"
                        break
                    elif "email" in content or "draft" in content or "pending email" in content:
                        route = "email"
                        break
                    elif "playlist" in content or "spotify" in content:
                        route = "spotify"
                        break
                    elif "todo" in content or "task" in content:
                        route = "todo"
                        break

    if route is None:
        route = "chat"

    return {
        "route": route
    }


def route_agent(state):
    return state["route"]
