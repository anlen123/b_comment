#!/bin/bash
os_check() { #检查系统
    if [ -e /etc/redhat-release ] ; then
        REDHAT=`cat /etc/redhat-release | cut -d' '  -f1 `
    else
        DEBIAN=`cat /etc/issue | cut -d' '  -f1 `
    fi

    if [ "$REDHAT" == "CentOS" -o "$REDHAT" == "RED" ] ; then 
        P_M=yum
    elif [ "$DEBIAN" == "Ubuntu" -o "$DEBIAN" == "ubuntu" ] ; then 
        P_M=apt-get
    else
        Operating system does not support
        exit 1
    fi
	echo 工具是 "$P_M"
}
os_check
if ! command -v qrencode&>/dev/null ;then
    $P_M install qrencode -y
fi  

if ! command -v curl&>/dev/null ;then
    $P_M install curl -y
fi  

log(){
    echo $(curl -s http://passport.bilibili.com/qrcode/getLoginUrl | grep "url"  |  awk -F\" '{print $12}') >web_url  
    qrencode -o - -t ANSI $(cat web_url)
    while true
    do
        sleep 2
    if [ $(curl -s http://passport.bilibili.com/qrcode/getLoginInfo -d  $(cat web_url | awk -F\? '{print $NF}') -c cook | awk -F\" '{print $3}') == ":false," ];then
        echo -n "NO" 
    else
        echo "YES"
        break
    fi
    done
}
if [ -f cook ];then
    if [ -f web_url ];then
        if [[  $(curl -s http://api.bilibili.com/x/web-interface/nav -b $(cat cook | grep 'SESSDATA' |awk '{printf "%s=%s",$(NF-1),$NF}') | awk -F\" '{print $3}') == ':0,' ]];then
            echo "成功登录"
        else 
            echo "NO"
            log       
        fi
    else
        echo "NO"
        log
    fi
else 
    echo "NO"
    log
fi

