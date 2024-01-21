FROM python:slim
WORKDIR /tmp/telebot
COPY . ./
RUN pip install
CMD ["pip", "install", "-r", "requirements.txt"]