FROM python:3.8-slim

ENV PROJECT_DIR /app
ENV BSREC_DEBUG=0

WORKDIR ${PROJECT_DIR}

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "bs_recommender.py"]
