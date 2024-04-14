FROM python:3.12-bookworm

WORKDIR /workspace
COPY requirements.txt .
RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "main.py" ]
