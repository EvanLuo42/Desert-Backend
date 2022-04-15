FROM ubuntu:20.04
ENV LANG C.UTF-8
WORKDIR /usr/app/
COPY . /usr/app/
# RUN sed -i s@/ports.ubuntu.com/@/mirrors.tuna.tsinghua.edu.cn/@g /etc/apt/sources.list \
RUN apt-get clean \
    && apt-get update -y \
    && apt-get install software-properties-common -y \
    && apt-get install python3-pip -y \
    && apt-get install -y gettext \
    && pip3 install --upgrade setuptools \
    && pip3 install -r ./requirements.txt \
    && python3 manage.py makemigrations player \
    && python3 manage.py makemigrations plot \
    && python3 manage.py makemigrations song \
    && python3 manage.py migrate \
    && python3 manage.py collectstatic \
    && python3 manage.py compilemessages
EXPOSE 8000
CMD ["gunicorn", "desert.wsgi", "-w", "4", "-k", "gevent", "-b", "0.0.0.0:8000"]