from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
OLLAMA_MODEL = "tinyllama"  # Đổi model nếu bạn dùng cái khác

@app.route("/chat", methods=["POST"])
def chat():
    messages = request.json.get("messages", [])

    # Gửi request đúng định dạng cho Ollama /api/chat
    response = requests.post("http://localhost:11434/api/chat", json={
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False
    })

    reply = response.json().get("message", {}).get("content", "").strip()
    return jsonify({"response": reply})

if __name__ == "__main__":
    print("✅ Ollama server đang chạy tại http://localhost:4891/chat")
    app.run(port=4891)
