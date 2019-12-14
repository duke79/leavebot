from pyppeteer.page import Page
from pyppeteer.browser import Browser
from pyppeteer.launcher import launch
from pyppeteer.element_handle import ElementHandle
import asyncio
import json


HEADLESS = False

class Driver:
    def __init__(self):
        self._cookies = dict()

    def _set_cookies(self, cookies):
        for cookie in cookies:
            self._cookies[cookie['name']] = cookie['value']

    async def login(self, userid, passwd, page: Page):
        login_url = 'https://llama.greythr.com/uas/portal/auth/login'
        await page.goto(login_url)
        await page.waitFor(3000)
        userid_selector = 'app-login > section > div > div > div > div:nth-child(1) > gt-icon-input > div > input'
        passwd_selector = 'app-login > section > div > div > div > div:nth-child(2) > gt-icon-input > div > input'
        login_selector = 'app-login > section > div > div > div > div:nth-child(3) > button > h6'
        
        element: ElementHandle = await page.J(userid_selector)
        await element.focus()
        await page.keyboard.type(userid)

        element: ElementHandle = await page.J(passwd_selector)
        await element.focus()
        await page.keyboard.type(passwd)

        element: ElementHandle = await page.J(login_selector)
        await element.click()
        await page.waitForSelector('#feeds')

        cookies = await page.cookies()
        self._set_cookies(cookies)


    async def apply_leave_interactively(self, page: Page, leave_options=None):
        leave_options = leave_options if leave_options else {}
        leave_url = 'https://llama.greythr.com/v2/employee/apply?key=/v2/employee/apply/leave'
        await page.goto(leave_url)
        await page.waitForNavigation()
        
        # cookies for leave page
        # cookies = await page.cookies()
        
        await page.waitForSelector('#gts-employee-apply-leave > form > fieldset > div:nth-child(1) > div.span4 > div > div > div > i')
        element: ElementHandle = await page.J('#gts-employee-apply-leave > form > fieldset > div:nth-child(1) > div.span4 > div > div > div > input.cb-autocomplete.ui-autocomplete-input')
        await element.click()

        await page.waitForSelector('body > ul:nth-child(19) > li:nth-child(1) > a')
        element: ElementHandle = await page.J('body > ul:nth-child(19) > li:nth-child(1) > a')
        await element.click()
        
        element: ElementHandle = await page.J('body > ul:nth-child(19) > li > a')
        await element.click()
        
        # await page.waitForSelector('#gts-employee-apply-leave > form > fieldset > div:nth-child(1) > div.span4 > div > div > div > input.cb-autocomplete.ui-autocomplete-input')
        # element: ElementHandle = await page.J('#gts-employee-apply-leave > form > fieldset > div:nth-child(1) > div.span4 > div > div > div > input.cb-autocomplete.ui-autocomplete-input')
        # await element.focus()
        # await page.keyboard.type(leave_options.get('leave_type', 'Paid-Sick-Casual'))
        # element: ElementHandle = await page.J('body > ul:nth-child(19) > li > a')
        # await element.click()

        await page.waitForSelector('#gts-employee-apply-leave > form > fieldset > div:nth-child(2) > div.span4 > div > div > input')
        element: ElementHandle = await page.J('#gts-employee-apply-leave > form > fieldset > div:nth-child(2) > div.span4 > div > div > input')
        await element.focus()
        await page.keyboard.type(leave_options.get('from_date', '11 Dec 2019'))

        await page.waitForSelector('#gts-employee-apply-leave > form > fieldset > div:nth-child(3) > div.span4 > div > div > input')
        element: ElementHandle = await page.J('#gts-employee-apply-leave > form > fieldset > div:nth-child(3) > div.span4 > div > div > input')
        await element.focus()
        await page.keyboard.type(leave_options.get('to_date', '13 Dec 2019'))

        await page.waitForSelector('#gts-employee-apply-leave > form > fieldset > div:nth-child(6) > div > div > div > div > input.cb-autocomplete.input-xlarge.ui-autocomplete-input')
        element: ElementHandle = await page.J('#gts-employee-apply-leave > form > fieldset > div:nth-child(6) > div > div > div > div > input.cb-autocomplete.input-xlarge.ui-autocomplete-input')
        await element.focus()
        await page.keyboard.type(leave_options.get('apply_to', 'Prince Chauhan (S12609)'))

        if 'reason' in leave_options:
            await page.waitForSelector('#gts-employee-apply-leave > form > fieldset > div.row.manualReason > div > div > div > textarea')
            element: ElementHandle = await page.get('#gts-employee-apply-leave > form > fieldset > div.row.manualReason > div > div > div > textarea')
            await element.focus()
            await page.keyboard.type(leave_options['reason'])

        if 'contact_details' in leave_options:
            await page.waitForSelector('#gts-employee-apply-leave > form > fieldset > div:nth-child(8) > div > div > div > textarea')
            element: ElementHandle = await page.get('#gts-employee-apply-leave > form > fieldset > div:nth-child(8) > div > div > div > textarea')
            await element.focus()
            await page.keyboard.type(leave_options['contact_details'])

        # submit: ElementHandle = await page.J('#gts-employee-apply-leave > form > div > button.btn.btn-primary')
        # await submit.click()

    async def apply_leave(self, start, end):
        import requests

        url = "https://llama.greythr.com/v2/employee/apply/leave"

        form_data = {
            'leaveType': '4',
            # 'fromDate': '17 Dec 2019',
            'fromDate': start,
            'fromSession': '1',
            # 'toDate': '17 Dec 2019',
            'toDate': end,
            'toSession': '2',
            'days': '0',
            'balance': '0.83',
            'encashBalance': '0',
            'manager': '7',
            'reason': 'test reason',
            'contactDetails': 'mars',
            'ccto': 'pulkit.singh@shipsy.co.in',
            'actionType': 'initiate',
            'actionId': '2',
            '__gtsajaxframe': 'true'
        }

        print(form_data)

        # payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"leaveType\"\r\n\r\n4\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"fromDate\"\r\n\r\n16 Dec 2019\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"fromSession\"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"toDate\"\r\n\r\n16 Dec 2019\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"toSession\"\r\n\r\n2\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"days\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"balance\"\r\n\r\n0.83\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"encashBalance\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"manager\"\r\n\r\n7\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"reason\"\r\n\r\nanother mysterious reason\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"contactDetails\"\r\n\r\ncatch me if you can\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ccto\"\r\n\r\nrahul.goswami@shipsy.co.in\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"actionType\"\r\n\r\ninitiate\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"actionId\"\r\n\r\n2\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__gtsajaxframe\"\r\n\r\ntrue\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        payload = form_data
        headers = {
            'authority': "llama.greythr.com",
            'cache-control': "max-age=0,no-cache",
            'origin': "https://llama.greythr.com",
            'upgrade-insecure-requests': "1",
            # 'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            'sec-fetch-user': "?1",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "nested-navigate",
            'referer': "https://llama.greythr.com/v2/employee/apply",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en-IN,en-US;q=0.9,en;q=0.8,hi-IN;q=0.7,hi;q=0.6,en-GB;q=0.5",
            'Postman-Token': "ca95e61f-7fc4-4d82-93c8-e03091c71ec5,ed54fb9f-f497-4609-97f5-c3bf1cb3f8e6",
            'Host': "llama.greythr.com",
            # 'Content-Length': "1594",
            'Connection': "keep-alive"
            }

        # print(self._cookies)
        response = requests.request("POST", url, data=payload, headers=headers, cookies=self._cookies)

        # import curlify
        # print(curlify.to_curl(response.request))

        # # print(response.text)
        # with open('apply_leave.html', 'w+') as f:
        #     f.write(response.text)
        # # import webbrowser
        # # webbrowser.open('apply_leave.html')

        res = json.loads(response.text)
        return res

async def apply(userid, passwd, start, end):
    browser: Browser = await launch(headless=HEADLESS)
    try:
        page, = await browser.pages()
        driver = Driver()
        await driver.login(userid, passwd, page)
        res = await driver.apply_leave(start, end)
        print(res)
    finally:
        await browser.close()

    return res

if __name__ == "__main__":
    userid, passwd = 'T12546', '@123456789'
    # userid, passwd = 'S12667', 'Dynamic@@123'
    asyncio.run(apply(userid, passwd))