from playwright.sync_api import Browser, sync_playwright
import time

url = "https://www.zhaopin.com/jobs?jl=636"
api_url = "https://fe-api.zhaopin.com/c/i/search/positions"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled",
        ],
    )
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        ignore_https_errors=True,
        storage_state="cookie.json",
        base_url="https://www.zhaopin.com/jobs?jl=636",
    )
    page = context.new_page()
    # page.on("request", lambda request: print("Request: " + request.url))
    # page.on("response", lambda response: print("Response: " + response.request.url))
    page.goto(url=url)

    api_request_context = context.request
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://www.zhaopin.com",
        "priority": "u=1, i",
        "referer": "https://www.zhaopin.com/",
        "sec-ch-ua": '"Chromium";v="153", "Not_A Brand";v="8"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "x-zp-business-system": "1",
        "x-zp-page-code": "0",
        "x-zp-platform": "13",
    }

    params = {
        "platform": "13",
        "version": "0.0.0",
    }

    # print(response.text())
    # time.sleep(20)
    for i in range(1, 51):
        json_data = {
            "S_SOU_WORK_CITY": "636",
            "order": 0,
            "pageSize": 20,
            "pageIndex": i,
            "eventScenario": "pcSearchedSouSearch",
            "anonymous": 0,
            "clickFilterBlackCompany": False,
            "platform": 13,
            "version": "0.0.0",
            "sortType": "JOB_PUBLISH_TIME",
        }
        response = api_request_context.post(
            "https://fe-api.zhaopin.com/c/i/search/positions",
            headers=headers,
            data=json_data,
        )
        with open(f"jobs/job{i}.json", "w") as f:
            f.write(response.text())
        print(f"[{i}/50]", end="\r")

    print()

    page.context.storage_state(path="cookie.json")
    browser.close()
