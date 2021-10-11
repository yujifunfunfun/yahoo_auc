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
                    if '都' in location:
                        p = r'(.*)都'
                        location = re.search(p, location).group(1)
                        location = location + '都'
                    elif '県'in location:
                        p = r'(.*)県'
                        location = re.search(p, location).group(1)
                        location = location + '県'
                except Exception as e:
                    pass
                shipping_charge = item[31]
                new_old = item[36]
                relist = item[46]
                if item[59] == '3日～7日':
                    send_days = 3
                elif item[59] == '2日～3日':
                    send_days = 2
                elif item[59] == '1日～2日':
                    send_days = 1
                else:
                    send_days = 3
                shipping_method = item[60]
                shipping_fee = item[61]
                # 出品画像を貼り付け
                driver.find_element_by_id('selectFile').send_keys(os.path.abspath(f'image/{img}'))
                # 出品タイトルを設定
                title  = title.replace('\"','\'')
                driver.execute_script(f'document.getElementById("fleaTitleForm").value="{title}"')
                #カテゴリ設定
                driver.execute_script(f'arguments[0].value = {category}', driver.find_element_by_name('category'))
                # 商品の状態
                Select(driver.find_element_by_name('istatus')).select_by_visible_text(new_old)
                # 商品説明
                try:
                    driver.find_element_by_id('aucHTMLtag').click()
                except Exception as e:
                    pass
                description  = description.replace('\"','\'')
                driver.execute_script(f'document.getElementsByName("Description_plain_work")[0].value = "{description}";')
                # 発送元の地域
                Select(driver.find_element_by_name("loc_cd")).select_by_visible_text(location)
                # 送料負担
                if shipping_charge == '落札者':
                    Select(driver.find_element_by_id("auc_shipping_who")).select_by_index(1)
                else:
                    Select(driver.find_element_by_id("auc_shipping_who")).select_by_index(0)
                # 配送方法
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
                # 支払いから発送までの日数
                Select(driver.find_element_by_name("shipschedule")).select_by_index(send_days)
                # 販売形式
                driver.find_element_by_xpath('//*[@id="js-PCPremiumSalesmodeArea"]/div[2]/label[1]').click()
                # 開始価格
                driver.execute_script(f'document.getElementById("auc_StartPrice_auction").value={start_price}')
                # 即決価格
                driver.execute_script(f'document.getElementById("auc_BidOrBuyPrice_auction").value={prompt_decision_price}')
                # 終了する日時
                Select(driver.find_element_by_id("ClosingYMD")).select_by_index(shipping_end)
                Select(driver.find_element_by_id("ClosingTime")).select_by_index(shipping_time)
                # 自動再出品
                try:
                    driver.find_element_by_xpath('//dt[text()="自動再出品を設定する"]').click()
                    Select(driver.find_element_by_id("numResubmit")).select_by_index(relist)
                except Exception as e:
                    driver.find_element_by_xpath('//dt[text()="自動再出品を設定する"]').click()
                    Select(driver.find_element_by_id("numResubmit")).select_by_index(relist)
                # オプション
                driver.find_element_by_class_name('HeaderExpand__title').click()
                if not driver.find_element_by_name('AutoExtension').is_selected():
                    driver.find_element_by_xpath('//span[text()="終了時間を自動延長する"]').click()
                if not driver.find_element_by_name('minBidRating').is_selected():
                    driver.find_element_by_xpath('//span[text()="総合評価で入札を制限する"]').click()
                if not driver.find_element_by_name('badRatingRatio').is_selected():
                    driver.find_element_by_xpath('//span[text()="悪い評価の割合で入札を制限する"]').click()
                if not driver.find_element_by_name('bidCreditLimit').is_selected():
                    driver.find_element_by_xpath('//span[text()="認証の有無で入札を制限する"]').click()
                if driver.find_element_by_name('salesContract').is_selected():
                    driver.find_element_by_xpath('//span[text()="出品者情報を手動で開示する"]').click()
                if driver.find_element_by_id('js-PCPremiumRetpolicyCheck').is_selected():
                    driver.find_element_by_xpath('//span[text()="返品を受け付ける"]').click()
                driver.find_element_by_class_name('Button--proceed').click()
                driver.find_element_by_id('auc_preview_submit_up').click()
                driver.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")
            except Exception as e:
                logger.info(e)
                driver.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")
        driver.quit()
        logger.info('出品完了')
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
                    if '都' in location:
                        p = r'(.*)都'
                        location = re.search(p, location).group(1)
                        location = location + '都'
                    elif '県'in location:
                        p = r'(.*)県'
                        location = re.search(p, location).group(1)
                        location = location + '県'
                except Exception as e:
                    pass
                shipping_charge = item[31]
                new_old = item[36]
                relist = item[46]
                if item[59] == '3日～7日':
                    send_days = 3
                elif item[59] == '2日～3日':
                    send_days = 2
                elif item[59] == '1日～2日':
                    send_days = 1
                else:
                    send_days = 3
                shipping_method = item[60]
                shipping_fee = item[61]

                # 出品画像を貼り付け
                driver2.find_element_by_id('selectFile').send_keys(os.path.abspath(f'image/{img}'))
                # 出品タイトルを設定
                title  = title.replace('\"','\'')
                driver2.execute_script(f'document.getElementById("fleaTitleForm").value="{title}"')
                #カテゴリ設定
                driver2.execute_script(f'arguments[0].value = {category}', driver2.find_element_by_name('category'))
                # 商品の状態
                Select(driver2.find_element_by_name('istatus')).select_by_visible_text(new_old)
                # 商品説明
                try:
                    driver2.find_element_by_id('aucHTMLtag').click()
                except Exception as e:
                    pass
                description  = description.replace('\"','\'')
                driver2.execute_script(f'document.getElementsByName("Description_plain_work")[0].value = "{description}";')
                # 発送元の地域
                Select(driver2.find_element_by_name("loc_cd")).select_by_visible_text(location)
                # 送料負担
                if shipping_charge == '落札者':
                    Select(driver2.find_element_by_id("auc_shipping_who")).select_by_index(1)
                else:
                    Select(driver2.find_element_by_id("auc_shipping_who")).select_by_index(0)
                # 配送方法
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

                # 支払いから発送までの日数
                Select(driver2.find_element_by_name("shipschedule")).select_by_index(send_days)
                # 販売形式
                driver2.find_element_by_xpath('//*[@id="js-PCPremiumSalesmodeArea"]/div[2]/label[1]').click()
                # 開始価格
                driver2.execute_script(f'document.getElementById("auc_StartPrice_auction").value={start_price}')
                # 即決価格
                driver2.execute_script(f'document.getElementById("auc_BidOrBuyPrice_auction").value={prompt_decision_price}')
                # 終了する日時
                Select(driver2.find_element_by_id("ClosingYMD")).select_by_index(shipping_end)
                Select(driver2.find_element_by_id("ClosingTime")).select_by_index(shipping_time)
                # 自動再出品
                try:
                    driver2.find_element_by_xpath('//dt[text()="自動再出品を設定する"]').click()
                    Select(driver2.find_element_by_id("numResubmit")).select_by_index(relist)
                except Exception as e:
                    driver2.find_element_by_xpath('//dt[text()="自動再出品を設定する"]').click()
                    Select(driver2.find_element_by_id("numResubmit")).select_by_index(relist)
                # オプション
                driver2.find_element_by_class_name('HeaderExpand__title').click()
                if not driver2.find_element_by_name('AutoExtension').is_selected():
                    driver2.find_element_by_xpath('//span[text()="終了時間を自動延長する"]').click()
                if not driver2.find_element_by_name('minBidRating').is_selected():
                    driver2.find_element_by_xpath('//span[text()="総合評価で入札を制限する"]').click()
                if not driver2.find_element_by_name('badRatingRatio').is_selected():
                    driver2.find_element_by_xpath('//span[text()="悪い評価の割合で入札を制限する"]').click()
                if not driver2.find_element_by_name('bidCreditLimit').is_selected():
                    driver2.find_element_by_xpath('//span[text()="認証の有無で入札を制限する"]').click()
                if driver2.find_element_by_name('salesContract').is_selected():
                    driver2.find_element_by_xpath('//span[text()="出品者情報を手動で開示する"]').click()
                if driver2.find_element_by_id('js-PCPremiumRetpolicyCheck').is_selected():
                    driver2.find_element_by_xpath('//span[text()="返品を受け付ける"]').click()
                driver2.find_element_by_class_name('Button--proceed').click()
                driver2.find_element_by_id('auc_preview_submit_up').click()
                driver2.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")
            except Exception as e:
                logger.info(e)
                driver2.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")
        driver2.quit()
        logger.info('出品完了')
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
                    if '都' in location:
                        p = r'(.*)都'
                        location = re.search(p, location).group(1)
                        location = location + '都'
                    elif '県'in location:
                        p = r'(.*)県'
                        location = re.search(p, location).group(1)
                        location = location + '県'
                except Exception as e:
                    pass
                shipping_charge = item[31]
                new_old = item[36]
                relist = item[46]
                if item[59] == '3日～7日':
                    send_days = 3
                elif item[59] == '2日～3日':
                    send_days = 2
                elif item[59] == '1日～2日':
                    send_days = 1
                else:
                    send_days = 3
                shipping_method = item[60]
                shipping_fee = item[61]
                # 出品画像を貼り付け
                driver3.find_element_by_id('selectFile').send_keys(os.path.abspath(f'image/{img}'))
                # 出品タイトルを設定
                title  = title.replace('\"','\'')
                driver3.execute_script(f'document.getElementById("fleaTitleForm").value="{title}"')
                #カテゴリ設定
                driver3.execute_script(f'arguments[0].value = {category}', driver3.find_element_by_name('category'))
                # 商品の状態
                Select(driver3.find_element_by_name('istatus')).select_by_visible_text(new_old)
                # 商品説明
                try:
                    driver3.find_element_by_id('aucHTMLtag').click()
                except Exception as e:
                    pass
                description  = description.replace('\"','\'')
                driver3.execute_script(f'document.getElementsByName("Description_plain_work")[0].value = "{description}";')
                # 発送元の地域
                Select(driver3.find_element_by_name("loc_cd")).select_by_visible_text(location)
                # 送料負担
                if shipping_charge == '落札者':
                    Select(driver3.find_element_by_id("auc_shipping_who")).select_by_index(1)
                else:
                    Select(driver3.find_element_by_id("auc_shipping_who")).select_by_index(0)
                # 配送方法
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
                # 支払いから発送までの日数
                Select(driver3.find_element_by_name("shipschedule")).select_by_index(send_days)
                # 販売形式
                driver3.find_element_by_xpath('//*[@id="js-PCPremiumSalesmodeArea"]/div[2]/label[1]').click()
                # 開始価格
                driver3.execute_script(f'document.getElementById("auc_StartPrice_auction").value={start_price}')
                # 即決価格
                driver3.execute_script(f'document.getElementById("auc_BidOrBuyPrice_auction").value={prompt_decision_price}')
                # 終了する日時
                Select(driver3.find_element_by_id("ClosingYMD")).select_by_index(shipping_end)
                Select(driver3.find_element_by_id("ClosingTime")).select_by_index(shipping_time)
                # 自動再出品
                try:
                    driver3.find_element_by_xpath('//dt[text()="自動再出品を設定する"]').click()
                    Select(driver3.find_element_by_id("numResubmit")).select_by_index(relist)
                except Exception as e:
                    driver3.find_element_by_xpath('//dt[text()="自動再出品を設定する"]').click()
                    Select(driver3.find_element_by_id("numResubmit")).select_by_index(relist)
                # オプション
                driver3.find_element_by_class_name('HeaderExpand__title').click()
                if not driver3.find_element_by_name('AutoExtension').is_selected():
                    driver3.find_element_by_xpath('//span[text()="終了時間を自動延長する"]').click()
                if not driver3.find_element_by_name('minBidRating').is_selected():
                    driver3.find_element_by_xpath('//span[text()="総合評価で入札を制限する"]').click()
                if not driver3.find_element_by_name('badRatingRatio').is_selected():
                    driver3.find_element_by_xpath('//span[text()="悪い評価の割合で入札を制限する"]').click()
                if not driver3.find_element_by_name('bidCreditLimit').is_selected():
                    driver3.find_element_by_xpath('//span[text()="認証の有無で入札を制限する"]').click()
                if driver3.find_element_by_name('salesContract').is_selected():
                    driver3.find_element_by_xpath('//span[text()="出品者情報を手動で開示する"]').click()
                if driver3.find_element_by_id('js-PCPremiumRetpolicyCheck').is_selected():
                    driver3.find_element_by_xpath('//span[text()="返品を受け付ける"]').click()
                driver3.find_element_by_class_name('Button--proceed').click()
                driver3.find_element_by_id('auc_preview_submit_up').click()
                driver3.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")
            except Exception as e:
                logger.info(e)
                driver3.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")   
        driver3.quit()
        logger.info('出品完了')
    except Exception as e:
        logger.info(e)



def main():
    p0 = multiprocessing.Process(target=listing_item)
    p1 = multiprocessing.Process(target=listing_item2)
    p2 = multiprocessing.Process(target=listing_item3)
    
    # プロセス開始
    p0.start()
    time.sleep(4)
    p1.start()
    time.sleep(4)
    p2.start()
  
    # プロセス終了待ち合わせ
    p0.join()
    p1.join()
    p2.join()
    

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    freeze_support()
    main()