from flask import Flask, request, jsonify
import time

app = Flask(__name__)

SERVICE_NAME = "Service A"


@app.before_request
def start_timer():
    request.start_time = time.perf_counter()


@app.after_request
def log_request(response):
    latency = (time.perf_counter() - request.start_time) * 1000

    print(
        f"service={SERVICE_NAME} "
        f"endpoint={request.path} "
        f"status={response.status_code} "
        f"latency={latency:.2f}ms"
    )

    return response


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "service": SERVICE_NAME,
        "status": "healthy"
    })


@app.route("/echo", methods=["GET"])
def echo():
    msg = request.args.get("msg", "")

    return jsonify({
        "message": msg
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)