FROM hualeel/python3_flask:latest
MAINTAINER lihua

# 环境变量
ENV SERVICE_PORT=6008 \
SERVICE_DIR=app \
PYPI=https://mirrors.aliyun.com/pypi/simple/
RUN python -m pip install --upgrade pip


COPY . /$SERVICE_DIR
WORKDIR /$SERVICE_DIR

RUN pip install -r requirements.txt

EXPOSE $SERVICE_PORT
CMD [ "python", "./main.py" ]