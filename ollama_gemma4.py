from ollama import Client

# Windows側のOllamaサーバーを指定
# 'localhost' だとWSL自身の環境を指してしまうため、host.docker.internal等を使います
client = Client(host='http://192.168.11.7:11434')

response = client.chat(
    model='gemma4:e4b',
    messages=[
        {'role': 'user', 'content': 'MYPP114514からこんにちは！'},
        {'role': 'user', 'content': '参考情報MYPP114514はWSLのことです。'}
    ],
)

print(response.message.content)