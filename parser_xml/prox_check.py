import requests
from concurrent.futures import ThreadPoolExecutor


def check_proxy(proxy):
    try:
        response = requests.get(
            "http://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=5
        )
        # Если статус код 200, значит прокси работает
        if response.status_code == 200:
            print(f"Прокси {proxy} работает")
            return proxy
    except:
        # Если возникла ошибка, значит прокси не работает
        print(f"Прокси {proxy} не работает")
        return None


with open("http.txt", "r") as file:
    proxies = file.read().splitlines()

working_proxies = []
with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(check_proxy, proxies)
    for result in results:
        if result:
            working_proxies.append(result)

with open("working_proxies.txt", "w") as file:
    for proxy in working_proxies:
        file.write(proxy + "\n")

print(
    f"Найдено {len(working_proxies)} рабочих прокси. Список сохранен в working_proxies.txt"
)
