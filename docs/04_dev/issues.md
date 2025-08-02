## issues

```
---issue { "title": "feat(frontend): 初回チュートリアル & ヘルプモーダル (US-001)", "body": "## Background\nUSDM: US-001\n\n## Goal\n初回アクセス時にアプリ概要・使い方チュートリアルを表示し、ヘルプモーダルから再表示できるようにする。\n\n## Acceptance Criteria\n- [ ] 初回アクセス時にチュートリアル表示\n- [ ] ヘルプボタンでモーダル再表示\n- [ ] E2E: US-001.feature Pass\n\n## Related Docs\n- docs/02_requirements/usdm/US-001.yaml\n- docs/03_design/diagrams/sequence/tutorial.puml", "labels": ["frontend", "3pt", "US-001"], "depends_on": [] }
```
```
---issue { "title": "test(e2e): US-001 チュートリアル表示シナリオ", "body": "## Background\nUSDM: US-001\n\n## Acceptance Criteria\n- [ ] 初回アクセス時のチュートリアル表示を自動テスト\n- [ ] ヘルプボタン再表示のテスト\n- [ ] CI でパス", "labels": ["test", "e2e", "US-001", "1pt"], "depends_on": ["#1"] }
```
```
---issue { "title": "feat(frontend): URL入力フォームとメタデータ取得 (US-002)", "body": "## Background\nUSDM: US-002\n\n## Goal\nトップページに YouTube URL 入力フォームを実装し、ユーザが入力した URL から動画タイトル・長さを 3 秒以内に表示する。\n\n## Acceptance Criteria\n- [ ] 入力フォームと Fetch ボタンを実装\n- [ ] API /api/metadata?url= へリクエストしタイトル・長さを取得\n- [ ] 成功時: 3 秒以内にメタデータを表示し Play ボタンを有効化\n- [ ] 失敗時: エラーメッセージ表示し Play ボタンは無効\n\n## Related Docs\n- docs/03_design/api/openapi.yaml#/components/schemas/UrlMetadata", "labels": ["frontend", "3pt", "US-002"], "depends_on": [] }
```
```
---issue { "title": "feat(backend): メタデータ取得 API /metadata 実装 (US-002)", "body": "## Background\nUSDM: US-002\n\n## Goal\nYouTube URL からタイトル・長さを取得し返すエンドポイント /api/metadata を実装。\n\n## Acceptance Criteria\n- [ ] Fastify ルート /api/metadata を追加\n- [ ] 入力 URL バリデーション\n- [ ] YouTube oEmbed または Data API v3 でメタデータ取得\n- [ ] 返却 JSON: { title, durationSec } (UrlMetadata)\n- [ ] 3 秒以内にレスポンス (外部 API キャッシュも考慮)\n- [ ] 契約テスト tests/contract/test_api_contract.py::test_metadata がパス", "labels": ["backend", "3pt", "US-002"], "depends_on": [] }
```
```
---issue { "title": "feat(backend): 譜面生成APIルート実装 (US-003)", "body": "## Background\nUSDM: US-003\n\n## Goal\nPOST /sessions エンドポイントで URL とシードを受け取り、譜面生成リクエストを受理する。\n\n## Acceptance Criteria\n- [ ] Fastify ルート POST /sessions を追加\n- [ ] 入力バリデーション\n- [ ] seed 指定なし→新規 randomUint32\n- [ ] 300 秒以内に譜面生成リクエストを受理\n- [ ] 契約テスト追加・パス", "labels": ["backend", "2pt", "US-003"], "depends_on": ["#4"] }
```
```
---issue { "title": "feat(backend): BeatmapGenerator サービス実装 (US-003)", "body": "## Background\nUSDM: US-003\n\n## Goal\nBeatmapGenerator サービスで譜面データ生成ロジックを実装し、単体テストを追加する。\n\n## Acceptance Criteria\n- [ ] BeatmapGenerator サービス実装\n- [ ] 単体テスト追加\n- [ ] 300 秒以内に譜面生成完了", "labels": ["backend", "3pt", "US-003"], "depends_on": ["#5"] }
```
```
---issue { "title": "feat(backend): seed ↔ Redis キャッシュ分離 (US-003)", "body": "## Background\nUSDM: US-003\n\n## Goal\n譜面生成時の seed を Redis へ一時保存し、TTL 15分で管理。\n\n## Acceptance Criteria\n- [ ] Redis への seed 保存/取得\n- [ ] TTL 設定\n- [ ] Integration test 追加\n- [ ] SeedRepository & ReplayService 実装", "labels": ["backend", "2pt", "US-003"], "depends_on": ["#6"] }
```
```
---issue { "title": "feat(audio-svc): proto & サーバ雛形 (US-005)", "body": "## Background\nUSDM: US-005 / ADR-0003\n\n## Goal\ngRPC サービスの proto 定義と Python サーバ雛形を作成。\n\n## Acceptance Criteria\n- [ ] Proto 定義 audio_analysis.proto 追加\n- [ ] サーバ雛形 (Python, grpcio)\n- [ ] CI 上でユニットテスト通過", "labels": ["microservice", "3pt", "US-005"], "depends_on": [] }
```
```
---issue { "title": "feat(audio-svc): BPM/Energy アルゴリズム実装 (US-005)", "body": "## Background\nUSDM: US-005\n\n## Goal\nlibrosa で BPM・エネルギー量を解析し gRPC で返す。\n\n## Acceptance Criteria\n- [ ] BPM/Energy 推定ロジック実装\n- [ ] テスト追加\n- [ ] ドキュメント更新", "labels": ["microservice", "3pt", "US-005"], "depends_on": ["#8"] }
```
```
---issue { "title": "feat(audio-svc): gRPC proto → TypeScript クライアント生成", "body": "## Background\nUSDM: US-005\n\n## Goal\ngRPC proto から TypeScript/JS クライアントを自動生成し、フロントエンドで利用可能にする。\n\n## Acceptance Criteria\n- [ ] gRPC Web クライアント生成\n- [ ] サンプル呼び出しテスト\n- [ ] ドキュメント更新", "labels": ["microservice", "frontend", "2pt", "US-005"], "depends_on": ["#8"] }
```
```
---issue { "title": "feat(frontend): Play開始API呼び出し&シード保存 (US-003)", "body": "## Background\nUSDM: US-003\n\n## Goal\nPlay ボタン押下で /sessions API 呼び出し、seed を保存する。\n\n## Acceptance Criteria\n- [ ] /sessions 呼び出し & seed 保存\n- [ ] ユニットテスト & E2E US-003 Pass", "labels": ["frontend", "2pt", "US-003"], "depends_on": ["#7"] }
```
```
---issue { "title": "feat(frontend): Canvas譜面描画&判定 (US-003)", "body": "## Background\nUSDM: US-003\n\n## Goal\nCanvas / WebGL で譜面ノート描画し、キー入力判定・リザルト画面遷移を実装。\n\n## Acceptance Criteria\n- [ ] Canvas / WebGL で譜面ノート描画\n- [ ] キー入力で判定: hit / miss / late 返却\n- [ ] リザルト画面へスコア伝搬\n- [ ] ユニットテスト & E2E US-003 Pass", "labels": ["frontend", "2pt", "US-003"], "depends_on": ["#11"] }
```
```
---issue { "title": "feat(frontend): Replay 機能 (同一シード) (US-003)", "body": "## Background\nUSDM: US-003 リプレイ同一譜面\n\n## Goal\nリザルト画面の Replay ボタンで前回 seed を再利用し同一譜面でプレイ開始。\n\n## Acceptance Criteria\n- [ ] seed をローカルストレージ or state に保持\n- [ ] Replay で /sessions に seed 指定し譜面取得\n- [ ] E2E シナリオ US-003 連続リプレイ Pass", "labels": ["frontend", "2pt", "US-003"], "depends_on": ["#12"] }
```
```
---issue { "title": "feat(frontend): Pause/Resume/Quit UI 実装 (US-004)", "body": "## Background\nUSDM: US-004\n\n## Goal\nプレイ中にポーズメニュー表示・再開・終了が可能な UI を実装。\n\n## Acceptance Criteria\n- [ ] \"P\" キー押下で Pause メニュー表示 & 再生停止\n- [ ] Resume で 3 秒カウントダウンし再開（音声フェードイン）\n- [ ] Quit でトップページへ遷移\n- [ ] 内部タイマー同期ズレなし\n- [ ] PATCH /sessions/{id}/state API で状態遷移\n- [ ] E2E US-004 Pass\n\n## Related Docs\n- docs/03_design/api/openapi.yaml#/paths/~1sessions~1{id}~1state\n- docs/03_design/diagrams/sequence/pause_resume.puml", "labels": ["frontend", "2pt", "US-004"], "depends_on": ["#13"] }
```
```
---issue { "title": "test(frontend): Pause/Resume/Quit タイマー同期テスト (US-004)", "body": "## Background\nUSDM: US-004\n\n## Goal\nPause/Resume/Quit UI のタイマー同期・状態遷移のテストを実装。\n\n## Acceptance Criteria\n- [ ] Pause/Resume/Quit のタイマー同期テスト\n- [ ] PATCH /sessions/{id}/state API 連携テスト\n- [ ] E2E US-004 Pass", "labels": ["test", "frontend", "1pt", "US-004"], "depends_on": ["#14"] }
```
```
---issue { "title": "feat(backend): セッション状態管理 & Redis TTL (US-004)", "body": "## Background\nUSDM: US-004 / ADR-0004\n\n## Goal\nセッション状態遷移 (pause/resume/end) を PATCH /sessions/{id}/state で一元管理し、Redis TTL 15分で保存。Kafka EventBus で状態変更を publish。\n\n## Acceptance Criteria\n- [ ] PATCH /sessions/{id}/state 実装（running/paused/ended）\n- [ ] Redis でセッション {seed, positionSec, color} 保存 TTL15m\n- [ ] TTL/cron で自動削除\n- [ ] Kafka topic session.state publish\n- [ ] Integration tests pass\n- [ ] Contract test: PATCH /sessions/{id}/state\n- [ ] Kafka Topic 定義 & consumer stub 実装", "labels": ["backend", "infra", "3pt", "US-004"], "depends_on": ["#7"] }
```
```
---issue { "title": "feat(backend): Redis フェイルオーバー実装 (NF-01)", "body": "## Background\nNF-01 可用性要件\n\n## Goal\nRedis 障害時にセカンダリへ自動フェイルオーバーする RetryHandler 実装。\n\n## Acceptance Criteria\n- [ ] RetryHandler 実装\n- [ ] failover.puml シナリオ通りのテスト\n- [ ] Integration test 追加", "labels": ["backend", "infra", "2pt", "NF-01"], "depends_on": ["#15"] }
```
```
---issue { "title": "feat(fx-engine): 基調色選択 UI & 適用 (US-006)", "body": "## Background\nUSDM: US-006\n\n## Goal\nカラーサークル UI で基調色選択し、プレイ画面の背景/UI 主色へ適用。\n\n## Acceptance Criteria\n- [ ] カラーサークルコンポーネント実装 (#FF6699 例)\n- [ ] 選択色を FX Engine に渡す\n- [ ] デフォルト時はサーバ解析推奨色\n- [ ] Replay 時も同色再適用\n- [ ] E2E US-006 Pass", "labels": ["fx-engine", "frontend", "3pt", "US-006"], "depends_on": ["#14"] }
```
```
---issue { "title": "feat(fx-engine): gRPC 受信ハンドラ実装 (US-005)", "body": "## Background\nUSDM: US-005 / ADR-0003\n\n## Goal\nAudioAnalysisSvc から gRPC stream で BPM/Energy データを受信し、プリセット切替ロジックのための受信ハンドラを実装。\n\n## Acceptance Criteria\n- [ ] gRPC Web クライアント生成\n- [ ] Audio-svc データ受信ハンドラ実装\n- [ ] サンプル受信テスト", "labels": ["fx-engine", "frontend", "2pt", "US-005"], "depends_on": ["#10", "#15"] }
```
```
---issue { "title": "feat(fx-engine): プリセット切替ロジック & FPS計測 (US-005)", "body": "## Background\nUSDM: US-005\n\n## Goal\nプリセット切替アルゴリズムを実装し、1秒以内切替・FPS計測を行う。\n\n## Acceptance Criteria\n- [ ] プリセット切替アルゴリズム実装\n- [ ] 1秒以内切替\n- [ ] FPS計測・テスト", "labels": ["fx-engine", "frontend", "2pt", "US-005"], "depends_on": ["#17"] }
```
```
---issue { "title": "feat(fx-engine): プリセット選択ロジック & JSON定義 (US-005)", "body": "## Background\nUSDM: US-005\n\n## Goal\nBPM / エネルギー指標に応じたプリセット選択ロジックとプリセット JSON 定義を実装。\n\n## Acceptance Criteria\n- [ ] バラード / アップテンポ プリセット JSON 定義\n- [ ] 選択ロジック実装\n- [ ] テスト追加", "labels": ["fx-engine", "3pt", "US-005"], "depends_on": ["#10", "#15"] }
```
```
---issue { "title": "feat(fx-engine): 彩度/輝度合成処理 (US-005/006)", "body": "## Background\nUSDM: US-005/006\n\n## Goal\n基調色 (US-006) と合成し彩度/輝度調整を行う。\n\n## Acceptance Criteria\n- [ ] 色合成アルゴリズム実装\n- [ ] E2E テスト", "labels": ["fx-engine", "2pt", "US-005", "US-006"], "depends_on": ["#21"] }
```
```
---issue { "title": "feat(backend): EffectPreset Push WebSocket サーバ実装 (US-005/006)", "body": "## Background\nADR-0005\n\n## Goal\n/ws/effectPreset で EffectPresetMessage を Push するサーバ実装。\n\n## Acceptance Criteria\n- [ ] gRPC -> VisualEffectEngine -> WebSocket のブリッジ実装\n- [ ] Preset params mapping\n- [ ] Contract test pass\n", "labels": ["backend","websocket","3pt","US-005","US-006"], "depends_on": ["#15","#21"] }
```
```
---issue { "title": "test(contract): WebSocket EffectPresetMessage schema validation", "body": "## Background\nADR-0005 / Issue #22\n\n## Acceptance Criteria\n- [ ] /ws/effectPreset Push を fixture で受信し JSON Schema 検証\n", "labels": ["test","contract","1pt","US-005","US-006"], "depends_on": ["#22"] }
```
```
---issue { "title": "feat(schema+docs): EffectPresetMessage JSON Schema & contract-test (US-005/006)", "body": "## Background\nADR-0005 / open_questions_2025-07-31.md\n\n## Goal\nWebSocket /ws/effectPreset で Push される EffectPresetMessage の JSON Schema を定義し、contract test を追加。\n\n## Acceptance Criteria\n- [ ] EffectPresetMessage JSON Schema 実装\n- [ ] contract test 追加\n- [ ] preset parameter table 反映\n- [ ] error_catalog.md 更新\n\n## Related Docs\n- docs/03_design/adr/0005-effect-preset-message-schema.md\n- docs/03_design/open_questions_2025-07-31.md", "labels": ["backend", "test", "2pt", "US-005", "US-006"], "depends_on": ["#10", "#23"] }
```
```
---issue { "title": "test(contract): API コントラクトテスト拡充 (metadata, generate, state, preset-select)", "body": "## Background\nAPI 安定性確保\n\n## Acceptance Criteria\n- [ ] 新テストケース追加 tests/contract/\n - 無効 URL\n - 長尺 URL カット警告\n - seed 指定生成\n - PATCH /sessions/{id}/state\n - /effects/presets/select\n- [ ] CI で実行しパス", "labels": ["test", "2pt"], "depends_on": ["#4", "#5", "#14", "#16"] }
```
```
---issue { "title": "docs: openapi.yaml & ADR-0005 反映 (metadata, generate, error catalog, preset params)", "body": "## Background\n新規エンドポイント追加・設計変更に伴うドキュメント更新\n\n## Acceptance Criteria\n- [ ] /api/metadata /sessions /effects/presets /sessions/{id}/state スキーマ追加\n- [ ] EffectPresetMessage/preset parameter table 反映\n- [ ] エラーカタログ HTTP422, 429, 400, BEATMAP_SEED_NOT_FOUND, INVALID_SESSION_STATE 追加\n- [ ] ADR-0005 反映\n- [ ] 必要なら follow-up Issue 起票", "labels": ["docs", "2pt"], "depends_on": ["#4", "#5"] }
```
```
---issue { "title": "risk: YouTube API クオータ・著作権確認", "body": "## Background\n外部 API 依存リスク\n\n## Goal\n- API キー取得とクオータ計測\n- 著作権ポリシー適合性確認\n- 必要ならキャッシュ/Proxy 方針立案\n", "labels": ["risk", "US-002", "1pt"], "depends_on": [] }
```
```
---issue { "title": "spike: WebAssembly vs gRPC 音声解析速度比較", "body": "## Background\nUS-005 needs real-time analysis. 要件300ms以内応答を満たす構成を検証。\n\n## Tasks\n- [ ] wasm-librosa (emscripten) ビルドしブラウザ実行\n- [ ] 同曲で gRPC audio-svc と処理時間計測 (BPM, RMS)\n- [ ] 50 サンプルで平均/分散取得\n- [ ] 結論: 採用構成 & フォローアップ Issue 提出", "labels": ["spike", "US-005", "1pt"], "depends_on": ["#8"] }
```
```
---issue { "title": "spike: WebGPU 描画性能 & fallback Three.js", "body": "## Background\nFX Engine の描画 API 選定\n\n## Tasks\n- [ ] WebGPU 対応ブラウザ割合調査\n- [ ] 同一シーンを WebGPU と Three.js でベンチ\n- [ ] FPS, CPU/GPU 使用率比較\n- [ ] 結論と Issue 提出", "labels": ["spike", "fx-engine", "1pt"], "depends_on": [] }
```
```
---issue { "title": "ci: integration パイプライン追加", "body": "## Background\n自動テスト拡充\n\n## Acceptance Criteria\n- [ ] GitHub Actions で integration テスト (Redis, gRPC, WebGPU) step 追加\n- [ ] サービス起動スクリプト具体化\n- [ ] README バッジ更新", "labels": ["ci", "infra", "2pt"], "depends_on": ["#14", "#15", "#16"] }
```
```
---issue { "title": "ci: e2e パイプライン追加", "body": "## Background\n自動テスト拡充\n\n## Acceptance Criteria\n- [ ] GitHub Actions で headless browser E2E 実行\n- [ ] E2E テストセットアップ\n- [ ] サービス起動スクリプト具体化", "labels": ["ci", "infra", "2pt"], "depends_on": ["#13", "#14", "#20"] }
```
```
---issue { "title": "feat(backend): WebSocket /ws/hit-judge JSON schema & 集計API (US-004)", "body": "## Background\n設計: sequence/hit_judge_ws.puml\n\n## Goal\nWebSocket /ws/hit-judge でヒット判定結果を JSON schema で送信し、リアルタイム統計 API を実装。\n\n## Acceptance Criteria\n- [ ] /ws/hit-judge 接続実装\n- [ ] hit イベント送信 & 受信 (self echo)\n- [ ] Backend stub handler (no persistence)\n- [ ] JSON schema 定義\n- [ ] 統計 API 実装", "labels": ["backend", "websocket", "3pt", "US-004"], "depends_on": ["#14"] }
```
```
---issue { "title": "feat(frontend): WebSocket /ws/hit-judge 結果リアルタイム送信", "body": "## Background\n将来マルチプレイ用に拡張\n\n## Acceptance Criteria\n- [ ] /ws/hit-judge 接続実装\n- [ ] hit イベント送信 & 受信 (self echo)\n- [ ] 統計 UI 実装", "labels": ["frontend", "websocket", "2pt"], "depends_on": ["#27"] }
```
```
---issue { "title": "test(e2e): US-006 基調色選択シナリオ", "body": "## Background\nUSDM: US-006\n\n## Acceptance Criteria\n- [ ] Play 開始前に色選択のみの E2E シナリオ\n- [ ] CI でパス", "labels": ["test", "e2e", "US-006", "1pt"], "depends_on": ["#16"] }
```
```
---issue { "title": "feat(test): US-005 E2E 動的演出シナリオ追加", "body": "## Background\n動的演出の自動テスト\n\n## Acceptance Criteria\n- [ ] Play 流程で BPM変化→プリセット切替確認\n- [ ] カラーベース演出検証 (#006選択色)\n- [ ] GitHub Actions headless pass", "labels": ["test", "e2e", "US-005", "1pt"], "depends_on": ["#18", "#9"] }
```
```
---issue { "title": "refactor: coding_guidelines.md にフロント/バックエンド例追加", "body": "## Background\n新コンポーネント追加に合わせスタイル例を拡充", "labels": ["docs", "devex", "1pt"], "depends_on": [] }
```

## Summary Table
|#|Issue Title|Label|Est|Depends|
|--|--|--|--|--|
|1|初回チュートリアル&ヘルプ|frontend|3pt|—|
|2|US-001 チュートリアルE2E|test|1pt|#1|
|3|URL入力フォームとメタデータ取得|frontend|3pt|—|
|4|メタデータ取得 API|backend|3pt|—|
|5|譜面生成APIルート実装|backend|2pt|#4|
|6|BeatmapGenerator サービス実装|backend|3pt|#5|
|7|seed ↔ Redis キャッシュ|backend|2pt|#6|
|8|audio-svc proto &雛形|microservice|3pt|—|
|9|audio-svc BPM/Energy|microservice|3pt|#8|
|10|gRPC proto→TSクライアント|microservice,frontend|2pt|#8|
|11|Play開始API呼び出し&シード保存|frontend|2pt|#7|
|12|Canvas譜面描画&判定|frontend|2pt|#11|
|13|Replay機能|frontend|2pt|#12|
|14|Pause/Resume/Quit UI|frontend|2pt|#13|
|15|Pause/Resume/Quit タイマー同期テスト|test,frontend|1pt|#14|
|16|セッション状態管理&Redis|backend,infra|3pt|#7|
|17|Redis フェイルオーバー|backend,infra|2pt|#15|
|18|基調色選択 UI|fx-engine,frontend|3pt|#14|
|19|gRPC受信ハンドラ|fx-engine,frontend|2pt|#10,#15|
|20|プリセット切替ロジック&FPS|fx-engine,frontend|2pt|#17|
|21|プリセット選択ロジック&JSON|fx-engine|3pt|#10,#15|
|22|EffectPreset Push WebSocketサーバ|backend,websocket|3pt|#15,#21|
|23|WebSocket EffectPresetMessage schema validation|test,contract|1pt|#22|
|24|EffectPresetMessage Schema+docs|backend,test|2pt|#10,#23|
|25|API契約テスト拡充|test|2pt|#4,#5,#16,#18|
|26|openapi.yaml&ADR-0005反映|docs|2pt|#4,#5|
|27|YouTube API クオータ確認|risk|1pt|—|
|28|WASM vs gRPC 解析|spike|1pt|#8|
|29|WebGPU 性能|spike,fx-engine|1pt|—|
|30|ci: integrationパイプライン|ci,infra|2pt|#16,#17,#18|
|31|ci: e2eパイプライン|ci,infra|2pt|#13,#14,#20|
|32|WebSocket /ws/hit-judge JSON&集計API|backend,websocket|3pt|#14|
|33|WebSocket /ws/hit-judge送信UI|frontend,websocket|2pt|#32|
|34|US-006 基調色E2E|test,e2e,US-006|1pt|#18|
|35|US-005 E2E 動的演出|test,e2e,US-005|1pt|#20,#9|
|36|coding_guidelines 更新|docs,devex|1pt|—|
