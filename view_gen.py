from multiprocessing.dummy import Pool as ThreadPool
from selenium import webdriver
from random import randrange
import time

class Browser:
    def __init__(self):
        # driver
        self.path = '/home/mik/Games/drivers/chromedriver'
        # options to set chrome to headless mode and to mute audio
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_experimental_option("prefs", {"profile.default_content_setting_values.geolocation" :2})
        #options.add_argument("user-agent=Mozilla/4.0 (compatible; MSIE 5.0; Windows NT; DigExt; YComp 5.0.2.6)")
        options.add_argument("--mute-audio")
        self.options = options

        # proxy list
        self.proxy_list = open("ip.lst").read().splitlines()
        #self.browser = webdriver.Chrome(self.path, chrome_options=options)

    def set_params(self, views, retention):
        self.views = views
        self.retention = retention

    def generate(self, url):
        loc = self.proxy_list[randrange(0,len(self.proxy_list))]
        self.options.add_argument('--proxy-server=%s' % loc)
        browser = webdriver.Chrome(self.path, options=self.options)
        for i in range(views):
            print ("generating view from {}".format(loc))
            browser.get(url)
            time.sleep(retention)
        browser.close()

if __name__ == "__main__":
    browser = Browser()

    url = input("\%PASTE URL\%\n")
    urls = [url]*4

    views = int(input("#views? "))
    retention = int(input("audience retention? (seconds) "))
    browser.set_params(views, retention)

    pool = ThreadPool(4)
    pool.map(browser.generate, urls)
    pool.close()
    pool.join()
