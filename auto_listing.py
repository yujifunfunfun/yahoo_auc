import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from tkinter import Tk
import eel
import time
from logger import *
import csv
import re
import random

logger = set_logger(__name__)

def start_chrome():
    user_agent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    ]
    UA = user_agent[random.randrange(0, len(user_agent), 1)]

    global option
    option = Options()  
    option.add_argument("--user-data-dir=user")
    option.add_argument('--lang=ja-JP')
    option.add_argument('--user-agent=' + UA)
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-ssl-errors')
    option.add_argument('--incognito') 
    option.add_argument("window-size=1300,1000")
    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)   


def listing_item():
    try:
        driver.get("https://auctions.yahoo.co.jp/jp/show/submit?category=0")
        user = 'xwabs75553' 
        password = 'Python1998' # パスワード

        time.sleep(1)

        driver.find_element_by_id('username').send_keys(user)
        driver.find_element_by_id('btnNext').click()
        time.sleep(1)


        driver.find_element_by_id('passwd').send_keys(password)
        driver.find_element_by_id('btnSubmit').click()
        time.sleep(1)

        driver.execute_script('document.getElementById("js-ListingModal").style.display = "none";')

        with open('item.csv') as f:
            reader = csv.reader(f)
            header = next(reader)
            l = [row for row in reader]
        for item in l:
            category = item[0]
            title = item[1]
            description = item[2]
            p = r'<font color="#660000" size="3">(.*)<br><br></font><br><br></td></tr></table> </td>'
            description = re.search(p, description).group(1)
            description = description.replace('<br>','\n')
            description = re.sub('<(.*)>','',description)
            start_price = item[3]
            prompt_decision_price = item[4]
            shipping_end = item[6]
            shipping_time = [7]
            img = item[9]
            location = item[29]
            p = r'(.*) '
            location = re.search(p, location).group(1)
            shipping_charge = item[31]
            new_old = item[36]
            product_return = item[38]
            if item[59] == '3日～7日':
                send_days = '3〜7日'
            elif item[59] == '2日～3日':
                send_days = '2〜3日'
            elif item[59] == '1日～2日':
                send_days = '1〜2日'
            else:
                send_days = '3〜7日'


            shipping_method = item[60]


            driver.find_element_by_id('selectFile').send_keys(os.path.abspath(f'image/{img}'))
            driver.find_element_by_id('selectFile').send_keys(os.path.abspath(f'image/{img}'))


            driver.find_element_by_id('fleaTitleForm').send_keys(title)


            driver.execute_script(f'arguments[0].value = {category}', driver.find_element_by_name('category'))


            Select(driver.find_element_by_name('istatus')).select_by_visible_text(new_old)
        

            if product_return:
                driver.find_element_by_class_name('CheckBox__viewCheckBox').click()


            iframe = driver.find_element_by_id('rteEditorComposition0')
            driver.switch_to.frame(iframe)
            tk = Tk()
            tk.withdraw()
            tk.clipboard_clear()
            tk.clipboard_append(description)
            driver.find_element_by_id('0').send_keys(Keys.CONTROL, "v")
            driver.switch_to.default_content()

            Select(driver.find_element_by_name("loc_cd")).select_by_visible_text(location)
            
            if shipping_charge == '落札者':
                driver.find_element_by_xpath('//*[@id="FormReqrd"]/section[2]/div[6]/label[2]').click()
            else:
                driver.find_element_by_xpath('//*[@id="FormReqrd"]/section[2]/div[6]/label[1]').click()


            driver.find_elements_by_class_name('RadioExpand__item')[1].click()

            driver.find_element_by_xpath(f'//label[text()="{send_days}"]').click()

            Select(driver.find_element_by_id("ClosingYMD")).select_by_index(shipping_end)
            Select(driver.find_element_by_id("ClosingTime")).select_by_index(shipping_time)


            driver.find_element_by_id("auc_StartPrice").clear()
            driver.find_element_by_id("auc_StartPrice").send_keys(int(start_price))

            driver.find_element_by_xpath('//dt[text()="即決価格を設定する"]').click()
            driver.find_element_by_id("auc_BidOrBuyPrice").send_keys(int(prompt_decision_price))


            # logger.info('リクエスト受付中ページへ遷移しました')
            # eel.view_log_js('リクエスト受付中ページへ遷移しました')
            time.sleep(3)




    except Exception as e:
        logger.info(e)
        # eel.view_log_js('エラーが発生しました')
 





def main():
    start_chrome()
    listing_item()
        
# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()