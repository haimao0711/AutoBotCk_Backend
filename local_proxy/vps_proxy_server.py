"""
VPS API Proxy Server - Chạy trên máy local Windows.
Nhận request từ Django server và forward lên bgapi.vps.com.vn.

Cách chạy:
    pip install flask requests
    python vps_proxy_server.py

Mặc định lắng nghe tại: http://0.0.0.0:9000
"""

from flask import Flask, request, Response
import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)

VPS_BASE_URL = "https://bgapi.vps.com.vn"

# Các header cần forward lên VPS (bỏ header liên quan đến proxy)
HOP_BY_HOP = {
    "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
    "te", "trailers", "transfer-encoding", "upgrade", "host"
}


@app.route("/proxy/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def proxy(path):
    target_url = f"{VPS_BASE_URL}/{path}"
    logger.info("[PROXY] %s %s → %s", request.method, path, target_url)

    # Forward headers từ client, lọc hop-by-hop
    forward_headers = {
        k: v for k, v in request.headers
        if k.lower() not in HOP_BY_HOP
    }

    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=forward_headers,
            json=request.get_json(silent=True),
            data=request.get_data() if request.content_type and "json" not in request.content_type else None,
            params=request.args,
            timeout=30,
            allow_redirects=True,
        )

        logger.info(
            "[PROXY] Response: HTTP=%s, Content-Type=%s",
            resp.status_code,
            resp.headers.get("Content-Type", "")
        )

        # Lọc header response
        excluded = HOP_BY_HOP | {"content-encoding", "content-length"}
        response_headers = {
            k: v for k, v in resp.headers.items()
            if k.lower() not in excluded
        }

        return Response(
            resp.content,
            status=resp.status_code,
            headers=response_headers,
        )

    except requests.RequestException as e:
        logger.error("[PROXY] Lỗi kết nối: %s", e)
        return Response(f"Proxy error: {e}", status=502)


@app.route("/health")
def health():
    return {"status": "ok", "proxy_target": VPS_BASE_URL}


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9000
    logger.info("VPS Proxy Server khởi động tại http://0.0.0.0:%d", port)
    logger.info("Ví dụ: POST http://localhost:%d/proxy/handler/core_check.login", port)
    app.run(host="0.0.0.0", port=port, debug=False)

