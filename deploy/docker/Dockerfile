FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHON=python \
    CFLAGS="-I/usr/include/python3.11 -I/usr/include/python3.11/cpython" \
    PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple \
    PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn

RUN if [ -f /etc/apt/sources.list ]; then \
        sed -i 's|http://deb.debian.org/debian|https://mirrors.aliyun.com/debian|g' /etc/apt/sources.list && \
        sed -i 's|http://deb.debian.org/debian-security|https://mirrors.aliyun.com/debian-security|g' /etc/apt/sources.list; \
    fi && \
    if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
        sed -i 's|http://deb.debian.org/debian|https://mirrors.aliyun.com/debian|g' /etc/apt/sources.list.d/debian.sources && \
        sed -i 's|http://deb.debian.org/debian-security|https://mirrors.aliyun.com/debian-security|g' /etc/apt/sources.list.d/debian.sources; \
    fi && \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential git curl pkg-config swig python3-dev \
    libssl-dev libffi-dev libpcap-dev libxml2-dev libxslt1-dev zlib1g-dev \
    libjpeg-dev libgmp-dev libpq-dev libcap-dev libmagic-dev libuv1-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN python -m pip install --no-cache-dir -U pip setuptools wheel && \
    python -m pip install --no-cache-dir -r requirements.txt

ENV GHOST_UI_HOST=0.0.0.0 \
    GHOST_UI_PORT=8089 \
    GHOST_UI_DATA=/data \
    HOME=/data

EXPOSE 8089

CMD ["python", "-m", "ghost.webui"]
