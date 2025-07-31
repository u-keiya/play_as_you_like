# language: ja
@us-001
Feature: US-001 即時リズム体験

  ライトゲーマーは、ブラウザにURLを貼り付けるだけで、
  インストールや複雑な操作なしに、お気に入りのYouTube曲でリズムゲームを体験できる。

  Scenario: URL から即プレイ開始
    Given ブラウザでゲームトップページを開いている
    When ユーザが有効なYouTube動画のURL "https://www.youtube.com/watch?v=dQw4w9WgXcQ" を入力して「Play」を選択する
    Then 300秒以内に譜面生成が完了し、プレイ画面へ遷移する
    And 音楽の再生とノートの表示が開始される

  Scenario: ワンキー操作でヒット判定
    Given プレイ画面で音楽が再生され、ノートが表示されている
    When ユーザが指定されたタイミングでキーを押下する
    Then ノートがヒットし、視覚的なフィードバックが表示される
    And ノートがヒットし、音声フィードバックが再生される

  Scenario: 曲の終了による結果表示
    Given プレイ中である
    When 曲が終了する
    Then スコアと命中率が表示され、セッションが終了する

  Scenario: 任意でのセッション終了による結果表示
    Given プレイ中である
    When ユーザが「Quit」を選択する
    Then スコアと命中率が表示され、セッションが終了する