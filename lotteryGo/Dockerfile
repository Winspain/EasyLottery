# 使用官方 Golang 镜像作为基础镜像
FROM golang:latest

RUN ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo Asia/Shanghai > /etc/timezone

# 将当前目录的文件复制到容器的 /app 目录下
COPY . /app

# 设置工作目录
WORKDIR /app/lotteryGo
RUN go mod download

# 编译 Go 应用
RUN go build -o main .

# 启动应用
CMD ["./main"]