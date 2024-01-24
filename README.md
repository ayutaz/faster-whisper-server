# faster-whisper-server

faster-whisper-serverは、FastAPIを利用して構築された、効率的な音声文字起こしサーバーです。このサーバーは、faster-whisperモデルを使用して音声ファイルをテキストに変換し、API経由でその結果を提供します。

<!-- TOC -->
* [faster-whisper-server](#faster-whisper-server)
  * [セットアップ（Docker使用）](#セットアップdocker使用)
  * [Dockerイメージのビルド:](#dockerイメージのビルド)
  * [使用方法](#使用方法)
  * [コントリビューション](#コントリビューション)
  * [ライセンス](#ライセンス)
<!-- TOC -->

## セットアップ（Docker使用）
Dockerを使用してfaster-whisper-serverをセットアップおよび実行するための手順は以下の通りです。

## Dockerイメージのビルド:
プロジェクトのルートディレクトリで、以下のコマンドを実行してDockerイメージをビルドします：

```bash
docker build -t faster-whisper-server .
```
Dockerコンテナの実行:
ビルドしたイメージからDockerコンテナを起動します。以下のコマンドを実行してください：

```bash
docker run --gpus all -p 8000:8000 faster-whisper-server
```
このコマンドは、コンテナのポート8000をホストのポート8000にバインドします。

## 使用方法
サーバーが起動したら、以下のエンドポイントを使用して音声ファイルの文字起こしをリクエストできます：

`GET /transcribe`
このエンドポイントは、指定された音声ファイルの文字起こしを行います。

パラメーター：
* file_path (string): 文字起こしを行う音声ファイルへのパス。
レスポンス：
* transcription (string): 文字起こし結果。

例：
```bash
curl "http://127.0.0.1:8000/transcribe?file_path=your_audio_file_path"
```

## コントリビューション
このプロジェクトはオープンソースであり、コントリビューションを歓迎します。バグの報告、機能の提案、プルリクエストなど、あなたの協力をお待ちしています。

## ライセンス
このプロジェクトは[Apache License Version 2.0]()の下で公開されています。