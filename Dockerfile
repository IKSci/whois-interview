FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Define environment variable
ENV FLASK_APP=crawler.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run crawler.py 
CMD ["flask", "run"]
