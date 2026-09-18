# cseun.github.io

최세은 · 로봇 시스템 개발자 포트폴리오 (정적 사이트)

공개 주소: `https://cseun.github.io`

## GitHub Pages 올리는 방법

1. GitHub에서 `cseun` 계정으로 로그인합니다.
2. https://github.com/new 에서 새 저장소를 만듭니다.
   - **Repository name**: `cseun.github.io` (정확히 이 이름이어야 합니다)
   - **Public** 선택
   - README 추가는 체크하지 않습니다
3. 이 폴더의 파일을 저장소 최상위에 올립니다.
4. 저장소 **Settings → Pages** 로 갑니다.
   - Source: **Deploy from a branch**
   - Branch: **main** / **/ (root)** → Save
5. 1~2분 뒤 `https://cseun.github.io` 에서 열립니다.

### 명령줄로 올릴 경우

```bash
cd cseun.github.io
git init
git add .
git commit -m "portfolio site"
git branch -M main
git remote add origin https://github.com/cseun/cseun.github.io.git
git push -u origin main
```

계정명과 같은 이름(`cseun.github.io`)의 저장소는 `Settings → Pages`에서 Source만 지정하면 바로 공개됩니다.

## 파일 구조

```
cseun.github.io/
├── index.html      단일 페이지 본문
├── styles.css      스타일 (외부 프레임워크 없음)
├── .nojekyll       Jekyll 처리 건너뛰기
├── README.md
└── assets/
    ├── profile.jpg
    ├── fms-styleguide.jpg
    ├── fms-layout.jpg
    ├── kickcan-tft.jpg
    ├── kickcan-wiring.jpg
    ├── safekick-modules.jpg
    ├── safekick-app.jpg
    ├── umjoo-case.jpg
    ├── umjoo-demo.jpg
    ├── plc-manual.jpg
    └── plc-servo.jpg
```

## 기술 사항

- 순수 HTML + CSS. 빌드 도구·프레임워크·JavaScript 없음
- 웹폰트: Google Fonts (Noto Sans KR, IBM Plex Mono)
- 색상은 E1I6 FMS UI 스타일 가이드 토큰 기준
- 반응형: 900px / 620px 두 개의 분기점
- 이미지 전체 약 900KB, `loading="lazy"` 적용

## 수정할 곳

| 내용 | 위치 |
| --- | --- |
| 이름·소개 문구 | `index.html` 의 `.hero` |
| 학력·경력·연락처 칩 | `index.html` 의 `.factlist` |
| 기술 스택 배지 | `index.html` 의 `.stack` |
| 경력 항목 | `index.html` 의 `#career` |
| 프로젝트 | `index.html` 의 `#fms` ~ `#plc` |
| 색상 토큰 | `styles.css` 의 `:root` |

이미지를 교체할 때는 `assets/` 안의 파일을 같은 이름으로 덮어쓰면 됩니다.
가로형은 폭 1200~1400px, 세로형은 700~1000px 정도로 줄여서 올리세요.
