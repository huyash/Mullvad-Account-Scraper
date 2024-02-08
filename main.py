import requests

urlBase = "https://api.mullvad.net/www/accounts/"
proxies = [ #Place your proxies here...]

with open("acc.txt") as file: #Name your file "acc.txt" which contains accounts
    j = 0
    direction = 1

    for line in file:
        login_number = line.strip()
        url = urlBase + login_number

        proxy = proxies[j % len(proxies)]

        try:
            response = requests.get(
                url, proxies={"http": proxy, "https": proxy})
            print(f"Current account {login_number} and proxy {proxy}")
            print(response.json())

            if response.status_code == 429:
                j += direction
                with open("tryAgain.txt", "a") as refile: #Create a "tryAgain.txt" file that will store failed accounts
                    refile.write(f"{login_number}\n")

        except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as e:
            print(f"Exception for account {login_number} and proxy {proxy}: {e}")

        j += direction

        j %= len(proxies)
