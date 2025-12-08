from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import webbrowser
import uvicorn
import Developer_GPT

app=FastAPI()
templates = Jinja2Templates(directory="templates")


@app.post("/build_app",response_class=HTMLResponse)
def build_app(request: Request,brief: str = Form(...)):
	print(brief)
	code=Developer_GPT.generate_app(brief)
	title_name=max(Developer_GPT.generate_app_name(brief).split("</think>")[1].split('\n'))
	print("Generated",title_name)
	try:
		code=code.split("```python")[1].split("```")[0]
	finally:
		return templates.TemplateResponse("file2.html", {"request": request, "title": title_name, "code": code})



@app.get("/")
def home():
	html=""
	with open('file.html','r') as file:
		html=file.read()

	return HTMLResponse(content=html)


if __name__ == "__main__":
	webbrowser.open('http://127.0.0.1:8000/')
	uvicorn.run(app, host="127.0.0.1", port=8000)