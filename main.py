import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from bs4 import BeautifulSoup

def get_it_trends():
    # 예시: 네이버 IT/과학 뉴스 헤드라인 가져오기
    url = "https://news.naver.com/section/105"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    
    # 뉴스 제목 추출 (네이버 뉴스 구조에 따라 변경될 수 있음)
    titles = soup.select(".sa_text_strong")
    
    content = "🤖 오늘의 IT 트렌드 뉴스 요약입니다:\n\n"
    for i, title in enumerate(titles[:10], 1): # 상위 10개만
        content += f"{i}. {title.get_text().strip()}\n"
    return content

def send_email(text_content):
    # 깃허브 금고에서 로그인 정보 가져오기
    sender_email = os.environ.get("EMAIL_USER")
    sender_password = os.environ.get("EMAIL_PASS")
    receiver_email = sender_email # 나에게 보내기 (바꾸셔도 됩니다)

    # 메일 메시지 설정
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "📢 [IT 트렌드 동향] 자동으로 배달된 메일입니다"
    msg.attach(MIMEText(text_content, "plain", "utf-8"))

    # Gmail SMTP 서버 연결 및 발송
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("메일 발송 성공!")
    except Exception as e:
        print(f"메일 발송 실패: {e}")

if __name__ == "__main__":
    news_data = get_it_trends()
    send_email(news_data)
