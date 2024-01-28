# faster-whisper-server

faster-whisper-serverは、FastAPIを利用して構築された、効率的な音声文字起こしサーバーです。このサーバーは、[faster-whisper](https://github.com/SYSTRAN/faster-whisper)モデルを使用して音声ファイルをテキストに変換し、API経由でその結果を提供します。

<!-- TOC -->

* [faster-whisper-server](#faster-whisper-server)
    * [セットアップ（Docker使用）](#セットアップdocker使用)
    * [サーバーの実行](#サーバーの実行)
    * [使用方法](#使用方法)
    * [コントリビューション](#コントリビューション)
    * [ライセンス](#ライセンス)

<!-- TOC -->

## セットアップ（Docker使用）

Dockerを使用してfaster-whisper-serverをセットアップおよび実行するための手順は以下の通りです。

## サーバーの実行

プロジェクトのルートディレクトリで、以下のコマンドを実行してDockerイメージをビルドします：

```bash
docker-compose up --build
```

## 使用方法

サーバーが起動したら、以下のエンドポイントを使用して音声ファイルの文字起こしをリクエストできます：

`GET /transcribe`
このエンドポイントは、指定された音声ファイルの文字起こしを行います。

パラメーター：

* file_path (string): 文字起こしを行う音声ファイルへのパス。
  レスポンス：
* transcription (string): 文字起こし結果。

例(client_sample.py)：

```python
import requests


def send_audio_to_api(file_path, url):
    with open(file_path, 'rb') as f:
        files = {'file': ('audio-test.wav', f, 'audio/wav')}
        response = requests.post(url, files=files)
    return response


api_url = "http://127.0.0.1:8000/transcribe"
wav_file_path = r"audio-test.wav"
response = send_audio_to_api(wav_file_path, api_url)

# レスポンスの確認
if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.text)

```

## コントリビューション

このプロジェクトはオープンソースであり、コントリビューションを歓迎します。バグの報告、機能の提案、プルリクエストなど、あなたの協力をお待ちしています。

## ライセンス

このプロジェクトは[Apache License Version 2.0](https://github.com/ayutaz/faster-whisper-server/blob/main/LICENSE)
の下で公開されています。