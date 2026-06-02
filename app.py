from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from langchain_core.messages import HumanMessage

from graph import graph

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/chat")
async def chat(message: str = Form(...)):

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=message)
            ]
        }
    )

    return {
        "response": result["messages"][-1].content
    }