FROM python:3.12

RUN mkdir /app

RUN apt -y update && apt -y upgrade

RUN apt -y install locales locales-all && locale-gen en_US.UTF-8 ru_RU.UTF-8
ENV LC_ALL=ru_RU.UTF-8 LANG=ru_RU.UTF-8 LANGUAGE=ru_RU:ru

ADD requirements.txt /app/src/

RUN pip install --no-cache-dir -r /app/src/requirements.txt

ADD . /app/src/

WORKDIR /app/src

RUN chmod +x docker/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["sh", "docker/entrypoint.sh"]