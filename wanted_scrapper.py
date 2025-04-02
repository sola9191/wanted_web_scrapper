# pip install playwright
# pip install playwright==1.19.0
# install playwright
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

jobs_db = []  

def get_job_data(keyword): 

    try: 
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=False) #headless --> keyword arguments
        page = browser.new_page()
        page.goto("https://www.wanted.co.kr/")
        time.sleep(2)
        page.click("button.Aside_searchButton__Ib5Dn")
        page.locator("input[placeholder='검색어를 입력해 주세요.']").fill(keyword)
        page.keyboard.down("Enter")
        page.click("a#search_tab_position")
        
        # scroll down
        for x in range(10):
            page.keyboard.down("End")
            time.sleep(2)

        content =  page.content()
        soup = BeautifulSoup(content, "html.parser")
        jobs = soup.find_all("div", class_="JobCard_container__zQcZs")

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
        browser.close() # browser 닫기
        # p.stop() # playwright 종료
    return jobs_db

def create_excel_file(keyword):
    
    file = open(f"{keyword}.csv", "w", encoding="utf-8")
    writter = csv.writer(file)
    writter.writerow(["title","company_name", "link"])

    for x in jobs_db:
        writter.writerow(x.values())
    file.close()




