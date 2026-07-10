from flask import Flask, render_template, request, send_file, redirect
# 1. 잡플래닛 함수도 같이 import 해줍니다.
from scrapper import search_incruit, search_jobplanet 
from file import save_to_csv

app = Flask(__name__)

db = {}
page = 2

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")

    if not keyword or keyword.strip() == "":
        return redirect("/")
    
    # 캐시(db)에 이미 있다면 저장된 데이터를 그대로 씁니다.
    if keyword in db:
        jobs = db[keyword]
    else:
        # [인크루트 데이터] 가져오기
        incruit_jobs = search_incruit(keyword, page)
        # 요구사항 1: 인크루트 데이터는 상위 30개만 슬라이싱
        incruit_jobs = incruit_jobs[:30]
        
        # [잡플래닛 데이터] 가져오기
        jobplanet_jobs = search_jobplanet(keyword)
        # 요구사항 2: 잡플래닛 데이터는 1개만 (이미 위에서 1개만 추출하도록 설계함)
        
        # 두 리스트를 결합 (총 31개)
        jobs = incruit_jobs + jobplanet_jobs
        
        # 결과 캐싱
        db[keyword] = jobs
        
    return render_template("search.html", jobs=enumerate(jobs), keyword=keyword, count=len(jobs))

@app.route("/file")
def file():
    keyword = request.args.get("keyword")

    if not keyword or keyword.strip() == "":
        return redirect("/")
    
    # 이미 /search 페이지를 거쳤으므로 db에 있을 확률이 높습니다.
    if keyword in db:
        jobs = db[keyword]
    else:
        incruit_jobs = search_incruit(keyword, page)[:30]
        jobplanet_jobs = search_jobplanet(keyword)
        jobs = incruit_jobs + jobplanet_jobs
        db[keyword] = jobs
        
    save_to_csv(jobs)
    return send_file("./downloads.csv", as_attachment=True)

    
if __name__ == '__main__':
    app.run()