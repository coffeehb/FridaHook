# 在Android手机里使用iptables将指定进程的流量强制转到目的IP上，默认是转到8080端口
# 使用场景： 解决Android手机HW P20 HTTPS无法抓包的问题
# 1、HW手机无法进行Frida HOOK ，设置全局代理后 应用打开出现异常。
# 2、HW 手机刷入了EdXposed 做了SSL Upinning （设置全局代理，大部分应用可以抓HTTPS的）
# 解决：切换到root 后，强制把流量转到Burp代理。这样bypass了应用检测是否设置了系统代理
#!/system/bin/sh


function usage(){
    echo "Usage: `basename $0` [-F] uid ip"
}




if [ $# != 2 -a $# != 1 ]  
then
    usage
    exit 55     
fi 


while getopts "AF" opt; do
  case $opt in
    F)
      echo "delete all redirect rule!" 
      iptables -t nat -F
      exit 0
      ;;
    A)
      echo "redirect all tcp traffic" 
      iptables -t nat -F

      iptables  -t nat -A OUTPUT -p tcp  -j DNAT --to-destination $2:8080
      iptables  -t nat -A POSTROUTING -p tcp  -j MASQUERADE
      exit 0
      ;;
    \?)
      echo "Invalid option: -$OPTARG" 
      exit 0
      ;;
  esac
done



if [ $# == 2  ]  
then

	echo " uid: "$1"    ip: "$2

	iptables -t nat -A OUTPUT -p tcp -m owner --uid-owner $1  -j DNAT --to-destination $2:8080
  iptables -t nat -A POSTROUTING -p tcp -m owner --uid-owner $1 -j MASQUERADE
  exit 0
        
fi 











