import json
from pylate import indexes, models, retrieve

# ---<引数>---
input_json_path = "./anthropic_id_to_text.json"
# 検索ワード　or 文
queries = ["最近アンソロピックで注目されているAIモデルの名前は何ですか"]
# ------------

# 対応表を読み込む
with open(input_json_path, "r", encoding="utf-8") as f:
    id_to_text_dict = json.load(f)


# 1. モデルのロード
model = models.ColBERT(
    model_name_or_path="./model_weights",
)
print("モデルがロードされました。")

# 2.クエリで検索用のエンベディング取得
queries_embeddings = model.encode(
    queries,
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

# 6. 検索結果の表示
for i, result in enumerate(results):
    retriever_id = result["id"]
    print(f"検索結果順位 {i+1}位:")
    print(f"Json ID: {retriever_id}")
    print(id_to_text_dict[retriever_id])
    print("-" * 40)
