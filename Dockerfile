FROM python:3.10.9-slim
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["gunicorn", "main:create_app()"]
