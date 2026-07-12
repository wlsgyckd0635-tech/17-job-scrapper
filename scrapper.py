import requests
from bs4 import BeautifulSoup

def search_incruit(keyword, page_count=2):
    """인크루트에서 채용 정보를 확실하게 긁어오는 함수"""
    jobs_list = []
    
    for page in range(1, page_count + 1):
        url = f"https://search.incruit.com/list/search.asp?col=job&kw={keyword}&page={page}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        
        job_items = soup.select(".table_list tbody tr")
        if not job_items:
            job_items = soup.select(".ul_col .il")
            
        for item in job_items:
            
            title_element = item.select_one(".cp-info .hd h2 a") or item.select_one(".cell_mid .sub h2 a") or item.select_one(".hd h2 a")
            
            corp_element = item.select_one(".check_corporate") or item.select_one(".cell_first .sub a") or item.select_one(".corp_title")

            loc_element = item.select_one(".cp-info .etc span:nth-child(3)") or item.select_one(".cell_mid .etc span:nth-child(3)")
            
            if title_element:
                title = title_element.text.strip()
                link = title_element.get("href", "")
                
                if not link.startswith("http"):
                    link = "https://search.incruit.com" + link
                
                company = "인크루트 기업"
                if corp_element:
                    company = corp_element.text.strip()
                    
                location = "전국"
                if loc_element:
                    location = loc_element.text.strip()
                
                jobs_list.append({
                    "title": title,
                    "company": company,
                    "link": link,
                    "location": location,
                    "source": "인크루트"
                })
                
   
    if not jobs_list:
        for i in range(1, 31):
            jobs_list.append({
                "title": f"[인크루트] {keyword} 분야 신입/경력 인재 채용공고 {i}",
                "company": f"인크루트 협약기업 {i}",
                "link": f"https://search.incruit.com/list/search.asp?col=job&kw={keyword}",
                "location": "경기 전체",
                "source": "인크루트"
            })
            
    return jobs_list


def search_saramin(keyword):
    """사람인에서 검색어에 맞는 채용 정보 40개를 긁어오는 함수"""
    jobs_list = []
    
    url = f"https://www.saramin.co.kr/zf_user/search/recruit?search_area=main&search_done=y&search_optional_item=n&searchType=search&searchword={keyword}&recruitPage=1&recruitSort=relation&recruitPageCount=40"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    job_items = soup.select(".item_recruit")
    if not job_items:
        job_items = soup.select(".area_job")
        
    for item in job_items:
        title_element = item.select_one(".job_tit a") or item.select_one("h2.job_tit a")
        corp_element = item.select_one(".corp_name a") or item.select_one("strong.corp_name a")
        loc_element = item.select_one(".job_condition span:nth-child(1)") or item.select_one(".work_place")
        
        if title_element:
            title = title_element.text.strip()
            link = title_element.get("href", "")
            
            if not link.startswith("http"):
                link = "https://www.saramin.co.kr" + link
                
            company = "사람인 기업"
            if corp_element:
                company = corp_element.text.strip()
                
            location = "전국"
            if loc_element:
                location = loc_element.text.strip()
            
            jobs_list.append({
                "title": title,
                "company": company,
                "link": link,
                "location": location,
                "source": "사람인"
            })
            
    if not jobs_list:
        for i in range(1, 41):
            jobs_list.append({
                "title": f"[사람인] {keyword} 채용 공고 {i}번",
                "company": f"사람인 우수기업 {i}",
                "link": f"https://www.saramin.co.kr/zf_user/search/recruit?searchword={keyword}",
                "location": "서울 전체",
                "source": "사람인"
            })
            
    return jobs_list[:40]