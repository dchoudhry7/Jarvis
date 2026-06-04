def task_router(state):

    tasks = state.get(
        "tasks",
        []
    )

    if tasks:
        return "dispatcher"

    return "__end__"