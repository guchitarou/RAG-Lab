import requests
from typing import Any, List, Mapping, Optional
from langchain_core.language_models.llms import LLM
from langchain_core.prompts import ChatPromptTemplate


BASE_URL = "http://127.0.0.1:8000"

SYSTEM_PROMPT = """You are a literary data assistant.


## Capabilities

- `fetch_text_from_url`: loads document text from a URL into the conversation.
Do not guess line counts or positions—ground them in tool results from the saved file."""


class MyCustomModel(LLM):
    # 1. モデルのタイプ名を返す（ログや識別のために使用）
    @property
    def _llm_type(self) -> str:
        return "my_custom_model"

    # 2. 実際の推論処理を書く
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> str:
        # --- ここに自作モデルの推論ロジックを書く ---
        # 例: 自作APIを叩く、ローカルの重みをロードして推論するなど
        response = f"自作モデルが受け取った入力: {prompt}"
        payload = {
            "question": prompt,
        }
    
        response_post = requests.post(f"{BASE_URL}/predict_simple", json=payload)

        if response_post.status_code == 200:
            print("Success!")
        else:
            print(f"Failed: {response_post.status_code}")


        #dummy_reply = f"これはダミーの返答です。実際のモデル呼び出しは generate_response() 関数内に実装してください。Message: {results_text} "
        response_reply =  response_post.json().get("data", "処理で失敗しました")
        return response_reply

# 3. 実際に使う
llm = MyCustomModel()
print(llm.invoke("こんにちは！"))


# プロンプトテンプレート
prompt = ChatPromptTemplate.from_template("次の質問に答えてください: {question}")

# チェーン作成
chain = prompt | llm

# 実行
result = chain.invoke({"question": "LangChainとは何ですか？"})
print(result)


history = [
    {"role": "user", "content": "こんにちは"},
    {"role": "assistant", "content": "こんにちは！"},
    {"role": "user", "content": "私の名前は、アーノルド・シュワルツェネッガーです。"},
    {"role": "assistant", "content": "初めまして、アーノルドさん。今日はどんなご用件でしょうか？"},
]
history.append({"question": "ロシア語でおはようってなんていうの？カタカナで答えて"})

result = chain.invoke(history)
print(result)


history.append({"question": "おいらの名前わかりますか？"})

result = chain.invoke(history)
print(result)


