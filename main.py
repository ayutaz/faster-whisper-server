from fastapi import FastAPI
from faster_whisper import WhisperModel
import os

app = FastAPI()
AUDIO_FILE_PATH = '/path/to/your/audiofile.wav'  # 適切なパスに置き換えてください

# WhisperModelの初期化（サーバー起動時に一度だけ行う）
model = WhisperModel("large-v3", device="cuda", compute_type="float16")

@app.get("/transcribe")
async def transcribe_audio():
    # 音声ファイルの文字起こし
    segments, info = model.transcribe(
        AUDIO_FILE_PATH,
        beam_size=5,
        vad_filter=True,
        without_timestamps=True,
    )

    # 結果のフォーマット
    result = "Detected language '%s' with probability %f\n" % (info.language, info.language_probability)
    for segment in segments:
        result += "[%.2fs -> %.2fs] %s\n" % (segment.start, segment.end, segment.text)

    # ファイルの削除
    os.remove(AUDIO_FILE_PATH)

    return result
