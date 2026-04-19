from ollama import Client

# Windows側のOllamaサーバーを指定
# 'localhost' だとWSL自身の環境を指してしまうため、host.docker.internal等を使います
client = Client(host='http://192.168.11.7:11434')

response = client.chat(
    model='gemma4:e4b',
    messages=[
        {'role': 'user', 'content': 'WSLからこんにちは！'}
    ],
)

print(response.message.content)