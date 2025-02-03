FROM python:3.12

# Install manually all the missing libraries
RUN apt-get update
RUN apt-get install -y libcairo2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libnss3

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install


ENV APP_HOME=/app
WORKDIR $APP_HOME
COPY . ./

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
