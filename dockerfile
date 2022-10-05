
FROM sanicframework/sanic:3.8-latest

WORKDIR /queryPPSUCClassRoomSpider

COPY . .

RUN apk add --update --no-cache g++ gcc libxslt-dev python3-dev openssl-dev

RUN apk add --no-cache gcc musl-dev libxslt-dev

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 8000

CMD ["python", "server.py"]
