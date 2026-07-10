import requests 
from bs4 import BeautifulSoup


def search_incruit(keyword, page=1):
    # 1 -> 0
    # 2 -> 30
    # 3 -> 60

    jobs = []

    for i in range(page):
        page = 30 * i
        url = f"https://search.incruit.com/list/search.asp?col=job&kw={keyword}&startno={page}"
        r = requests.get(url) 
        # print(r.text)
        soup = BeautifulSoup(r.text, "html.parser")
        lis = soup.find_all("li", class_="c_col")


        for li in lis:
            company = li.find("a", class_="cpname").text
            title = li.find("div", class_="cell_mid").find("div", class_="cl_top").find("a").text
            location = li.find("div", class_="cl_md").find_all("span")[0].text
            link = li.find("div", class_="cell_mid").find("div", class_="cl_top").find("a").get("href")
            
            job_data = {
                "company": company, 
                "title" : title, 
                "location": location, 
                "link" : link
            }

            jobs.append(job_data)

    return jobs


if __name__ == "__main__": 
    result = search_incruit("간호사", 2)
    print(result)
    print(len(result))





import requests
from bs4 import BeautifulSoup

# ... 기존 인크루트 search_incruit 함수 코드는 그대로 두고, 아래 함수를 추가합니다 ...

def search_jobplanet(keyword):
    """잡플래닛에서 검색어에 맞는 채용 정보 딱 1개만 가져오는 함수"""
    try:
        url = f"https://www.jobplanet.co.kr/search?query={keyword}&category=search_new&search_keyword_hint_id=&_rs_act=&_rs_mod=&_rs_element="
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, 'Gecko') Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 잡플래닛 채용공고 카드 요소 선택 (웹사이트 구조 변경 시 셀렉터 수정이 필요할 수 있음)
        job_card = soup.select_one("a.item_card") 
        
        if job_card:
            # 절대경로 주소 매핑
            link = "https://www.jobplanet.co.kr" + job_card.get("href", "")
            title = job_card.select_one("span.title").text.strip() if job_card.select_one("span.title") else "채용 정보"
            company = job_card.select_one("span.company_name").text.strip() if job_card.select_one("span.company_name") else "잡플래닛 기업"
            
            return [{
                "title": title,
                "company": company,
                "link": link,
                "source": "잡플래닛"  # 인크루트와 구분하기 위한 태그
            }]
    except Exception as e:
        print(f"잡플래닛 크롤링 실패: {e}")
        
    # 실패하거나 결과가 없을 경우 빈 리스트 반환
    return []




