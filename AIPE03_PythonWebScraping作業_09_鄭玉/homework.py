from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os

def comic_dowmload(url):
    save_dir = "./homework_manga"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"已建立資料夾: {save_dir}")
        options = webdriver.ChromeOptions()


    options.add_experimental_option('excludeSwitches', ["enable-automation"])
    options.add_experimental_option('useAutomationExtension' , False)
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36")

    options.add_argument('--disable-blink-features=AutomatoinControlled')

    driver = webdriver.Chrome(options=options)

    url = 'https://www.mangaz.com/book/detail/157901' 
    driver.get(url)

    button = driver.find_element(By.CSS_SELECTOR,'button.open-viewer.book-begin.ga')
    button.click()

    all_windows = driver.window_handles

    driver.switch_to.window(all_windows[-1])
    Read_Now = driver.find_element(By.PARTIAL_LINK_TEXT,'すぐに読む')

    Read_Now.click()

    wait_element = WebDriverWait(driver,10)


    total_image_count = 0


    while True:


        image_elements = driver.find_elements(By.CSS_SELECTOR,'div.page_image img.image')

        for img_element in image_elements:

            if img_element.is_displayed():
                file_path = f"manga_page_{total_image_count}.png"


                img_element.screenshot(f"./homework/{file_path}")

                print(f"成功擷取頁面並儲存為: {file_path}")

                total_image_count += 1

        try:

            next_page = wait_element.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div.flip.flip-left')))

            next_page.click()

            print("已點擊下一頁，等待畫面載入...")


            time.sleep(10)

        except TimeoutException:

            print("【系統提示】找不到下一頁按鈕，已達最後一頁，結束爬取迴圈。")
            break
        driver.quit()

def main():
    user_input = input("請輸入下載漫畫的網址")
    comic_dowmload(user_input)

if __name__ == "__main__":
    main()
    