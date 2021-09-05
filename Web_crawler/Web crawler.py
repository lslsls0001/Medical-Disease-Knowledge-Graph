"""
# -*- coding: utf-8 -*-
# @File    : web_crawler.py
# @Time    : 04/27/2021
# @Author  : Yibo Li
# @Email   : yibo_Li@student.uml.edu
# @Software: PyCharm
"""

import requests
import re
import urllib
import json
from lxml import etree
from lxml import html
from urllib.parse import urljoin

#1.http://mmbl.net/health/jb/1.html  ——  name desc category
#2.https://dxy.com/search/result?query=百日咳 —— prevent, cause
#3.https://jbk.39.net/gxb/ —— symptom, yibo_status, easy_way, get_way,acompany, cure_department, cure_way, cure_lasttime, cured_probe, common_drug, cost_money, check,
#                             do_eat, not_eat, recommand_eat, recommand_drug, drug_detail.
#4.http://mmbl.net/health/jb/1.html —— get_prob; the web page is blocked somehow, just give the url

def Disease_Search(search_item):

    disease_list = []
    disease_each = {}

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }

    for item in search_item:
        url = "http://mmbl.net/health/search.php?keyword=" + item
        page_text = requests.get(url=url, headers=headers).text
        tree = html.fromstring(page_text)

        '''--------------------------------find the disease name and nickname-----------------------------'''
        try:
            url_1 = tree.xpath('//div[@class="jktitl l"]/h3/a/@href')[0]
            url_1 = "http://mmbl.net/health/" + url_1  # url_1 = "http://mmbl.net/health/jb/1.html"
            page_text_1 = requests.get(url=url_1, headers=headers).text
            tree_1 = html.fromstring(page_text_1)
            disease_name = tree_1.xpath('//div[@class="jkd_intro"]/b/text()')[0]
            disease_nickname = tree_1.xpath('//ul[@class="jkd_list"]/li[1]/p[1]//a/text()')
        except Exception as e:
            pass
        '''
        if disease_nickname is not None:
            disease_name_final = disease_name + " (" + ",".join(i for i in disease_nickname) + ")"
            disease_each["name"] = disease_name_final
        else:
            disease_each["name"] = disease_name
        '''
        disease_each["name"] = disease_name
        # print(disease_each["name"])

        '''--------------------------------find the disease description-----------------------------'''
        try:
            disease_desc = tree_1.xpath('//div[@class="jkd_intro"]/p/text()')[0]
            disease_each["desc"] = disease_desc
        except Exception as e:
            pass
        # print(disease_desc)
        # print(disease_each["desc"])

        '''--------------------------------find the disease category-----------------------------'''
        try:
            disease_category = tree_1.xpath('//ul[@class="jkd_list"]/li[1]/p[2]/text()')[0]
            disease_each["category"] = re.split(' ', disease_category)
        except Exception as e:
            pass
        # print(disease_category)
        # print(disease_each["category"])

        '''---------------------------------------------------------------------------------------'''

        url_2 = "https://dxy.com/search/result?query=" + disease_name
        page_text_2 = requests.get(url=url_2, headers=headers).text
        tree_2 = html.fromstring(page_text_2)
        #print(page_text_2)
        '''--------------------------------find the disease prevent-----------------------------'''
        try:
            url_2_sub = tree_2.xpath('//a[@class="tag-content-title-link"]/@href')[0]
            page_text_2_sub = requests.get(url=url_2_sub, headers=headers).text
            tree_2_sub = html.fromstring(page_text_2_sub)
            disease_prevent = tree_2_sub.xpath('//li[@id="6"]//ul//p//text()')
            # print(disease_prevent)
            if disease_prevent is not None:
                str = ""
                disease_each["prevent"] = str.join(disease_prevent)
            else:
                disease_each["prevent"] = ""
        except Exception as e:
            pass
        # print(disease_each["prevent"])

        '''--------------------------------find the disease cause-----------------------------'''
        try:
            disease_cause = tree_2_sub.xpath('//li[@id="2"]//div[@class="html-parse tag-html"]//p//text()')
            # print(disease_cause)
            if disease_cause is not None:
                str = ""
                disease_each["cause"] = str.join(disease_cause)
            else:
                disease_each["cause"] = ""
        except Exception as e:
            pass
        # print(disease_each["cause"])

        '''---------------------------------------------------------------------------------------'''

        url_3 = "https://jbk.39.net/bw/key=" + disease_name
        page_text_3 = requests.get(url=url_3, headers=headers).text
        tree_3 = html.fromstring(page_text_3)

        '''--------------------------------find the disease symptom-----------------------------'''
        try:
            url_3_sub = tree_3.xpath('//p[@class="result_item_top_l"]/a/@href')[0]
            page_text_3_sub = requests.get(url=url_3_sub, headers=headers).text
            tree_3_sub = html.fromstring(page_text_3_sub)
            disease_symptom = tree_3_sub.xpath('//div[@class="disease_box"]//ul/li[11]/span//a/text()')
            if disease_symptom is not None:
                disease_each["symptom"] = disease_symptom
            else:
                disease_each["symptom"] = []
        except Exception as e:
            pass
        # print(disease_each["symptom"])

        '''--------------------------------find the disease yibao_status-----------------------------'''
        try:
            disease_yibao_status = tree_3_sub.xpath('//div[@class="disease_box"]//ul/li[2]/span/text()')[0]
            disease_each["yibao_status"] = disease_yibao_status
        except Exception as e:
            pass
        # print(disease_each["yibao_status"])

        '''--------------------------------find the disease get_prob-----------------------------'''
        # url_get_prob = f'http://mmbl.net/health/search.php?keyword={disease_name}'
        args = {"keyword": disease_name}
        url_get_prob = "http://mmbl.net/health/search.php?{}".format(urllib.parse.urlencode(args))
        disease_each["get_prob"] = "Please check this url to search " + disease_name + ": " + url_get_prob
        # print(disease_each["get_prob"])

        '''--------------------------------find the disease easy_get-----------------------------'''
        try:
            disease_easy_get = tree_3_sub.xpath('//div[@class="disease_box"]//ul/li[9]/span//text()')[0]
            disease_each["easy_get"] = disease_easy_get
        except Exception as e:
            pass
        # print(disease_each["easy_get"])

        '''--------------------------------find the disease get_way-----------------------------'''
        try:
            disease_get_way = tree_3_sub.xpath('//div[@class="disease_box"]//ul/li[5]/span//text()')[0]
            disease_each["get_way"] = disease_get_way
        # print(disease_each["get_way"])
        except Exception as e:
            pass
        '''--------------------------------find the disease acompany-----------------------------'''
        try:
            disease_acompany = tree_3_sub.xpath('//div[@class="disease_box"]//ul/li[13]/span//a/text()')
            disease_each["acompany"] = disease_acompany
        except Exception as e:
            pass
        # print(disease_each["acompany"])

        '''--------------------------------find the disease cure department-----------------------------'''
        try:
            disease_cure_department = tree_3_sub.xpath('//div[@class="disease_box"]//ul/li[4]/span//a/text()')
            disease_each["cure_department"] = disease_cure_department
        except Exception as e:
            pass
        # print(disease_each["cure_department"])

        '''--------------------------------find the disease cure way-----------------------------'''
        try:
            disease_cure_way = tree_3_sub.xpath('//div[@class="disease_box"]//ul/li[6]/span//a/text()')
            disease_each["cure_way"] = disease_cure_way
        except Exception as e:
            pass
        # print(disease_each["cure_way"])

        '''--------------------------------find the disease cure_lasttime-----------------------------'''
        try:
            disease_cure_lasttime = tree_3_sub.xpath('//div[@class="disease_box"]//ul/li[8]/span/text()')[0]
            disease_each["cure_lasttime"] = disease_cure_lasttime
        except Exception as e:
            pass
        # print(disease_each["cure_lasttime"])

        '''--------------------------------find the disease cured_prob-----------------------------'''
        try:
            disease_cured_prob = tree_3_sub.xpath('//div[@class="disease_box"]//ul/li[7]/span/text()')[0]
            disease_each["cured_prob"] = disease_cured_prob
        except Exception as e:
            pass
        # print(disease_each["cured_prob"])

        '''--------------------------------find the disease common_drug-----------------------------'''
        try:
            disease_common_drug = tree_3_sub.xpath('//div[@class="disease_box"]//ul[2]/li[1]/span//a/text()')
            disease_each["common_drug"] = disease_common_drug
        except Exception as e:
            pass
        # print(disease_each["common_drug"])

        '''--------------------------------find the disease cost_money-----------------------------'''
        try:
            disease_cost_money = tree_3_sub.xpath('//div[@class="disease_box"]//ul/li[10]/span/text()')[0]
            disease_each["cost_money"] = disease_cost_money
        except Exception as e:
            pass
        # print(disease_each["cost_money"])

        '''--------------------------------find the disease check-----------------------------'''
        try:
            disease_check = tree_3_sub.xpath('//div[@class="disease_box"]//ul/li[12]/span//a/text()')
            disease_each["check"] = disease_check
        except Exception as e:
            pass
        # print(disease_each["check"])

        '''--------------------------------find the disease do_eat-----------------------------'''
        try:
            url_3_sub_eat = tree_3_sub.xpath('//div[@class="navigation"][3]//ul/li[5]/a/@href')[0]
            page_text_3_sub_eat = requests.get(url=url_3_sub_eat, headers=headers).text
            tree_3_sub_eat = html.fromstring(page_text_3_sub_eat)
            disease_do_eat = tree_3_sub_eat.xpath('//div[@class="yinshi_table"]//table[1]//tr[position()>1]//td[1]/text()')
            disease_each["do_eat"] = disease_do_eat
        except Exception as e:
            pass
        # print(disease_each["do_eat"])

        '''--------------------------------find the disease not_eat-----------------------------'''
        try:
            disease_not_eat = tree_3_sub_eat.xpath('//div[@class="yinshi_table"]//table[2]//tr[position()>1]//td[1]/text()')
            disease_each["not_eat"] = disease_not_eat
        except Exception as e:
            pass
        # print(disease_each["not_eat"])

        '''--------------------------------find the disease recommand_eat-----------------------------'''
        try:
            disease_each["recommand_eat"] = disease_each["do_eat"]
        except Exception as e:
            pass
        # print(disease_each["recommand_eat"])

        '''--------------------------------find the disease recommand_drug-----------------------------'''
        try:
            if tree_3_sub.xpath('//div[@class="navigation"][4]//ul/li[3]/a/text()')[0] == "药品":
                url_3_sub_drug = tree_3_sub.xpath('//div[@class="navigation"][4]//ul/li[3]/a/@href')[0]
            else:
                url_3_sub_drug = tree_3_sub.xpath('//div[@class="navigation"][4]//ul/li[2]/a/@href')[0]
            page_text_3_sub_drug = requests.get(url=url_3_sub_drug, headers=headers).text
            tree_3_sub_drug = html.fromstring(page_text_3_sub_drug)
            disease_recommand_drug_1 = tree_3_sub_drug.xpath('//div[@class="chi-drug"]//ul//li/h4/a/text()')
            disease_recommand_drug = list(set(disease_recommand_drug_1))
            disease_each["recommand_drug"] = disease_recommand_drug
        except Exception as e:
            pass
        # print(disease_each["recommand_drug"])

        '''--------------------------------find the disease drug_detail-----------------------------'''
        try:
            disease_recommand_drug_2 = tree_3_sub_drug.xpath('//div[@class="chi-drug"]//ul//li/h4/a/text()')
            disease_drug_production = tree_3_sub_drug.xpath('//div[@class="chi-drug"]//ul//li/p/i/text()')
            for i in range(len(disease_drug_production)):
                disease_drug_production[i] = disease_drug_production[i].split("] ")[1]

            disease_drug_detail = []

            for (i, j) in zip(disease_recommand_drug_2, disease_drug_production):
                str = j + "(" + i + ")"
                disease_drug_detail.append(str)

            disease_each["drug_detail"] = disease_drug_detail
        except Exception as e:
            pass
        #print(disease_drug_detail)
        #print(disease_each)
        disease_temp = json.dumps(disease_each,ensure_ascii=False)
        f = open("disease_summary.json","a+", encoding= 'utf-8')
        f.write(disease_temp)
        f.write('\r\n')

    f.close()

    #print(disease_each)

if __name__ == "__main__":
    #["百日咳", "痛经", "腹泻", "冠心病","前列腺炎"]
    #["糖尿病", "高血压", "心绞痛", "高血脂","肺炎"]
    #["甲状腺肿大", "坏血病", "发烧", "骨折", "感冒"]
    #["脑震荡", "胃癌", "乳腺癌", "消化不良", "哮喘", "酒精中毒"]
    #["过敏性鼻炎","鼻窦炎"]
    #["牙龈肿痛", "雀斑", "青光眼", "肝硬化", "脂肪肝"]
    #["癫痫","痛经","皮肤过敏","风湿病","支气管炎"]
    #["便秘", "自闭", "乙肝", "偏头疼", "牛皮癣"]
    #["中风", "动脉硬化", "咳嗽", "关节炎", "水痘", "近视", "扁导体炎"]
    search_item =["黑痣", "尿不尽", "肺结核", "白血病","脚气"]
    Disease_Search(search_item)

    #index_list=[i for i in range(1,2001)]





