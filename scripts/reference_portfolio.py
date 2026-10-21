"""Five-page portfolio matching the supplied editorial reference layout."""
from create_application_pdfs import *
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
import create_application_pdfs as base

COLORS = {'#17344D':'#26354A','#28659C':'#526B91','#8D505C':'#657695',
          '#647384':'#657184','#DDE5EC':'#DCE2EA','#F0F5F9':'#F1F4F8',
          '#F8EFF1':'#EEF0F6','#F3F6F8':'#F3F5F8'}
base.ACCENT='#657695'
base.NAVY='#26354A'
base.BLUE='#526B91'

class Editorial(Book):
    def text(self,text,x,y,w,size=10,color=NAVY,bold=False,leading=None):
        for old,new in COLORS.items(): text=text.replace(old,new)
        return super().text(text,x,y,w,size,COLORS.get(color,color),bold,leading)
    def rect(self,x,y,w,h,fill=PALE,stroke=None):
        fill=COLORS.get(fill,fill); stroke=COLORS.get(stroke,stroke)
        self.c.setFillColor(HexColor(fill)); self.c.setStrokeColor(HexColor(stroke or fill))
        self.c.rect(x,y-h,w,h,fill=1,stroke=bool(stroke))
    def line(self,y,x=38,w=W-76,color=LINE):
        self.c.setStrokeColor(HexColor(COLORS.get(color,color))); self.c.setLineWidth(.7); self.c.line(x,y,x+w,y)
    def image(self,file,x,y,w,h,caption=None):
        with Image.open(ROOT/'assets'/file) as im:
            iw,ih=im.size; scale=min(w/iw,h/ih); dw,dh=iw*scale,ih*scale
            im=im.convert('RGB'); im.thumbnail((1600,1200))
            data=BytesIO(); im.save(data,format='JPEG',quality=90,optimize=True); data.seek(0)
            self.c.drawImage(ImageReader(data),x+(w-dw)/2,y-h+(h-dh)/2,dw,dh)
        yy=y-h-5
        if caption: yy=self.text(caption,x,yy,w,8,MUTED)-9
        return yy
    def qr(self,url,x,y,label,size=45):
        self.rect(x-3,y+3,size+8,size+18,'#FFFFFF')
        q=QrCodeWidget(url); a,b,c,d=q.getBounds(); scale=size/(c-a)
        drawing=Drawing(size,size,transform=[scale,0,0,scale,0,0]); drawing.add(q)
        renderPDF.draw(drawing,self.c,x,y-size)
        self.c.linkURL(url,(x,y-size,x+size,y),relative=0)
        self.text(label,x-3,y-size-3,size+12,6.5,MUTED)
    def title(self,kicker,title,desc=None):
        y=self.page(kicker)
        y=self.text(kicker,38,y,W-76,8,ACCENT,True)-8
        y=self.text(title,38,y,W-76,23,bold=True,leading=30)-8
        if desc:y=self.text(desc,38,y,W-76,9,MUTED)-14
        self.line(y,color=ACCENT)
        return y-14
    def band(self,title,body,x,y,w,h,fill=PALE):
        self.rect(x,y,w,h,fill)
        self.c.setStrokeColor(HexColor(COLORS[BLUE])); self.c.setLineWidth(1.5); self.c.line(x,y,x,y-h)
        yy=self.text(title,x+8,y-7,w-16,9,BLUE,True)-5
        self.text(body,x+8,yy,w-16,8.3,leading=12.5)

def portfolio():
    b=Editorial('choi-seeun-portfolio.pdf',5,'ROBOTICS PORTFOLIO')
    b.page('PROFILE / SKILLS')
    x=204; w=W-x-38
    b.c.setStrokeColor(HexColor(COLORS[BLUE])); b.c.setLineWidth(.6); b.c.line(187,70,187,H-70)
    b.image('profile.jpg',53,754,119,158)
    y=568
    for title,body in [
        ('연락처','<b>이메일</b><br/>cseeun98@gmail.com<br/><br/><b>GitHub</b><br/>github.com/cseun'),
        ('학력','<b>신구대학교</b><br/>IT소프트웨어학과 · 3년제<br/>2025년 졸업<br/><b>학점 4.18 / 4.5</b>'),
        ('주요 경력','<b>에어텔닷컴 그룹</b><br/>웹 백엔드 · 1년 7개월<br/>2023.09 - 2025.03<br/><br/><b>엑서테크 프리랜서</b><br/>검사장비 S/W · 현장 대응<br/>2025.04 - 2026.01'),
        ('전문 교육','<b>AI융합 로봇 SW개발자 3기</b><br/>대한상공회의소<br/>서울기술교육센터 · 진행 중')]:
        y=b.text(title,38,y,135,10,BLUE,True)-5; b.line(y,38,135); y-=9
        y=b.text(body,38,y,135,8.5,leading=13)-21
    b.text('ROBOTICS SOFTWARE PORTFOLIO',x,756,w,8,ACCENT,True)
    b.text('최세은',x,733,w,33,bold=True,leading=42)
    b.text('로봇 시스템 개발자',x,684,w,12,BLUE,True)
    b.text('웹 백엔드와 현장 장비 경험을 바탕으로<br/>로봇 제어와 관제 소프트웨어를 개발합니다.',x,656,w-12,9,bold=True)
    b.qr('https://github.com/cseun',W-89,736,'GitHub 저장소',43)
    b.text('주요 분야  FMS UI / AI 경로 판단 / 장치 제어',x,604,w,9,bold=True)
    b.line(584,x,w)
    b.text('01 / SKILLS & EXPERIENCE',x,570,w,8,ACCENT,True)
    b.text('기술 역량과 개발 경험',x,548,w,18,bold=True)
    b.text('화면·데이터·장치 상태를 연결한 구현 경험',x,516,w,9,BLUE)
    y=493
    skills=[
        ('01','웹 백엔드 개발','PHP · Laravel · 커머스 연동 · ERP','상품·주문·정산 데이터 처리<br/>커머스 채널 상품 연동과 내부 ERP 유지보수'),
        ('02','FMS 관제 UI·프론트엔드','Figma · React · Claude AI · ChatGPT','관제 화면 설계와 React 프론트엔드 구현<br/>AI 도구로 구성한 화면·코드 검토 및 통합'),
        ('03','AI 모델 비교·경로 생성','LLM · Iterative · 경로 평가','모델·입력 조건별 도착률·경로·응답 시간 비교<br/>최단 경로 생성과 시뮬레이션 주행 반영'),
        ('04','임베디드·산업 장치 제어','STM32 · CAN · PLC · HMI','차량 상태 표시와 조명·부저 출력<br/>수동·자동 운전과 HMI 조작·상태 화면 구성')]
    for n,title,tech,body in skills:
        b.line(y,x,w,ACCENT if n=='01' else LINE)
        b.text(n,x,y-10,22,10,ACCENT,True)
        b.text(title,x+26,y-10,w-26,11,bold=True)
        b.text(tech,x+26,y-31,w-26,8,BLUE,True)
        b.text('• '+body.replace('<br/>','<br/>• '),x+26,y-50,w-26,8.5,leading=13)
        y-=95
    b.line(y,x,w); b.text('협업 도구',x,y-10,w,9,bold=True)
    b.text('Git / GitHub / Jira / Confluence / Slack',x,y-29,w,8.5,BLUE)

    y=b.title('02 / PROJECTS','AI 융합 다중 로봇 물류','AX MULTI-ROBOT LOGISTICS  |  팀 E1I6 · 7명 · 담당 FMS AI')
    y=b.text('프로젝트 목표',38,y,W-76,8,ACCENT,True)-5
    y=b.text('주문에 따라 여러 TurtleBot이 물품을 운반하도록 관제하고, 이동 중 상황 판단과 경로 생성을 AI로 확장하는 물류 자동화 시스템입니다.',38,y,W-76,9)-13
    b.text('주문부터 이동·작업까지',38,y,245,11,bold=True)
    b.text('담당 역할',309,y,245,11,bold=True); y-=25
    for i,(title,desc) in enumerate([('FMS','주문·배차·경로 관제'),('AMR','자율주행·물품 이동'),('작업 장치','물품 적재·하역')]):
        xx=38+i*83
        b.rect(xx,y,77,66,'#F8EFF1' if i==0 else '#FFFFFF',ACCENT if i==0 else LINE)
        b.text(('담당<br/>' if i==0 else '')+'<b>'+title+'</b><br/>'+desc,xx+6,y-9,65,8.3)
    b.band('01 · UI 설계 및 React 구현','Figma·Claude AI로 설계하고 ChatGPT·Figma를 활용해 프론트엔드를 구현·통합했습니다.',309,y,248,59)
    b.band('02 · AI 모델 선정·경로 생성','조건별 모델 비교와 최단 경로 주행을 구현했습니다. 충돌 모니터링·예측은 진행 중입니다.',309,y-65,248,59,'#F8EFF1')
    b.text('주문·배차 → 경로 생성 → 이동 → 작업',38,y-75,249,8,MUTED)
    b.text('팀원 담당: ROS 2 / MQTT 연동,<br/>A* 탐색 알고리즘 및 예외 처리',38,y-95,249,8,MUTED)
    y-=132; b.line(y); y-=12
    y=b.text('시연 · 관제 화면',38,y,W-76,12,bold=True)-10
    b.image('fms-dashboard.png',38,y,250,101)
    b.image('fms-dashboard-live.png',307,y,250,101)
    b.qr('https://youtu.be/HqL8_q4xefw',510,y-5,'시연 영상',40)
    y-=108
    b.text('<b>Figma 관제 화면 설계</b>',38,y,250,8.5)
    b.text('<b>FMS 웹 관제 대시보드</b>',307,y,250,8.5)
    y-=22; b.line(y); y-=11
    y=b.text('담당 업무',38,y,W-76,11,ACCENT,True)-9
    b.rect(38,y,W-76,18,BLUE); b.text('구현 완료 · 화면 구현 / 모델 비교 / 최단 경로 주행',44,y-3,W-88,8,'#FFFFFF',True); y-=25
    cw=(W-96)/3
    for i,(t,d) in enumerate([('01  관제 UI·React','화면 설계와 프론트엔드 구현·통합. AI 도구로 작성한 코드 검토.'),
                             ('02  모델·입력 비교','7개 모델 × 2개 입력 × 84쌍 × 5회 반복, 총 5,880회 테스트.'),
                             ('03  경로 생성·주행','Iterative 선택에 연결 검증·재방문 제한을 적용하고 주행에 반영.')]):
        b.band(t,d,38+i*(cw+10),y,cw,65)
    y-=74
    b.rect(38,y,W-76,18,ACCENT); b.text('진행 중 · AI 충돌 모니터링·예측 / 최적 경로 확장',44,y-3,W-88,8,'#FFFFFF',True); y-=25
    b.band('최적 경로가 필요한 이유','여러 로봇이 통로를 함께 사용하므로 이동 거리뿐 아니라 충돌 위험·대기 시간·하드웨어·주행 환경을 고려해 안전하고 효율적인 경로를 선택하는 것이 목표입니다.',38,y,W-76,52,'#F8EFF1')

    y=b.title('02 / PROJECTS','이전 프로젝트','임베디드 계기판, 안전 앱, 센서 데모와 PLC 제어 프로젝트입니다.')
    projects=[
        ('kickcan-real-card.jpg','01 / EMBEDDED','CAN 기반 RC카 계기판','개인 담당 · Node 2 | STM32 · CAN · SPI','CAN 수신 ID·형식·길이 검증 및 상태 갱신<br/>TFT 2대·CLCD 표시, 조명·부저 출력<br/>SPI 공유·개별 CS 제어와 핀맵·배선 구성','https://github.com/kick-can/Node_2'),
        ('safekick-app-flow.png','02 / APP & DEVICE','SafeKick 안전 앱','React Native · Expo · HTTP · SSE','가입·면허·QR·셀피 인증·안전 점검 화면 구현<br/>HTTP 결과와 SSE 상태를 앱에 표시<br/>데모 장치 지원 및 제출 영상 기획·편집','https://github.com/safe-kick/safe-kick-app'),
        ('umjoo-case.jpg','03 / SENSOR & PROTOTYPE','음주 측정 데모와 시제품','개인 담당 · STM32 데모 · Fusion 360','MQ-3 기준값 변화와 버튼·LED·부저 연동<br/>실측 기반 케이스·센서 홀더 모델링·3D 출력<br/>얼굴 인식·실제 하드웨어 최종 통합은 팀원 담당','https://github.com/Umjoo-Cut/StmDemo'),
        ('plc-manual.jpg','04 / FACTORY AUTOMATION','PLC 수동·자동 제어와 HMI','MELSEC Q · GX Works2 · GT Designer3','수동 입출고·실린더·서보 동작 확인<br/>자동 운전 시퀀스 구성<br/>서보 원점 복귀·위치 티칭·JOG 점검',SITE+'#plc')]
    for file,k,t,tech,body,url in projects:
        b.image(file,38,y,132,111)
        b.text(k,182,y,320,7,BLUE,True)
        b.text(t,182,y-15,320,13,bold=True)
        b.text(tech,182,y-39,320,8,BLUE)
        b.text('• '+body.replace('<br/>','<br/>• '),182,y-57,315,8.3,leading=12)
        b.qr(url,514,y-5,'상세 / 코드',39)
        b.link('프로젝트 상세 보기',url,y-117,182,320)
        y-=137; b.line(y,color=BLUE); y-=10

    y=b.title('02 / PROJECTS','문제 해결','직접 수행한 비교 실험과 구현 과정에서의 판단을 정리했습니다.')
    cases=[
        ('01 / LLM · 평가 기준','비교 기준 수립',[
            ('문제','모델이 생성한 경로를 평가할 최단 경로 기준과 모델 선택 우선순위가 필요했습니다.'),
            ('접근','논문의 Dijkstra·A* 비교 결과를 검토하고, 단일 목적지·좌표 정보가 있는 프로젝트 조건에 맞춰 A*를 평가 기준으로 선정했습니다.'),
            ('기준','도착률을 우선 확인하고 A* 최단 비용 일치율과 응답 시간을 함께 비교했습니다.')]),
        ('02 / LLM · 경로 선택','입력·선택 방식 비교',[
            ('대상','전체 경로를 한 번에 생성하는 Direct 방식에서 성능이 좋았던 3개 모델을 선정하고, 같은 출발·도착 10쌍으로 비교했습니다.'),
            ('조건','<b>입력 정보 2종</b>: 전체 경로 정보만 / 인접 노드 정보도 추가<br/><b>생성 방식 3종</b><br/>① 전체 경로를 한 번에 생성<br/>② 프롬프트로 가까운 노드를 하나씩 추출하도록 요청<br/>③ 코드가 모델을 반복 호출해 바로 다음 이동 노드를 선택'),
            ('결과','입력 2종 × 생성 방식 3종 = 6조건을 비교했습니다. <b>인접 정보 추가 + 코드 반복 호출</b> 방식에서 30회(3개 모델 × 10쌍) 중 28회 도착했습니다.')]),
        ('03 / LLM · 모델 선정','도착 안정성 우선',[
            ('대상','<b>모델 7종</b><br/>Gemma 3 12B · DeepSeek Coder 6.7B · Phi-4 14B<br/>Kev 0.8B · Kev 4B · Laya · Laya multilingual'),
            ('조건','<b>입력 2종</b>: 전체 그래프만 / 전체 그래프 + 인접 정보<br/><b>출발·목적지 84쌍</b>: 출발은 모든 노드 13개, 목적지는 물품을 싣고 내리는 도킹 노드 7개입니다.<br/>13 × 7 − 출발과 도착이 같은 7쌍 = 84쌍<br/><b>총 5,880회</b>: 7개 모델 × 2개 입력 × 84쌍 × 5회 반복'),
            ('결과','Kev 0.8B + 인접 추가: 도착 420/420, 최단 비용 일치 220/420(52.4%), 중앙값 0.409초. Kev 4B + 전체: 도착 400/420, 최단 일치 315/420(75.0%), 0.613초.'),
            ('선택','<b>Kev 0.8B + 인접 정보 추가</b>를 채택했습니다. 도착률 100%와 경로 생성 시간 중앙값 <b>0.409초</b>를 함께 고려했습니다. 최단 비용 일치율이 높은 Kev 4B + 전체 그래프(중앙값 0.613초)는 대안으로 비교했습니다.')]),
        ('04 / COLLABORATION','작업·문서·알림 연결',[
            ('필요','스프린트 작업, 문서, 코드 변경과 회의 일정을 팀에서 함께 확인할 환경이 필요했습니다.'),
            ('구현','Jira 스프린트·백로그 운영을 설정하고 Slack 티켓 생성, Confluence·Jira 연결, GitHub 알림을 구성했습니다.'),
            ('운영','Slack에서 티켓 상태와 push·commit 알림을 확인하고, Slackbot 리마인더로 회의 알림을 받도록 설정했습니다.')])]
    for k,t,rows in cases:
        b.text(k,38,y,143,7.5,ACCENT,True)
        b.text(t,38,y-17,143,11,bold=True)
        yy=y
        for label,body in rows:
            b.text(label,192,yy,32,8.5,ACCENT,True)
            yy=b.text(body,236,yy,W-274,8.7,leading=13)-9
        y=min(y-120,yy-6); b.line(y,color=ACCENT); y-=13

    y=b.title('03 / EXPERIENCE & EDUCATION','주요 이력','웹 백엔드 개발과 현장 장비 경험을 로봇 소프트웨어로 확장하고 있습니다.')
    for date,title,body,h in [
        ('2025.04 - 2026.01','엑서테크 | 프리랜서','BMS 검사장비 CS 및 테스트 보조와 C# S/W 유지보수<br/>미국 현장 파견 2회<br/>검사장비 테스트·유지보수 1.5개월 / 장비 셋업·CS 3개월',106),
        ('2023.09 - 2025.03','에어텔닷컴 그룹 | 웹 백엔드','PHP / Laravel 기반 상품·주문·정산 데이터 처리<br/>커머스 채널 상품 연동과 내부 ERP 유지보수<br/>재직 중 소속 변경: 마케팅하이랜즈 → 에어텔닷컴',106),
        ('2017.12 - 2019.06','마케팅하이랜즈 | 여행 OP · 비개발','베트남 다낭 현지 파견, 호텔 B2B 세일즈와 여행 운영<br/>예약·정산·고객 대응 및 호텔 협업',94)]:
        b.text(date,38,y,122,8,BLUE,True)
        b.text(title,174,y,W-212,12,bold=True)
        b.text('• '+body.replace('<br/>','<br/>• '),174,y-26,W-212,9,leading=15)
        y-=h; b.line(y,color=BLUE); y-=17
    y=b.text('웹 백엔드 개발 경력은 1년 7개월입니다. 운영직으로 근무했던 회사에 소프트웨어로 전공을 바꿔 2023년 개발자로 다시 합류했습니다.',38,y,W-76,9)-24
    cw=(W-92)/2
    for xx,title,logo,body in [
        (38,'학력','singgu-symbol.png','<b>신구대학교 · IT소프트웨어학과</b><br/>3년제 · 2025년 졸업<br/>학점 4.18 / 4.5'),
        (54+cw,'전문 교육','kcci-symbol.png','<b>대한상공회의소 서울기술교육센터</b><br/>AI융합 로봇 SW개발자 3기<br/>진행 중')]:
        b.rect(xx,y,cw,150,'#F3F6F8'); b.line(y,xx,cw,BLUE)
        b.text(title,xx+12,y-14,cw-24,12,bold=True)
        b.c.drawImage(str(ROOT/'assets'/logo),xx+12,y-79,30,30,mask='auto',preserveAspectRatio=True)
        b.text(body,xx+12,y-91,cw-24,9,leading=16)
    y-=166
    b.text('프로젝트 상세 자료와 시연 영상은 온라인 포트폴리오에서 확인할 수 있습니다.',38,y,W-76,9)
    b.link('cseun.github.io',SITE,y-22)
    b.save()
    shutil.copy2(b.path,ROOT/'assets'/b.path.name)

if __name__=='__main__':portfolio()


