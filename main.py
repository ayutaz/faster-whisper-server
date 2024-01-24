from fastapi import FastAPI, Query
from faster_whisper import WhisperModel
import torch
import os

app = FastAPI()

def initialize_model():
    if torch.cuda.is_available():
        # CUDAが利用可能な場合、CUDAデバイスを使用
        return WhisperModel("large-v3", device="cuda", compute_type="float16")
    else:
        # CUDAが利用不可の場合、CPUを使用し、利用可能な最大スレッド数を設定
        cpu_threads = os.cpu_count()
        return WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=cpu_threads)

# WhisperModelの初期化（サーバー起動時に一度だけ行う）
model = initialize_model()

@app.get("/transcribe")
async def transcribe_audio(file_path: str = Query(..., description="The path to the audio file")):
    # 音声ファイルの文字起こし
    try:
        segments, info = model.transcribe(
            file_path,
            beam_size=5,
            vad_filter=True,
            without_timestamps=True,
        )
    except Exception as e:
        return {"error": str(e)}

    # 結果のフォーマット
    result = "Detected language '%s' with probability %f\n" % (info.language, info.language_probability)
    for segment in segments:
        result += "[%.2fs -> %.2fs] %s\n" % (segment.start, segment.end, segment.text)

    # ファイルの削除
    # try:
    #     os.remove(file_path)
    # except OSError as e:
    #     # ファイル削除時のエラーハンドリング
    #     return {"error": f"Failed to delete file: {str(e)}"}

    return {"transcription": result}
