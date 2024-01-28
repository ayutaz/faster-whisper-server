# 指定されたNVIDIA CUDAイメージ
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# 環境変数の設定
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev

# 作業ディレクトリの設定
WORKDIR /app

# 必要なPythonライブラリをインストール
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコピー
COPY . /app

# ポートを公開
EXPOSE 8000

# FastAPIサーバーを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
