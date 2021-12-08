# Formatted and Linted with Black
# All code is trash, especially this.
# Read NOTES TO USERS for more info.
# ========================================
from datetime import datetime as dt
from inspect import stack
from itertools import islice
from json import dump, load
from logging import (
    basicConfig as lbc,
    StreamHandler as lsh,
    debug as l0,
    info as l1,
    warning as l2,
    error as l3,
    critical as l4,
)
from os import environ as env, listdir, remove, replace
from pathlib import Path
from random import choice, randint, uniform
from re import sub, search, compile
from string import ascii_letters as abc
from subprocess import check_call as subp
from sys import exit as xit, executable as xec
from time import sleep
from uuid import uuid4 as uu
from zipfile import ZipFile as zf

try:
    from bs4 import BeautifulSoup as bs
except ModuleNotFoundError:
    subp([xec, "-m", "pip3", "install", "beautifulsoup4"])
    # TODO: Lint Ignore
    from bs4 import BeautifulSoup as bs

try:
    from dotenv import load_dotenv as dotenv
except ModuleNotFoundError:
    subp([xec, "-m", "pip3", "install", "python-dotenv"])
    # TODO: Lint Ignore
    from dotenv import load_dotenv as dotenv

try:
    from selenium import webdriver as wd
except ModuleNotFoundError:
    subp([xec, "-m", "pip3", "install", "selenium"])
    # TODO: Lint Ignore
    from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service as sv
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wdw

try:
    from selenium_stealth import stealth as shh
except ModuleNotFoundError:
    subp([xec, "-m", "pip3", "install", "selenium-stealth"])
    # TODO: Lint Ignore
    from selenium_stealth import stealth as shh

DIR_ROOT = Path(__file__).resolve(strict=1).parent
DIR_DATA = f"{DIR_ROOT}/data/"
DIR_LOGS = f"{DIR_ROOT}/logs/"
DIR_HTML = f"{DIR_ROOT}/html/"
PROXY_ZIP = f"{DIR_ROOT}/botproxy.zip"
CHROME_DRIVER = f"{DIR_ROOT}/chrome"
DOT_ENV = dotenv(f"{DIR_ROOT}/.env")


class Angel:
    """

    NOTES TO USERS:
    ==============
    1. Angel List goes to extreme lenths to keep bots out.
    Most annoying of all - they change up all there html struncture and tag values every couple days.
    Even if your bot is perfect, it will be useless shit in less than a week.
    I grew tired of the project after the third push in less than a week and open sourced it.
    If someone was to work on this with me I'd be more than happy to help but its become a drain of a project for me with no pay off.
    Hope someone finds a use for this.


    2. I went out of my way to make this slow and human-like.
    (for example: def zzz(), def web_type(), and def duckit() + many others)
    If you want something fast, go elsewhere.
    It would be better to create from scratch instead of trying to change this.

    PRE-REQUISITES:
    ===============
        1. Add 2Captcha plugin to (recommended unused) chrome-profile and set to auto-solve
        ... Cost: $0.76 per 1000 CAPTCHAS and $2.99 per 1000 reCAPTCHAS
        ... Link: https://chrome.google.com/webstore/detail/2captcha-solver/ifibfemgeogfhoebkmokieepdoobkbpo?hl=en
        2. Create Botproxy subscription
        ... Cost: $10/month
        ... Note: I had to use 3rd party auth. Normal doesnt work.
        ... Note: You'll also need funds in PayPal ... annoying, I know.
        ... Link: https://botproxy.net/accounts/signup/
        3. Configure Angel list profile
        ... Note: Make sure to create a filtered search
        ... Link: https://angel.co/join
        4. Fill in .env-sample variables and remove '-sample'
        5. Adjust __SETTINGS__ variables

    HOW TO RUN:
    ===========
        while in ROOT, run:
        >>> python3 angel.py

    HOW TO CONTRIBUTE:
    ==================
        1. Search for "TODO:" for specifics.
        2. Its hard to distinguish between different iFrames
        such as is used for bocked, captcha, and cloudflare.
        Each of the above requires a unique response. I've
        only been able try sleeping long enough for anti-captcha
        to work. if it doesnt work in time then I assume im blocked.
        If it does work, the sleep will often have a lot of time left.
        3. HTML structure is always changing. Will need to update pretty consistenly.
    """

    # INIT SECTION
    ##############
    def __init__(self):
        self.log_config()
        self.log_clean()
        self.__SETTINGS__()
        self.main()

    def __SETTINGS__(self):
        self.log_start(extra=1)
        # PROJECT SETTINGS
        ##################
        self.LIVE = 0
        self.CLICK_ANGEL = 1
        self.SEND_APPLICATIONS = 0
        # Best not to change self.NUMER or self.RETRIES
        # self.DENOM determines how many applications to send per run
        self.NUMER, self.DENOM = 0, randint(10, 20)
        self.RETRIES = 0
        # LOCATING DATAFILE
        ###################
        if not self.LIVE and not self.SEND_APPLICATIONS:
            self.DATAFILE = f"{DIR_DATA}applied-test.json"
        elif self.LIVE and not self.SEND_APPLICATIONS:
            self.DATAFILE = f"{DIR_DATA}applied-staging.json"
        elif self.LIVE and self.SEND_APPLICATIONS:
            self.DATAFILE = f"{DIR_DATA}applied-live.json"
        self.APPLIED = self.json_load(self.DATAFILE)
        # BROWSER CONFIG
        ################
        # Configured for MacOS
        # Advised to keep 'self.CLICK_ANGEL = 0' until confirmed correct.
        self.CHROME_PATH = "/Users/home/Library/Application Support/Google/Chrome/"
        # Advised to keep 'self.CLICK_ANGEL = 0' until confirmed correct.
        self.CHROME_PROFILE = "Profile 3"
        # Don't change this. It's the only option for slenium_stealth
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36"
        # BOT PROXY INFO
        #################
        self.PROXY_HOST = "x.botproxy.net"
        self.PROXY_PORT = 8080
        self.PROXY_USER = env.get("MY_BOTPROXY_USERNAME_IS")
        self.PROXY_PASS = env.get("MY_BOTPROXY_PASSWORD_IS")
        # ANGEL LIST INFO
        ##################
        self.EMAIL = env.get("MY_ANGEL_EMAIL_IS")
        self.PASSWORD = env.get("MY_ANGEL_PASSWORD_IS")
        # PERSONAL INFO
        ###############
        self.PHONE = env.get("MY_PHONE_NUMBER_IS")
        self.FULL_NAME = env.get("MY_FULL_NAME_IS")
        # PROFESIONAL INFO
        ###################
        self.TITLE = env.get("MY_CURRENT_TITLE_IS")
        self.REGION = env.get("I_LIVE_IN")
        self.EXPERIENCE = env.get("I_HAVE_N_YEARS_EXPERIENCE")
        # PUBLIC INFO
        ##############
        self.PORTFOLIO = env.get("MY_PORTOFILO_WEBSITE_IS")
        self.GITHUB = env.get("MY_GITHUB_PROFILE_IS")
        self.LINKEDIN = env.get("MY_LINKEDIN_PROFILE_IS")
        # SITE FEATURES SECTION
        #######################
        # Angel List constantly changes tag and class values
        # Probably to keep out ... ha. ha.
        # Best to store them here for quick changes when needed.
        self.COS_TAG = "data-test"
        self.COS_VALUE = "StartupResult"
        self.LISTING_CLASS = compile("styles_jobListingList__*")
        self.LOGIN_TITLE = "Log In | AngelList"
        self.JOBS_TITLE = "Startup Jobs | AngelList Talent"
        self.FRAME_TITLE = "angel.co"

    def main(self):
        self.log_start(extra=1)
        if self.LIVE:
            self.live()
        else:
            self.test()

    def live(self):
        self.log_start(extra=1)
        l2(f"SEND_APPLICATIONS IS SET TO: {self.SEND_APPLICATIONS}")
        self.web()
        self.duckit()
        self.end()

    def test(self):
        self.log_start(extra=1)

        main = self.bs_read("main")
        apply = self.bs_read("apply")

        self.json_dump({}, self.DATAFILE)
        while 1:
            # COMPANIES SECTION
            ####################
            cos = self.cos_get(main)
            cos = self.cos_lst(cos)
            jobs_lst = []
            for co in cos:
                # COMPANY SECTION
                ##################
                dct = self.co_dct(co)
                print(dct)
                print("\n" * 4)
                co = self.co_get(co)
                # JOBS SECTION
                ##############
                jobs = self.jobs_get(co)
                for job in jobs:
                    jobs_lst.append(job)
                    try:
                        # JOB SECTION
                        ##############
                        spans = self.job_get_spans(job)
                        dct = self.job_dct(dct, spans)
                        # APPLICATION SECTION
                        #####################
                        dct = self.apply_dct(dct, apply)

                        self.update(dct)
                    except Exception as e:
                        print(e)
        r = self.json_load(self.DATAFILE)
        ids = len(list(set([r[i]["ids"] for i in r])))
        if ids == len(r):
            print("UNIQUE IDS PASS")
        else:
            print("UNIQUE IDS FAIL")

    ##############################
    # MAIN PROJECT SECTION BEGIN #
    ##############################

    # ENTRY SECTION
    ###############
    def duckit(self):
        self.log_start(extra=1)
        url = "duckduckgo.com/?q=Angel+List+Login&t=h_&ia=web"
        html = self.web_go(url=url, get=1)
        if self.CLICK_ANGEL:
            self.bs_click(html, key="href", val="https://angel.co/login")
            self.router()

    # ROUTER SECTION
    ################
    def router(self):
        self.log_start(extra=1)

        title = self.bs_title()

        if title == self.LOGIN_TITLE:
            self.login()

        elif title == self.JOBS_TITLE:
            self.router_jobs()

        elif title == self.FRAME_TITLE:
            self.router_frame()

        else:
            self.bs_save("unknown")
            self.retry()

    def router_jobs(self):
        self.log_start()
        self.send_cancels()
        self.cos()

    def router_frame(self):
        self.log_start()
        self.zzz(mn=30, mx=60)

        title = self.bs_title()
        if title == self.FRAME_TITLE:
            self.retry()
        else:
            self.router()

    # LOGIN SECTION
    ###############
    def login(self):
        self.log_start(extra=1)
        try:
            html = self.bs_html()
            self.login_username(html)
            self.login_password(html)
            self.login_click(html)
            self.cos()
        except Exception as e:
            self.log_except(e)
            self.router()

    def login_username(self, html):
        self.log_start()
        email_box = self.bs_element(html, key="id", val="user_email")
        self.web_type(email_box, self.EMAIL)

    def login_password(self, html):
        self.log_start()
        password_box = self.bs_element(html, key="id", val="user_password")
        self.web_type(password_box, self.PASSWORD)

    def login_click(self, html):
        self.log_start()
        self.bs_click(html, key="name", val="commit")

    # COMPANIES SECTION
    ####################
    def cos(self):
        self.log_start(extra=1)
        while 1:
            self.zzz(mn=7, mx=12)
            self.web_scroll()
            html = self.bs_html()
            cos = self.cos_get(html)
            cos = self.cos_lst(cos)
            if cos:
                self.cos_loop(cos)
            else:
                self.router()

    def cos_get(self, html):
        self.log_start()
        cos = html.find_all(attrs={self.COS_TAG: self.COS_VALUE})
        return cos

    def cos_lst(self, cos):
        self.log_start()
        cos = [co for co in cos if not self.promotion(co)]
        return cos

    def cos_loop(self, cos):
        _name_ = self.log_start()
        count = 0
        for co in cos:
            count += 1
            l0(f"{_name_} status: {count}/{len(cos)}")
            self.co(co)

    # COMPANY SECTION
    ##################
    def co(self, co):
        self.log_start(nap=1, extra=1)
        dct = self.co_dct(co)
        co = self.co_get(co)
        self.jobs(co, dct)

    def co_dct(self, co, dct={}):
        self.log_start()
        dct["employer"] = self.employer(co)
        dct["description"] = self.description(co)
        dct["employees"] = self.employees(co)
        return dct

    def co_get(self, co):
        self.log_start()
        co = co.find_all("div", {"class": self.LISTING_CLASS})[0]
        co = co.find_all("div")[0]
        return co

    # JOBS SECTION
    ##############
    def jobs(self, co, dct):
        self.log_start(extra=1)
        jobs = self.jobs_get(co)
        self.jobs_loop(jobs, dct)

    def jobs_get(self, co):
        self.log_start()
        children = self.bs_children(co)
        jobs_class = self.jobs_get_class(children)
        jobs = co.find_all("div", {"class": jobs_class})
        return jobs

    def jobs_get_class(self, jobs):
        self.log_start()
        for job in jobs:
            job_class = job.find_all("div")[0]["class"]
            yield job_class[0]

    def jobs_loop(self, jobs, dct):
        self.log_start()
        for job in jobs:
            try:
                self.job(job, dct)
            except Exception as e:
                self.log_except(e)
                self.send_cancels()

    # JOB SECTION
    ##############
    def job(self, job, dct):
        self.log_start(extra=1)
        spans = self.job_get_spans(job)
        dct = self.job_dct(dct, spans)
        if dct["id"] not in self.APPLIED:
            self.apply(job, dct)

    def job_dct(self, dct, spans):
        self.log_start()
        dct["role"] = self.role(spans)
        dct["salary"], dct["equity"] = self.payment(spans)
        dct["time"] = f"{dt.now()}"
        dct["id"] = self.identify(dct)
        return dct

    def job_get_spans(self, job):
        self.log_start()
        link = job.find_all("a")[0]
        div = link.find_all("div")[0]
        spans = div.find_all("span")
        return spans

    # APPLICATION SECTION
    #####################
    def apply(self, job, dct):
        self.log_start(extra=1)

        self.bs_click(job, key="button")
        self.zzz(mn=5, mx=10)

        html = self.bs_html()

        dct = self.apply_dct(dct, html)
        self.send(dct, html)

    def apply_dct(self, dct, html):
        self.log_start()
        dct["contact"] = self.contact(html)
        dct["message"] = self.message(dct)
        return dct

    # SEND SECTION
    ###############
    def send(self, dct, html):
        self.log_start(extra=1)
        self.send_text(html, dct["message"])
        if self.SEND_APPLICATIONS:
            self.bs_click(html, key="button", n=-1)
        else:
            self.send_cancel()
        self.update(dct)

    def send_text(self, html, message):
        self.log_start()
        textarea = self.bs_element(html, key="textarea")
        self.web_type(textarea, message)

    def send_cancel(self):
        self.log_start(nap=1)
        html = self.bs_html()
        self.bs_click(html, key="button", n=-2)

    def send_cancels(self):
        self.log_start(nap=1)
        html = self.bs_html()
        b = self.bs_element(html, key="button", n=-2)
        try:
            while 1:
                l2("Throwing wild click cancel")
                inner_html = b.get_attribute("innerHTML")
                l1("grabbed inner html")
                inner_soup = bs(inner_html, "html.parser")
                l1("parsed inner html")
                text = inner_soup.find(text=1)
                l1("grabbed inner text")
                text = self.str_clean(text)
                l1(f"cleaned inner text: {text}")
                if text == "Cancel":
                    l1(f"clicking cancel")
                    self.bs_click(html, key="button", n=-2)
                    assert 1
                else:
                    assert 0
        except:
            pass

    # UPDATE SECTION
    ################
    def update(self, dct):
        self.log_start(extra=1)
        self.update_applied(dct)
        self.update_datafile()
        self.update_numer()

    def update_applied(self, dct):
        self.log_start()
        self.APPLIED[dct["id"]] = dct
        l0(f"updated application data: {dct}")

    def update_datafile(self):
        self.log_start()
        self.json_dump(self.APPLIED, self.DATAFILE)
        l0(f"updated {self.DATAFILE}")

    def update_numer(self):
        self.log_start()
        self.NUMER += 1
        l2(f"updated numer: {self.NUMER}/{self.DENOM}")
        if self.NUMER == self.DENOM:
            self.end()

    # ERROR SECTION
    ################
    def retry(self, mx=3):
        self.log_start(extra=1)
        self.RETRIES += 1
        if self.RETRIES <= mx:
            self.driver.quit()
            self.main()
        else:
            l4("RETRIED TOO MANY TIMES")
            self.end()

    def end(self):
        self.log_start(extra=1)
        if self.LIVE:
            self.driver.quit()
        xit()

    ###################################
    # PROJECT HELPERS AND UTILS BEGIN #
    ###################################

    # COMPANY DICT HELPERS
    ######################
    def promotion(self, co):
        self.log_start()
        e = bool(search("Promoted", co.prettify()))
        return e

    def employer(self, co):
        self.log_start()
        e = co.find_all("h2")[0].string
        e = self.str_clean(e)
        return e

    def description(self, co):
        self.log_start()
        e = co.find_all("span")[0].string
        e = self.str_clean(e)
        return e

    def employees(self, co):
        self.log_start()
        e = co.find_all("span")[1]
        e = e.contents[0].string
        e = self.str_clean(e)
        return e

    def role(self, spans):
        self.log_start()
        role = self.str_clean(spans[0].string)
        return role

    def identify(self, dct):
        self.log_start()
        identify = str(dct["employer"] + "---" + dct["role"])
        return identify

    def payment(self, spans):
        self.log_start()
        # for i in range(len(spans)):
        #     print(i, "*" * 100)
        #     print(spans[i])
        payment = spans[-1].string.split(" • ")
        salary = self.str_clean(payment[0])
        equity = self.str_clean(payment[1])
        return salary, equity

    def contact(self, html):
        self.log_start()
        form = html.find_all("form")[-1]
        h4 = form.find_all("h4")[0].string
        full = h4.replace("Your hiring contact is ", "")
        full = self.str_clean(full)
        first = full.split(" ")[0]
        return first

    def message(self, dct):
        self.log_start()

        hour = int(str(dt.now().time()).split(":")[0])
        weekday = int(dt.today().weekday())

        greeting = self.greeting(dct["contact"], hour)
        warmer = self.warmer(hour, weekday)
        intro = self.intro()
        body = self.body(dct["role"])
        closer = self.closer()
        footer = self.footer()

        message = f"{greeting}{warmer}\n\n{intro}{body}\n\n{closer}\n\n{footer}"
        return message

    # COMPANY MESSAGE HELPERS
    #########################
    def greeting(self, contact, hour):
        self.log_start()

        greetings = [
            f"Hey {contact}, ",
            f"Hello {contact}, ",
        ]
        if 4 <= hour <= 10:
            greetings.append(f"Good morning {contact}, ")
        elif 13 <= hour <= 16:
            greetings.append(f"Good afternoon {contact}, ")
        elif 18 <= hour <= 19:
            greetings.append(f"Good evening {contact}, ")
        greeting = choice(greetings)
        return greeting

    def warmer(self, hour, weekday):
        self.log_start()

        # The first one is blank on purpose.
        warmers = [
            "",
            "I hope this message finds you well. ",
        ]
        adj = choice([" great ", "n excellent "])
        having = "I hope you're having a" + adj
        had = "I hope you've had a" + adj
        if 10 <= hour <= 15:
            warmers.append(f"{having}day. ")
        elif 16 <= hour <= 19:
            warmers.append(f"{had}day. ")

        if weekday == 0:
            warmers.append(f"{had}weekend. ")
        elif weekday in [1, 2, 3, 4]:
            warmers.append(f"{having}week. ")
        elif weekday in [5.6]:
            warmers.append(f"{having}weekend. ")
        warmer = choice(warmers)
        return warmer

    def intro(self):
        self.log_start()

        intros = [
            f"My name is {self.FULL_NAME}. ",
            f"My name is {self.FULL_NAME}. I'm a {self.TITLE} with {self.EXPERIENCE} years of experience. ",
            f"My name is {self.FULL_NAME}. I'm a {self.TITLE} based out of {self.REGION} with {self.EXPERIENCE} years of experience. ",
        ]
        intro = choice(intros)
        return intro

    def body(self, role):
        self.log_start()

        l2("TODO: add more bodies")
        bodies = [
            f"""I'm reaching out in response to the opening you posted for '{role}' - It looks like I'd be a great fit! Plus, it seems like you guys have a pretty cool mission and I'd love to be a part of it.""",
            f"""I saw you had an openning for '{role}'. I'd love to learn more about what the role entails and see if I'd be a good fit to help you guys out.""",
        ]
        body = choice(bodies)
        return body

    def closer(self):
        self.log_start()

        l2("TODO: add more closers")
        closers = [
            f"If interested in learning more or reaching out, I've attatched a few helpful links and my contact information below. \n\nThank you for your time,\n\n- {self.FULL_NAME}",
        ]
        closer = choice(closers)
        return closer

    def footer(self):
        self.log_start()

        email = f"Email address - {self.EMAIL}"
        phone = f"Phone number - {self.PHONE}"
        portfolio = f"Portfolio - https://{self.PORTFOLIO}"
        github = f"GitHub - https://github.com/{self.GITHUB}"
        linkedin = f"LinkedIn - https://www.linkedin.com/in/{self.LINKEDIN}/"
        footer = f"{email}\n{phone}\n\n{portfolio}\n{github}\n{linkedin}"

        return footer

    ###################################
    # GENERAL HELPERS AND UTILS BEGIN #
    ###################################

    # BOTPROXY CONFIG
    #################
    def proxy_manifest_json(self):
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """
        return manifest_json

    def proxy_background_js(self):
        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (
            self.PROXY_HOST,
            self.PROXY_PORT,
            self.PROXY_USER,
            self.PROXY_PASS,
        )
        return background_js

    # SELENIUM CONFIG
    #################
    def web(self):
        self.log_start()
        self.web_options()
        self.web_driver()
        self.web_action()
        self.web_shh()
        self.web_clear()

    def web_options(self):
        self.log_start()
        self.options = wd.ChromeOptions()

        self.options.add_argument(f"--user-data-dir={self.CHROME_PATH}")
        self.options.add_argument(f"--profile-directory={self.CHROME_PROFILE}")

        with zf(PROXY_ZIP, "w") as zp:
            manifest_json = self.proxy_manifest_json()
            zp.writestr("manifest.json", manifest_json)
            background_js = self.proxy_background_js()
            zp.writestr("background.js", background_js)
        self.options.add_extension(PROXY_ZIP)
        self.options.add_argument("--user-agent=%s" % self.USER_AGENT)

        self.options.add_argument("start-maximized")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", 0)

    def web_driver(self):
        self.log_start()

        self.driver = sv(CHROME_DRIVER)
        self.driver = wd.Chrome(service=self.driver, options=self.options)
        self.driver.set_script_timeout(1000)
        self.driver.implicitly_wait(30)

    def web_action(self):
        self.log_start()
        self.action = ac(self.driver)

    def web_shh(self):
        self.log_start()
        shh(
            driver=self.driver,
            user_agent=self.USER_AGENT,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=1,
            run_on_insecure_origins=0,
        )

    def web_clear(self):
        self.log_start()
        # I think they place a blocked cookie in browser ...
        # sneaky little fuckers. Ruins the proxy rotation
        self.driver.delete_all_cookies()

    # SELENIUM HELPERS
    ##################
    def web_go(self, url, get=0, https=1):
        self.log_start()
        if https:
            self.driver.get(f"https://{url}")
        else:
            self.driver.get(f"{url}")
        if get:
            return self.bs_html()

    def web_scroll(self):
        self.log_start()
        for i in range(15):
            l0(f"{stack()[1][3]} status ({i}/15)")
            html = self.bs_html()
            body = self.bs_element(html, key="body")
            l0("Down keys to be sent.")
            body.send_keys(Keys.PAGE_DOWN)
            self.zzz()

    def web_type(self, element, txt):
        self.log_start()
        element.click()
        for char in txt:
            self.zzz(mn=0.1, mx=0.2)
            pf = [1] * 59
            pf.append(0)
            pf = choice(pf)
            if pf == 1:
                element.send_keys(char)
            else:
                element.send_keys(choice(abc))
                element.send_keys(Keys.BACK_SPACE)
                element.send_keys(char)

    # BS4 HELPERS
    #############
    def bs_children(self, element):
        self.log_start()
        elements = element.children
        for e in elements:
            if len(str(e)) > 1:
                yield bs(str(e), "html.parser")

    def bs_click(self, html, key, val=0, n=0):
        self.log_start()
        if val:
            element = html.find_all(attrs={key: val})[n]
        else:
            element = html.find_all(key)[n]
        xpath = self.bs_xpath(element)
        wdw(self.driver, 30).until(
            ec.element_to_be_clickable((By.XPATH, xpath))
        ).click()
        self.zzz()

    def bs_element(self, html, key, val=0, n=0):
        self.log_start()
        if val:
            element = html.find_all(attrs={key: val})[n]
        else:
            element = html.find_all(key)[n]
        xpath = self.bs_xpath(element)
        l0(f"grabbed xpath: {xpath}")
        element = self.driver.find_element(By.XPATH, xpath)
        l0(f"found element: {element}")
        return element

    def bs_html(self, pretty=0):
        self.log_start()
        src = self.driver.page_source
        l0("grabbed page src")
        html = bs(src, "html.parser")
        l0("parsed page src")
        if pretty:
            l0("making html pretty")
            return html.prettify()
        l0("html complete")
        return html

    def bs_read(self, page):
        self.log_start()
        f = open(f"{DIR_HTML}/{page}.html", "r")
        html = f.read()
        soup = bs(html, "html.parser")
        self.bs_save(page=page, html=soup)
        return soup

    def bs_save(self, page, html=0):
        self.log_start()
        if html:
            html = html.prettify()
        else:
            html = self.bs_html(pretty=1)
        with open(f"{DIR_HTML}{page}.html", "w") as fout:
            fout.write(html)

    def bs_title(self):
        html = self.bs_html(pretty=1)
        soup = bs(html, "html.parser")
        title = soup.title.string
        title = self.str_clean(str(title))
        return title

    def bs_xpath(self, element):
        self.log_start()
        """
        Generate xpath of soup element
        :param element: bs4 text or node
        :return: xpath as string
        """
        components = []
        child = element if element.name else element.parent
        for parent in child.parents:
            """
            @type parent: bs4.element.Tag
            """
            previous = islice(parent.children, 0, parent.contents.index(child))
            xpath_tag = child.name
            xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
            components.append(
                xpath_tag if xpath_index == 1 else "%s[%d]" % (xpath_tag, xpath_index)
            )
            child = parent
        components.reverse()
        return "/%s" % "/".join(components)

    # LOGGING HELPERS
    #################
    def log_config(self):
        t = str(dt.now()).split(".")[0].replace(" ", "@")
        lbc(
            filename=f"{DIR_LOGS}{t}.log",
            encoding="utf-8",
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d@%H:%M:%S",
            level=0,
        )
        lsh().setLevel(0)

    def log_clean(self, store=3):
        self.log_start()
        logs = listdir(DIR_LOGS)
        names = []
        for i in range(len(logs)):
            names.append(str(logs[i]).split(".")[0])
        names.sort(key=lambda date: dt.strptime(date, "%Y-%m-%d@%H:%M:%S"))
        keepers = names[-store:]
        for f in logs:
            name = str(f).split(".")[0]
            if name not in keepers:
                remove(f"{DIR_LOGS}{f}")

    def log_start(self, nap=0, extra=0, n=3):
        if extra:
            look = ">" * 45
        else:
            look = ">" * 15

        name = str(stack()[1][n])
        l0(f"{look} starting {name} ")
        if nap:
            self.zzz()
        return name

    def log_except(self, e):
        look = "!" * 15
        return l3(f"{look} error at {stack()[1][3]}: {e}")

    # JSON HELPERS
    ##############
    def json_dump(self, content, dest):
        self.log_start()
        pth = f"{DIR_ROOT}/{uu()}{uu()}.json"
        with open(pth, "w") as f:
            dump(content, f, indent=4)
        try:
            with open(pth) as f:
                q = load(f)
            replace(pth, dest)
        except:
            remove(pth)

    def json_load(self, pth):
        self.log_start()
        try:
            with open(pth, "r") as json_file:
                data = load(json_file)
        except FileNotFoundError as e:
            self.log_except(e)
            data = {}
            self.json_dump(data, pth)
        return data

    # OTHER
    #######
    # string cleaning hahaha .. get it? like sPring cleaning hahaha!
    def str_clean(self, s, json=0):
        self.log_start()
        s = sub(r"…", "...", s)
        s = sub(r"[`‘’‛⸂⸃⸌⸍⸜⸝]", "'", s)
        s = sub(r"[„“]|(\'\')|(,,)", '"', s)
        s = sub(r"\s+", " ", s).strip()
        if json:
            l0("cleaning json")
            s = s.replace("'", '"')
        return s

    def zzz(self, mn=1, mx=5):
        t = round(uniform(mn, mx), 7)
        if t > 5:
            l0(f"sleeping for {t}")
        sleep(t)


if __name__ == "__main__":
    Angel()
