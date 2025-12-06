from fastapi import FastAPI
from cerebras.cloud.sdk import Cerebras
import webbrowser, os
import uvicorn

app=FastAPI()

client = Cerebras(api_key=str(os.environ.get('CEREBRAS_API_KEY')))

chat_history = [
    {"role": "system", "content": "You are a helpful Programming Assistant, help me with my project."}
    ]


@app.get("/chat")
def get_chat():
	global chat_history
	return {'content':chat_history}

@app.post("/chat")
def post_chat(message:str):
    global chat_history
    chat_history.append({'role':'user','content':message})
    
    reply = client.chat.completions.create(
        model="qwen-3-32b",
        messages=chat_history,
        max_completion_tokens=2048,
    )
    reply = reply.choices[0].message.content.split("</think>")[1][2:]
    

    chat_history.append({"role": "assistant", "content": reply})

    return {'reply':reply}




if __name__ == "__main__":
	webbrowser.open('http://127.0.0.1:8000/docs')
	uvicorn.run(app, host="127.0.0.1", port=8000)