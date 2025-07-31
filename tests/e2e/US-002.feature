# language: ja
@us-002
Feature: US-002 URL から曲情報を取得しプレイ準備できる

  ライトゲーマーは、URLを貼り付けたときにタイトル・長さが表示され、
  正常にプレイ可能かを即確認できる。

  Scenario: 有効なURLでメタデータが表示される
    Given トップページでURL入力フォームが表示されている
    When ユーザが有効なYouTube URL "https://www.youtube.com/watch?v=3bhr4-pV2f4" を入力し「Fetch」を押す
    Then 3秒以内に動画タイトルと再生時間が表示される
    And 「Play」ボタンが有効になる

  Scenario: 無効なURLでエラーメッセージが表示される
    Given トップページでURL入力フォームが表示されている
    When ユーザが無効なURL "this is not a url" を入力し「Fetch」を押す
    Then エラーメッセージ "無効なURLです" が表示される
    And 「Play」ボタンは無効のままである

  Scenario: 対応していないサービスのURLでエラーメッセージが表示される
    Given トップページでURL入力フォームが表示されている
    When ユーザが対応していないURL "https://vimeo.com/12345678" を入力し「Fetch」を押す
    Then エラーメッセージ "対応していないサービスです" が表示される
    And 「Play」ボタンは無効のままである

  Scenario: 10分を超える長尺動画で警告が表示される
    Given トップページでURL入力フォームが表示されている
    When ユーザが10分を超える動画のURLを入力し「Fetch」を押す
    Then 「10分を超える部分は自動的にカットして再生します」という警告が表示される
    And 「Play」ボタンは有効になる