# EasyLottery

> 🚀定期通知大乐透中奖情况🚀使用golang重构中🚀

![img.png](img.png)
## Feature

1.
    - [x] 录入自选号码
2.
    - [x] 定期通知消息到钉钉机器人
3.
    - [x] docker部署
4.
    - [x] 镜像上传至dockerhub,提供部署说明
5.
    - [x] 使用golang重构，减少资源消耗

## Install

```
docker pull winspain0/easy_lottery:latest
```

## Usage

```shell
docker run -v /root/lotteryGo/config.ini:/app/lotteryGo/config.ini -itd winspain0/easy_lottery:v2.0.0
```

## Contributing

PRs accepted.

## License

MIT © Winspain

## Gitpod

https://gitpod.io/workspaces
