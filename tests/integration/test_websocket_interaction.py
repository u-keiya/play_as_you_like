import pytest
import json
import time
from websocket import create_connection
from urllib.parse import urljoin

# --- Test Configuration ---
BASE_URL = "ws://api.playasul.local"

# --- Test Cases ---

def test_hit_judge_interaction():
    """
    /ws/hit-judge エンドポイントとの基本的なインタラクションをテストする。
    クライアントが PlayerInput を送信し、サーバーが HitResult または Warning を返すことを確認する。
    """
    ws_url = urljoin(BASE_URL, "/ws/hit-judge")
    
    player_input = {
        "timestamp": int(time.time() * 1000),
        "lane": 2,
        "action": "hit"
    }

    try:
        ws = create_connection(ws_url, timeout=10)
        
        # 1. PlayerInput を送信
        ws.send(json.dumps(player_input))
        
        # 2. サーバーからの応答を受信
        message_str = ws.recv()
        message = json.loads(message_str)
        
        # 3. 応答が HitResult または Warning の構造を持つことを確認
        # (契約テストほど厳密ではないが、キーの存在で基本的な構造をチェック)
        is_hit_result = "result" in message and "score" in message
        is_warning = "type" in message and "message" in message
        
        assert is_hit_result or is_warning, f"Received message is not a valid HitResult or Warning: {message}"

    except TimeoutError:
        pytest.fail("WebSocket connection timed out. No message received from server.")
    except Exception as e:
        pytest.fail(f"An error occurred during WebSocket interaction: {e}")
    finally:
        if 'ws' in locals() and ws.connected:
            ws.close()

def test_hit_judge_rapid_fire():
    """
    短時間に連続して PlayerInput を送信しても、サーバーが正常に応答を返し続けることをテストする。
    """
    ws_url = urljoin(BASE_URL, "/ws/hit-judge")
    
    try:
        ws = create_connection(ws_url, timeout=10)
        
        for i in range(10):
            player_input = {
                "timestamp": int(time.time() * 1000) + i * 10,
                "lane": i % 4,
                "action": "hit"
            }
            ws.send(json.dumps(player_input))
        
        # 10回分の応答を受信する
        for _ in range(10):
            message_str = ws.recv()
            message = json.loads(message_str)
            is_hit_result = "result" in message and "score" in message
            is_warning = "type" in message and "message" in message
            assert is_hit_result or is_warning, f"Received message is not a valid HitResult or Warning: {message}"

    except TimeoutError:
        pytest.fail("WebSocket connection timed out during rapid fire test.")
    except Exception as e:
        pytest.fail(f"An error occurred during rapid fire test: {e}")
    finally:
        if 'ws' in locals() and ws.connected:
            ws.close()

def test_hit_judge_invalid_json():
    """
    不正な形式のJSONを送信した際に、サーバーが適切に処理することをテストする。
    (例: Warningを返す、または接続を閉じる)
    """
    ws_url = urljoin(BASE_URL, "/ws/hit-judge")
    invalid_json_string = "this is not a valid json"

    try:
        ws = create_connection(ws_url, timeout=10)
        ws.send(invalid_json_string)
        
        # サーバーからの応答を待つ
        # 応答は Warning か、あるいは接続が閉じられることを期待
        try:
            message_str = ws.recv()
            message = json.loads(message_str)
            assert message.get("type") == "invalid_input", f"Expected an invalid_input warning, but got: {message}"
        except Exception:
            # サーバーが接続を閉じた場合、recvはエラーを発生させる
            # これも期待される動作の一つ
            assert not ws.connected, "Server should have closed the connection on invalid JSON."

    except Exception as e:
        pytest.fail(f"An error occurred during invalid JSON test: {e}")
    finally:
        if 'ws' in locals() and ws.connected:
            ws.close()