from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import webbrowser
import uvicorn
import Developer_GPT
from cerebras.cloud.sdk import Cerebras
import os 

app=FastAPI()
templates = Jinja2Templates(directory="templates")
client = Cerebras(api_key=str(os.environ.get('CEREBRAS_API_KEY')))

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
	with open('homepage.html','r') as file:
		html=file.read()

	return HTMLResponse(content=html)

@app.get("/build")
def home():
	html=""
	with open('file.html','r') as file:
		html=file.read()

	return HTMLResponse(content=html)


chat_sp="""
You are a Software Business Analyst, you've been given a client who has almost no clue of the technical details of their brief,
The client will first give you the brief , and then your job is to clarify all their requirements by talking to the client and asking them questions, bare in mind they have little to no technical knowledge.

Once you've understood their exact requirements and only when the client agrees with you, write the complete software requirements brief (non-technical),
The final brief MUST begin with "FINAL BRIEF", and must ONLY include the brief itself, the client can no longer hear you, as what you've written will instead be given to the project manager.

Make sure to talk with the client , and remember to only come up with the final brief after the client agrees with everything you say, and not before.
Before showing the final brief to the client, show them a sample brief, and proceed further to the final brief ONLY IF they agree with it.

Ask the client ONLY 1 QUESTION AT A TIME, DO NOT state multiple questions or statements at once.
Don't include any formatting , just questions, and don't include anything else.
"""[1:-1]

chat_history = [
    {"role": "system", "content": chat_sp}
]



@app.get("/chat")
def chat_page(request: Request):
    global chat_history
    chat_history = [
    {"role": "system", "content": chat_sp}
    ]

    return templates.TemplateResponse("chat.html",{"request": request})




@app.post("/chat")
async def chat(request: Request):
    global chat_history

    data = await request.json()
    user_msg = data.get("message", "")
    chat_history.append({"role": "user", "content": user_msg})

    completion = client.chat.completions.create(
        model="qwen-3-32b",
        messages=chat_history,
        max_completion_tokens=2048,
    )

    reply = completion.choices[0].message.content.split("</think>")[1][2:]
    #print(reply)

    chat_history.append({"role": "assistant", "content": reply})

    #print('\n\n')
    #print(chat_history)

    if "FINAL BRIEF" in reply:
    	return {"reply":reply.replace("FINAL BRIEF",''),'final':'yes'}
    
    return {"reply": reply,'final':'no'}


if __name__ == "__main__":
	webbrowser.open('http://127.0.0.1:8000/')
	uvicorn.run(app, host="127.0.0.1", port=8000)