from fastapi import FastAPI
from fastapi import Request
from fastapi import Form

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from langchain_core.messages import HumanMessage

from graph import graph

app = FastAPI()

templates = Jinja2Templates(
    directory="templates"
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/chat", response_class=HTMLResponse)
async def chat(
        request: Request,
        message: str = Form(...)
):
    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=message)
            ]
        },
        config={
            "configurable": {
                "thread_id": "user_1"
            }
        }
    )

    response = result["messages"][-1].content

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "response": response
        }
    )
