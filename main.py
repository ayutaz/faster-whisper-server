from fastapi import FastAPI, File
from faster_whisper import WhisperModel
import torch
import os

app = FastAPI()

def initialize_model():
    if torch.cuda.is_available():
        print("CUDA is available")
        return WhisperModel("large-v3", device="cuda", compute_type="float16")
    else:
        print("CUDA is not available or not enabled")
        cpu_threads = os.cpu_count()
        return WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=cpu_threads)

model = initialize_model()

@app.post("/transcribe")
async def transcribe_audio(file: bytes = File(...)):
    try:
        # 音声ファイルの文字起こし
        segments, info = model.transcribe(
            file,  # ここでバイナリデータを渡す
            beam_size=5,
            vad_filter=True,
            without_timestamps=True,
        )

        # 結果のフォーマット
        result = "Detected language '%s' with probability %f\n" % (info.language, info.language_probability)
        for segment in segments:
            result += "[%.2fs -> %.2fs] %s\n" % (segment.start, segment.end, segment.text)

        return {"transcription": result}
    except Exception as e:
        return {"error": str(e)}
