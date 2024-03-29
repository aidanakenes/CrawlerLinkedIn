FROM python:3.8
WORKDIR /usr/src
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY ./src ./src
EXPOSE 8080
