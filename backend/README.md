# 관리자 방문 통계

운영 서버: https://portfolio-community.cseeun98.workers.dev

GitHub Pages에서 화면을 제공하고 Cloudflare Worker + D1에서 방문을 집계합니다.
댓글 화면과 댓글 API는 제거했습니다. 기존 방문 기록은 유지합니다.

- 사이트 하단 관리자 버튼 → 비밀번호 입력.
- ADMIN_PASSWORD와 IP_SALT는 서버 secret으로 저장합니다. ALLOWED_ORIGIN은 https://cseun.github.io 입니다.
- 세션은 메모리에만 유지되며 30분 만료, 관리자 창을 닫으면 로그아웃합니다.
- 조회 수는 페이지를 열 때 1회, 방문 수는 한국 시간 기준 같은 브라우저의 하루 중복을 제외한 추정치입니다.
- 누적 조회, 오늘 조회·방문, 최근 30일 일별 조회·방문을 확인합니다.
- 관리자 창 자체는 추가 집계하지 않습니다. 관리자가 포트폴리오를 열면 일반 조회에 포함됩니다.
- IP 원문 대신 salt를 사용한 해시로 요청을 제한합니다. 매일 만료 세션·제한 정보를 정리합니다.

서버 수정 배포: 이 폴더에서 `npx wrangler deploy`.
신규 DB 초기화: `npx wrangler d1 execute portfolio-community --remote --file=schema.sql`.
검증: `node --test worker.test.mjs`.
