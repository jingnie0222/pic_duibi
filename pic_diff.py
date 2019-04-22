#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'yinjingjing'
__mtime__ = '2019/2/22'
"""

from selenium import webdriver
import picture_duibi
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from PIL import Image
from urllib.parse import unquote
from urllib.parse import quote
from testHightDiffV2 import saveComparedImg
import logging
import os, sys
import datetime
import re


dcap = dict(DesiredCapabilities.PHANTOMJS)
#dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
driver = webdriver.PhantomJS(desired_capabilities=dcap)

querys_file = open('yy', 'r', encoding='utf8')
querys = querys_file.readlines()
querys_file.close()
num = len(querys)

base_url_prefix = "http://djt.www.sogou/web?query="
test_url_prefix = "http://1tc.www.sogou/web?query="

def log_error(str):
    time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    sys.stderr.write('[%s] [error] %s\n' % (time_str, str))
    sys.stderr.flush()

def get_compare(pic_path):
    global driver
    index = 0
    for query in querys:
        if index%800 == 0:
            driver.close()
            driver = webdriver.PhantomJS(desired_capabilities=dcap)
        index = index + 1

        if index < -1 :
            continue
        print(query.strip('\n'))

        p_query = '_'.join(re.split(r'[\s.:]',query))  #去掉query中的空白符 . :,这些会导致图片保存错误,保存图片使用
        base_url = base_url_prefix + quote(query.strip())
        try:
            driver.get(base_url)
            time.sleep(1)
            file_path_base = pic_path + "\\" + str(index) + "_" + p_query + "_" + "base" + ".png"
            driver.save_screenshot(file_path_base)
            time.sleep(0.2)
        except Exception as e:
            print("base--%s有异常：%s" % (query.strip('\n'),e))
            driver = webdriver.PhantomJS(desired_capabilities=dcap)
            continue

        test_url = test_url_prefix + quote(query.strip())
        try:
            driver.get(test_url)
            time.sleep(1)
            file_path_test = pic_path + "\\" + str(index) + "_" + p_query + "_" + "test" + ".png"
            driver.save_screenshot(file_path_test)
        except Exception as e:
            print("test--%s有异常：%s" % (query.strip('\n'), e))
            driver = webdriver.PhantomJS(desired_capabilities=dcap)
            continue

        ####图片对比
        try:
            time.sleep(0.2)
            duibidu = picture_duibi.calc_similar_by_path(file_path_base, file_path_test)
            print("duibidu=%f" % duibidu)
            if duibidu < 0.99:
                file_path_compared = pic_path + "\\" + str(index) + "_" + p_query + "_"  + "compared" + ".png"
                saveComparedImg(file_path_base, file_path_test, file_path_compared)
                #整合三张图片到一张图片上
                base = Image.open(file_path_base)
                base_w = base.size[0]

                test = Image.open(file_path_test)
                test_w = test.size[0]

                compared = Image.open(file_path_compared)
                compared_w = compared.size[0]
                compared_h = compared.size[1]

                image_merge = Image.new('RGB',((base_w + test_w + compared_w ), compared_h), 0xffffff)
                image_merge.paste(base, (0, 0))
                image_merge.paste(test, (base_w, 0))
                image_merge.paste(compared, (base_w+test_w, 0))

                file_path_total = pic_path + "\\" + str(index) + "_" + p_query +'_total' + '.png'
                image_merge.save(file_path_total)

            res_str = ("第%d个query," %(index)) + ("共 %d个query," %(num)) + (query.strip('\n'))+ ",图片相似度为：" + str(duibidu)
            print(res_str + "\n")
        except Exception as err:
            print(err)
            print("图片对比度失败，暂时跳过。\n")
            continue
    driver.close()
    driver.quit()


def gen_result_dir(result_dir_prefix):
    try:
        time_stamp = time.time()
        time_now = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(time_stamp))
        os.mkdir(result_dir_prefix + time_now)
    except FileExistsError:
        log_error('[gen_result_dir] Dir exists: %s. remove dir, mkdir again' % (result_dir_prefix + time_now))
        shutil.rmtree(result_dir_prefix + time_now)
        os.mkdir(result_dir_prefix + time_now)

    result_dir = result_dir_prefix + time_now
    return result_dir


def main():
    result_dir_prefix = "D:\\python\\pic_result\\"
    result_dir = gen_result_dir(result_dir_prefix)
    get_compare(result_dir)

if __name__ == "__main__":
    main()