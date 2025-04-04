# pip install playwright
# pip install playwright==1.19.0
# install playwright
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

def get_job_data(keyword): 
    browser = None
    p = None
    jobs_db = []  

    try: 
        p = sync_playwright().start()
        # browser = p.chromium.launch(headless=True,args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"])
        # browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        # browser = p.chromium.launch(headless=False, slow_mo=500)
        browser = p.chromium.launch(headless=True,args=["--no-sandbox","--disable-gpu","--disable-dev-shm-usage"])
        context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0 Safari/537.36")
        page = context.new_page()
        time.sleep(2)
        print("페이지이동")
        # page.goto("https://www.wanted.co.kr/")
        # page.goto("https://www.wanted.co.kr/", timeout=60000, wait_until="domcontentloaded")
        page.goto("https://www.wanted.co.kr/", wait_until="domcontentloaded", timeout=60000)
        print("check html")
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        print("✅ debug.html 저장 완료")
        print("wait for selector & click page")
        # page.wait_for_selector("button.Aside_searchButton__Ib5Dn", timeout=10000)
        # page.wait_for_selector("button[aria-label='검색']", timeout=15000)
        # page.wait_for_selector("button[aria-label='검색']", timeout=15000, state="attached")
        # page.click("button[aria-label='검색']")
        # page.locator("button[aria-label='검색']").click(timeout=15000)
        page.evaluate("""
            document.querySelector("button[aria-label='검색']").scrollIntoView()
        """)
        page.locator("button.Aside_searchButton__Ib5Dn").click(timeout=20000, force=True)
        print("fill keyword")
        page.locator("input[placeholder='검색어를 입력해 주세요.']").fill(keyword)
        print("keyboard down")
        page.keyboard.down("Enter")
        print("click page")
        page.click("a#search_tab_position")

        print("scroll down")
        # scroll down
        for x in range(10):
            page.keyboard.down("End")
            time.sleep(2)

        content =  page.content()
        print("==================content===================")
        print(content)
        soup = BeautifulSoup(content, "html.parser")
        jobs = soup.find_all("div", class_="JobCard_container__zQcZs")

        print("extract job data from jobs")
        for job in jobs:
            link = f"https://www.wanted.co.kr/{job.find('a')['href']}"
            title = job.find("strong", class_="JobCard_title___kfvj").text
            company_name = job.find("span", class_="JobCard_companyName__kmtE0").text
            job = {
                "title" : title,
                "company_name" : company_name,
                "link" : link
            }
            jobs_db.append(job)

    except Exception as e:
        print(f"Error: {e}")
    finally:   
        if browser:
            browser.close() # browser 닫기
        if p :
            p.stop()
        return jobs_db

def create_excel_file(keyword, jobs):
    
    file = open(f"{keyword}.csv", "w", encoding="utf-8")
    writter = csv.writer(file)
    writter.writerow(["title","company_name", "link"])

    for job in jobs:
        writter.writerow(job.values())
    file.close()




