## bypass APP检测系统全局代理方法一

### 场景

在Android手机里使用iptables将指定进程的流量强制转到目的IP上，默认是转到8080端口【脚本来自我司大佬】

使用场景： 解决Android手机HW P20 HTTPS无法抓包的问题
- 1、HW手机无法进行Frida HOOK ，设置全局代理后 应用打开出现异常。
- 2、HW 手机刷入了EdXposed 做了SSL Upinning （设置全局代理，大部分应用可以抓HTTPS的）

解决：切换到root 后，强制把流量转到Burp代理。这样bypass了应用检测是否设置了系统代理

### 使用方法：

- 首先找到目标APP 包名: 比如：HW的账号服务SDK的，com.huawei.hwid
adb shell dumpsys activity | grep real

```
➜  ~ adb shell dumpsys activity | grep real
    authority=com.huawei.jos.realname.provider
  realActivity=com.huawei.android.launcher/.unihome.UniHomeLauncher
      realActivity=com.huawei.hwid/com.huawei.hms.jos.api.account.JosSignInActivity
      realActivity=com.youdao.course/.activity.StartJumperActivity
      realActivity=com.huawei.android.launcher/.unihome.UniHomeLauncher
      realActivity=com.topjohnwu.magisk/a.c
```

- 然后通过报名找到进程ID：u0_a103
adb shell ps -A | grep com.huawei.hwid

```
➜  ~ adb shell ps -A | grep com.huawei.hwid
u0_a103       1088  4521 4966304 117780 0                   0 S com.huawei.hwid
u0_a103       2334  4521 4291944  59976 0                   0 S com.huawei.hwid.container1
u0_a103       5886  4521 4297128  71536 0                   0 S com.huawei.hwid.persistent
u0_a103       5949  4521 4480996  73780 0                   0 S com.huawei.hwid.core
➜
```

- 然后上传脚本，使用如下：

```
强制账号应用的流量转到10.222.333.34的8080端口
HWEML:/ # sh /data/local/tmp/redirect.sh u0_a103 10.117.122.34
 uid: u0_a103    ip: 10.222.333.34
 
```
- 清除转发
sh /data/local/tmp/redirect.sh -F


## 遗留问题

- 1、如何安装Edxposed
- 2、如何做到SSL Unpinning

u1s1, 我还没有是实操过。等我体验过后再分享。

