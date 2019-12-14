from src.driver import apply
from src.db import DB
import asyncio

def exec_command(message):
    args = message['text']
    user = message['user']
    # print('args: ' + args)
    if ' ' in args:
        cmd, args = tuple(args.split(' ', 1))
    else:
        cmd = args
    # print(cmd)
    # print(args)
    # to_exec = f"""ret = Commands('{args}').{cmd}()"""

    return Commands().run(cmd, args, user)

class Commands:
    def __init__(self):
        pass

    def run(self, cmd, args, user):
        # slack_id = user['id']
        slack_id = user
        # print("slack_id: " + user)
        db = DB(slack_id)

        # print(cmd)
        if cmd == "help":
            ret = "\n".join(("Available commands:",
                        "help: Prints the list of available commands",
                        "login: User login, required before any other action",
                        "apply: Apply for leave",
            ))
            return ret
        elif cmd == "login":
            # print(args)
            user_id, user_pass = args.split(' ')
            # print('setting user details')
            db.greythr_user_id = user_id
            db.greythr_password =  user_pass
            db.freeze()
        elif cmd == "apply":
            start, end = args.split(' ')
            # userid, passwd = 'T12546', '@123456789'
            # userid, passwd = 'S12667', 'Dynamic@@123'
            
            # login T12546 @123456789
            # apply ‘18 Dec 2019’ ‘19 Dec 2019’
            res = asyncio.run(apply(db.greythr_user_id, db.greythr_password, start[1:-1], end[1:-1]))
            return res

        else:
            ret = "Command not available!"
            return ret

    def apply(self):
        import requests

        url = "https://llama.greythr.com/v2/employee/apply/leave"

        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"leaveType\"\r\n\r\n4\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"fromDate\"\r\n\r\n16 Dec 2019\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"fromSession\"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"toDate\"\r\n\r\n16 Dec 2019\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"toSession\"\r\n\r\n2\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"days\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"balance\"\r\n\r\n0.83\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"encashBalance\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"manager\"\r\n\r\n7\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"reason\"\r\n\r\nanother mysterious reason\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"contactDetails\"\r\n\r\ncatch me if you can\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ccto\"\r\n\r\nrahul.goswami@shipsy.co.in\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"actionType\"\r\n\r\ninitiate\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"actionId\"\r\n\r\n2\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__gtsajaxframe\"\r\n\r\ntrue\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        headers = {
            'authority': "llama.greythr.com",
            'cache-control': "max-age=0,no-cache",
            'origin': "https://llama.greythr.com",
            'upgrade-insecure-requests': "1",
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            'sec-fetch-user': "?1",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "nested-navigate",
            'referer': "https://llama.greythr.com/v2/employee/apply",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en-IN,en-US;q=0.9,en;q=0.8,hi-IN;q=0.7,hi;q=0.6,en-GB;q=0.5",
            'cookie': "v2.ajax.page-message=; ajs_user_id=null; ajs_group_id=null; amplitude_idundefinedgreythr.com=eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==; ajs_anonymous_id=%22bc47ed13-d67b-497b-9999-0bdf798f0c43%22; _BEAMER_USER_ID_eWSQffTA7374=520ea19d-5eeb-4589-936c-c67b54346109; _BEAMER_FIRST_VISIT_eWSQffTA7374=2019-12-13T09:35:53.930Z; _BEAMER_LAST_PUSH_PROMPT_INTERACTION_eWSQffTA7374=1576230497087; intercom-session-uycc0o6a=aVN0MUJzdFk1SEtCRGxrQ1pKejY0ZVdyeXJOMEhIZ0xTR2puejd3djB1NHJ6Z3BVazZBdTlJdVZiRG5lVFBwWC0tanZ0V05SWjUySWNXZUlEWmM2dXgrQT09--c14a186c1b965cbea1edf8d6d954cb0f0b9411c7; _BEAMER_FILTER_BY_URL_eWSQffTA7374=false; access_token=8CYOFfrisAfA4aM4PQm_84aYLHp3iaqC_dUERE4gA7A._6LFBaJZd0Vgm5gpZt24IFZvA2ghhHinNusJK2FSOEA; JSESSIONID=1BF2703E53D5BAB7603409FAE47E2686-n2; amplitude_id_68a53e4aaa416980b350edb16524b238greythr.com=eyJkZXZpY2VJZCI6ImM5NjBjZTIxLTBjZTUtNDc1Yi04NDhiLTU4ZWQ1N2VjMzU1M1IiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU3NjI1MTU2MDQxMCwibGFzdEV2ZW50VGltZSI6MTU3NjI1MTg2ODM4MCwiZXZlbnRJZCI6MSwiaWRlbnRpZnlJZCI6OCwic2VxdWVuY2VOdW1iZXIiOjl9,v2.ajax.page-message=; ajs_user_id=null; ajs_group_id=null; amplitude_idundefinedgreythr.com=eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==; ajs_anonymous_id=%22bc47ed13-d67b-497b-9999-0bdf798f0c43%22; _BEAMER_USER_ID_eWSQffTA7374=520ea19d-5eeb-4589-936c-c67b54346109; _BEAMER_FIRST_VISIT_eWSQffTA7374=2019-12-13T09:35:53.930Z; _BEAMER_LAST_PUSH_PROMPT_INTERACTION_eWSQffTA7374=1576230497087; intercom-session-uycc0o6a=aVN0MUJzdFk1SEtCRGxrQ1pKejY0ZVdyeXJOMEhIZ0xTR2puejd3djB1NHJ6Z3BVazZBdTlJdVZiRG5lVFBwWC0tanZ0V05SWjUySWNXZUlEWmM2dXgrQT09--c14a186c1b965cbea1edf8d6d954cb0f0b9411c7; _BEAMER_FILTER_BY_URL_eWSQffTA7374=false; access_token=8CYOFfrisAfA4aM4PQm_84aYLHp3iaqC_dUERE4gA7A._6LFBaJZd0Vgm5gpZt24IFZvA2ghhHinNusJK2FSOEA; JSESSIONID=1BF2703E53D5BAB7603409FAE47E2686-n2; amplitude_id_68a53e4aaa416980b350edb16524b238greythr.com=eyJkZXZpY2VJZCI6ImM5NjBjZTIxLTBjZTUtNDc1Yi04NDhiLTU4ZWQ1N2VjMzU1M1IiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU3NjI1MTU2MDQxMCwibGFzdEV2ZW50VGltZSI6MTU3NjI1MTg2ODM4MCwiZXZlbnRJZCI6MSwiaWRlbnRpZnlJZCI6OCwic2VxdWVuY2VOdW1iZXIiOjl9; JSESSIONID=28A731B2CBCA8189F47BCC31294E538C-n1",
            'Postman-Token': "ca95e61f-7fc4-4d82-93c8-e03091c71ec5,ed54fb9f-f497-4609-97f5-c3bf1cb3f8e6",
            'Host': "llama.greythr.com",
            'Content-Length': "1594",
            'Connection': "keep-alive"
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)
