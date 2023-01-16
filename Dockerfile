FROM python:3.11
COPY . /opt/
RUN pip install -r /opt/requirements.txt
ENTRYPOINT ["/opt/entrypoint.sh"]

