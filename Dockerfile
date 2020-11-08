FROM python:3.8-slim-buster
WORKDIR /project
COPY requirements.txt .
RUN pip3 install --user -r requirements.txt
COPY /etl /project
ENTRYPOINT [ "python" ]