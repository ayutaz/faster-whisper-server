from fastapi import FastAPI, UploadFile, File
from faster_whisper import WhisperModel
import torch
import os

app = FastAPI()

def initialize_model():
    model_path = "/models/whisper-large-v3"
    if torch.cuda.is_available():
        print("CUDA is available")
        return WhisperModel("large-v3", device="cuda", compute_type="float16", download_root=model_path)
    else:
        print("CUDA is not available or not enabled")
        cpu_threads = os.cpu_count()
        return WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=cpu_threads, download_root=model_path)

model = initialize_model()

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        print("file type:", type(file))
        print("file name:", file.filename)
        # UploadFileのfileオブジェクトをそのまま使用
        segments, info = model.transcribe(
            file.file,  # UploadFileのfileオブジェクトを直接渡す
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
