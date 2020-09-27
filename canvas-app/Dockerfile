FROM python:3.6.5-alpine
WORKDIR /canvas
ADD . /canvas

RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["python", "server.py"]