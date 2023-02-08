FROM python:3.7.3-stretch

COPY requirements.txt /tmp/
RUN python3 -m pip install --upgrade pip && \
    pip3 install -r /tmp/requirements.txt

COPY src .