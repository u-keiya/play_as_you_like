# Android向け音楽ゲーム「Play as You Like」要件定義書

## 1. 概要
本書は、Android向けモバイル音楽ゲーム「**Play as You Like**」の要件定義書です。本ゲームはリズムゲームと簡易バトルアクションを融合させたもので、プレイヤー自身の楽曲ファイルを使用してプレイできることが最大の特徴です。Unityゲームエンジンを用いて開発し、プレイヤーのタップ操作により画面上のキャラクターが敵と戦う演出を楽しめるよう設計します。以下に、本ゲームの詳細な仕様と要件を示します。

## 2. ゲームシステム仕様

### 2.1 楽曲読み込み機能
- **ユーザー楽曲対応**: プレイヤーは自分のデバイスに保存された好きな楽曲ファイル（例：MP3形式。将来的にWAVやOGGなど主要な音声形式にも対応可能）をゲームに読み込み、その曲に合わせてプレイできます。  
- **楽曲選択UI**: 楽曲読み込みのためにファイル選択またはプレイリスト選択のUIを提供し、ユーザーが直感的に自分の曲を選べるようにします。選択後、ゲームは楽曲データを取得し、ゲーム開始の準備を行います。  
- **読み込み制御**: 楽曲読み込み時にファイルサイズや長さの上限を設定し、極端に長い楽曲や不正なファイルによる問題を防ぎます。読み込みが成功すると、次項のリズム解析とノーツ生成処理へ進みます。

### 2.2 リズム解析とノーツ自動生成
- **自動ノーツ生成**: 読み込んだ楽曲に対してリズム解析（ビート検出や音量・周波数解析）を行い、楽曲のテンポやリズムパターンに同期した**ノーツ**（リズムアイコン）を自動生成します。解析アルゴリズムは楽曲の拍や強弱に基づいてノーツ出現タイミングを決定し、同じ曲であれば毎回同じタイミング・配置でノーツが生成されるようにします（再現性の確保）。  
- **ノーツ属性の付与**: 生成された各ノーツには**ランダムで「攻撃」または「防御」の属性**を付与します。攻撃ノーツか防御ノーツかは一定の確率で振り分けられ、ゲーム開始毎にランダム決定されます。ただし、楽曲の盛り上がりなどに応じて攻撃/防御ノーツの比率を変化させるなど、ゲームバランス調整も検討します。  
- **ノーツデータ構造**: ノーツはタイミング（出現時刻）、位置（左ラインか右ラインか）、属性（攻撃/防御）、判定時間幅（判定猶予）などの情報を持つデータとして扱います。これにより楽曲開始から終了までの譜面（ノートシーケンス）が自動生成されます。

### 2.3 ノーツの種類と動作
- **攻撃ノーツ**: 攻撃属性を持つノーツです。プレイヤーがタイミング良くタップすることで**攻撃アクション**が発動し、敵キャラクターにダメージを与えます。攻撃ノーツを見逃したりミスタップした場合、本来与えられるはずだった敵へのダメージチャンスを失い、逆に敵から反撃を受けたものとみなしてプレイヤーのHPが減少します。  
- **防御ノーツ**: 防御属性を持つノーツです。タイミング良くタップすることで**防御アクション**（ガード）が成功し、敵の攻撃を防いだ演出が行われます。防御ノーツをミスした場合、敵の攻撃を防げなかったとみなしプレイヤーがダメージを受けてHPが減少します。  
- **ノーツの視覚表現**: 攻撃ノーツと防御ノーツは色や形状で視覚的に区別します（例：攻撃ノーツは赤色、防御ノーツは青色など）。画面上ではノーツが流れてくる際に一目で種類が判別できるようデザインします。プレイヤーは種類に関わらずタイミングよくタップする操作自体は同じですが、ノーツ種別によって発生する演出（攻撃モーションか防御モーションか）が異なります。

### 2.4 リズムゲームプレイと戦闘演出
- **キャラクター表示**: プレイヤーキャラクター（自機）と敵キャラクターをゲーム画面内に表示します。例えばプレイヤーキャラは画面左側、敵キャラは画面右側に配置し、両者が向かい合うような演出にします。キャラクターのデザインはファンタジー風の戦士など、本ゲームのバトル＆リズム要素に合致したものとします（初期はプレイヤーキャラ1体のみ実装）。  
- **ノーツ出現とアクション**: 楽曲に合わせ、画面上部からノーツが出現し左右方向へ流れていきます（詳細なUI仕様は後述）。プレイヤーはノーツがそれぞれの判定ラインに重なるタイミングで画面をタップし、ノーツを「処理」します。タップ成功時、該当ノーツの属性に応じて以下のアクション演出が起こります：
  - 攻撃ノーツを成功 = プレイヤーキャラの攻撃アニメーションが再生され、敵キャラにダメージ演出（攻撃エフェクトや敵のリアクション）が発生します。  
  - 防御ノーツを成功 = プレイヤーキャラの防御アニメーション（シールドガード等）が再生され、敵の攻撃を防いだ演出（攻撃エフェクトがはじける等）が発生します。  
- **ミス時の挙動**: プレイヤーがノーツのタイミングに合わせてタップできなかった場合（ノーツを取り逃がす、または判定範囲外のタイミングでタップした場合）、そのノーツは**ミス**となります。ミスが発生するとプレイヤーキャラは攻撃・防御いずれも失敗した状態となり、敵キャラの攻撃がヒットした演出（プレイヤーがダメージを受けるモーション）が行われます。この時、プレイヤーのHPが減少します（後述のHPシステム参照）。  
- **アクションとゲーム進行**: 上記の攻撃/防御アクションは楽曲の進行に合わせて連続的に発生し、楽曲終了までリズムゲームとバトル演出がシームレスに展開されます。1つのノーツが1回の攻防アクションに対応し、楽曲終了時には一連のバトル結果が判定されます。

### 2.5 HPシステムとライフ管理
- **プレイヤーHP**: プレイヤーキャラクターには体力値としての**HP（ヒットポイント）**が設定されます。ゲーム開始時にHP満タン（具体的な最大値はゲームバランスにより決定、例：100）からスタートします。  
- **HP減少条件**: 以下の場合にプレイヤーHPが減少します。
  - ノーツをミスした場合（タイミング良くタップできなかった場合）  
  - 明らかにタイミングと異なる場所/タイミングで画面をタップする**ミスタップ**を行った場合（判定の無いタイミングで無効なタップをした場合もペナルティを与える想定）  
  - ※攻撃ノーツ・防御ノーツどちらのミスであっても、共通してプレイヤーがダメージを受ける扱いとします。  
- **ダメージ計算**: 1回のミスごとに減少するHP量はゲーム難易度や楽曲の長さに応じて調整します（例：EasyではHP-5、HardではHP-10など）。全ノーツ数に対し数回のミスでゲームオーバーになるよう調整し、緊張感を維持します。  
- **ゲームオーバー**: プレイヤーHPが0になった時点でゲームオーバーとなり、楽曲の途中でもプレイ失敗となります。ゲームオーバー時はその場で曲を停止し、敗北演出（プレイヤーキャラが倒れる等）とリザルト表示へ遷移します。  

### 2.6 リズム判定とスコアリング
- **タイミング判定**: ノーツをタップしたタイミングの精度に応じて判定を行い、スコアを加算します。判定のランク例として「**PERFECT**（完璧）」「**GREAT**（良）」「**GOOD**（可）」「**MISS**（不可）」を設け、タイミングが判定枠の中心に近いほど高評価となります。  
- **判定別スコア**: 判定ランクに応じてノーツごとのスコア加点値を設定します（例：PERFECTなら+100点、GREATなら+70点、GOODなら+50点、MISSは0点かつHP減少のみ）。これによりリズム良く正確にタップするほど高得点になります。連続してノーツを成功させた場合は**コンボ数**を表示し、コンボに応じたスコアボーナスや演出強化（例えば攻撃エフェクトが派手になる等）も検討します。  
- **スコア表示**: プレイ中は現在のスコアを画面上部にリアルタイム表示します。各ノーツ判定時に、その判定ランクと得点をポップアップ表示してフィードバックを与えます（例：「PERFECT +100」など）。判定結果に応じて音を鳴らす（成功音/ミス音）など、聴覚的フィードバックも行います。

### 2.7 勝敗条件
- **勝利条件**: 楽曲終了時まで生存し（HPが残っている状態で最後まで演奏し切る）、なおかつ**最終スコアが所定の基準値を上回った場合**、プレイヤーの勝利となります。この時、敵キャラクターは倒される演出（敵が崩れ落ちる・消滅する等）を行い、ゲームクリアとなります。基準値となるスコア閾値は難易度設定や楽曲のノーツ数に応じて決定します。例えば難易度Normalでは「楽曲内全ノーツの80%以上をGOOD以上で取る」程度のスコアを閾値とするなど、プレイヤーの達成度によって勝敗を判定します。  
- **敗北条件**: 以下のいずれかの場合、プレイヤーの敗北（ゲーム失敗）となります。
  - プレイ途中でHPが0になった場合（前述のゲームオーバー）。  
  - 楽曲終了時にHPが残っていても、**最終スコアが基準値に達していない場合**。この場合、敵を倒しきれなかったものと見なし敗北となります（生き残ったが敵は健在という結果）。ゲーム上はクリア失敗扱いとして、リザルト画面で「敗北」やスコア不足を通知します。  
- **リザルト評価**: 楽曲終了後のリザルト画面では、最終スコア、判定ごとの数（PERFECT何回など）、最大コンボ数、クリア成否（勝利 or 敗北）を表示します。勝利の場合は「敵撃破！」などのメッセージと共に演出を行い、敗北の場合は敵が健在な演出や「RETRY」ボタンの表示を行います。

## 3. ユーザーインターフェース (UI)・画面設計

### 3.1 ゲーム画面レイアウト
- **判定ラインとノーツ軌道**: プレイ画面には、画面左右に1本ずつ**判定ライン**（ノーツのターゲット位置）を配置します。左側ラインはプレイヤー側、右側ラインは敵側を表します。ノーツは楽曲の進行に合わせて**横方向（左右方向）にスクロール**し、このライン上に達した時がタップの判定タイミングです。具体的には、**攻撃ノーツは画面左側から右方向へ流れ、右側の判定ラインに到達**します。一方、**防御ノーツは画面右側から左方向へ流れ、左側の判定ラインに到達**します。これにより、攻撃ノーツ＝敵に向かって飛んでいく、防御ノーツ＝敵からプレイヤーに飛んでくる、という演出上の違いを表現します。ノーツは滑らかな横スクロール移動で視認しやすく表示し、判定ライン付近でノーツが十分見えるようカメラ視野やレーン配置を調整します。  
- **キャラクター表示位置**: プレイヤーキャラクターは画面の左側手前に立ち、敵キャラクターは画面右側手前に配置されます（横画面想定）。両者の間が戦闘フィールドとなり、その背景でノーツが流れていく形です。キャラクターの足元付近または各側にHPゲージを配置します（プレイヤーHPゲージはプレイヤーキャラの近く、敵のHPゲージは敵キャラの近くに表示するなど）。ただし敵のHPゲージは実際のヒットポイントではなく、**スコア達成度に応じた演出的なゲージ**とします。プレイヤーがノーツ成功で稼いだスコアに応じて敵HPゲージを減少させ、楽曲終了時にゲージがゼロ（＝必要スコア達成）なら敵撃破、残っていれば敵生存とする視覚効果を提供します。  
- **情報表示**: 画面上部中央に**スコア**、上部左にプレイヤーHP、上部右に目標スコアや敵HPゲージを配置して、現在の進行状況が一目でわかるようにします。判定ライン付近にはタイミングインジケータ（ガイドとなる目印やノーツ接近時のエフェクト）を表示し、プレイヤーがリズムを取りやすいよう工夫します。

### 3.2 操作方法と入力
- **基本操作**: 本ゲームの操作は**タップ操作のみ**で完結します。プレイヤーは画面上の**どこをタップしても**判定可能です。左右それぞれのラインに対応した専用ボタン等は設けず、タイミングさえ合っていればタップ場所は自由とします。これにより直感的でシンプルな操作性を実現します。  
- **同時押し対応**: 楽曲や難易度によっては左右両ラインに同時にノーツが到達する（2つのノーツを同時に処理する）場面もあり得ます。そのため、マルチタッチによる**同時複数タップ入力**に対応します。プレイヤーは複数の指を使って同時に画面をタップでき、同時ノーツにも対処可能です。  
- **禁止操作**: スライド（フリック）操作や長押し（ホールド）操作といったジェスチャーは本ゲームには登場しません。全てのノーツは単発のタップで処理するデザインとし、画面上でスワイプやドラッグを検出した場合は入力を無視します（誤操作防止のため）。また、長押しし続けても特に意味はないため、長押し中は連続タップ扱いにしない等、タップ以外の操作はスコアやゲーム進行に影響を与えないようにします。  
- **UIフィードバック**: プレイヤーがタップした際、反応がわかるようにタップエフェクト（波紋や光る円）を表示します。特にノーツ判定成功の場合は判定ライン上でノーツが消滅し、対応する攻撃/防御のエフェクトが発生します。タップ入力に遅延が無いよう、UnityのInputシステムやフレームレートを最適化し、音ズレや入力遅延のない快適な操作性を目指します。

### 3.3 画面遷移
- **メインメニュー**: アプリ起動後のメニュー画面では、「楽曲選択」「難易度選択」「設定」などの項目を配置します。ユーザーが楽曲を選んでゲームを開始できるフローを明確にします。  
- **ゲームプレイ画面**: 前述のとおり、プレイ中はノーツ流れとバトル演出が行われる画面です。ポーズボタンを配置し、一時停止やリスタートができるようにします（ポーズ中は楽曲とノーツ進行を停止）。  
- **リザルト画面**: 楽曲終了後にスコアや判定結果、勝敗を表示する画面に遷移します。ここではリトライ（同じ曲を再挑戦）、曲選択画面に戻る、などの選択肢を提供します。勝利の場合は「敵撃破！クリアおめでとう」のメッセージ、敗北の場合は「撃破ならず…リトライしますか？」等を表示します。

## 4. 難易度設定
- **難易度レベル**: 本ゲームには段階的な難易度設定を用意します。例えば **Easy（初心者向け）**, **Normal（標準）**, **Hard（上級）** といった複数のレベルを設け、プレイヤーは楽曲選択時に任意の難易度を選べます。  
- **ノーツ密度の調整**: 難易度が高いほど、同じ楽曲でも生成されるノーツの数・頻度が増加します。Easyでは主なビート（4分音符程度）中心のシンプルなノーツ配置にし、Hardでは細かなリズム（8分音符や16分音符）まで検出してノーツに含めるようにします。また、高難易度では同時押しや連打的な配置も発生しやすくします。一方、低難易度ではプレイヤーがリズムに慣れるための余裕を持たせます。  
- **スピードや判定**: 基本的に楽曲の再生速度自体は変えませんが、高難易度ではノーツ移動速度を上昇させるオプションを設けても良いでしょう（譜面の流れる速さを調整して難易度を演出）。判定の厳しさ（判定枠の広さ）は難易度によって調整可能です。Easyでは判定猶予を広めに設定し、Hardではシビアにすることで腕前に応じた挑戦性を提供します。  
- **スコア閾値**: 勝利条件となるスコア基準値は難易度ごとに設定します。一般に高難易度の方がノーツ数が多く最大スコアも高いため、閾値も相対的に高く設定します。ただし達成割合（パーセンテージ）としては一貫性を持たせ、例えば全ノーツ中何％以上成功で勝利といった基準を統一する方針です。これによりプレイヤーは難易度を変えても求められる達成度の感覚を掴みやすくなります。  
- **難易度表示**: 楽曲選択時やゲーム開始前に、現在選択している難易度がプレイヤーに明確に伝わるようUI上に表示します。また、リザルト画面にも選択難易度を記載し、スコアランキング等を難易度別に管理できるようにします。

## 5. キャラクターと演出要素
- **プレイヤーキャラクター**: プレイヤーが操作するキャラクターは初期状態では1体のみ実装します。このキャラクターはゲーム内でプレイヤーの分身として機能し、攻撃・防御のモーションが用意されます。キャラクターデザインやモーションはUnity上でアニメーションさせ、タイミング良くノーツを取ることで気持ちよくアクションが決まるよう調整します。  
- **敵キャラクター**: 対戦相手となる敵キャラクターを用意します。初期バージョンでは汎用的な敵を1種類配置し、楽曲プレイ中ずっと同じ敵と戦う形です（例：モンスターやロボットなどテーマに沿った敵）。敵キャラにも攻撃モーション（プレイヤーが防御ノーツ成功時に再生）や被ダメージモーション（攻撃ノーツ成功時に再生）を用意し、プレイヤーのアクションに反応するよう演出します。敵キャラは楽曲終了まで倒れずに戦い続け、終了時に勝敗に応じて最終リアクション（倒れる、勝ち誇る等）を見せます。  
- **将来的なキャラクター拡張**: 将来的にプレイヤーキャラクターの追加やカスタマイズ要素を拡充する可能性があります。本仕様では1体のみですが、複数キャラから選択できる拡張に備え、キャラクター管理をモジュール化しておきます。新キャラごとに異なる外見や攻撃エフェクトを持たせたり、敵キャラもステージごとに変化させるなどの発展要素に対応できる設計とします。ただしゲームバランス上、どのキャラを選んでもゲームプレイの難易度・判定に影響しないようにし（性能差はつけない方針）、あくまで演出やプレイヤーのモチベーション要素として扱います。  

- **演出とエフェクト**: リズムゲームとしての爽快感を高めるため、演出面にも配慮します。攻撃が成功した際のヒットエフェクト（爆発や斬撃のエフェクト）、防御成功時のガードエフェクト、ミス時のダメージエフェクトなど、状況に応じた視覚効果を実装します。また、曲の盛り上がりに合わせて背景が変化したり、コンボが一定数続くとキャラクターにオーラが出る等、プレイヤーの達成感を演出する仕掛けも検討します。これら演出はゲーム性を妨げない範囲で盛り込み、Unityのパーティクルシステムやアニメーションを活用して実現します。

## 6. 技術要件・開発環境
- **ゲームエンジン**: Unity (ユニティ) を使用して本ゲームを開発します。Unityを選定する理由は、マルチプラットフォーム対応の容易さ、2D及び3D表現の柔軟性、豊富な音声解析プラグインやツールの利用可能性があるためです。プロジェクトは2Dベースで進行しつつ、キャラクターは必要に応じて3Dモデルを利用しても構いません（開発チームのリソースとゲームの方向性による）。  
- **対応プラットフォーム**: Android OS をターゲットとします。できるだけ幅広い端末で動作するよう、AndroidのAPIレベルや対応OSバージョンを決定します（例：Android 8.0 Oreo以上をサポート）。画面解像度は各種スマートフォン／タブレットに対応できるようUIレイアウトを可変に設計します。タッチ操作の検出やマルチタッチ処理はUnityの標準Inputシステムを用います。  
- **音声解析**: Unity上で楽曲ファイル（MP3等）を解析する仕組みを組み込みます。MP3デコードと波形解析にはUnityのAudioClip機能やFFTを用いるか、必要に応じて外部ライブラリ（例：NAudio、OnsetDetectionなど）を利用します。楽曲の読込みから譜面生成までの処理はゲーム開始前に短時間で完了するよう最適化し、大容量ファイルでも数秒程度で譜面生成が行われることを目標とします。  
- **パフォーマンスと最適化**: リアルタイムの音楽再生とノーツ描画、アニメーションがスムーズに動作するよう、60FPS程度での描画を目標とします。オブジェクトプールの利用によるノーツ生成/破棄の効率化、Update処理の軽量化、必要に応じてマルチスレッドでの解析（別スレッドで譜面生成）など、快適なゲームプレイのための最適化を行います。音と入力の同期ズレ（レイテンシ）は特に注意し、Unityの設定調整や端末ごとの補正機能（タイミングキャリブレーションオプション）も提供します。  
- **データ管理**: ユーザーが使用した楽曲に紐づく譜面データ（ノーツシーケンス）は一時的にメモリ上に保持し、都度解析します。必要であれば楽曲ハッシュ値に対する譜面キャッシュを導入し、一度プレイした曲は次回以降すぐ開始できるようにします。スコアや設定データは端末ローカルに保存し、将来的にオンラインランキング等を実装する際に拡張できるよう準備します。  

## 7. セキュリティ・その他考慮事項
- **楽曲ファイルの扱い**: ユーザーが読み込む楽曲ファイルはプライバシーに関わる可能性があるため、アプリ内で外部に流出しないように扱います。譜面生成のために必要な解析以上の処理は行わず、楽曲データ自体をアプリが無断で送信・保存することはありません。  
- **ライセンス**: 本アプリはユーザー所有の楽曲を利用する前提のため、著作権的にはユーザー自身が私的利用する範囲となります。アプリ側では楽曲データを提供しないため、音源ライセンスの問題はありません。ただし、将来的にデフォルト楽曲や共有機能を実装する場合は別途ライセンスに配慮します。  
- **拡張性**: 今後のアップデートで機能追加や調整がしやすいように、コードとアセットのアーキテクチャをモジュール化します。特に譜面生成アルゴリズム部分は差し替えやチューニングが可能なよう設計し、難易度ロジックやキャラクター追加も容易に行える構造にします。Unityを用いることでマルチプラットフォーム展開（iOSへの対応など）も視野に入れ、プロジェクト設定を管理します。  

以上が、Android向け音楽ゲーム「Play as You Like」の要件定義となります。本仕様を基に開発を進め、プレイヤーが自分の好きな音楽で直感的なリズムバトルを楽しめるゲーム体験を提供してください。