from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import threading

# Start Prometheus metrics server in a background thread
from prometheus_client import start_http_server
threading.Thread(target=start_http_server, args=(8000,), daemon=True).start()

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-125M")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-125M")

response_time = Gauge('response_time_seconds', 'Time taken to generate response in seconds')

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json.get("prompt", "")
    start = time.time()

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_length=100,
        num_return_sequences=1,
        no_repeat_ngram_size=2
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    end = time.time()

    response_time.set(end - start)
    return jsonify({"response": response})

# Optional: expose /metrics manually if needed (not required with start_http_server)
@app.route("/metrics")
def metrics():
    from flask import Response
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# Only needed if you run `python app.py` directly (not used in gunicorn)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
