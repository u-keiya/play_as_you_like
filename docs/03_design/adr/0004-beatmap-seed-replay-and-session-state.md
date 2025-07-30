# ADR-0004: Beatmap Seedリプレイ保証・Session State統合・曲解析方針

## ステータス
Accepted

## 日付
2025-07-30

## コンテキスト
USDM要件(US-001〜006)と基本設計(C4, ADR)の整合性レビューにより、以下の重要な設計決定が必要となった。

- リプレイ時に同一Beatmapを再現するためのSeed管理
- セッション状態遷移のREST/WS統合
- 曲解析のタイミングとリアルタイム補完の扱い
- 用語統一(Beatmap)
- 基調色適用APIの設計方針

## 決定

### 1. Beatmap Seedリプレイ保証
- `/replay/{id}` APIのレスポンスに `beatmapSeed: string` を追加し、リプレイ時に同一譜面を再現可能とする。
- BeatmapSeedRepository, ReplayServiceを新設し、Seedの永続・取得・再利用を担保する。

### 2. Session State統合API
- セッション状態遷移(pause/resume/end)は `PATCH /sessions/{id}/state` で一元管理し、Bodyで `state: running|paused|ended` を指定。
- 状態変更はRESTで更新、WebSocketで `state-update` イベントをPushする二層モデルとする。

### 3. 曲解析方針
- **MVPでは「プレイ開始前」に全曲解析(≤300秒)を完了し、Beatmap生成・初期FXプリセット決定までを保証する。**
- リアルタイム追跡(再生位置のRMS/Spectrum監視によるFX切替)は将来拡張とし、MVPではFeatureFlagで無効化。
- 曲途中セクション解析(サビ等)は事前解析でセグメント情報を抽出し、必要に応じてgRPCストリームで補完する設計とする。

### 4. 用語統一
- Beatmapを正式用語とし、ScoreSheet等の表記は全てBeatmapへ統一する。

### 5. 基調色適用API
- `/effects/presets/select` の `presetId` に `color-<hex>` 形式を許可し、基調色適用をPreset拡張で実現。専用エンドポイントは設けない。

### 6. エラーカタログ拡充
- `BEATMAP_SEED_NOT_FOUND`, `INVALID_SESSION_STATE` をerror_catalogに追加。

## 影響範囲
- `openapi.yaml` (ReplayDataスキーマ、SessionState統合、PresetId拡張)
- クラス図/シーケンス図 (seed_management, session_state, replay_same_seed, section_fx_switch, color_personalize)
- error_catalog.md

## トレーサビリティ
- #US-003, #US-004, #US-005, #US-006
- #NF-01 パフォーマンス・拡張性

## 代替案
- セッション状態を個別エンドポイントで管理（API肥大化・一貫性低下のため却下）
- 基調色専用API追加（Preset拡張で十分なため却下）
- リアルタイム解析のみでFX切替（事前解析のSLA/UX保証が困難なため却下）
