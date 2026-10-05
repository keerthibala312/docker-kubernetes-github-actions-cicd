from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.get("/")
def home():
    return jsonify(
        message="Hello from Docker + Kubernetes + GitHub Actions",
        environment=os.getenv("APP_ENV", "local"),
        version=os.getenv("APP_VERSION", "dev")
    )

@app.get("/health")
def health():
    return jsonify(status="UP")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
