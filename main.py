from fastapi import FastAPI
import webbrowser
import uvicorn
import Developer_GPT

app=FastAPI()


@app.post("/build_app")
def build_app(brief: str):
    code=Developer_GPT.generate_app(brief)
    return {'code':code}


if __name__ == "__main__":
	webbrowser.open('http://127.0.0.1:8000/docs')
	uvicorn.run(app, host="127.0.0.1", port=8000)