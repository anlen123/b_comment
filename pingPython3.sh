#!/bin/env bash

ps -a | grep 'python3' &>/dev/null

if [ $? -eq 0 ];then
    echo $(date +%F-%H:%M)"-进程存在" >> /root/shell_mark/pinglun/pingPython3.txt
else
    python3 /root/shell_mark/pinglun/youxiang.py
    echo $(date +%F-%H:%M)"-进程不存在" >> /root/shell_mark/pinglun/pingPython3.txt
    sed -ri '15s/^/#\ &/g' /etc/crontab
fi
