import pytest
import json
import jsonschema
from websocket import create_connection
from urllib.parse import urljoin
import yaml
import time

# --- Test Configuration ---
BASE_URL = "ws://api.playasul.local"
OPENAPI_PATH = "docs/03_design/api/openapi.yaml"

# --- Fixtures ---

@pytest.fixture(scope="module")
def openapi_spec():
    """OpenAPIファイルをロードして返す"""
    with open(OPENAPI_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="module")
def schema_resolver(openapi_spec):
    """$refを解決するためのリゾルバを提供する"""
    return jsonschema.RefResolver.from_schema(openapi_spec)

@pytest.fixture(scope="module")
def effect_preset_schema(openapi_spec):
    """EffectPresetMessageスキーマを返す"""
    return openapi_spec["components"]["schemas"]["EffectPresetMessage"]

@pytest.fixture(scope="module")
def hit_judge_schemas(openapi_spec):
    """Hit Judge関連のスキーマを返す"""
    schemas = openapi_spec["components"]["schemas"]
    return {
        "PlayerInput": schemas["PlayerInput"],
        "HitResult": schemas["HitResult"],
        "Warning": schemas["Warning"],
    }

# --- Test Cases ---

def test_effect_preset_message_contract(openapi_spec, effect_preset_schema, schema_resolver):
    """
    /ws/effectPreset から受信したメッセージが
    OpenAPIで定義されたスキーマ(discriminatorを含む)に準拠していることを検証する。
    """
    ws_url = urljoin(BASE_URL, "/ws/effectPreset")

    try:
        ws = create_connection(ws_url, timeout=10)

        message_str = ws.recv()
        message = json.loads(message_str)

        # 1. discriminator を使って、どの oneOf スキーマか特定する
        preset_id = message.get("presetId")
        assert preset_id is not None, "Message must contain 'presetId'"

        mapping = effect_preset_schema.get("discriminator", {}).get("mapping", {})
        schema_ref = mapping.get(preset_id)
        assert schema_ref is not None, f"No schema mapping found for presetId: {preset_id}"

        # 2. $ref から具体的なスキーマを取得
        # schema_ref は '#/components/schemas/EffectPresetMessage/oneOf/0' のような形式
        with schema_resolver.resolving(schema_ref) as specific_schema:
            # 3. 特定したスキーマでバリデーション実行
            jsonschema.validate(instance=message, schema=specific_schema, resolver=schema_resolver)

    except TimeoutError:
        pytest.fail("WebSocket connection timed out. No message received from server.")
    except Exception as e:
        pytest.fail(f"An error occurred: {e}")
    finally:
        if 'ws' in locals() and ws.connected:
            ws.close()

def test_hit_judge_message_contract(hit_judge_schemas, schema_resolver):
    """
    /ws/hit-judge との送受信メッセージが
    OpenAPIで定義されたスキーマに準拠していることを検証する。
    """
    ws_url = urljoin(BASE_URL, "/ws/hit-judge")
    
    # テスト用の入力データ
    player_input = {
        "timestamp": int(time.time() * 1000),
        "lane": 1,
        "action": "hit"
    }
    
    try:
        ws = create_connection(ws_url, timeout=10)
        
        # 1. PlayerInputの送信メッセージを検証
        jsonschema.validate(instance=player_input, schema=hit_judge_schemas["PlayerInput"], resolver=schema_resolver)
        ws.send(json.dumps(player_input))
        
        # 2. HitResult/Warningの受信メッセージを検証
        message_str = ws.recv()
        message = json.loads(message_str)
        
        # 受信メッセージがHitResultかWarningのどちらかのスキーマに合致するか検証
        try:
            jsonschema.validate(instance=message, schema=hit_judge_schemas["HitResult"], resolver=schema_resolver)
        except jsonschema.ValidationError:
            try:
                jsonschema.validate(instance=message, schema=hit_judge_schemas["Warning"], resolver=schema_resolver)
            except jsonschema.ValidationError as e:
                pytest.fail(f"Received message does not match HitResult or Warning schema: {e}")

    except TimeoutError:
        pytest.fail("WebSocket connection timed out. No message received from server.")
    except Exception as e:
        pytest.fail(f"An error occurred: {e}")
    finally:
        if 'ws' in locals() and ws.connected:
            ws.close()
