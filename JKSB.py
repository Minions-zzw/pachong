#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import os
import time
import threading
from bs4 import BeautifulSoup
from verification import Identification_verification
from verification import ResNet
from verification import ResidualBlock
import json
import re
import cv2#识别验证码模块
import os
import execjs
def download_page(url): 
    headers = {'Connection': 'keep-alive',
        'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    req  = requests.get(url, headers=headers)  # 增加headers, 模拟浏览器
    encode_content = req.text
    if req.encoding == 'ISO-8859-1': #解决中文乱码的终极方法
        encodings = requests.utils.get_encodings_from_content(req.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = req.apparent_encoding

        # encode_content = req.content.decode(encoding, 'replace').encode('utf-8', 'replace')
        encode_content = req.content.decode(encoding, 'replace') #如果设置为replace，则会用?取代非法字符；
        
    return encode_content
def find_werzhi(i):
    return -1 != str(i).find('selected')

import pandas as pd

import pandas as pd
import xlrd

def excel_to_matrix(path): #读取excel的函数
    data = xlrd.open_workbook(path)
    table = data.sheets()[0] 
    nrows = table.nrows
    data_usr_pas = []
    for row in range(nrows):
        data_usr_pas.append(table.row_values(row))
    data_usr_pas.pop(0)
    return data_usr_pas
def shangbao(datas): #签到主流程
    for data in datas:
        url = "https://jksb.v.zzu.edu.cn"
        login_url = 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/login'
        headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        html = download_page(url)
        soup = BeautifulSoup(html,'html.parser')
        frame_url = soup.find('div', id = 'mt_2').find('iframe').get('src') #找到表格的地址
        html = download_page(frame_url)
        soup = BeautifulSoup(html,'html.parser')
        yanzheng = soup.find_all('div', class_ = 'mt_3b')
        m = 0
        if "验证码" == yanzheng[2].get_text(): #有验证码时候的处理
            while(1):

                html = download_page(url)
                script_code = """
                function zzjfun1109a()
                  {
                    var s127=Math.round(Math.random()*10000);
                    src="https://jksb.v.zzu.edu.cn/vls6sss/zzjlogin3d.dll/zzjgetimg?ids="+s127;
                    return src
                  }
                """
                js = execjs.compile(script_code)
                url = js.call('zzjfun1109a')

                soup2 = BeautifulSoup(html,'html.parser')
                #生成验证码网址

                js = execjs.compile(script_code)
                verification_url = js.call('zzjfun1109a')
                #获得验证码网址
                r = requests.get('https://jksb.v.zzu.edu.cn/vls6sss/zzjlogin3d.dll/zzjgetimg?ids=8778', headers=headers)  # 下载图片，之后保存到文件
                with open('H:\Code\shizhan\pachong\data\123.png', 'wb') as f:
                    f.write(r.content)

                img = cv2.imread('H:\Code\shizhan\pachong\data\123.png')
                verification_text = Identification_verification(img)
                os.remove('H:\Code\shizhan\pachong\data\123.png')

                data['ver6'] = verification_text #更改要提交的数据

                headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
                session = requests.Session()
                response = session.post(login_url, data=data, headers=headers)  # 获取此次文本
                response.encoding = response.apparent_encoding #转码
                soup = BeautifulSoup(response.text, 'html.parser') #转换成bf
                a1 = soup.find("title").get_text()
                print("识别验证码：")
                if a1.find("郑州") >= 0 :
                    b1 = soup.find("div", id="bak_0").get_text()
                    if b1.find("验证码") >= 0 :
                        print("验证码错误，尝试重新登录。")
                        m = m+1
                        time.sleep(1)
                        if m > 20:
                            break
                        continue;
                print("验证码识别成功。")
                break;
        else:#无验证码时候的处理
            session = requests.Session()
            response = session.post(login_url, data=data, headers=headers)  # 获取此次文本
            response.encoding = response.apparent_encoding #转码
            soup = BeautifulSoup(response.text, 'html.parser') #转换成bf
        
        str_pat = re.compile(r'"(.*)"') #设置正则表达式搜索用于页面网址
        text_list = str_pat.findall(str(soup.find('script')))#找到所有双引号的内容
        url = max(text_list, key=len, default='') #得到链表中最长的元素，也就是url
        
        if 0 >= url.count('https'):
            print('学号：{}密码错误，跳过此学号'.format(data['uid']))
            continue;
        
        time.sleep(1)
        html = download_page(url) #下载下一个页面
        soup = BeautifulSoup(html,'html.parser')
        frame_url = soup.find('iframe', id = 'zzj_top_6s').get('src') #找到表格的地址
        time.sleep(1)
        html = download_page(frame_url)
        soup = BeautifulSoup(html,'html.parser') 
        con = soup.find('div', id = 'bak_0')
        con_list = con.find_all('input')#找到要提交的几个value参数
        value_list = [i.get('value') for i in con_list]
        tianbao_url = "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb"
        data = {
            'day6' : value_list[0],
            'did': value_list[1],
            'door': value_list[2],
            'men6': value_list[3],
            'ptopid': value_list[4],
            'sid':value_list[5],
        }
        time.sleep(1)
        response = session.post(tianbao_url, data=data, headers=headers)  # 获取此次文本
        response.encoding = response.apparent_encoding #转码
        soup = BeautifulSoup(response.text, 'html.parser') #转换成bf
        input_list = soup.find_all('input')
        weizhi_a = soup.find('select', id='myvs_13a').find_all('option')
        weizhi_b = soup.find('select', id='myvs_13b').find_all('option')
        werzhi_a_selected = list(filter(find_werzhi,weizhi_a))[0].get('value')
        werzhi_b_selected = list(filter(find_werzhi,weizhi_b))[0].get('value')
        if_at_school = '在校'
        data = { #构建要提交的表单
            'myvs_1': '否','myvs_2': '否','myvs_3': '否', 'myvs_4': '否','myvs_5': '否','myvs_6': '否','myvs_7': '否','myvs_8': '否','myvs_9': '否','myvs_10': '否','myvs_11': '否','myvs_12': '否',
            'myvs_13a': werzhi_a_selected,
            'myvs_13b': werzhi_b_selected,
            'myvs_13c': input_list[25].get('value'),
            'myvs_14': input_list[27].get('value'),
            'myvs_14b': input_list[28].get('value'),
            'myvs_30': if_at_school,
            'memo22': input_list[29].get('value'),
            'did': input_list[30].get('value'),
            'door': input_list[31].get('value'),
            'day6': input_list[32].get('value'),
            'men6': input_list[33].get('value'),
            'sheng6': input_list[34].get('value'),
            'shi6': input_list[35].get('value'),
            'fun3': input_list[36].get('value'),
            'jingdu': input_list[37].get('value'),
            'werdu': input_list[38].get('value'),
            'ptopid': input_list[39].get('value'),
            'std': input_list[40].get('value')
        }
        time.sleep(1)
        post_url = 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb'
        response = session.post(tianbao_url, data=data, headers=headers)  # 进行健康签到
        response.encoding = response.apparent_encoding #转码
        soup = BeautifulSoup(response.text, 'html.parser') #转换成bf
        con = soup.find('div', style='width:296px;height:100%;font-size:14px;color:#333;line-height:26px;float:left;').get_text() #提取返回信息
        print(con)
        print("等待3秒......")
        time.sleep(3)
def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)
def main(): #开始签到
    data = excel_to_matrix('H:\Code\shizhan\pachong\data\data.xlsx') #用于读取文件
    datas = []
    for i in range(len(data)):
        data_one = {
            'uid': data[i][1],
            'upw': data[i][2],
            'smbtn': '进入健康状况上报平台',
            'ver6': '',
            'hh28': 540
        }
        datas.append(data_one)
    print("一共:"+str(len(datas))+"名学生需要签到,开始签到")
    create_dir('H:\\Code\\shizhan\\pachong\\test-wenjianjia')
    shangbao(datas)
    os.system("pause")
    time.sleep(5)
    os.system("pause")
if __name__ == '__main__':
    main()

