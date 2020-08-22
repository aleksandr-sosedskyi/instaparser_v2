FROM python:3.8

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

RUN curl -O https://dl.google.com/go/go1.10.3.linux-amd64.tar.gz 
RUN tar xvf go1.10.3.linux-amd64.tar.gz
RUN chown -R root:root ./go
RUN mv go /usr/local
RUN echo "export PATH=$PATH:/usr/local/go/bin" >> sudo vi /etc/profile
RUN source /etc/profile