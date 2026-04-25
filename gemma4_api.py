from fastapi import FastAPI
import uvicorn
from ollama import Client
import requests

app = FastAPI()

try:
    with open("config.txt", "r", encoding="utf-8") as f:
        # read().strip() で、前後の余計な改行やスペースを取り除きます
        target_url = f.read().strip()
except FileNotFoundError:
    print("config.txtが見つかりません。")
    target_url = "http://localhost:11434" # 見つからない場合のデフォルト

client = Client(host=target_url)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/predict")
def predict(data: dict):
    print("ollama動きました！")
    question = data.get("question", "")
    selected_chunk = data.get("selected_chunk", "")
    print(f"質問: {question}")
    print("---"*3)
    print(f"選択されたチャンク: {selected_chunk}")
    print("---"*3)
    response = client.chat(
        model='gemma4:e4b',
        messages=[
             {"role": "system", "content": "あなたはアシスタントです。参考情報をもとに回答を作成してください。ただし、そのまま参考情報を回答に含めないでください。"},
            {'role': 'user', 'content': f"参考情報: {selected_chunk}"},
            {'role': 'user', 'content': question},    
        ],
    )

    return {"result": "success", "data": response.message.content}

@app.post("/predict_simple")
def predict(data: dict):
    print("ollama動きました！")
    question = data.get("question", "")
    print(f"質問: {question}")
    print("---"*3)
    response = client.chat(
        model='gemma4:e4b',
        messages=[
             {"role": "system", "content": "あなたはアシスタントです。参考情報をもとに回答を作成してください。ただし、そのまま参考情報を回答に含めないでください。"},
            {'role': 'user', 'content': question},    
        ],
    )

    return {"result": "success", "data": response.message.content}


# 2. このブロックを追加
if __name__ == "__main__":
    uvicorn.run("gemma4_api:app", host="127.0.0.1", port=8000, reload=True)