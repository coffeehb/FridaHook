# 说明

## ssl unpinning使用

- 启动Frida-Server
```
adb forward tcp:27042 tcp:27042
adb forward tcp:27043 tcp:27043
adb shell /data/local/tmp/frida-server -D
```
- 配置全局代理到Burp

- 打开APP，开始hook

python frida_attach.py hooks.js com.sankuai.meituan.meituanwaimaibusiness

- 完成HTTPS抓包
