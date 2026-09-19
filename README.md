# 최세은 · 로봇 시스템 개발자 포트폴리오

웹 백엔드와 현장 장비 경험을 바탕으로 로봇 제어와 관제 소프트웨어를 개발합니다.

**→ https://cseun.github.io**

---

## 프로젝트

| | 프로젝트 | 담당 | 기술 |
| --- | --- | --- | --- |
| 01 | **Logistics FMS** — 다중 로봇의 이동 명령과 상태를 연결하는 관제 | FMS 관제 프로그램과 화면 설계 (팀 7명 중 ACS 관제 2인) | ROS 2 Jazzy, Nav2, Zenoh, FastAPI, PostgreSQL, React |
| 02 | **Kick CAN** — CAN 기반 RC카의 계기판 노드 | Node 2 — 상태 표시와 출력 제어 | STM32, CAN, SPI, I2C |
| 03 | **SafeKick** — 출발 전 안전 점검을 안내하는 앱 | UI/UX, 앱 화면 흐름, 프론트엔드 | React Native, Expo, SSE |
| 04 | **음주컷** — 음주 측정 데모와 시제품 제작 | 기획, STM32 측정 데모, 케이스 모델링 | STM32, MQ-3, UART, Fusion 360 |
| 05 | **PLC MPS** — 수동 장비 제어와 HMI 화면 구성 | 수동 동작, 장비 제어, HMI 화면 | MELSEC Q, GX Works2, GT Designer3 |

저장소: [Logistics_FMS](https://github.com/E1I6-Logistics/Logistics_FMS) · [Kick CAN Node 2](https://github.com/kick-can/Node_2) · [safe-kick-app](https://github.com/safe-kick/safe-kick-app) · [StmDemo](https://github.com/Umjoo-Cut/StmDemo)

## 경력

| 기간 | 소속 | 역할 |
| --- | --- | --- |
| 2025.05 – 2026.01 | 엑서테크 (프리랜서) | BMS 검사장비 테스트 보조와 C# S/W 유지보수, 미국 현장 파견 2회 |
| 2023.09 – 2025.04 | 에어텔닷컴 그룹 | 웹 백엔드 1년 8개월 — PHP / Laravel 기반 상품 · 주문 · 정산 데이터 처리 |
| 2017.12 – 2019.06 | 마케팅하이랜즈 | 비개발 — 베트남 다낭 현지 호텔 B2B 세일즈와 여행 운영 |

## 기술

- **언어** C / C++ / C# (WinForms) / Python
- **웹 · 백엔드** PHP / Laravel / JavaScript / HTML, MySQL, PostgreSQL, Docker, REST API
- **로봇 · 관제** Linux, ROS 2, Nav2, Zenoh, FastAPI
- **임베디드 · 통신** STM32, CAN / UART / SPI / I2C / PWM
- **앱 · 프론트** React, React Native, Expo
- **협업 · 도구** Git, Jira, Confluence, Figma, Fusion 360

## 연락처

- cseeun98@gmail.com
- [github.com/cseun](https://github.com/cseun)
- [slowbreeze.tistory.com](https://slowbreeze.tistory.com)

---

### 이 저장소에 대하여

GitHub Pages로 서비스되는 정적 사이트입니다. 빌드 도구나 프레임워크 없이 HTML과 CSS만 사용합니다.

```
index.html      단일 페이지 본문
styles.css      스타일
.nojekyll       Jekyll 처리 건너뛰기
assets/         이미지 11장
```

수정 후 `git push`하면 1~2분 내에 반영됩니다. 이미지를 교체할 때는 `assets/` 안의 파일을 같은 이름으로 덮어쓰면 되고, 가로형은 폭 1200~1400px, 세로형은 700~1000px 정도로 줄여서 올리는 편이 좋습니다.
