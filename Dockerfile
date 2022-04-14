FROM ubuntu:20.04
ENV LANG C.UTF-8
WORKDIR /usr/app/
COPY . /usr/app/
RUN sed -i s@/ports.ubuntu.com/@/mirrors.tuna.tsinghua.edu.cn/@g /etc/apt/sources.list \
    && apt-get clean \
    && apt-get update -y \
    && apt-get install software-properties-common -y \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get install redis-server -y \
    && apt-get install python3.9 -y\
    && apt-get install python3-pip -y \
    && apt-get install -y gettext \
    && pip3 install --upgrade setuptools \
    && pip3 install -r ./requirements.txt \
    && python3 manage.py makemigrations player \
    && python3 manage.py makemigrations plot \
    && python3 manage.py makemigrations song \
    && python3 manage.py migrate \
    && python3 manage.py compilemessages \
    && python3 manage.py collectstatic \
    && rm -rf /usr/bin/python3 \
    && ln -s /usr/bin/python3.9 /usr/bin/python3 \
EXPOSE 8000
CMD ["gunicorn", "desert.wsgi", "-w", "4", "-k", "gevent", "-b", "0.0.0.0:8000"]