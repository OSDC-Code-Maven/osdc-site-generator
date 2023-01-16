FROM python:3.11
COPY . .
RUN pip install -r requirements.txt
#ENTRYPOINT ["python", "generate.py"]
ENTRYPOINT ["./entrypoint.sh"]

