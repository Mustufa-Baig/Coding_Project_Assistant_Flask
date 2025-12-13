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
	title_name=max(Developer_GPT.generate_app_name(brief).split('\n'))
	print("Generated",title_name)
	try:
		code=code.split("```python")[1].split("```")[0]
	finally:
		return templates.TemplateResponse("file2.html", {"request": request, "title": title_name, "code": code})



@app.get("/")
def home():
	html=""
	with open('homepage.html','r') as file:
		html=file.read()

	return HTMLResponse(content=html)

@app.get("/build")
def home():
	html=""
	with open('file.html','r') as file:
		html=file.read()

	return HTMLResponse(content=html)

@app.get("/fix")
def home():
	html=""
	with open('file3.html','r') as file:
		html=file.read()

	return HTMLResponse(content=html)



@app.get("/chat")
def chat_page(request: Request):
    Developer_GPT.chat_history = [
    {"role": "system", "content": Developer_GPT.chat_sp}
    ]

    return templates.TemplateResponse("chat.html",{"request": request})




@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_msg = data.get("message", "")
    reply=Developer_GPT.chat(user_msg)

    if "FINAL BRIEF" in reply:
    	return {"reply":reply.replace("FINAL BRIEF",''),'final':'yes'}
    
    return {"reply": reply,'final':'no'}


@app.post("/debug_code", response_class=HTMLResponse)
def debug_code(
    request: Request,
    problem: str = Form(...),
    sol: str = Form(...),
    code: str = Form(...),
    filename: str = Form(...)
):
    print("Debug request received for:", filename)

    debug_output = Developer_GPT.debug_existing_code(
        problem=problem,
        sol=sol,
        code=code,
        filename=filename
    )

    try:
        debug_output = debug_output.split("```")[1]
    except Exception:
        pass

    print("Fixed:",filename)
    return templates.TemplateResponse("file2.html", {"request": request, "title": "Fixed: "+filename, "code": debug_output})


if __name__ == "__main__":
	webbrowser.open('http://127.0.0.1:8000/')
	uvicorn.run(app, host="127.0.0.1", port=8000)