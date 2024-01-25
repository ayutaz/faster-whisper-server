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
