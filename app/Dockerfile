FROM python:3.6.5-alpine
WORKDIR /canvas
ADD . /canvas

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install -r requirements.txt \
    && apk del .build-deps gcc musl-dev

CMD ["python", "server.py"]