# Client file

import argparse
import json

import websocket


def on_open(ws):
    print("WebSocket connection is open")


def on_message(ws, message):
    print("Received message from server:", message)


def on_close(ws):
    print("WebSocket connection is closed")


if __name__ == "__main__":
    # WebSocket URL
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", type=int, help="Project ID for a given user")
    parser.add_argument("--token", type=str, help="Authorization token")
    parser.add_argument(
        "--hostname", type=str, help="Authorization token", default="43.207.233.238"
    )
    args = parser.parse_args()
    ws_url = f"ws://{args.hostname}:8000/ws/projects/{args.project_id}/"

    headers = {
        "Authorization": f"Bearer {args.token}",
    }

    # Create WebSocket connection
    ws = websocket.WebSocketApp(
        ws_url,
        header=headers,
        on_open=on_open,
        on_message=on_message,
        on_close=on_close,
    )

    # Start WebSocket connection
    ws.run_forever()
