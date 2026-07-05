from ollama import chat

response = chat(
    model="granite4.1:3b",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.message.content)
