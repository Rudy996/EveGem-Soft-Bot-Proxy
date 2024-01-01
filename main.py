import sys
import os
import random
import threading
import time
import requests

from twocaptcha import TwoCaptcha

with open('proxy.txt', 'r') as proxy_file:
    proxies_list = proxy_file.readlines()

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
    "Mozilla/5.0 (iPad; CPU OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0"
]

def work(line, proxy):
    s = 1



    while True:
        visitor, request1, cookie = line.strip().split(':')
        sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

        proxy_url = f"http://{proxy}"
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }

        response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
        if response.status_code == 200:
            pass
        else:
            print(f"Прокси {proxy} не работает. Статус: {response.status_code}. Поток засыпает до конца работы")
            time.sleep(99999999999)
            


        api_key = os.getenv('APIKEY_2CAPTCHA', 'api')

        solver = TwoCaptcha(api_key)

        try:
            result = solver.hcaptcha(
                sitekey='d1add268-b915-46c1-afd3-960faba20822',
                url='https://evergem.io/claim?redirect_to=/game',
            )

        except Exception as e:
            sys.exit(e)

        else:
            gh = result.get('code')
            gh = gh.replace(" ", "")
            # print(gh)
            random_user_agent = random.choice(user_agents)

            params = {
                'redirect_to': '/game'
            }

            url = 'https://evergem.io/claim?redirect_to=/game'
            payload = {
                # 'g-recaptcha-response': gh,
                'h-captcha-response': gh,
                'visitorId': f'{visitor}',
                'requestId': f'{request1}',
                'item_id': '28072'
            }

            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'uk,ru-RU;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6,bg;q=0.5,es;q=0.4',
                'Cache-Control': 'max-age=0',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': f'{cookie}',
                'Origin': 'null',
                'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': f'{random_user_agent}'
            }

            response = requests.post(url,headers=headers, params=params, data=payload, proxies=proxies)
            pot = threading.current_thread().name

            if response.status_code == 200:
                print(f"Поток: {pot}: Заклеймлино наград: {s}  | Автор Rudy Crypto - https://t.me/rudtyt")
            else:
                print("Хуй знает, но почему-то не заклеймилось")

            s = s + 1
            time.sleep(300)

threads = []
with open('info.txt', 'r') as file:
    for idx, line in enumerate(file):
        proxy = proxies_list[idx % len(proxies_list)].strip()  # Циклическое использование прокси
        thread = threading.Thread(target=work, args=(line, proxy))
        threads.append(thread)
        thread.start()

for thread in threads:
    thread.join()
