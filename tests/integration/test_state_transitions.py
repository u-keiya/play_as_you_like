import requests
from urllib.parse import urljoin

# --- Test Configuration ---
BASE_URL = "https://api.playasul.local"

# --- Helper Functions ---

def create_session():
    """テスト用のセッションを作成し、sessionIdを返すヘルパー関数"""
    url = urljoin(BASE_URL, "/sessions")
    payload = {
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "colorHex": "#FFFFFF"
    }
    response = requests.post(url, json=payload, verify=False) # ローカルテストのためSSL検証を無効化
    response.raise_for_status()
    return response.json()["sessionId"]

# --- Test Cases ---

def test_valid_state_transitions():
    """
    セッションの正常な状態遷移 (running -> paused -> running -> ended) をテストする。
    """
    session_id = create_session()
    state_url = urljoin(BASE_URL, f"/sessions/{session_id}/state")

    # 1. Pause the session
    pause_payload = {"state": "paused", "pausedAt": 12345}
    response = requests.patch(state_url, json=pause_payload, verify=False)
    assert response.status_code == 204, "Failed to pause session"

    # 2. Resume the session
    resume_payload = {"state": "running"}
    response = requests.patch(state_url, json=resume_payload, verify=False)
    assert response.status_code == 204, "Failed to resume session"

    # 3. End the session
    end_payload = {"state": "ended"}
    response = requests.patch(state_url, json=end_payload, verify=False)
    assert response.status_code == 204, "Failed to end session"


def test_invalid_state_transition_from_ended():
    """
    終了済みのセッションに対して状態変更を試みた際に、エラーが返ることをテストする。
    """
    session_id = create_session()
    state_url = urljoin(BASE_URL, f"/sessions/{session_id}/state")

    # 1. End the session first
    end_payload = {"state": "ended"}
    response = requests.patch(state_url, json=end_payload, verify=False)
    assert response.status_code == 204

    # 2. Try to pause the ended session
    pause_payload = {"state": "paused", "pausedAt": 67890}
    response = requests.patch(state_url, json=pause_payload, verify=False)
    assert response.status_code == 422, "Should not be able to pause an ended session"
    error_data = response.json()
    assert error_data["code"] == "VALIDATION_ERROR"


def test_pause_without_timestamp_fails():
    """
    'paused'状態への遷移時に'pausedAt'タイムスタンプがないとエラーになることをテストする。
    """
    session_id = create_session()
    state_url = urljoin(BASE_URL, f"/sessions/{session_id}/state")

    # Try to pause without pausedAt
    pause_payload = {"state": "paused"}
    response = requests.patch(state_url, json=pause_payload, verify=False)
    assert response.status_code == 422, "Pausing should require a timestamp"
    error_data = response.json()
    assert error_data["code"] == "VALIDATION_ERROR"
