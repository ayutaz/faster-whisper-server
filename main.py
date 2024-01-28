import io
import json
import os

import torch
from fastapi import FastAPI, UploadFile, Form
from faster_whisper import WhisperModel

app = FastAPI()

def initialize_model():
    model_path = "/models/whisper-large-v3"
    if torch.cuda.is_available():
        print("CUDA is available")
        return WhisperModel("large-v3", device="cuda", compute_type="float16", download_root=model_path)
    else:
        print("CUDA is not available or not enabled")
        cpu_threads = os.cpu_count()
        return WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=cpu_threads,
                            download_root=model_path)


model = initialize_model()

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = Form(...)):
    try:
        # ファイルの内容をバイナリデータとして読み込む
        file_content = await file.read()

        # バイナリデータをBinaryIOオブジェクトに変換
        file_stream = io.BytesIO(file_content)

        # 音声ファイルの文字起こし
        segments, info = model.transcribe(
            audio=file_stream,  # BinaryIOオブジェクトを渡す
            beam_size=5,
            language="ja",
            vad_filter=True,
            without_timestamps=True,
        )

        # JSONオブジェクトを構築
        response_json = {
            "language": info.language,
            "language_probability": info.language_probability,
            "translations": []
        }

        total_time = 0.0
        for segment in segments:
            segment_duration = segment.end - segment.start
            total_time += segment_duration

            response_json["translations"].append({
                "start_time": segment.start,
                "end_time": segment.end,
                "duration": segment_duration,
                "text": segment.text
            })

        response_json["total_translation_time"] = total_time

        # JSON形式の文字列に変換
        json_response = json.dumps(response_json, indent=2, ensure_ascii=False)

        # JSON形式の文字列を出力（または返す）
        print(json_response)
        return json_response
    except Exception as e:
        return {"error": str(e)}
