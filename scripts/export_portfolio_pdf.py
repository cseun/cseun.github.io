"""Build the downloadable portfolio from index.html and its existing assets."""
from pathlib import Path
from html import escape
from urllib.parse import urljoin
import os
import shutil
import re

from lxml import html
from PIL import Image as PILImage
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, Flowable

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'output' / 'pdf' / 'choi-seeun-portfolio.pdf'
ASSET = ROOT / 'assets' / OUTPUT.name
SITE = 'https://cseun.github.io/'
TREE = html.fromstring((ROOT / 'index.html').read_text(encoding='utf-8'))
PAGE_W, PAGE_H = A4
WIDTH = PAGE_W - 72
BLUE = colors.HexColor('#1C619E')
INK = colors.HexColor('#202C3A')
MID = colors.HexColor('#536273')
PALE = colors.HexColor('#EDF5FC')
LINE = colors.HexColor('#DCE5EE')

FONT_DIR = Path(os.environ.get('WINDIR', r'C:\Windows')) / 'Fonts'
pdfmetrics.registerFont(TTFont('Malgun', str(FONT_DIR / 'malgun.ttf')))
pdfmetrics.registerFont(TTFont('Malgun-Bold', str(FONT_DIR / 'malgunbd.ttf')))
pdfmetrics.registerFontFamily('Malgun', normal='Malgun', bold='Malgun-Bold', italic='Malgun', boldItalic='Malgun-Bold')

STYLES = {
    'body': ParagraphStyle('body', fontName='Malgun', fontSize=9, leading=14, textColor=INK, wordWrap='CJK', spaceAfter=5),
    'small': ParagraphStyle('small', fontName='Malgun', fontSize=7.6, leading=11.4, textColor=MID, wordWrap='CJK', spaceAfter=4),
    'label': ParagraphStyle('label', fontName='Malgun-Bold', fontSize=8, leading=12, textColor=BLUE, wordWrap='CJK', spaceAfter=5),
    'heading': ParagraphStyle('heading', fontName='Malgun-Bold', fontSize=15, leading=21, textColor=INK, wordWrap='CJK', spaceAfter=10),
    'title': ParagraphStyle('title', fontName='Malgun-Bold', fontSize=22, leading=29, textColor=INK, wordWrap='CJK', spaceAfter=8),
    'name': ParagraphStyle('name', fontName='Malgun-Bold', fontSize=29, leading=36, textColor=INK, spaceAfter=6),
    'experiment': ParagraphStyle('experiment', fontName='Malgun', fontSize=10, leading=16, textColor=INK, wordWrap='CJK', spaceAfter=7),
}


def cls(name):
    return f"contains(concat(' ',normalize-space(@class),' '),' {name} ')"


def find(node, name):
    return node.xpath('.//*[' + cls(name) + ']')


def by_id(name):
    return TREE.get_element_by_id(name)


def plain(node):
    return re.sub(r'\s+', ' ', ' '.join(node.itertext())).strip()


def inner(node):
    result = escape(node.text or '')
    for child in node:
        tag = child.tag
        content = inner(child)
        if tag in ('b', 'strong'):
            result += '<b>' + content + '</b>'
        elif tag == 'br':
            result += '<br/>'
        elif tag == 'a' and child.get('href'):
            href = escape(urljoin(SITE, child.get('href')), quote=True)
            result += f'<a href="{href}" color="#1C619E">{content}</a>'
        else:
            result += content
            if tag == 'span':
                result += ' '
        result += escape(child.tail or '')
    return result


def p(text, style='body'):
    return Paragraph(text if isinstance(text, str) else inner(text), STYLES[style])


def paragraphs(node, style='body'):
    return [p(x, 'label' if 'label' in x.get('class', '').split() else style) for x in node.xpath('.//p')]


def link(label, url):
    return p(f'<a href="{escape(url, quote=True)}" color="#1C619E"><b>{escape(label)}</b></a>', 'small')


def card(content, width=WIDTH, fill=PALE):
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), fill),
        ('BOX', (0, 0), (-1, -1), .5, LINE),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
    ]))
    return t


def columns(left, right, split=.5):
    gap = 14
    widths = [(WIDTH - gap) * split, gap, (WIDTH - gap) * (1 - split)]
    t = Table([[left, '', right]], colWidths=widths)
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0), ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
    return t


def image(src, width=WIDTH, max_height=300):
    path = ROOT / src
    with PILImage.open(path) as im:
        iw, ih = im.size
    scale = min(width / iw, max_height / ih)
    item = Image(str(path), width=iw * scale, height=ih * scale)
    item.hAlign = 'CENTER'
    return item


def figure(src, caption, width=WIDTH, max_height=300):
    return [image(src, width, max_height), Spacer(1, 5), p(caption, 'small'), Spacer(1, 8)]


def repo_links(article):
    return [link(plain(a), urljoin(SITE, a.get('href'))) for a in find(article, 'repo')]


def project_header(article, kicker=None):
    return [p(kicker or plain(find(article, 'proj-eyebrow')[0]), 'label'), p(article.xpath('./h2')[0], 'title')] + [p(x) for x in article.xpath('./p')]


TITLES = ['프로필 · 경력 · 교육', '기술 스택 · 프로젝트', 'E1I6 · FMS UI와 AI', 'E1I6 · LLM 경로 판단', 'E1I6 · 발표자료와 시연', 'Kick CAN · 계기판 노드', 'Kick CAN · 하드웨어', 'SafeKick · 담당 범위', 'SafeKick · 화면과 서버', '음주컷 · 데모와 시제품', 'PLC MPS · 제어와 HMI', '협업 환경 · 알림 연동']


def decorate(c, doc):
    c.saveState()
    c.setStrokeColor(BLUE)
    c.setLineWidth(2)
    c.line(36, PAGE_H - 28, PAGE_W - 36, PAGE_H - 28)
    c.setFont('Malgun', 7.4)
    c.setFillColor(MID)
    c.drawString(36, PAGE_H - 43, 'CHOI SEEUN  /  ROBOTICS SOFTWARE PORTFOLIO')
    c.setStrokeColor(LINE)
    c.setLineWidth(.5)
    c.line(36, 35, PAGE_W - 36, 35)
    c.drawString(36, 23, '최세은 · 로봇 시스템 개발자')
    c.drawCentredString(PAGE_W / 2, 23, 'cseun.github.io')
    c.linkURL(SITE, (PAGE_W / 2 - 42, 20, PAGE_W / 2 + 42, 32), relative=0)
    c.drawRightString(PAGE_W - 36, 23, f'{doc.page:02d} / {len(TITLES):02d}')
    c.bookmarkPage(f'page{doc.page}')
    if doc.page <= len(TITLES):
        c.addOutlineEntry(TITLES[doc.page - 1], f'page{doc.page}', level=0)
    c.restoreState()


class ToolDiagram(Flowable):
    def __init__(self):
        super().__init__()
        self.width = WIDTH
        self.height = 160

    def draw(self):
        c = self.canv
        positions = [('Jira', 'jira-mark.png', 50, 85, '스프린트 · 백로그'), ('Confluence', 'confluence-mark.png', WIDTH - 165, 85, '문서 · 이슈 연결'), ('Slack', 'slack-mark.png', WIDTH / 2 - 57, 38, '티켓 생성 · 회의 알림'), ('GitHub', 'github-mark.png', WIDTH / 2 - 57, -6, 'push · 커밋 알림')]
        c.setStrokeColor(colors.HexColor('#ADC9E2'))
        c.setLineWidth(1)
        c.line(165, 111, WIDTH - 165, 111)
        c.line(165, 85, WIDTH / 2, 62)
        c.line(WIDTH - 165, 85, WIDTH / 2, 62)
        c.line(WIDTH / 2, 38, WIDTH / 2, 17)
        for name, logo, x, y, desc in positions:
            c.setFillColor(colors.white)
            c.setStrokeColor(LINE)
            c.roundRect(x, y, 115, 42, 6, fill=1, stroke=1)
            c.drawImage(str(ROOT / 'assets' / logo), x + 9, y + 10, 25, 25, preserveAspectRatio=True, mask='auto')
            c.setFillColor(INK)
            c.setFont('Malgun-Bold', 9)
            c.drawString(x + 41, y + 26, name)
            c.setFillColor(MID)
            c.setFont('Malgun', 6.5)
            c.drawString(x + 41, y + 12, desc)


def build():
    story = []
    add = story.extend
    gap = lambda n=10: story.append(Spacer(1, n))
    def new_page():
        story.append(PageBreak())

    # 01 - Profile and factual career history.
    hero = find(TREE, 'hero-content')[0]
    profile = [p('ROBOTICS SOFTWARE PORTFOLIO', 'label'), p('최세은', 'name'), p('로봇 시스템 개발자', 'heading'), p(hero.xpath('./p')[1]), p('웹 백엔드 1년 7개월 · 장비 S/W 및 현장 대응 경험', 'small')]
    profile += [link(plain(a), a.get('href')) for a in find(hero, 'hero-links')[0].xpath('./a') if not a.get('download')]
    story.append(columns([image('assets/profile.jpg', 92, 124)], profile, .22))
    gap(14)
    story.append(p('경력', 'heading'))
    for job in find(by_id('career'), 'job'):
        left = [p(find(job, 'when')[0], 'label'), p(job.xpath('./div/h3')[0]), p(find(job, 'role')[0], 'small')]
        if len(find(job, 'role')) > 1:
            left.append(p(find(job, 'role')[1], 'small'))
        details = [p(x) for x in find(job, 'detail')[0].xpath('./p')]
        story.append(columns(left, details, .33))
        gap(10)
    story.append(card([p(find(by_id('career'), 'note')[0], 'small')]))
    gap(14)
    story.append(p('학력 및 전문 교육', 'heading'))
    entries = find(by_id('education'), 'education-entry')
    edu = []
    for entry in entries:
        details = entry.xpath('.//div[' + cls('institution') + ']/div')[0]
        content = [p(x) for x in details.xpath('./h3|./p')]
        content += [link(plain(a), urljoin(SITE, a.get('href'))) for a in details.xpath('.//a')]
        edu.append(card(content, (WIDTH - 14) / 2, colors.HexColor('#F7FAFD')))
    story.append(columns(edu[0], edu[1]))

    # 02 - Stack, navigable project index, working approach.
    new_page()
    add([p('SKILLS & PROJECTS', 'label'), p('기술 스택과 프로젝트', 'title')])
    for row in find(TREE, 'stack-row'):
        heading = row.xpath('./h3')
        if heading:
            badges = find(row, 'badge')
            story.append(columns([p(heading[0], 'label')], [p(' · '.join(plain(x) for x in badges))], .19))
            gap(7)
    add([p('실무 사용: C#(WinForms), PHP, Laravel, REST API, MySQL, JavaScript, HTML, Git, Jira, Confluence', 'small'), Spacer(1, 12), p('프로젝트 찾아보기', 'heading')])
    for item, page in zip(find(by_id('projects'), 'projcard'), [3, 6, 8, 10, 11]):
        add([p(f'<link href="#page{page}" color="#1C619E"><b>{escape(plain(item.xpath(".//h3")[0]))}</b></link>'), p(item.xpath('.//div/p[last()]')[0], 'small')])
        gap(3)
    add([link('기타 · 협업 환경 셋업과 알림 연동 (12쪽)', '#page12'), Spacer(1, 12), p('일하는 방식', 'heading')])
    for item in find(by_id('method'), 'card'):
        add([p(item.xpath('./h3')[0], 'label'), p(item.xpath('./p')[0])])

    # 03 - FMS responsibilities, purpose and actual UI.
    fms = by_id('fms')
    new_page()
    add(project_header(fms))
    roles = find(fms, 'fms-role-grid')[0]
    cards = roles.xpath('./div')
    role_cards = []
    for item in cards[:2]:
        content = paragraphs(item)
        if find(item, 'chip'):
            content.insert(0, p('진행 중', 'label'))
        role_cards.append(card(content, (WIDTH - 14) / 2))
    story.append(columns(*role_cards))
    gap()
    story.append(p(cards[2], 'small'))
    purpose = find(fms, 'fms-purpose')[0]
    story.append(card([p(purpose.xpath('./strong')[0], 'label'), p(purpose.xpath('./p')[0])]))
    gap(12)
    add(figure('assets/fms-dashboard.png', 'FMS 시뮬레이션 관제 화면', max_height=235))
    add([link('Figma 관제 화면 설계 보기', fms.xpath('.//a[contains(@href,"figma.com")]/@href')[0]), link('핵심 기능 시연 · 전체 시나리오', 'https://youtu.be/HqL8_q4xefw')])
    add(repo_links(fms))

    # 04 - Experiments and ongoing work remain clearly differentiated.
    new_page()
    add([p('E1I6 / FMS AI', 'label'), p('LLM 경로 판단', 'title'), p(find(fms, 'fms-presentation-lead')[0])])
    for item in find(fms, 'fms-presentation-points')[0].xpath('./li'):
        add([p(inner(item).replace('</b>', '</b><br/>', 1), 'experiment'), Spacer(1, 8)])
    story.append(card([p(find(fms, 'fms-presentation-scope')[0].xpath('./strong')[0], 'label')] + paragraphs(find(fms, 'fms-presentation-scope')[0])))
    gap(12)
    add(paragraphs(find(fms, 'fms-presentation-detail')[0]))
    gap(12)
    ongoing = find(fms, 'fms-ongoing')[0]
    story.append(card([p('진행 중 · AI 기반 충돌 모니터링·예측', 'label')] + [p(x) for x in ongoing.xpath('./p')], fill=colors.HexColor('#FFF5DF')))

    # 05 - Representative slides retain visual evidence and live links.
    new_page()
    add([p('E1I6 / EXPERIMENT EVIDENCE', 'label'), p('경로 판단 발표자료와 시연', 'title')])
    add(figure('assets/fms-presentation-03.png', 'V1·V2 기법 비교 · 발표자료 3장', max_height=282))
    add(figure('assets/fms-presentation-04.png', '84쌍 최종 테스트 결과 · 발표자료 4장', max_height=282))
    add([link('전체 발표자료 11장 보기 · 웹 슬라이드', SITE + '#fms'), link('LLM 경로 생성 및 시뮬레이션 주행 시연', SITE + 'assets/fms-llm-route-demo.mp4')])

    # 06-07 - CAN software and full-size hardware evidence.
    kick = by_id('kickcan')
    new_page()
    add(project_header(kick))
    mine = find(kick, 'mine')[0]
    story.append(card(paragraphs(mine)))
    gap(12)
    for row in find(kick, 'noderow'):
        story.append(p(' · '.join(plain(x) for x in row.xpath('./span')), 'small'))
    gap(10)
    for step in find(kick, 'step'):
        add([p(step.xpath('.//h4')[0], 'label'), p(step.xpath('.//p')[0])])
    gap(10)
    half = (WIDTH - 14) / 2
    story.append(columns(figure('assets/kickcan-real-card.jpg', 'RC카 실물 · Node 2 계기판', half, 190), figure('assets/kickcan-tft.jpg', 'TFT 화면 구성과 SPI 연결', half, 190)))
    add(repo_links(kick))
    new_page()
    add([p('KICK CAN / NODE 2', 'label'), p('하드웨어 연결과 핀맵', 'title')])
    add(figure('assets/kickcan-wiring.jpg', 'Node 2 하드웨어 연결 구성', max_height=300))
    add(figure('assets/kickcan-pinmap.jpg', '직접 작성한 핀맵 · 기능별 사용 핀과 연결 대상', max_height=295))
    add(repo_links(kick))

    # 08-09 - SafeKick responsibilities vs implemented application.
    safe = by_id('safekick')
    new_page()
    add(project_header(safe))
    story.append(card(paragraphs(find(safe, 'mine')[0])))
    gap(12)
    add([p('사용자 흐름', 'label'), p('면허증 등록 · QR 연결 → 얼굴·헬멧 및 안전 점검 → 운행 상태 확인 · 반납')])
    add([p(find(safe, 'theirs')[0], 'small'), Spacer(1, 8)])
    add(figure('assets/safekick-modules.jpg', '팀 시제품과 장치 구성', max_height=310))
    add(repo_links(safe))
    new_page()
    add([p('SAFEKICK / APPLICATION', 'label'), p('인증·안전 점검 화면과 서버 연동', 'title')])
    cards = [x for x in find(safe, 'kv') if x.xpath('./p[' + cls('label') + ']') and plain(x.xpath('./p[' + cls('label') + ']')[0]) in ['화면 구현', '서버와 연결']]
    story.append(columns(*[card(paragraphs(x), half) for x in cards]))
    gap(16)
    add(figure('assets/safekick-app-flow.png', 'SafeKick 앱 화면 흐름 · 홈, 인증, 안전 점검', max_height=285))
    story.append(card([p('2026 ESW Contest 출품 시연 영상', 'label'), p('2분 29초 · 기획 및 편집'), link('YouTube에서 시연 영상 보기', 'https://youtu.be/aibkoaQ87P8')]))
    gap(10)
    add(repo_links(safe))

    # 10 - Physical alcohol sensor demo.
    umjoo = by_id('umjoo')
    new_page()
    add(project_header(umjoo))
    cards = find(umjoo, 'umjoo-cards')[0].xpath('./div')
    for pair in [cards[:2], cards[2:]]:
        story.append(columns(*[card(paragraphs(x) if x.xpath('./p') else [p(x)], half) for x in pair]))
        gap(10)
    gap(8)
    story.append(columns(figure('assets/umjoo-case.jpg', '실측 모델링 · STL 출력 케이스와 센서 거치대', half, 295), figure('assets/umjoo-demo.jpg', '팀 통합 시연 장면', half, 295)))
    add(repo_links(umjoo))

    # 11 - PLC manual and servo screens both retained.
    plc = by_id('plc')
    new_page()
    add(project_header(plc))
    story.append(card(paragraphs(find(plc, 'mine')[0])))
    gap(10)
    for item in find(plc, 'kv'):
        add(paragraphs(item))
    gap(10)
    add(figure('assets/plc-manual.jpg', '수동 적재 · 배출 화면', max_height=215))
    add(figure('assets/plc-servo.jpg', '실린더 · 서보 점검 화면', max_height=215))

    # 12 - Vector diagram plus each of the four integration screenshots.
    collab = by_id('collaboration')
    new_page()
    add(project_header(collab))
    story.append(ToolDiagram())
    gap(14)
    slides = find(collab, 'presentation-slide')
    for pair in [slides[:2], slides[2:]]:
        story.append(columns(*[figure(x.xpath('.//img')[0].get('src'), plain(x.xpath('./figcaption')[0]), half, 140) for x in pair]))
        gap(10)
    add([link('협업 환경과 연동 화면 · 웹에서 크게 보기', SITE + '#collaboration')])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=36, leftMargin=36, topMargin=58, bottomMargin=48, title='최세은 | 로봇 시스템 개발자 포트폴리오', author='최세은', subject='FMS AI · React · STM32/CAN · PLC', pageCompression=1)
    doc.build(story, onFirstPage=decorate, onLaterPages=decorate)
    from pypdf import PdfReader
    reader = PdfReader(OUTPUT)
    if len(reader.pages) != len(TITLES):
        raise RuntimeError(f'Expected {len(TITLES)} pages; got {len(reader.pages)}. Review pagination before publishing.')
    shutil.copy2(OUTPUT, ASSET)
    print(f'{OUTPUT}\nPages: {len(reader.pages)} | Size: {OUTPUT.stat().st_size:,} bytes')


if __name__ == '__main__':
    build()
