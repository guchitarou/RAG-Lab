"""
Gradio を使った VLM（Vision Language Model）チャットアプリ
========================================================
- テキストと画像を入力してモデルと会話できるシンプルな例
- gradio==6.11.0 対応
"""

import os

os.environ["GRADIO_TEMP_DIR"] = "./gradio_tmp"  # カレントディレクトリ内に保存
import gradio as gr
from PIL import Image
import time
from PIL import Image
import requests
import torch

import json
from pylate import indexes, models, retrieve


# WSLのIPアドレス（localhostで繋がらない場合は 172.x.x.x を指定）
BASE_URL = "http://127.0.0.1:8000"


# ---<引数>---
input_json_path = "./anthropic_id_to_text.json"

# 対応表を読み込む
with open(input_json_path, "r", encoding="utf-8") as f:
    id_to_text_dict = json.load(f)

# 1. モデルのロード
model = models.ColBERT(
    model_name_or_path="./model_weights",
)

def initialize_model():
    """ボタンを押したときに呼ばれる関数"""
    global messages
    messages = [{"role": "system", "content": [{"type": "text", "text": system_text}]}]
    print(messages)
    yield "✅ メッセージ履歴初期化できました"


# メッセージの初期化
initialize_model()
# ============================================================
# 【2】推論関数（モデルへの問い合わせ）
# ============================================================


def generate_response(message: str, image: Image.Image | None, history: list) -> str:
    """
    テキストと（任意で）画像を受け取り、モデルの返答を返す関数。

    Args:
        message : ユーザーが入力したテキスト
        image   : アップロードされた画像（なければ None）
        history : これまでの会話履歴 [{"role": "user"/"assistant", "content": ...}, ...]

    Returns:
        str: モデルの返答テキスト
    """

    # --- 実際のモデル呼び出しはここに書く ---
    # （今はダミーの返答を返しています）

    # 2.クエリで検索用のエンベディング取得
    queries_embeddings = model.encode(
        message,
        batch_size=32,
        is_query=True,
        show_progress_bar=True,
    )

    # 3. インデックスのロード
    index = indexes.Voyager(
        index_folder="./my_pylate-index",
        index_name="jacolbert-index",
        override=False,
    )

    # 4. リトリーバーのセットアップ
    retriever = retrieve.ColBERT(index=index)

    # 5. クエリで検索実施
    results = retriever.retrieve(
        queries_embeddings=queries_embeddings,
        k=3
    )[0]


    retriever_id = results[0]["id"]


    results_text = id_to_text_dict[retriever_id]


    payload = {
        "question": message,
        "selected_chunk": results_text
    }
    
    response_post = requests.post(f"{BASE_URL}/predict", json=payload)
    
    if response_post.status_code == 200:
        print("Success!")
        print(f"Response: {response_post.json()}")
    else:
        print(f"Failed: {response_post.status_code}")
        

    #dummy_reply = f"これはダミーの返答です。実際のモデル呼び出しは generate_response() 関数内に実装してください。Message: {results_text} "
    dummy_reply =  response_post.json().get("data", "処理で失敗しました")
    return dummy_reply


# ============================================================
# 【3】チャット処理（Gradio の ChatInterface 向け）
# ============================================================


def chat(
    message: dict,  # {"text": str, "files": [PIL.Image, ...]}
    history: list,  # [{"role": ..., "content": ...}, ...]
):
    """
    Gradio の multimodal ChatInterface から呼ばれるメイン関数。
    """
    text = message.get("text", "")
    files = message.get("files", [])

    # 画像は最初の1枚だけ使用（複数枚対応したい場合はここを変更）
    image = files[0] if files else None

    response = generate_response(text, image, history)
    partial = ""
    for char in response:
        partial += char
        yield partial
        time.sleep(0.01)  # 1文字ごとに 0.01秒 待つ


# ============================================================
# 【4】Gradio UI の定義
# ============================================================
with gr.Blocks() as demo:

    gr.Markdown("# Gemma3n 4b it チャットアプリ")
    gr.Markdown("テキストと画像を送って、モデルと会話できます。")

    # ChatInterface: チャット画面を簡単に作れる Gradio のコンポーネント
    chat_interface = gr.ChatInterface(
        fn=chat,  # チャット処理関数
        multimodal=True,  # 画像の入力を有効にする
        textbox=gr.MultimodalTextbox(  # テキスト＋ファイルの入力欄
            placeholder="メッセージを入力（画像も添付できます）",
            file_types=["image"],  # 画像ファイルのみ受け付ける
            file_count="single",  # 1枚だけ
        ),
        cache_examples=False,
    )

    with gr.Row():
        init_button = gr.Button("🚀 会話の履歴初期化", variant="primary")
        status_box = gr.Textbox(
            label="ステータス",
            value="未初期化",
            interactive=False,  # ユーザーが編集できないようにする
        )

    # ボタンを押したら initialize_model() を呼び出す
    init_button.click(
        fn=initialize_model,
        inputs=None,
        outputs=status_box,
    )


# ============================================================
# 【5】アプリの起動
# ============================================================

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",  # 外部からアクセスする場合（ローカルのみなら "127.0.0.1"）
        server_port=7860,  # ポート番号
        share=False,  # True にすると公開 URL が発行される（Gradio の共有機能）
    )



