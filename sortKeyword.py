#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/3 13:16
# @Author  : nanganglei
# @File    : teshuzifudiff.pya# -*- coding:utf-8 -*-
from selenium import webdriver
import picture_duibi
import urllib
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from PIL import Image
from urllib import unquote

from selenium.webdriver.chrome.options import Options
#import matplotlib.pyplot as plt;plt.rcdefaults()
#import numpy as np
from testHightDiffV2 import saveComparedImg
import logging
#import xiangsidutest
#import matplotlib



logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("sortKeyword_log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

dcap = dict(DesiredCapabilities.PHANTOMJS)
#dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G36  Safari/601.1")
#dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Linux; Android 6.0.1; vivo X9 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/38.0.0.0 Mobile Safari/537.36 VivoBrowser/5.1.2")
dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1")
#dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X; zh-CN) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/14G60 UCBrowser/11.7.7.1031 Mobile  AliApp(TUnionSDK/0.1.20")
# dcap["phantomjs.page.settings.accept"] = ("image/webp")


# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('disable-gpu')
# options.add_argument('User-Agent:"Mozilla/5.0 (Linux; Android 6.0.1; vivo X9 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/38.0.0.0 Mobile Safari/537.36 VivoBrowser/5.1.2)"')
# options.add_argument('window-size=420x4200')

# headers = {
#     "Connection" : "keep-alive",
#     "Cache-Control" : "max-age=0",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#     "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
#     "userAgent": "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; SM-G9280 Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.2 Mobile Safari/537.36"
# }
#
#
# for key, value in headers.iteritems():
#     dcap['phantomjs.page.customHeaders.{}'.format(key)] = value

#driver = webdriver.Chrome(chrome_options = options )

driver = webdriver.PhantomJS(executable_path='phantomjs.exe')
#driver = webdriver.PhantomJS(desired_capabilities=dcap)
status=[]#用来保存每个query对比后的值，当对比失败的时候为-1
status_Distance = []
querys_file = open('sortKeyword','r')
# querys_file = open('xianshangzoucha.txt','r')
querys = querys_file.readlines()
num = len(querys)
path_pictures_saved = "D:\\py\\107114\\"
path_pictures_saved1 = "D:\\py\\107114\\"
js="var ads = document.getElementsByClassName(\"ad_resultD:\python_projects\pic_compare_new_ls\pic_compared_top\"); if (ads !=null){for(i=0;i<ads.length;i++){ads[i].style.d" \
   "isplay = \"none\"; }}var dibu_ad = document.getElementById(\"bottomAd\");if (dibu_ad!=null){dibu_ad.style.display=\"none\";}var zhongbu_" \
   "ad = document.getElementById(\"kmap-business-container\");if(zhongbu_ad!= null){zhongbu_ad.style.display=\"none\";}"

#f = open('nginxtc_black.txt','w+')

def get_compare():
    global status
    global status_Distance
    global driver
    index = 0
    for query in querys:
        if index%800 == 0:
            driver.close()
            driver = webdriver.PhantomJS(desired_capabilities=dcap)
        index = index + 1
        if index < 19326 :
            continue
        url_tem_xianxia ="http://10.134.107.114/web/searchList.jsp?keyword=" + quote(query.strip())
        try:
            driver.get(url_tem_xianxia)
            driver.find_element_by_id("keyword").click()
            time.sleep(1)
            # print driver.get_log("browser")
            # driver.execute_script(js)
            # time.sleep(1.5)
            file_Path_Name_xianxia = path_pictures_saved + str(index) +"_"+ str(num) + "--" + "xianxia" + ".png"
            driver.save_screenshot(file_Path_Name_xianxia)  # 截取全屏，并保存
            time.sleep(0.2)
        except Exception as e:
            #print "线下query--"+query.strip('\n') + "有异常："
            print("线下query--%s有异常：" % query.strip('\n'))
            driver = webdriver.PhantomJS(desired_capabilities=dcap)
            continue

        url_tem_xianshang ="http://wap.sogou.com/web/searchList.jsp?keyword=" + quote(query.strip())
        try:
            driver.get(url_tem_xianshang)
            driver.find_element_by_id("keyword").click()
            # print driver.page_source
            time.sleep(1)
            # print driver.get_log("browser")
            # driver.execute_script(js)
            # time.sleep(1.5)
            file_Path_Name_xianshang = path_pictures_saved + str(index) +"_"+ str(num) + "--" +"线上" + ".png"
            driver.save_screenshot(file_Path_Name_xianshang)  # 截取全屏，并保存
        except Exception as e:
            #print "线上query--"+query.strip('\n') + "有异常："
            print("线下query--%s有异常：" % query.strip('\n'))
            driver = webdriver.PhantomJS(desired_capabilities=dcap)
            continue

        ####图片对比
        # time.sleep(3)
        try:

            time.sleep(0.2)
            duibidu = picture_duibi.calc_similar_by_path(file_Path_Name_xianxia,file_Path_Name_xianshang)
            if duibidu < 0.99:
                file_Path_Name_compared = path_pictures_saved + str(index) +"_"+ str(num) + "--"  + "compared" + ".png"
                saveComparedImg(file_Path_Name_xianshang,file_Path_Name_xianxia,file_Path_Name_compared)

                #整合三张图片到一张图片上
                resin1 = Image.open(file_Path_Name_xianshang)
                #print  file_Path_Name_xianshang
                resin1_w = resin1.size[0]

                node1 = Image.open(file_Path_Name_xianxia)
                node1_w = node1.size[0]

                compared1 = Image.open(file_Path_Name_compared)
                compared1_w = compared1.size[0]
                compared1_h = compared1.size[1]

                image_merge = Image.new('RGB',((resin1_w + node1_w + compared1_w ), compared1_h), 0xffffff)
                image_merge.paste(resin1, (0, 0))
                image_merge.paste(node1, (resin1_w, 0))
                image_merge.paste(compared1, (resin1_w+node1_w, 0))
                file_Path_Name_zong=path_pictures_saved1 + str(index)+ query.strip() +'--zong'+'.png'
                image_merge.save(file_Path_Name_zong)

            # h1 = xiangsidutest.avhash(file_Path_Name_xianxia)
            # h2 = xiangsidutest.avhash(file_Path_Name_xianshang)
            # juli = xiangsidutest.hamming(h1,h2
            # time.sleep(0.1)
            status.append(duibidu)
            # status_Distance.append(juli)
            # print ("第%d个query，" %(index)) + ("共 %d个query!--" %(num)) + urllib.unquote(query.strip('\n')) + "线上和线下图片距离为：" + str(juli)
            #print ("第%d个query，" %(index)) + ("共 %d个query!--" %(num)) + urllib.unquote(query.strip('\n')) + "线上和线下图片相似度为：" + str(duibidu)
            a = ("第%d个query，" %(index)) + ("共 %d个query!--" %(num)) + urllib.unquote(query.strip('\n'))+ "线上和线下图片相似度为：" + str(duibidu)
            #f.write(a + '\n')
            print(a)
            logger.info(a)
            # print print_current_time()
            # compare_result_file.write(query.strip('\n') + "线上和线下图片对比度为：" + str(picture_duibi.calc_similar_by_path(file_Path_Name_xianxia,file_Path_Name_xianshang))+'\n')
        except:
            print("图片对比度失败，暂时跳过。")
            status.append(-1)
            status_Distance.append(-1)
            continue
    driver.close()
    driver.quit()

def print_current_time():
    timeTemp = time.time()
    timeTempNext = time.localtime(timeTemp)
    timeNow = time.strftime("%Y-%m-%d-%H-%M-%S", timeTempNext)   #转化为当前时间
    return timeNow
def recordResults():
    global status
    global status_Distance
    compare_result_file = open("compare_results_phantomJS_failed.txt",'w')
    num = 0
    for query in querys:
        if status[num] < 0.99:
            compare_result_file.write(str(num+1) +"_"+ str(len(querys))+":"+urllib.unquote(query.strip('\n')) + "Similarity ------"+ str(status[num]))
            compare_result_file.write("\n")
            # compare_result_file.write(str(num+1) +"_"+ str(len(querys))+":"+urllib.unquote(query.strip('\n')) + "Distance ------"+ str(status_Distance[num]))
            # compare_result_file.write("\n")
        # elif status[num] < 0.5:
        #     compare_result_file.write(str(num+1) +"_"+ str(len(querys))+":"+urllib.unquote(query.strip('\n')) + "Similarity ------"+ str(status[num]))
        #     compare_result_file.write("\n")
            # compare_result_file.write(str(num+1) +"_"+ str(len(querys))+":"+urllib.unquote(query.strip('\n')) + "Distance ------"+ str(status_Distance[num]))
            # compare_result_file.write("\n")
        num = num + 1
    compare_result_file.write(print_current_time())
    compare_result_file.write("\n")
    compare_result_file.close()

#####################case全部跑完后绘图#################
def huitu():
    global  status
    # for nn in status:
    #     print nn
    print(len(status))
    method = ('failed','0-0.5','0.5-0.6','0.6-0.7','0.7-0.8','0.8-0.9','0.9-0.95','0.95-0.97','0.97-0.99','0.99-1')
    performance=[]
    x_pos = np.arange(10)
    xulie1 =0
    xulie2 =0
    xulie3 =0
    xulie4 =0
    xulie5 =0
    xulie6 =0
    xulie7 =0
    xulie8 =0
    xulie9 =0
    xulie10 =0
    for sta in status:
        if sta == -1:
            xulie1 = xulie1 + 1
            print("cuo+" + str(sta))
        elif sta <= 0.5:
            xulie2 = xulie2 +  1
            print("0.5+" + str(sta))
        elif sta <= 0.6:
            xulie3 = xulie3 + 1
            print("0.6+" + str(sta))
        elif sta <= 0.7:
            xulie4 = xulie4 + 1
            print("0.7+" + str(sta))
        elif sta <= 0.8:
            xulie5 + xulie5 + 1
            print("0.8+" + str(sta))
        elif sta <= 0.9:
            xulie6 + xulie6 + 1
            print("0.9+" + str(sta))
        elif sta <= 0.95:
            xulie7 = xulie7 + 1
        elif sta <= 0.97:
            xulie8 = xulie8 + 1
            print("0.97+" + str(sta))
        elif sta <= 0.99:
            xulie9 = xulie9 + 1
            print("0.99+" + str(sta))
        elif sta <= 1:
            xulie10 = xulie10 + 1
            print("1+" + str(sta))
    performance.append(xulie1);performance.append(xulie2);performance.append(xulie3);performance.append(xulie4);performance.append(xulie5);performance.append(xulie6);performance.append(xulie7);performance.append(xulie8);
    performance.append(xulie9);performance.append(xulie10);
    plt.bar(x_pos,performance,align = 'center',alpha = 0.4)
    plt.xticks(x_pos,method)
    plt.title('results of pictures compared')
    # plt.text(0.3,0.3,'results of pictures compared')
    plt.show()
print(print_current_time())
get_compare()
recordResults()
#f.cloes()
# huitu()
