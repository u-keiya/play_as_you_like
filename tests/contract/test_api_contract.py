import schemathesis
from hypothesis import settings

# OpenAPIスキーマファイルをロード
# このパスはプロジェクトのルートディレクトリからの相対パスです
schema = schemathesis.from_path(
    "docs/03_design/api/openapi.yaml",
    base_url="https://api.playasul.local"
)

# CI環境で実行時間を無制限にするための設定
settings.register_profile("ci", deadline=None)
settings.load_profile("ci")

# pytestで実行されるテストクラス
# schemathesisがスキーマからテストケースを自動生成します
@schema.parametrize()
def test_api_contract(case):
    """
    APIエンドポイントがOpenAPIスキーマ定義に準拠していることを検証する。
    """
    # `case.call_and_validate()` は以下の処理を自動的に行います:
    # 1. スキーマに基づいたリクエストデータを生成
    # 2. APIエンドポイントへリクエストを送信
    # 3. 受信したレスポンスのステータスコード、Content-Type、およびボディが
    #    スキーマ定義と一致するかを検証
    case.call_and_validate()