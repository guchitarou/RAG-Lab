from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/predict")
def predict(data: dict):
    # ここに処理を書く
    print(data)
    return {"result": "success", "data": data}


# 2. このブロックを追加
if __name__ == "__main__":
    uvicorn.run("gemma4_api:app", host="127.0.0.1", port=8000, reload=True)