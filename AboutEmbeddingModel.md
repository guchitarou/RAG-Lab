# Embeddingsモデル

## 🔠 MiniLM_L6_v2 _weights
軽量・高速な Sentence Embedding モデル。主な特徴は下記です。
* 文章を 384 次元ベクトルに変換する。
* 意味検索・類似度計算・クラスタリングなど幅広い用途で高い精度を発揮する。
* ベースで計算コストが低く、GPU なしでも実用的に動作する。
* 汎用性が高く、英語中心のタスクでバランスの良い性能を持つ
* 日本語は「ある程度は動くが最適ではない」レベル。日本語文でも埋め込みは生成でき、短文の類似度・検索なら実用レベルで使えることが多い。

マルチリンガル用途や軽量性を重視するならアリ、日本語精度を最優先するなら別モデル推奨。
```
hf download sentence-transformers/all-MiniLM-L6-v2 --local-dir ./embedding_models/MiniLM_L6_v2_weights
```

## 🌍intfloat/multilingual-e5-base
多言語対応の高性能 Sentence Embedding モデル。主な特徴は下記です。
* 文章を 768 次元ベクトルに変換する（base モデル、12層）。
* 100言語以上をサポートし、英語以外の言語でも高精度な意味検索・類似度計算が可能。
* “query:” / “passage:” の prefix を付ける独自仕様により、検索タスクで高い性能を発揮する。
* 大規模な多言語テキストペア（約10億）でコントラスト学習され、MTEB でも上位の成績を持つ。
* 日本語でも高精度で、RAG・検索タスクで実用レベル（large は特に日本語タスクで高評価）。
```
hf download intfloat/multilingual-e5-base --local-dir ./embedding_models/multilingual_e5_base_weights
```

## 🗾 pkshatech/GLuCoSE-base-ja-v2
日本語特化のEmbeddingモデル。主な特徴は下記です。
* 文章を 768 次元ベクトルに変換する日本語特化モデル（最大 512 トークン）。 
* 検索タスクに最適化され、MIRACL などで同サイズモデル中トップ級の性能を発揮。 
* query: / passage: の prefix を付ける独自仕様により、検索精度が向上。 
* 大規模モデルの知識を蒸留し、多段階コントラスト学習で高精度化された軽量モデル。 
* CPU でも高速に動作し、RAG・FAQ検索・ナレッジ検索など実運用に向く。 
* 日本語タスクに特化しており、他の多言語モデルと比較しても高い正答率を示す。（実験で 94% の正答率）
```
hf download pkshatech/GLuCoSE-base-ja-v2 --local-dir ./embedding_models/GLuCoSE_base_ja_v2_weights
```