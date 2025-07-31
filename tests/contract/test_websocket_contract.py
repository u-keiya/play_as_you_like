import pytest
import json
import jsonschema
from websocket import create_connection
from urllib.parse import urljoin
import yaml

# --- Test Configuration ---
BASE_URL = "ws://api.playasul.local"
OPENAPI_PATH = "docs/03_design/api/openapi.yaml"

@pytest.fixture(scope="module")
def effect_preset_schema():
    """OpenAPIファイルからEffectPresetMessageスキーマをロードする"""
    with open(OPENAPI_PATH, 'r') as f:
        openapi_spec = yaml.safe_load(f)
    schema = openapi_spec["components"]["schemas"]["EffectPresetMessage"]
    
    # $refを解決するために、完全な仕様をリゾルバに渡す
    resolver = jsonschema.RefResolver.from_schema(openapi_spec)
    
    return schema, resolver

@pytest.mark.skip(reason="This test requires a running WebSocket server that pushes messages.")
def test_effect_preset_message_contract(effect_preset_schema):
    """
    /ws/effectPreset から受信したメッセージが
    OpenAPIで定義されたスキーマに準拠していることを検証する。
    """
    schema, resolver = effect_preset_schema
    ws_url = urljoin(BASE_URL, "/ws/effectPreset")
    
    try:
        ws = create_connection(ws_url, timeout=10)
        
        # サーバーからのメッセージを1つ待つ
        message_str = ws.recv()
        message = json.loads(message_str)
        
        # スキーマ検証
        jsonschema.validate(instance=message, schema=schema, resolver=resolver)
        
    except TimeoutError:
        pytest.fail("WebSocket connection timed out. No message received from server.")
    except Exception as e:
        pytest.fail(f"An error occurred: {e}")
    finally:
        if 'ws' in locals() and ws.connected:
            ws.close()
