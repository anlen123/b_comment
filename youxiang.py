def qq_youjian(fajianren,shoujianren,zhuti,txt):
    import smtplib
    from email.mime.text import MIMEText
    msg_from=fajianren                                 #发送方邮箱
    # passwd='eyfdfamsmdsldchg'                                   #填入发送方邮箱的授权码
    passwd='fscarlaxbdsxbgae'                         #填入发送方邮箱的授权码
    msg_to=shoujianren                                       #收件人邮箱

    subject=zhuti                                   #主题
    content=txt #正文
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com",465) #邮件服务器及端口号
        s.login(msg_from, passwd)                               #登录SMTP服务器
        s.sendmail(msg_from, msg_to, msg.as_string())#发邮件 as_string()把MIMEText对象变成str
        print ("发送成功")
    except s.SMTPException:
        print ("发送失败")
    finally:
        s.quit()
        
qq_youjian("1761512493@qq.com","1761512493@qq.com","代码出错了","评论代码出错!赶快去看看吧!!")