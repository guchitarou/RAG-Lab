import requests
from typing import Any, List, Mapping, Optional

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
import pymupdf4llm
from langchain_core.language_models.llms import LLM

BASE_URL = "http://127.0.0.1:8000"

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



#EMBEDDING_MODEL_PATH = "./embedding_models/MiniLM_L6_v2_weights"
#EMBEDDING_MODEL_PATH = "./embedding_models/multilingual_e5_base_weights"
EMBEDDING_MODEL_PATH = "./embedding_models/GLuCoSE_base_ja_v2_weights"

# -------------------
# ① ドキュメント準備
# -------------------
PDF_PATH = "./AboutAnthropic.pdf"

pdf_text = pymupdf4llm.to_markdown(PDF_PATH)

docs = [Document(page_content=pdf_text)]

# -------------------
# ② テキストを分割
# -------------------
splitter = CharacterTextSplitter(chunk_size=50, chunk_overlap=0)
chunks = splitter.split_documents(docs)

# -------------------
# ③ ベクトル化して保存
# -------------------

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL_PATH
)


db = FAISS.from_documents(chunks, embeddings)

# -------------------
# ④ 検索
# -------------------
query = "Anthropicってどんな会社？"
results = db.similarity_search(query, k=3)


print("検索ランキング")
context = "\n--------\n".join([r.page_content for r in results])
print(context)


# -------------------
# ⑤ LLMに渡す
# -------------------
llm = MyCustomModel()


prompt = f"""
以下の情報を使って答えてください：

{context}

質問: {query}
"""

answer = llm.invoke(prompt)


print("回答")
print(answer)
print("---"*9)

