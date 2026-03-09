from flask import Flask, jsonify, request

from crawler_service.crawler import crawl_page
from crawler_service.s3_uploader import upload_to_s3
from rag_service.qa import RAGEngine

app = Flask(__name__)

rag = RAGEngine("rag_service/docs.csv")

@app.route("/")
def home():
    return {"message":"Webknowledge AI is running"}

@app.route("/crawl",methods=['POST'])
def crawl():
    url = request.json["url"]
    df = crawl_page(url)
    upload_to_s3(df)
    return {"message":"URL crawled successfully"}

@app.route("/ask",methods=['POST'])
def ask():
    question = request.json["question"]
    response = rag.ask(question)
    return jsonify({"answer":response})

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
