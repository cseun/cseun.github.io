"""One-page resume, using the portfolio's editorial typography."""
from reference_portfolio import *

def resume():
    b=Editorial('choi-seeun-resume.pdf',1,'RESUME')
    b.page('CAREER / EDUCATION')
    b.text('최세은',38,756,350,29,bold=True,leading=39)
    b.text('로봇 시스템 개발자',38,711,350,12,BLUE,True)
    b.text('웹 백엔드와 현장 장비 경험을 바탕으로<br/>로봇 제어와 관제 소프트웨어를 개발합니다.',38,684,365,9.5)
    b.image('profile.jpg',464,758,85,110)
    b.text('<a href="mailto:cseeun98@gmail.com">cseeun98@gmail.com</a>  |  <a href="https://github.com/cseun">github.com/cseun</a>',38,642,510,8.5)
    b.line(619,color=BLUE)
    b.text('경력',38,607,100,12,bold=True)
    y=580
    for date,title,body,h in [
        ('2025.04 - 2026.01','엑서테크 · 프리랜서','BMS 검사장비 CS·테스트 보조 및 C# S/W 유지보수 · 미국 파견 2회<br/>검사장비 테스트·유지보수 1.5개월 / 장비 셋업·CS 3개월',69),
        ('2023.09 - 2025.03','에어텔닷컴 그룹 · 웹 백엔드 (1년 7개월)','PHP / Laravel 상품·주문·정산 데이터 처리<br/>커머스 채널 상품 연동·내부 ERP 유지보수',69),
        ('2017.12 - 2019.06','마케팅하이랜즈 · 여행 OP (비개발)','베트남 다낭 현지 파견 · 호텔 B2B 세일즈·여행 운영<br/>예약·정산·고객 대응 및 호텔 협업',69)]:
        b.text(date,38,y,125,8,BLUE,True)
        b.text(title,175,y,382,10,bold=True)
        b.text(body,175,y-22,382,8.5,leading=13)
        y-=h
    b.line(y,color=BLUE); y-=13
    b.text('학력·교육',38,y,125,12,bold=True)
    b.text('<b>신구대학교 IT소프트웨어학과</b> · 3년제 · 2025년 졸업 · 4.18 / 4.5',175,y,382,9)
    b.text('<b>대한상공회의소 서울기술교육센터</b><br/>AI융합 로봇 SW개발자 3기 과정 진행 중',175,y-26,382,9)
    y-=76; b.line(y,color=BLUE); y-=13
    b.text('기술',38,y,125,12,bold=True)
    b.text('PHP · Laravel / React · React Native · Expo / Python<br/>STM32 · CAN · PLC · HMI / Figma · Git · Jira · Confluence · Slack',175,y,382,8.7,leading=14)
    y-=51; b.line(y,color=BLUE); y-=13
    b.text('주요 프로젝트',38,y,125,12,bold=True)
    b.text('<b>AX Multi-Robot Logistics</b> · FMS UI·React 구현, LLM 경로 평가<br/>7개 모델·2개 입력 조건을 5,880회 평가하고 시뮬레이션 주행에 연결.<br/><b>Kick CAN</b> · Node 2 계기판, TFT 2대·CLCD·조명·부저 제어<br/><b>SafeKick</b> · React Native·Expo 앱, HTTP·SSE 서버 연동<br/><b>음주컷 / PLC MPS</b> · 측정 데모·시제품 / 수동·자동 제어·HMI',175,y,382,8.6,leading=14)
    y-=90
    b.link('상세 포트폴리오 · cseun.github.io',SITE,y,175,382)
    b.save()

if __name__=='__main__':resume()
