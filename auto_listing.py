import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import time
from logger import *
import csv
import re
import random
import numpy as np
import multiprocessing
from multiprocessing import freeze_support

logger = set_logger(__name__)

def start_chrome():
    user_agent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    ]
    UA = user_agent[random.randrange(0, len(user_agent), 1)]
    global option
    option = Options()  
    option.add_argument('--user-data-dir=' + os.path.join(os.getcwd(),"profile1"))    
    option.add_argument('--lang=ja-JP')
    option.add_argument('--user-agent=' + UA)
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-ssl-errors')
    option.add_argument("window-size=1000,800")
    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)   
def start_chrome2():
    user_agent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    ]
    UA = user_agent[random.randrange(0, len(user_agent), 1)]
    global option2
    option2 = Options() 
    option2.add_argument('--user-data-dir=' + os.path.join(os.getcwd(),"profile2"))    
    option2.add_argument('--lang=ja-JP')
    option2.add_argument('--user-agent=' + UA)
    option2.add_argument('--ignore-certificate-errors')
    option2.add_argument('--ignore-ssl-errors')
    option2.add_argument("window-size=1000,800")
    global driver2
    driver2 = webdriver.Chrome(ChromeDriverManager().install(),options=option2)   
def start_chrome3():
    user_agent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    ]
    UA = user_agent[random.randrange(0, len(user_agent), 1)]
    global option3
    option3 = Options() 
    option3.add_argument('--user-data-dir=' + os.path.join(os.getcwd(),"profile3"))    
    option3.add_argument('--lang=ja-JP')
    option3.add_argument('--user-agent=' + UA)
    option3.add_argument('--ignore-certificate-errors')
    option3.add_argument('--ignore-ssl-errors')
    option3.add_argument("window-size=1000,800")
    global driver3
    driver3 = webdriver.Chrome(ChromeDriverManager().install(),options=option3)   

def load_csv():
    with open('item+500.csv') as f:
        reader = csv.reader(f)
        header = next(reader)
        l = [row for row in reader]
    return l

def listing_item():
    start_chrome()
    try: 
        driver.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")
        l = load_csv()
        item_lists = np.array_split(l, 3)[0]
        for item in item_lists:
            try:
                category = item[0]
                title = item[1]
                description = item[2]
                start_price = item[3]
                prompt_decision_price = item[4]
                shipping_end = item[6]
                shipping_time = item[7]
                img = item[9]
                location = item[29]
                try:
                    if '???' in location:
                        p = r'(.*)???'
                        location = re.search(p, location).group(1)
                        location = location + '???'
                    elif '???'in location:
                        p = r'(.*)???'
                        location = re.search(p, location).group(1)
                        location = location + '???'
                except Exception as e:
                    pass
                shipping_charge = item[31]
                new_old = item[36]
                relist = item[46]
                if item[59] == '3??????7???':
                    send_days = 3
                elif item[59] == '2??????3???':
                    send_days = 2
                elif item[59] == '1??????2???':
                    send_days = 1
                else:
                    send_days = 3
                shipping_method = item[60]
                shipping_fee = item[61]
                # ???????????????????????????
                driver.find_element_by_id('selectFile').send_keys(os.path.abspath(f'image/{img}'))
                # ???????????????????????????
                title  = title.replace('\"','\'')
                driver.execute_script(f'document.getElementById("fleaTitleForm").value="{title}"')
                #??????????????????
                driver.execute_script(f'arguments[0].value = {category}', driver.find_element_by_name('category'))
                # ???????????????
                Select(driver.find_element_by_name('istatus')).select_by_visible_text(new_old)
                # ????????????
                try:
                    driver.find_element_by_id('aucHTMLtag').click()
                except Exception as e:
                    pass
                description  = description.replace('\"','\'')
                driver.execute_script(f'document.getElementsByName("Description_plain_work")[0].value = "{description}";')
                # ??????????????????
                Select(driver.find_element_by_name("loc_cd")).select_by_visible_text(location)
                # ????????????
                if shipping_charge == '?????????':
                    Select(driver.find_element_by_id("auc_shipping_who")).select_by_index(1)
                else:
                    Select(driver.find_element_by_id("auc_shipping_who")).select_by_index(0)
                # ????????????
                if driver.find_element_by_id('ship_delivery_n').is_selected():
                    driver.find_elements_by_class_name('CheckExpand__label')[0].click()
                if driver.find_element_by_id('ship_delivery_s').is_selected():
                    driver.find_elements_by_class_name('CheckExpand__label')[1].click()
                if driver.find_element_by_id('ship_delivery_l').is_selected():
                    driver.find_elements_by_class_name('CheckExpand__label')[2].click()
                if driver.find_element_by_id('ship_delivery_yupacket').is_selected():
                    driver.find_elements_by_class_name('CheckExpand__label')[3].click()
                if driver.find_element_by_id('ship_delivery_yupack').is_selected():
                    driver.find_elements_by_class_name('CheckExpand__label')[4].click()
                if driver.find_element_by_id('shipping_other_check1').is_selected():
                    pass
                else:
                    driver.find_element_by_id('auc_add_shipform').click()
                    driver.find_element_by_class_name('CheckExpand__label--postageBox').click()
                    Select(driver.find_element_by_id("auc_shipname_standard1")).select_by_index(12)
                    driver.find_element_by_id('auc_shipname_text1').send_keys(shipping_method)
                    driver.find_element_by_id('auc_shipname_uniform_fee_data1').send_keys(shipping_fee)
                # ????????????????????????????????????
                Select(driver.find_element_by_name("shipschedule")).select_by_index(send_days)
                # ????????????
                driver.find_element_by_xpath('//*[@id="js-PCPremiumSalesmodeArea"]/div[2]/label[1]').click()
                # ????????????
                driver.execute_script(f'document.getElementById("auc_StartPrice_auction").value={start_price}')
                # ????????????
                driver.execute_script(f'document.getElementById("auc_BidOrBuyPrice_auction").value={prompt_decision_price}')
                # ??????????????????
                Select(driver.find_element_by_id("ClosingYMD")).select_by_index(shipping_end)
                Select(driver.find_element_by_id("ClosingTime")).select_by_index(shipping_time)
                # ???????????????
                try:
                    driver.find_element_by_xpath('//dt[text()="??????????????????????????????"]').click()
                    Select(driver.find_element_by_id("numResubmit")).select_by_index(relist)
                except Exception as e:
                    driver.find_element_by_xpath('//dt[text()="??????????????????????????????"]').click()
                    Select(driver.find_element_by_id("numResubmit")).select_by_index(relist)
                # ???????????????
                driver.find_element_by_class_name('HeaderExpand__title').click()
                if not driver.find_element_by_name('AutoExtension').is_selected():
                    driver.find_element_by_xpath('//span[text()="?????????????????????????????????"]').click()
                if not driver.find_element_by_name('minBidRating').is_selected():
                    driver.find_element_by_xpath('//span[text()="????????????????????????????????????"]').click()
                if not driver.find_element_by_name('badRatingRatio').is_selected():
                    driver.find_element_by_xpath('//span[text()="?????????????????????????????????????????????"]').click()
                if not driver.find_element_by_name('bidCreditLimit').is_selected():
                    driver.find_element_by_xpath('//span[text()="???????????????????????????????????????"]').click()
                if driver.find_element_by_name('salesContract').is_selected():
                    driver.find_element_by_xpath('//span[text()="???????????????????????????????????????"]').click()
                if driver.find_element_by_id('js-PCPremiumRetpolicyCheck').is_selected():
                    driver.find_element_by_xpath('//span[text()="????????????????????????"]').click()
                driver.find_element_by_class_name('Button--proceed').click()
                driver.find_element_by_id('auc_preview_submit_up').click()
                driver.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")
            except Exception as e:
                logger.info(e)
                driver.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")
        driver.quit()
        logger.info('????????????')
    except Exception as e:
        logger.info(e)

def listing_item2():
    start_chrome2()
    try: 
        driver2.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")
        l = load_csv()
        item_lists = np.array_split(l, 3)[1]
        for item in item_lists:
            try:
                category = item[0]
                title = item[1]
                description = item[2]
                start_price = item[3]
                prompt_decision_price = item[4]
                shipping_end = item[6]
                shipping_time = item[7]
                img = item[9]
                location = item[29]
                try:
                    if '???' in location:
                        p = r'(.*)???'
                        location = re.search(p, location).group(1)
                        location = location + '???'
                    elif '???'in location:
                        p = r'(.*)???'
                        location = re.search(p, location).group(1)
                        location = location + '???'
                except Exception as e:
                    pass
                shipping_charge = item[31]
                new_old = item[36]
                relist = item[46]
                if item[59] == '3??????7???':
                    send_days = 3
                elif item[59] == '2??????3???':
                    send_days = 2
                elif item[59] == '1??????2???':
                    send_days = 1
                else:
                    send_days = 3
                shipping_method = item[60]
                shipping_fee = item[61]

                # ???????????????????????????
                driver2.find_element_by_id('selectFile').send_keys(os.path.abspath(f'image/{img}'))
                # ???????????????????????????
                title  = title.replace('\"','\'')
                driver2.execute_script(f'document.getElementById("fleaTitleForm").value="{title}"')
                #??????????????????
                driver2.execute_script(f'arguments[0].value = {category}', driver2.find_element_by_name('category'))
                # ???????????????
                Select(driver2.find_element_by_name('istatus')).select_by_visible_text(new_old)
                # ????????????
                try:
                    driver2.find_element_by_id('aucHTMLtag').click()
                except Exception as e:
                    pass
                description  = description.replace('\"','\'')
                driver2.execute_script(f'document.getElementsByName("Description_plain_work")[0].value = "{description}";')
                # ??????????????????
                Select(driver2.find_element_by_name("loc_cd")).select_by_visible_text(location)
                # ????????????
                if shipping_charge == '?????????':
                    Select(driver2.find_element_by_id("auc_shipping_who")).select_by_index(1)
                else:
                    Select(driver2.find_element_by_id("auc_shipping_who")).select_by_index(0)
                # ????????????
                if driver2.find_element_by_id('ship_delivery_n').is_selected():
                    driver2.find_elements_by_class_name('CheckExpand__label')[0].click()
                if driver2.find_element_by_id('ship_delivery_s').is_selected():
                    driver2.find_elements_by_class_name('CheckExpand__label')[1].click()
                if driver2.find_element_by_id('ship_delivery_l').is_selected():
                    driver2.find_elements_by_class_name('CheckExpand__label')[2].click()
                if driver2.find_element_by_id('ship_delivery_yupacket').is_selected():
                    driver2.find_elements_by_class_name('CheckExpand__label')[3].click()
                if driver2.find_element_by_id('ship_delivery_yupack').is_selected():
                    driver2.find_elements_by_class_name('CheckExpand__label')[4].click()
                if driver2.find_element_by_id('shipping_other_check1').is_selected():
                    pass
                else:
                    driver2.find_element_by_id('auc_add_shipform').click()
                    driver2.find_element_by_class_name('CheckExpand__label--postageBox').click()
                    Select(driver2.find_element_by_id("auc_shipname_standard1")).select_by_index(12)
                    driver2.find_element_by_id('auc_shipname_text1').send_keys(shipping_method)
                    driver2.find_element_by_id('auc_shipname_uniform_fee_data1').send_keys(shipping_fee)

                # ????????????????????????????????????
                Select(driver2.find_element_by_name("shipschedule")).select_by_index(send_days)
                # ????????????
                driver2.find_element_by_xpath('//*[@id="js-PCPremiumSalesmodeArea"]/div[2]/label[1]').click()
                # ????????????
                driver2.execute_script(f'document.getElementById("auc_StartPrice_auction").value={start_price}')
                # ????????????
                driver2.execute_script(f'document.getElementById("auc_BidOrBuyPrice_auction").value={prompt_decision_price}')
                # ??????????????????
                Select(driver2.find_element_by_id("ClosingYMD")).select_by_index(shipping_end)
                Select(driver2.find_element_by_id("ClosingTime")).select_by_index(shipping_time)
                # ???????????????
                try:
                    driver2.find_element_by_xpath('//dt[text()="??????????????????????????????"]').click()
                    Select(driver2.find_element_by_id("numResubmit")).select_by_index(relist)
                except Exception as e:
                    driver2.find_element_by_xpath('//dt[text()="??????????????????????????????"]').click()
                    Select(driver2.find_element_by_id("numResubmit")).select_by_index(relist)
                # ???????????????
                driver2.find_element_by_class_name('HeaderExpand__title').click()
                if not driver2.find_element_by_name('AutoExtension').is_selected():
                    driver2.find_element_by_xpath('//span[text()="?????????????????????????????????"]').click()
                if not driver2.find_element_by_name('minBidRating').is_selected():
                    driver2.find_element_by_xpath('//span[text()="????????????????????????????????????"]').click()
                if not driver2.find_element_by_name('badRatingRatio').is_selected():
                    driver2.find_element_by_xpath('//span[text()="?????????????????????????????????????????????"]').click()
                if not driver2.find_element_by_name('bidCreditLimit').is_selected():
                    driver2.find_element_by_xpath('//span[text()="???????????????????????????????????????"]').click()
                if driver2.find_element_by_name('salesContract').is_selected():
                    driver2.find_element_by_xpath('//span[text()="???????????????????????????????????????"]').click()
                if driver2.find_element_by_id('js-PCPremiumRetpolicyCheck').is_selected():
                    driver2.find_element_by_xpath('//span[text()="????????????????????????"]').click()
                driver2.find_element_by_class_name('Button--proceed').click()
                driver2.find_element_by_id('auc_preview_submit_up').click()
                driver2.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")
            except Exception as e:
                logger.info(e)
                driver2.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")
        driver2.quit()
        logger.info('????????????')
    except Exception as e:
        logger.info(e)

def listing_item3():
    start_chrome3()
    try: 
        driver3.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")
        l = load_csv()
        item_lists = np.array_split(l, 3)[2]
        for item in item_lists:
            try:
                category = item[0]
                title = item[1]
                description = item[2]
                start_price = item[3]
                prompt_decision_price = item[4]
                shipping_end = item[6]
                shipping_time = item[7]
                img = item[9]
                location = item[29]
                try:
                    if '???' in location:
                        p = r'(.*)???'
                        location = re.search(p, location).group(1)
                        location = location + '???'
                    elif '???'in location:
                        p = r'(.*)???'
                        location = re.search(p, location).group(1)
                        location = location + '???'
                except Exception as e:
                    pass
                shipping_charge = item[31]
                new_old = item[36]
                relist = item[46]
                if item[59] == '3??????7???':
                    send_days = 3
                elif item[59] == '2??????3???':
                    send_days = 2
                elif item[59] == '1??????2???':
                    send_days = 1
                else:
                    send_days = 3
                shipping_method = item[60]
                shipping_fee = item[61]
                # ???????????????????????????
                driver3.find_element_by_id('selectFile').send_keys(os.path.abspath(f'image/{img}'))
                # ???????????????????????????
                title  = title.replace('\"','\'')
                driver3.execute_script(f'document.getElementById("fleaTitleForm").value="{title}"')
                #??????????????????
                driver3.execute_script(f'arguments[0].value = {category}', driver3.find_element_by_name('category'))
                # ???????????????
                Select(driver3.find_element_by_name('istatus')).select_by_visible_text(new_old)
                # ????????????
                try:
                    driver3.find_element_by_id('aucHTMLtag').click()
                except Exception as e:
                    pass
                description  = description.replace('\"','\'')
                driver3.execute_script(f'document.getElementsByName("Description_plain_work")[0].value = "{description}";')
                # ??????????????????
                Select(driver3.find_element_by_name("loc_cd")).select_by_visible_text(location)
                # ????????????
                if shipping_charge == '?????????':
                    Select(driver3.find_element_by_id("auc_shipping_who")).select_by_index(1)
                else:
                    Select(driver3.find_element_by_id("auc_shipping_who")).select_by_index(0)
                # ????????????
                if driver3.find_element_by_id('ship_delivery_n').is_selected():
                    driver3.find_elements_by_class_name('CheckExpand__label')[0].click()
                if driver3.find_element_by_id('ship_delivery_s').is_selected():
                    driver3.find_elements_by_class_name('CheckExpand__label')[1].click()
                if driver3.find_element_by_id('ship_delivery_l').is_selected():
                    driver3.find_elements_by_class_name('CheckExpand__label')[2].click()
                if driver3.find_element_by_id('ship_delivery_yupacket').is_selected():
                    driver3.find_elements_by_class_name('CheckExpand__label')[3].click()
                if driver3.find_element_by_id('ship_delivery_yupack').is_selected():
                    driver3.find_elements_by_class_name('CheckExpand__label')[4].click()
                if driver3.find_element_by_id('shipping_other_check1').is_selected():
                    pass
                else:
                    driver3.find_element_by_id('auc_add_shipform').click()
                    driver3.find_element_by_class_name('CheckExpand__label--postageBox').click()
                    Select(driver3.find_element_by_id("auc_shipname_standard1")).select_by_index(12)
                    driver3.find_element_by_id('auc_shipname_text1').send_keys(shipping_method)
                    driver3.find_element_by_id('auc_shipname_uniform_fee_data1').send_keys(shipping_fee)
                # ????????????????????????????????????
                Select(driver3.find_element_by_name("shipschedule")).select_by_index(send_days)
                # ????????????
                driver3.find_element_by_xpath('//*[@id="js-PCPremiumSalesmodeArea"]/div[2]/label[1]').click()
                # ????????????
                driver3.execute_script(f'document.getElementById("auc_StartPrice_auction").value={start_price}')
                # ????????????
                driver3.execute_script(f'document.getElementById("auc_BidOrBuyPrice_auction").value={prompt_decision_price}')
                # ??????????????????
                Select(driver3.find_element_by_id("ClosingYMD")).select_by_index(shipping_end)
                Select(driver3.find_element_by_id("ClosingTime")).select_by_index(shipping_time)
                # ???????????????
                try:
                    driver3.find_element_by_xpath('//dt[text()="??????????????????????????????"]').click()
                    Select(driver3.find_element_by_id("numResubmit")).select_by_index(relist)
                except Exception as e:
                    driver3.find_element_by_xpath('//dt[text()="??????????????????????????????"]').click()
                    Select(driver3.find_element_by_id("numResubmit")).select_by_index(relist)
                # ???????????????
                driver3.find_element_by_class_name('HeaderExpand__title').click()
                if not driver3.find_element_by_name('AutoExtension').is_selected():
                    driver3.find_element_by_xpath('//span[text()="?????????????????????????????????"]').click()
                if not driver3.find_element_by_name('minBidRating').is_selected():
                    driver3.find_element_by_xpath('//span[text()="????????????????????????????????????"]').click()
                if not driver3.find_element_by_name('badRatingRatio').is_selected():
                    driver3.find_element_by_xpath('//span[text()="?????????????????????????????????????????????"]').click()
                if not driver3.find_element_by_name('bidCreditLimit').is_selected():
                    driver3.find_element_by_xpath('//span[text()="???????????????????????????????????????"]').click()
                if driver3.find_element_by_name('salesContract').is_selected():
                    driver3.find_element_by_xpath('//span[text()="???????????????????????????????????????"]').click()
                if driver3.find_element_by_id('js-PCPremiumRetpolicyCheck').is_selected():
                    driver3.find_element_by_xpath('//span[text()="????????????????????????"]').click()
                driver3.find_element_by_class_name('Button--proceed').click()
                driver3.find_element_by_id('auc_preview_submit_up').click()
                driver3.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")
            except Exception as e:
                logger.info(e)
                driver3.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")   
        driver3.quit()
        logger.info('????????????')
    except Exception as e:
        logger.info(e)



def main():
    p0 = multiprocessing.Process(target=listing_item)
    p1 = multiprocessing.Process(target=listing_item2)
    p2 = multiprocessing.Process(target=listing_item3)
    
    # ??????????????????
    p0.start()
    time.sleep(4)
    p1.start()
    time.sleep(4)
    p2.start()
  
    # ?????????????????????????????????
    p0.join()
    p1.join()
    p2.join()
    

# ??????????????????????????????main()?????????(???????????????????????????????????????????????????????????????????????????????????????)
if __name__ == "__main__":
    freeze_support()
    main()