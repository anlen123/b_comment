#!/bin/env bash

if ! command -v qrencode&>/dev/null ;then
    yum install qrencode -y
fi  

if ! command -v curl&>/dev/null ;then
    yum install curl -y
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

