FROM python:3.9

WORKDIR /app

COPY requirements.txt .

COPY credentials.json /app/credentials.json
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json


RUN pip install --no-cache-dir -r requirements.txt
RUN pip install selenium

COPY . .

CMD [ "python", "main.py" ]
