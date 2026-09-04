from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

SERVICE_NAME = "Service B"
SERVICE_A_URL = "http://127.0.0.1:8080"


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


@app.route("/call-echo", methods=["GET"])
def call_echo():
    msg = request.args.get("msg", "")

    try:
        response = requests.get(
            f"{SERVICE_A_URL}/echo",
            params={"msg": msg},
            timeout=2
        )

        response.raise_for_status()

        return jsonify({
            "service": SERVICE_NAME,
            "service_a_response": response.json()
        })

    except requests.exceptions.Timeout:
        print("Service B error: Service A request timed out")
        return jsonify({
            "error": "Service A request timed out"
        }), 503

    except requests.exceptions.RequestException as e:
        print(f"Service B error: {e}")
        return jsonify({
            "error": "Service A is unavailable"
        }), 503


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081)