from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


# python3.10 -m pip install selenium

class Catizen:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--log-level=3')

        self.driver = webdriver.Chrome(options=chrome_options)

        self.urls = []

        self.timer = 60*20


    def load_script(self, window_index):
        self.driver.switch_to.window(window_index)
        script = "function enable_auto(){try{window['DialogManager']['_instance']['_mainDlgs'][0]['buyAuto']();} catch (error) {setTimeout(enable_auto, 5000);}};enable_auto();"
        self.driver.execute_script(script)


    def login_to_replit(self, email, password):
        self.driver.get('https://replit.com/login')

        username_field=self.driver.find_element(By.NAME, 'username')
        username_field.send_keys(email)
        password_field=self.driver.find_element(By.NAME, 'password')
        password_field.send_keys(password)

        login_button = self.driver.find_element(By.CSS_SELECTOR, '[data-cy="log-in-btn"]')
        login_button.click()
        self.driver.implicitly_wait(10)


    def print_time(self, sec):
        h = sec//3600
        if h<10: h = f'0{h}'
        m = (sec%3600)//60
        if m<10: m = f'0{m}'
        s = sec%60
        if s<10: s = f'0{s}'
        print(f" < {h}:{m}:{s} >", end='\r')

    def load_urls(self):
        with open('urls.txt') as f:
            urls = f.readlines()
        for i in range(len(urls)): urls[i] = urls[i].strip()
        self.urls = urls
    
    def sleep(self, sec):
        for i in range(sec, -1, -1):
            self.print_time(i)
            time.sleep(1)
        print()

    def open_tabs(self):
        self.driver.switch_to.window(self.driver.window_handles[0])
        for url in self.urls:
            self.driver.execute_script(f"window.open('{url}');")
            time.sleep(3)
    
    def close_tabs(self):
        for tab_index in range(len(self.urls), 0, -1):
            self.driver.switch_to.window(self.driver.window_handles[tab_index])
            self.driver.close()
            time.sleep(1)
    
    def run_script_on_tabs(self):
        for tab_index in range(len(self.urls), 0, -1):
            self.driver.switch_to.window(self.driver.window_handles[tab_index])
            script = "function enable_auto(){try{window['DialogManager']['_instance']['_mainDlgs'][0]['buyAuto']();} catch (error) {setTimeout(enable_auto, 5000);}};enable_auto();"
            self.driver.execute_script(script)
            time.sleep(1)


    def quit(self):
        self.driver.quit()

    def start(self):
        self.load_urls()
        while True:
            try:
                self.open_tabs()
                time.sleep(2)
                self.run_script_on_tabs()
                time.sleep(2)
                self.sleep(self.timer)
                self.close_tabs()
                time.sleep(2)
            except KeyboardInterrupt:
                print(" Closing !! ")
                self.quit()
                break
            except:
                print(" Error !")

    

if __name__ == '__main__':
    x=Catizen()
    x.start()
        
