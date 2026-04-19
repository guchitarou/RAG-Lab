"""
PDF → JaColBERT インデックス構築スクリプト

このスクリプトはPDFファイルを読み込み、JaColBERTで検索できる形に変換・保存します。

出力:
    pylate-index/
    └── jacolbert-index/
        ├── index.voyager
        ├── document_ids_to_embeddings.sqlite
        └── embeddings_to_documents_ids.sqlite

    anthropic_id_to_text.json  ← チャンクIDと元テキストの対応表
    ※ 検索時は pylate-index/ と id_to_text.json の両方が必要です
"""
import json

from pylate import indexes, models, retrieve
import pymupdf4llm
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ---<引数>---
PDF_PATH = "./AboutAnthropic.pdf"
OUTPUT_JSON_PATH = "anthropic_id_to_text.json"
# ------------

md_text = pymupdf4llm.to_markdown(PDF_PATH)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=256,      # トークン数ではなく文字数なので少し多めに
    chunk_overlap=50,    # 前後の文脈を引き継ぐ
    separators=["。", "、", "\n", " ", ""],  # 日本語向け区切り
)

documents_chunks = splitter.split_text(md_text)

# チャンクとIDの対応をJSONで保存
id_to_text = {str(i): chunk for i, chunk in enumerate(documents_chunks)}

with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(id_to_text, f, ensure_ascii=False, indent=2)

print(f"PDFから抽出されたテキストを{len(documents_chunks)}チャンクに分割し、IDと対応付けて保存しました。")

# 1. モデルのロード
model = models.ColBERT(
    model_name_or_path="./model_weights",
)
print("モデルがロードされました。")
documents_embeddings = model.encode(
    documents_chunks,
    batch_size=32,
    is_query=False,
    show_progress_bar=True,
)

# 2. インデックスの初期化
index = indexes.Voyager(
    index_folder="./my_pylate-index",
    index_name="jacolbert-index",
    override=True,
)
documents_ids = [str(i) for i in range(len(documents_chunks))]

index.add_documents(
    documents_ids=documents_ids,
    documents_embeddings=documents_embeddings,
)


print("pylate-index/ に保存されました。")