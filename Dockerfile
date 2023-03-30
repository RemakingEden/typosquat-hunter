FROM python:3.8-slim-buster
WORKDIR /typosquatHunter
COPY typosquatHunter.py requirements.txt ./
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "typosquatHunter.py"]