FROM python:3.10-slim

WORKDIR /ghost

COPY . /ghost

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    swig \
    python3-setuptools \
    libmagic1 \
    && pip install --no-build-isolation M2Crypto netaddr rsa pycryptodome pyaes tinyec pyelftools hexdump pygments dnslib netifaces requests tornado pefile python-magic tqdm ldap3 defusedxml chardet dateparser psutil impacket

ENV PYTHONPATH=/ghost

CMD ["python3", "ghost/cli/ghostsh.py"]