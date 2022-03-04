# 自动批量脱壳 V1.0
# By CFHB
# 脚本思路：
# 1、遍历base_path下面有哪些APK
# 2、adb 强制安装APK
# 3、adb 查找刚刚安装的APP的包名
# 4、adb 寻找这个应用的主类并打开（打开应用）
# 5、adb 运行Frida脱壳脚本
# 6、记录脱壳成功的记录，写入文件
# 7、adb 卸载这个应用
# 8、继续 2～7步骤


import time
import os

black_list = ['com.android.mms','com.ted.number']
base_path = "/Users/CFHB/androidapp/"
cmd1 = 'adb install -r -d '
cmd2 = 'adb shell ls /data/data/ -alh | grep 2022-03 | awk \'OFS="\t"{print $8}\''
cmd5 = 'adb shell monkey -c android.intent.category.LAUNCHER -v -v -v  0 | grep %s |awk \'OFS="\t"{print $6}\''
cmd6 = 'adb shell am start -n '
cmd3 = 'python2 main.py'
cmd4 = 'adb shell pm uninstall '

def init_blacklist_app():
    cmd_bl = 'adb shell ls /data/data/ -alh | grep 2021-11 | awk \'OFS="\t"{print $8}\''
    result = os.popen(cmd_bl)
    res = result.read()
    for line in res.splitlines():
        if line not in black_list and len(line) > 5:
            black_list.append(line)

init_blacklist_app()
print(len(black_list) , " 个APP")

def logger_file(pkname):
    with open ("success.txt", 'a+') as wf:
        wf.write(pkname)
        wf.write("\n")

for fileapk in os.listdir(base_path):
    try:
        path = base_path+fileapk

        print("1. 开始安装 " + fileapk)
        os.system(cmd1 + path)
        pkname = ''
        print("2. 寻找包名 " + fileapk)
        result = os.popen(cmd2)
        res = result.read()
        for line in res.splitlines():
            if line not in black_list and len(line) > 5:
                pkname = line
        if pkname =='':
            print("[WARNING] 找到黑名单类: " + fileapk)
            continue
        print ("3. 寻找应用的主类" + pkname)
        result = os.popen(cmd5 % pkname)
        res = result.read()
        for line in res.splitlines():
            MainClass = line
            temp = MainClass.split(".")[-1]
            MainClass = MainClass.replace("."+temp,"/."+temp)

        print ("4. 打开应用的主类 " + MainClass)
        os.system(cmd6 + MainClass)
        time.sleep(8)
        print("5. 运行Frida脱壳")
        os.system(cmd3)
        print("6. 脱壳成功记录文件:%s <==> %s " % (path,pkname))
        logger_file("dumpdex success: %s <==> %s " % (path,pkname))
        # 7. 卸载这个包
        print("7. 开始卸载 --> " + pkname)
        os.system(cmd4 + pkname)
        # break
    except Exception as e:
        print (e)
        # break
