FROM python:3.11
WORKDIR /opt
#COPY . .
#RUN pip install -r requirements.txt
COPY entrypoint.sh /opt/entrypoint.sh
#ENTRYPOINT ["python", "generate.py"]
ENTRYPOINT ["/opt/entrypoint.sh"]

