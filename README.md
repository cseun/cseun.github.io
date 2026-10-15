# 최세은 · 로봇 시스템 개발자 포트폴리오

웹 백엔드와 현장 장비 경험을 바탕으로 로봇 제어와 관제 소프트웨어를 개발합니다.

**→ https://cseun.github.io**

---

## 프로젝트

| | 프로젝트 | 담당 | 기술 |
| --- | --- | --- | --- |
| 01 | **AX MULTI-ROBOT LOGISTICS** — 팀 E1I6, 담당 파트 FMS AI | **디자인·프론트엔드:** Figma·Claude AI로 UI 설계, ChatGPT·Figma를 활용한 React 구현<br>**AI·LLM:** 모델 선정·테스트·비교와 최단 경로 생성·주행 구현<br>**팀원 담당:** ROS 2/MQTT 로봇 연동, A*·예외 처리 | React, Figma, ROS 2, MQTT |
| 02 | **Kick CAN** — CAN 기반 RC카의 계기판 노드 | Node 2 — 상태 표시와 출력 제어 | STM32, CAN, SPI, I2C |
| 03 | **SafeKick** — 출발 전 안전 점검을 안내하는 앱 | UI/UX, 앱 화면 흐름, 프론트엔드 | React Native, Expo, SSE |
| 04 | **음주컷** — 음주 측정 데모와 시제품 제작 | 기획, STM32 측정 데모, 케이스 모델링 | STM32, MQ-3, UART, Fusion 360 |
| 05 | **PLC MPS** — 수동 장비 제어와 HMI 화면 구성 | 수동 동작, 장비 제어, HMI 화면 | MELSEC Q, GX Works2, GT Designer3 |

**기타 · 협업 환경 셋업과 알림 연동:** E1I6 프로젝트의 Jira 스프린트·백로그 운영 방식 설정, Slack에서 Jira 티켓 생성 및 작업 알림 연동, Confluence 문서와 Jira 이슈 연결, GitHub 작업 알림 연동 및 Slackbot 회의 리마인더 설정.

저장소: [Logistics_FMS](https://github.com/E1I6-Logistics/Logistics_FMS) · [Kick CAN Node 2](https://github.com/kick-can/Node_2) · [safe-kick-app](https://github.com/safe-kick/safe-kick-app) · [StmDemo](https://github.com/Umjoo-Cut/StmDemo)

## 경력

| 기간 | 소속 | 역할 |
| --- | --- | --- |
| 2025.04 – 2026.01 | 엑서테크 (프리랜서) | 검사장비 S/W 유지보수·현장 대응, BMS 검사장비 CS·테스트 보조와 C# S/W 유지보수, 미국 현장 파견 2회 (개발 1.5개월 / 비개발 3개월) |
| 2023.09 – 2025.03 | 에어텔닷컴 그룹 | 웹 백엔드 1년 7개월 — PHP / Laravel 기반 상품 · 주문 · 정산 데이터 처리 |
| 2017.12 – 2019.06 | 마케팅하이랜즈 | 비개발 — 베트남 다낭 현지 호텔 B2B 세일즈와 여행 운영 |

## 학력 · 교육

- 신구대학교 IT소프트웨어학과(3년제) 2025년 졸업 · 학부 성적 4.18 / 4.5
- 대한상공회의소 서울기술교육센터 AI융합 로봇 SW개발자 3기 과정 진행 중

## 기술

- **언어** C / C++ / C# (WinForms) / Python
- **웹 · 백엔드** PHP / Laravel / JavaScript / HTML, MySQL, PostgreSQL, Docker, REST API
- **로봇 · 관제** Linux, ROS 2, Nav2, MQTT, FastAPI
- **임베디드 · 통신** STM32, CAN / UART / SPI / I2C / PWM
- **앱 · 프론트** React, React Native, Expo
- **협업 · 도구** Git, Jira, Confluence, Figma, Fusion 360

## 연락처

- cseeun98@gmail.com
- [github.com/cseun](https://github.com/cseun)
- [slowbreeze.tistory.com](https://slowbreeze.tistory.com)

---

### 이 저장소에 대하여

GitHub Pages로 서비스되는 정적 사이트입니다. 빌드 도구나 프레임워크 없이 HTML, CSS, JavaScript를 사용합니다.

```
index.html      단일 페이지 본문
styles.css      스타일
presentation.js 발표자료 넘김
.nojekyll       Jekyll 처리 건너뛰기
assets/         이미지와 시연 영상
```

수정 후 `git push`하면 1~2분 내에 반영됩니다. 이미지를 교체할 때는 `assets/` 안의 파일을 같은 이름으로 덮어쓰면 되고, 가로형은 폭 1200~1400px, 세로형은 700~1000px 정도로 줄여서 올리는 편이 좋습니다.
