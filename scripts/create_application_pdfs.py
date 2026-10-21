"""Create a concise portfolio and a separate factual career statement."""
from pathlib import Path
from io import BytesIO
import shutil
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/pdf'
OUT.mkdir(parents=True, exist_ok=True)
for name, file in [('M','malgun.ttf'),('MB','malgunbd.ttf')]:
    pdfmetrics.registerFont(TTFont(name, 'C:/Windows/Fonts/'+file))
pdfmetrics.registerFontFamily('M', normal='M', bold='MB', italic='M', boldItalic='MB')
W,H=A4
NAVY='#17344D'; BLUE='#28659C'; MUTED='#647384'; LINE='#DDE5EC'; PALE='#F0F5F9'; ACCENT='#8D505C'
SITE='https://cseun.github.io/'

class Book:
    def __init__(self,name,total,label):
        self.path=OUT/name; self.total=total; self.label=label; self.n=0
        self.c=canvas.Canvas(str(self.path),pagesize=A4,pageCompression=1)
        self.c.setTitle('최세은 | '+label); self.c.setAuthor('최세은')
    def text(self,text,x,y,w,size=10,color=NAVY,bold=False,leading=None):
        st=ParagraphStyle('t',fontName='MB' if bold else 'M',fontSize=size,leading=leading or size*1.6,textColor=HexColor(color),wordWrap='CJK')
        p=Paragraph(text,st); _,h=p.wrap(w,1000)
        if y-h < 40: raise ValueError(f'Page {self.n}: text below safe area: {text[:50]} at {y-h}')
        p.drawOn(self.c,x,y-h); return y-h
    def rect(self,x,y,w,h,fill=PALE,stroke=None):
        self.c.setFillColor(HexColor(fill)); self.c.setStrokeColor(HexColor(stroke or fill))
        self.c.roundRect(x,y-h,w,h,7,fill=1,stroke=bool(stroke))
    def page(self,section):
        if self.n: self.c.showPage()
        self.n+=1; c=self.c
        c.setStrokeColor(HexColor(NAVY)); c.setLineWidth(1.2); c.line(38,H-30,W-38,H-30)
        self.text('최세은  /  '+self.label,38,H-40,350,8,bold=True)
        self.text(section,W-190,H-40,150,8,MUTED)
        c.setStrokeColor(HexColor(ACCENT)); c.setLineWidth(.7); c.line(38,31,W-38,31)
        c.setFillColor(HexColor(MUTED)); c.setFont('M',7)
        c.drawString(38,19,'CHOI SEEUN  |  cseun.github.io'); c.drawRightString(W-38,19,f'{self.n:02d} / {self.total:02d}')
        c.bookmarkPage('p'+str(self.n)); c.addOutlineEntry(section,'p'+str(self.n),level=0)
        return H-83
    def title(self,kicker,title,desc=None):
        y=self.page(kicker)
        y=self.text(kicker.upper(),38,y,W-76,9,BLUE,True)-7
        y=self.text(title,38,y,W-76,24,bold=True,leading=32)-10
        if desc: y=self.text(desc,38,y,W-76,10.3,MUTED)-16
        return y
    def heading(self,title,y,x=38,w=W-76):
        return self.text(title,x,y,w,12,bold=True)-8
    def block(self,title,body,y,x=38,w=W-76,fill=PALE):
        # Measure with the same paragraph styles used for painting.
        def height(s,size,bold=False):
            p=Paragraph(s,ParagraphStyle('m',fontName='MB' if bold else 'M',fontSize=size,leading=size*1.6,wordWrap='CJK'))
            return p.wrap(w-28,1000)[1]
        h=height(title,10,True)+height(body,9.5)+35
        self.rect(x,y,w,h,fill)
        yy=self.text(title,x+14,y-12,w-28,10,BLUE,True)-5
        self.text(body,x+14,yy,w-28,9.5)
        return y-h-12
    def image(self,file,x,y,w,h,caption=None):
        self.rect(x,y,w,h,'#11161D')
        path=ROOT/'assets'/file
        with Image.open(path) as im:
            iw,ih=im.size; scale=min(w/iw,h/ih); dw,dh=iw*scale,ih*scale
            # Downsample large originals for compact application attachments.
            im=im.convert('RGB'); im.thumbnail((1600,1200))
            data=BytesIO(); im.save(data,format='JPEG',quality=87,optimize=True); data.seek(0)
            self.c.drawImage(ImageReader(data),x+(w-dw)/2,y-h+(h-dh)/2,dw,dh)
        yy=y-h-5
        if caption: yy=self.text(caption,x,yy,w,8,MUTED)-9
        return yy
    def link(self,label,url,y,x=38,w=W-76):
        return self.text(f'<a href="{url}" color="{BLUE}"><u>{label} ↗</u></a>',x,y,w,8.5)-8
    def save(self):
        assert self.n==self.total,(self.n,self.total)
        self.c.save(); print(self.path)

def portfolio():
    b=Book('choi-seeun-portfolio.pdf',6,'ROBOTICS SOFTWARE PORTFOLIO')
    y=b.page('PROFILE & SKILLS')
    b.rect(38,y,164,624)
    yy=b.image('profile.jpg',52,y-14,136,182)-8
    yy=b.text('CONTACT',52,yy,136,9,BLUE,True)-8
    yy=b.link('cseeun98@gmail.com','mailto:cseeun98@gmail.com',yy,52,136)
    yy=b.link('GitHub / cseun','https://github.com/cseun',yy,52,136)
    yy=b.link('기술 블로그','https://slowbreeze.tistory.com',yy,52,136)-17
    yy=b.text('학력 및 전문 교육',52,yy,136,10,bold=True)-9
    yy=b.text('<b>신구대학교</b><br/>IT소프트웨어학과 · 3년제<br/>2025년 졸업<br/><b>4.18 / 4.5</b>',52,yy,136,9)-18
    b.text('<b>대한상공회의소<br/>서울기술교육센터</b><br/>AI융합 로봇 SW개발자<br/>3기 과정 진행 중',52,yy,136,9)
    x=222; w=W-x-38
    yy=b.text('로봇 시스템 개발자',x,y-5,w,14,BLUE,True)-4
    yy=b.text('최세은',x,yy,w,34,bold=True,leading=44)-13
    yy=b.text('웹 백엔드와 현장 장비 경험을 바탕으로<br/>로봇 제어와 관제 소프트웨어를 개발합니다.',x,yy,w,11)-16
    yy=b.block('01  웹 백엔드 실무','PHP / Laravel 기반 상품·주문·정산 데이터 처리<br/>커머스 채널 연동과 내부 ERP 유지보수',yy,x,w)
    yy=b.block('02  관제 화면과 프론트엔드','Figma·Claude AI로 UI 설계<br/>ChatGPT·Figma를 활용한 React 구현 및 통합',yy,x,w)
    yy=b.block('03  AI 경로 생성과 비교 실험','모델·프롬프트·입력 범위 비교<br/>Iterative 경로 생성과 시뮬레이션 주행 반영',yy,x,w)
    yy=b.block('04  장비 제어와 팀 협업','STM32 / CAN / PLC·HMI 프로젝트<br/>Jira·Confluence·Slack·GitHub 협업 환경 구성',yy,x,w)
    b.link('온라인 포트폴리오 전체 보기',SITE,yy,x,w)

    y=b.title('01 / FEATURED PROJECT','AX MULTI-ROBOT LOGISTICS','팀 E1I6 · 7명 · 담당 FMS AI | TurtleBot 기반 물류 관제 시스템')
    y=b.block('최적 경로가 필요한 이유','여러 로봇이 같은 통로를 사용하므로 이동 거리와 함께 충돌 위험·대기 시간·하드웨어 및 주행 환경을 고려해 안전하고 효율적인 경로를 선택하는 것이 목표입니다.',y)
    w=(W-88)/2
    y1=b.block('개인 담당 01 · 디자인 및 프론트엔드','Figma·Claude AI를 활용한 화면 설계<br/>ChatGPT·Figma를 활용한 React 구현<br/>관제 화면의 구성 및 프론트엔드 통합',y,38,w)
    y2=b.block('개인 담당 02 · AI·LLM','모델 선정·테스트·비교<br/>최단 경로 생성 및 주행 반영 구현<br/>AI 충돌 모니터링·예측 진행 중',y,50+w,w,'#EEF0F8')
    y=min(y1,y2)
    y=b.text('팀원 담당 · ROS 2 / MQTT 로봇 연동, A* 탐색 알고리즘 및 예외 처리',38,y,W-76,9,MUTED)-15
    y=b.image('fms-dashboard.png',38,y,W-76,225,'React 기반 FMS 시뮬레이션 관제 화면')
    y=b.link('Figma 관제 화면 설계 보기','https://www.figma.com/make/z7YojOyW17K9Ld52J3RrW2/E1I6---AX-Multi-Robot-Logistics-FMS-Dashboard-Wireframe',y)
    y=b.link('핵심 기능 시연 · 전체 시나리오','https://youtu.be/HqL8_q4xefw',y)
    b.link('소스 코드 / Logistics FMS','https://github.com/E1I6-Logistics/Logistics_FMS',y)

    y=b.title('02 / AI EXPERIMENTS','LLM 경로 판단','비교 기준 수립 → 조건별 실험 → 모델 선택 → 시뮬레이션 주행 반영')
    y=b.block('01  비교 기준과 실험 조건','논문의 Dijkstra·A* 비교 결과를 검토하고, 프로젝트의 단일 목적지·좌표 조건에 맞춰 A*를 LLM 경로 평가 기준으로 선정했습니다.<br/><br/>PC와 Jetson 환경, Direct / CoT / Iterative 방식, 전체 그래프 / 인접 노드 입력을 비교했습니다.',y)
    y=b.block('02  도착 안정성과 선택 정확도 개선','7개 모델 × 2개 입력 범위 × 84개 출발·목적지 쌍 × 5회 반복으로 5,880회 테스트했습니다. 별도의 6조건 비교에서 인접 노드를 단계적으로 선택하는 Iterative 방식은 30회 중 28회 도착했습니다.<br/><br/>연결 검증과 재방문 제한을 적용해 존재하지 않는 간선 선택과 반복 경로를 줄였습니다.',y)
    y=b.heading('03  도착률을 우선하고 최단 경로 일치율·응답 시간을 함께 비교',y)
    w=(W-88)/2
    a=b.block('채택 · Kev 0.8B + 인접 정보','<b>도착 100%</b><br/>최단 경로 일치율 52.4%<br/>중앙 응답 시간 0.41초',y,38,w)
    z=b.block('비교 대안 · Kev 4B + 전체 그래프','<b>도착 95.2%</b><br/>최단 경로 일치율 75.0%<br/>중앙 응답 시간 0.61초',y,50+w,w)
    y=min(a,z)
    y=b.block('진행 중 · AI 기반 충돌 모니터링·예측','충돌 모니터링·예측 기능을 구현 중입니다. 이후 예측 결과와 하드웨어·주행 환경을 반영한 최적 경로 판단으로 확장할 예정입니다.',y,fill='#F8EFED')
    b.link('LLM 경로 생성 및 시뮬레이션 주행 시연',SITE+'assets/fms-llm-route-demo.mp4',y)

    y=b.title('03 / EMBEDDED & APP','장치 상태를 화면으로 연결','담당 범위를 기준으로 정리한 임베디드·앱 프로젝트')
    y=b.heading('Kick CAN · CAN 기반 RC카의 계기판 노드',y)
    y=b.text('개인 담당 Node 2 | NUCLEO-F103RB · CAN 500 kbps · SPI',38,y,W-76,9,BLUE)-10
    yy=b.image('kickcan-real-card.jpg',38,y,213,163,'실물 · LCD 및 TFT 계기판')
    z=b.text('<b>구현</b><br/>CAN 수신 데이터의 ID·형식·길이를 확인하고 차량 상태를 TFT·CLCD에 표시했습니다. 방향 지시등·조명·부저 출력과 핀맵·배선을 구성했습니다.<br/><br/><b>처리 흐름</b><br/>수신 큐 → 검증 → 상태 갱신 → 화면·출력 장치 반영',267,y,W-305,9.5)
    y=min(yy,z)-5
    y=b.link('Node 2 소스 코드','https://github.com/kick-can/Node_2',y)-13
    y=b.heading('SafeKick · 전동 킥보드 안전 앱',y)
    y=b.text('팀 프로젝트 | 담당 UI/UX · 앱 프론트엔드 · 데모 지원',38,y,W-76,9,BLUE)-9
    yy=b.image('safekick-app-flow.png',38,y,213,169,'홈 · 인증 · 안전 점검 화면 흐름')
    z=b.text('<b>화면 구현</b><br/>가입·로그인, 면허 촬영/OCR, QR, 셀피 인증, 안전 점검과 반납 흐름을 구현·통합했습니다. HTTP 결과와 SSE 상태를 화면에 반영했습니다.<br/><br/>Figma AI와 LLM으로 화면·코드를 구성한 뒤 검토하고 통합했습니다.<br/><br/><b>팀원 담당</b> 서버·AI 모델·주 장치 펌웨어·기존 하드웨어 최종 통합',267,y,W-305,9.5)
    y=min(yy,z)-10
    y=b.link('SafeKick 앱 소스 코드','https://github.com/safe-kick/safe-kick-app',y)
    b.link('SafeKick 시연 영상','https://youtu.be/aibkoaQ87P8',y)

    y=b.title('04 / DEVICE CONTROL','측정 데모와 제어 화면','입출력 상태를 확인할 수 있도록 구성한 장치·HMI 프로젝트')
    y=b.heading('음주컷 · 음주 측정 데모와 시제품 제작',y)
    y=b.text('초기 기획 · 협업 환경 구성 · STM32 측정 데모 · Fusion 360',38,y,W-76,9,BLUE)-9
    y=b.text('MQ-3 센서의 기준값 변화를 확인하고 버튼·LED·부저와 시동 상태를 연결했습니다. 케이스와 센서 홀더를 모델링하고 STL로 제작 자료를 준비했습니다.',38,y,W-76,9.5)-12
    w=(W-88)/2
    a=b.image('umjoo-demo.jpg',38,y,w,137,'측정 및 장치 제어 데모')
    z=b.image('umjoo-case.jpg',50+w,y,w,137,'케이스 · 센서 홀더 설계')
    y=min(a,z)
    y=b.text('팀원 담당 · 얼굴 인식과 실제 하드웨어 최종 통합',38,y,W-76,8.5,MUTED)-6
    y=b.link('STM32 데모 소스 코드','https://github.com/Umjoo-Cut/StmDemo',y)-12
    y=b.heading('PLC MPS · 수동·자동 제어와 HMI 화면 구성',y)
    y=b.text('MELSEC Q · GX Works2 · GT Designer3',38,y,W-76,9,BLUE)-8
    y=b.text('수동 입출고와 실린더·서보 동작 확인, 자동 운전 시퀀스를 구성했습니다. 터치 버튼과 상태 램프를 같은 위치에 배치해 조작과 결과를 함께 확인하도록 만들었습니다.',38,y,W-76,9.5)-12
    a=b.image('plc-manual.jpg',38,y,w,130,'수동 운전 HMI')
    b.image('plc-servo.jpg',50+w,y,w,130,'서보 제어 HMI')

    y=b.title('05 / COLLABORATION','협업 환경 셋업과 알림 연동','팀의 작업·문서·코드 변경을 Slack에서 확인하도록 연결했습니다.')
    y=b.block('개인 담당 · 팀 운영 방식과 도구 연동','Jira 스프린트·백로그 운영 방식을 설정하고, Slack에서 Jira 티켓을 생성하도록 연결했습니다. Confluence 문서와 Jira 이슈를 연결하고 GitHub push·commit 알림을 Slack에 표시했습니다.<br/><br/>Slack 리마인더를 설정해 Slackbot의 회의 알림을 받도록 구성했습니다.',y)
    # Four tool cards: clear relationships, with the same assets as the website.
    w=(W-100)/3; cy=y-42
    for i,(logo,title,body) in enumerate([('jira-mark.png','Jira','스프린트 · 티켓'),('slack-mark.png','Slack','티켓 생성 · 회의 알림'),('confluence-mark.png','Confluence','문서 · 이슈 연결')]):
        x=38+i*(w+12); b.rect(x,y,w,104)
        with Image.open(ROOT/'assets'/logo) as im:
            im=im.convert('RGBA'); b.c.drawImage(ImageReader(im),x+(w-27)/2,y-39,27,27,mask='auto',preserveAspectRatio=True)
        b.text(title,x+10,y-47,w-20,10,BLUE,True)
        b.text(body,x+10,y-68,w-20,8,MUTED)
    y-=120
    y=b.text('<b>GitHub → Slack</b> · 코드 변경 알림을 팀 채널에 공유',38,y,W-76,9.5)-16
    w=(W-88)/2
    a=b.image('collab-jira-backlog.png',38,y,w,120,'Jira 스프린트 · 백로그 운영 설정')
    z=b.image('collab-jira-slack.png',50+w,y,w,120,'Jira 티켓 상태의 Slack 알림')
    y=min(a,z)-2
    a=b.image('collab-schedule-slack.png',38,y,w,112,'일일 계획 공유 · Slackbot 회의 알림')
    z=b.image('collab-github-slack.png',50+w,y,w,112,'GitHub push · commit 알림')
    y=min(a,z)-5
    b.link('온라인에서 프로젝트 화면과 상세 자료 보기',SITE,y)
    b.save()
    shutil.copy2(b.path,ROOT/'assets'/b.path.name)

def career():
    b=Book('choi-seeun-career-statement.pdf',2,'경력기술서')
    y=b.title('01 / CAREER SUMMARY','최세은 | 경력기술서','웹 백엔드 개발 · 검사장비 소프트웨어 유지보수 및 현장 대응')
    y=b.link('cseeun98@gmail.com','mailto:cseeun98@gmail.com',y)
    y=b.link('포트폴리오 / cseun.github.io',SITE,y)-4
    y=b.block('경력 요약','<b>웹 백엔드 개발 1년 7개월</b>의 실무 경험이 있습니다. PHP / Laravel 기반 상품·주문·정산 데이터 처리와 커머스 채널 연동, 내부 ERP 유지보수를 담당했습니다.<br/><br/>이후 BMS 검사장비의 테스트·CS 보조와 C# 소프트웨어 유지보수, 미국 현장 파견을 경험했습니다.',y)
    y=b.heading('에어텔닷컴 그룹 | 웹 백엔드 개발',y)
    y=b.text('2023.09 - 2025.03 · 1년 7개월 | PHP / Laravel',38,y,W-76,10,BLUE,True)-15
    y=b.block('담당 업무 01 · 업무 데이터 처리','PHP / Laravel 기반의 상품·주문·정산 데이터 처리 업무를 수행했습니다. 커머스 운영에 필요한 백엔드 기능과 데이터 처리 영역을 담당했습니다.',y)
    y=b.block('담당 업무 02 · 커머스 채널 연동','커머스 채널의 상품 연동 업무를 담당했습니다. 외부 판매 채널과 내부 업무 시스템 사이의 상품 정보를 다루는 개발·유지보수 업무를 수행했습니다.',y)
    y=b.block('담당 업무 03 · 내부 ERP 유지보수','내부 ERP의 유지보수 업무를 수행했습니다. 상품·주문·정산을 다루는 업무 시스템의 개발 경험을 쌓았습니다.',y)
    y=b.text('재직 중 소속이 마케팅하이랜즈에서 에어텔닷컴으로 변경되었으며, 동일 개발 조직에서 업무를 지속했습니다.',38,y,W-76,9,MUTED)-15
    b.text('운영 경험에서 개발 업무로의 전환<br/>2017년 운영직으로 근무했던 회사에 소프트웨어로 전공을 바꿔 2023년 개발자로 다시 합류했습니다.',38,y,W-76,10)

    y=b.title('02 / FIELD EXPERIENCE','장비 소프트웨어와 현장 대응','프리랜서 실무 · 이전 운영 경력 · 학력 및 현재 교육')
    y=b.heading('엑서테크 | 프리랜서',y)
    y=b.text('2025.04 - 2026.01 | 검사장비 S/W 유지보수 · 현장 대응',38,y,W-76,10,BLUE,True)-14
    y=b.block('BMS 검사장비 CS 및 테스트 보조와 C# S/W 유지보수','검사장비의 테스트·유지보수와 C# 소프트웨어 유지보수 업무를 수행했습니다. 장비 셋업·CS 업무를 지원했으며 미국 현장 파견에 2회 참여했습니다.<br/><br/>참여 업무 기준: 검사장비 테스트·유지보수 1.5개월 / 장비 셋업·CS 3개월',y)
    y=b.heading('마케팅하이랜즈 | 현지 파견 · 여행 OP',y)
    y=b.text('2017.12 - 2019.06 | 비개발 경력',38,y,W-76,9.5,BLUE)-9
    y=b.text('베트남 다낭에서 호텔 B2B 세일즈와 여행 운영을 담당했습니다. 예약·정산·고객 대응과 호텔 협업 업무를 수행했습니다. 해당 회사는 현재 에어텔닷컴 그룹입니다.',38,y,W-76,9.5)-20
    y=b.heading('학력 및 전문 교육',y)
    y=b.block('신구대학교 · IT소프트웨어학과','3년제 · 2025년 졸업 · 학점 4.18 / 4.5',y)
    y=b.block('대한상공회의소 서울기술교육센터','AI융합 로봇 SW개발자 3기 과정 진행 중<br/>FMS 관제 UI·React 구현, AI 모델 비교·경로 생성, STM32 / CAN 및 PLC·HMI 프로젝트를 수행하고 있습니다.',y)
    y=b.heading('교육 프로젝트는 별도 포트폴리오로 첨부',y)
    y=b.text('교육 프로젝트의 개인 담당 업무·구현 화면·비교 실험 결과는 포트폴리오에 정리했습니다. 실무 경력과 교육 프로젝트를 구분해 확인할 수 있습니다.',38,y,W-76,9.5)-9
    b.link('프로젝트 및 소스 코드 확인',SITE,y)
    b.save()

if __name__=='__main__':
    portfolio()
    career()
