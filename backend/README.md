# 댓글 · 관리자 통계 연결

GitHub Pages는 그대로 사용하고, Cloudflare Worker + D1에 댓글과 통계를 저장합니다.
운영 서버: https://portfolio-community.cseeun98.workers.dev

Cloudflare에 서버·D1 연결·비밀 설정·일일 정리 일정을 구성했습니다. 사이트 게시 후 댓글 저장과 방문 집계를 시작합니다. 과거 방문은 복원할 수 없습니다.

## 최초 설정

이 폴더에서 다음 순서로 실행합니다. Node.js와 Cloudflare 계정이 필요합니다.

```powershell
npx wrangler login
npx wrangler d1 create portfolio-community
```

출력된 database_id를 wrangler.jsonc에 입력합니다.

```powershell
npx wrangler d1 execute portfolio-community --remote --file=schema.sql
npx wrangler secret put ADMIN_PASSWORD
npx wrangler secret put IP_SALT
npx wrangler deploy
```

ADMIN_PASSWORD에는 관리자용 긴 비밀번호를, IP_SALT에는 별도의 임의 문자열을 입력합니다.
비밀번호와 salt는 소스·브라우저 설정 파일에 넣지 않습니다.
배포 후 Worker 주소를 상위 community-config.js의 PORTFOLIO_API_URL에 입력하고 사이트를 게시합니다.
도메인을 바꾸면 ALLOWED_ORIGIN도 실제 사이트 출처로 변경합니다.

## 동작

- 공개 댓글: 닉네임 40자, 본문 5~2,000자. 최신순, 20개 단위 더 보기.
- 관리자: 사이트 하단 관리자 버튼 → 비밀번호 입력. 세션은 메모리에서만 유지되며 30분 만료, 창을 닫으면 로그아웃.
- 조회 수: 페이지를 열 때 1회. 방문 수: 브라우저에 하루만 유지하는 임의 식별자로 한국 시간 기준 중복 제거. 실제 사람 수가 아닌 추정치.
- 통계: 누적 조회, 오늘 조회·방문, 댓글 수, 최근 30일 일별 조회·방문.
- 관리자 창 자체는 추가 집계하지 않습니다. 관리자가 포트폴리오를 여는 조회는 일반 조회와 같이 포함됩니다.
- IP 원문을 저장하지 않으며, salt로 해시한 IP로 댓글/로그인/조회 요청을 제한합니다. 만료된 제한·세션 데이터는 매일 정리합니다.
- 통계는 공개 API로 노출하지 않습니다. 댓글은 공개되므로 개인정보 입력 안내를 표시합니다.
- 스팸 댓글 삭제는 Cloudflare D1 콘솔에서 ID 확인 후 매개변수에 해당하는 ID를 지정해 삭제할 수 있습니다. 관리자 UI 삭제 기능은 포함하지 않습니다.

검증: `node --test worker.test.mjs`
공식 문서: https://developers.cloudflare.com/d1/ 및 https://developers.cloudflare.com/workers/configuration/secrets/
