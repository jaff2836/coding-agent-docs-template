# 프로젝트 작업 목록

> 프로젝트 전체의 변경·마일스톤·우선순위·의존성을 관리합니다. 제품 기준과 결정은 [00-PROJECT.md](./00-PROJECT.md), 상세 상태의 소유권은 [DOCS_GUIDE.md](./DOCS_GUIDE.md)를 따릅니다.
>
> 이 branch에서는 템플릿 저장소 자체의 다국어 변경을 추적합니다. 기존 사용자용 한국어 TODO 양식은 구현 시 `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`에서 `locales/ko/docs/02-TODO.md`로 이관하며, 이 maintainer 작업은 locale artifact에 포함하지 않습니다.

## Metadata

- **Status:** Active
- **Owner:** Chae Sangwon
- **Last reviewed:** 2026-09-20 (UTC)
- **Review cadence:** 작업 범위·우선순위·의존성·통합 결과 변경 시
- **Integration target:** local `main`; 공개 저장소 target `jaff2836/coding-agent-docs-template`; v1.7.1 payload 기준 `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`

## Current Milestone

- **Name:** `v2.1.1` checker·installer 진단 수정과 release 검증 운영
- **Goal:** Origin `main`에 통합된 T-008·T-009를 patch release로 준비하고, 실제 draft와 immutable release에서 candidate·published 검증 경로를 확인
- **Target:** `v2.1.1` GitHub Release와 T-008 candidate·published 운영 기록
- **Status:** In Progress — T-008·T-009 구현은 Origin `main`에 통합됐고, release 준비 PR과 draft 운영 검증이 남았습니다. 이전 마일스톤 `v2.1.0`은 2026-09-19 공개와 T-004·T-005 완료로 종료했습니다.
- **다음 마일스톤:** `v2.1.1` 공개 뒤 업그레이드용 `adopt` 분류 T-007을 설계하고, 정책 결정 T-010은 별도 후보로 유지합니다.

## 운영 규칙

- 변경별 PLAN이 있으면 이 문서는 링크·우선순위·선행조건과 통합 여부만 관리합니다. 상세 체크박스·검증 로그를 복제하지 않습니다.
- PLAN이 없는 작은 작업은 아래 항목 안에서 범위·구현 순서·완료 조건·검증을 관리합니다.
- `In Progress`는 프로젝트가 선택한 진행 작업입니다. 다른 브랜치나 열린 PR의 실시간 상태를 보장하지 않습니다. 작업 시작 시 실제 Git·PR 상태와 해당 변경의 PLAN을 확인합니다.
- 각 브랜치는 자기 변경의 상세 기록을 갱신합니다. 다른 브랜치 작업을 오래된 사본만 보고 완료·미완료로 되돌리지 않습니다.
- 공통 항목은 범위·의존성·통합 결과가 달라질 때만 수정합니다. 충돌은 최신 기준과 변경-ID를 대조해 해결하고, 영향받은 계약·검증 전제를 재확인합니다.
- `Completed`는 필요한 검증과 지정한 대상에의 반영을 확인한 항목만 담습니다. 브랜치 구현 완료·리뷰 통과·병합·릴리스·지원 검증을 구분하고 해당 작업의 완료 조건으로 판단합니다.
- `T-nnn`은 이 문서의 전역 작업 ID입니다. 변경-ID·PROJECT의 `D-nnn`·변경 폴더의 `R-nnn`/`W-nnn`과 범위가 다릅니다. 발급·충돌 처리는 [DOCS_GUIDE.md](./DOCS_GUIDE.md)의 식별자 범위를 따릅니다. 아래 `T-001` 등은 자리 표시입니다.
- 취소한 변경은 Cancelled에 두고 변경 폴더는 유지합니다. 완료된 SPEC을 현재 제품 기준으로 읽지 않으며, 구현된 계약은 통합 후 PROJECT에 반영합니다.
- 원격 저장소나 PR은 필수가 아닙니다. 로컬 작업은 기준 revision과 대상 브랜치 또는 검토한 작업 트리 범위로 근거를 남깁니다. 미커밋 결과를 commit SHA로 재현된다고 표현하지 않습니다.
- 문서 갱신은 commit·push·merge 권한이 아닙니다. 리뷰 라운드 통과 후 반영은 [REVIEW_ROUND.md](./REVIEW_ROUND.md) §9를 따릅니다.

## In Progress

- [ ] **T-008 release 검증 절차 스크립트화** — Origin `main` 통합, 다음 draft 운영 검증 대기
  - 변경-ID: `2026-09-20-release-verification`
  - 결정: [PROJECT D-007](./00-PROJECT.md#8-decisions)과 [변경 문서](./changes/2026-09-20-release-verification/01-CHANGE.md)에 따라 tag·release mutation은 사람이 유지하고 candidate·published 검증만 자동화합니다.
  - 구현 범위: clean exact-source gate, package 2회 byte 대조, Origin·GitHub `main`·annotated tag 대조, draft·published asset 대조, 공개 latest·exact의 모든 공식 locale `list-locales`·`install`·`export`·`adopt`와 source export 비교
  - 현재 근거: Origin PR #20 merge commit `40306b65fe211402090d7a11b5c3ffafcb3689eb`에 통합됐습니다. 통합 `main`에서 unit test 12개를 포함한 전체 unittest 154개, root docs, stable locale, Python compile과 `git diff --check`가 통과했고, immutable Latest `v2.1.0`의 exact checkout에서 package의 installer를 실행하는 실환경 `published` 검증이 통과했습니다.
  - 남은 한계: 현재 draft release가 없고 이를 임의로 만드는 것은 범위 밖이므로 candidate 성공 경로의 실환경 검증은 다음 release의 기존 draft에서 publish 전에 수행합니다.
  - 완료 조건: 다음 release 운영 기록에서 실제 draft의 candidate 성공 경로와 게시 후 published 경로를 확인합니다.

- [ ] **T-009 checker·installer 확정 결함 수정** — Origin `main` 통합, `v2.1.1` release 준비 중
  - 범위: `check_versions()`가 `docs/TEMPLATE_GUIDE.md`의 실제 부재만 허용하고 외부 symlink·비파일 entry를 오류로 보고합니다. manifest schema가 실행 중인 installer와 다르면 같은 release version의 `installer.py`를 사용하라는 복구 안내를 제공합니다.
  - 근거: consumer PR #28의 pr-bot P3를 현재 checker에서 재현했고, `v2.0.0` installer와 `schema_version` 2 release를 조합하면 원인만 있고 복구 방법이 없는 오류를 확인했습니다.
  - 현재 검증: checker test 51개, installer test 34개와 전체 unittest 154개가 통과했습니다. 외부 symlink·directory·실제 부재와 schema mismatch CLI 오류를 고정하는 회귀 테스트를 각각 추가했고, root docs·stable locale·en/ko export artifact checker와 각 artifact test 49개·Python compile·`git diff --check`가 통과했습니다.
  - 비범위: skill metadata와 maintainer 가이드 동기화 정책은 T-010, `--base-version`과 adoption report 확장은 T-007이 소유합니다. version bump·package·draft·공개 release는 이 구현 단계에서 수행하지 않습니다.
  - 완료 조건: `v2.1.1` release 준비 commit을 Origin·GitHub `main`에 통합하고, T-008 candidate·published gate로 tag·draft·immutable release를 검증합니다.

- [ ] **T-011 release verifier adoption plan 진단 강화** — 구현·검증 중
  - 근거: Origin PR #20 C20-002에서 `published` E2E가 문법상 유효하지만 `summary` 구조가 잘못된 `adoption-plan.json`을 읽으면 `VerificationError` 대신 `KeyError` traceback을 내는 경로를 재현했습니다.
  - 구현 범위: plan 최상위와 `summary`를 object로 제한하고, 정확한 adoption status 집합과 non-negative integer 값을 검증한 뒤 합계를 계산합니다.
  - 현재 검증: malformed plan의 누락·추가 status, `bool`, 음수와 비-object 구조를 `VerificationError`로 고정하는 회귀 테스트를 추가했습니다. verifier test 13개와 전체 unittest 155개, root docs, stable locale, Python compile과 `git diff --check`가 통과했습니다.
  - 완료 조건: 전체 gate 통과 후 Origin `main`에 통합하고 `v2.1.1` candidate 검증에 반영합니다.

## Next

없음.

## Blocked

없음.

## Backlog

아래 T-007·T-010은 `v2.1.0` 작업에서 드러난 미승인 후보입니다. T-009의 실행 결함과 분리했으며 결정이 필요한 질문은 [PROJECT §11](./00-PROJECT.md#11-open-questions)에 있습니다.
- [ ] **T-007 이미 적용한 저장소의 업그레이드를 위한 `adopt` 분류 개선** — 설계 필요
  - 근거: 2026-09-19 consumer PR #28을 `v2.0.0`에서 `v2.1.0`으로 갱신할 때 `adopt`의 2-way report가 병합 13개를 보고했습니다. 실제로 템플릿이 바뀐 파일은 6개였고, 나머지 7개는 프로젝트 값만 달랐습니다. 이를 가리기 위해 `v2.0.0` artifact를 따로 export해 base로 수동 비교했습니다.
  - 제안: `--base-version <SemVer>`로 이전 release artifact를 같은 검증 절차로 받아, 경로마다 "템플릿만 변경 / 프로젝트만 변경 / 양쪽 변경"을 report에 추가합니다. 대상 무변경, 자동 병합 없음, 실험적 report 원칙은 유지합니다.
  - 선행조건: D-006 SPEC이 비범위로 둔 "3-way merge·자동 upgrade"와의 경계를 새 결정으로 확정([01-DESIGN.md](./01-DESIGN.md) 절차)
- [ ] **T-010 skill metadata·maintainer 가이드 정책 정리** — 설계 결정 필요
  - `project-analysis` skill의 `Owner`·`Last reviewed` placeholder를 템플릿 소유 skill에서 제거할지, 적용 시 두 skill 사본을 함께 채우는 현재 계약을 유지할지 정합니다.
  - root `docs/TEMPLATE_GUIDE.md`·`docs/DOCS_GUIDE.md`를 locale 가이드의 복제본으로 계속 동기화할지, locale 가이드 링크와 maintainer 전용 내용만 남길지 정합니다.
  - 이 단위는 확정 결함 T-009의 `v2.1.1` patch를 지연시키지 않으며, artifact 계약이 바뀌면 별도 SemVer 범위를 결정합니다.
- [ ] `v2.2.0` 준비 시 [REVIEW.md](./REVIEW.md) §9 DFR-001(checker Markdown 지원 범위 밖 구문) 재검토
- [ ] `en`·`ko` 외 community locale — v2의 locale 추가 계약과 두 공식 locale 지원 검증 후 재검토

## Cancelled

취소한 변경만 둡니다. 변경-ID, 취소 이유, Intent/Spec의 `Rejected` 근거, 유지 중인 변경 폴더 경로를 남깁니다. 완료·진행 항목과 섞지 않으며 폴더는 삭제하지 않습니다.

## Completed

실제 완료 항목만 추가합니다. 변경-ID, 통합 대상, 확인한 revision 또는 작업 트리 범위, 검증 근거의 위치를 남깁니다. 변경 폴더는 유지하고, 구현된 계약이 현재 지원 범위가 되면 PROJECT를 갱신합니다. PR이 있으면 실제 병합 결과를 확인하며, 로컬 작업에 가상의 PR·merge SHA를 만들지 않습니다.

- [x] **T-001 다국어 템플릿 source와 선택형 배포 도입**
  - 변경-ID: `2026-09-09-multilingual-template`
  - 통합 결과: W-001~W-006이 PR #3~#8로 `main`에 통합됐고 W-007 exact-head consumer probe와 bilingual release README가 `9cea178`에 반영됐습니다.
  - 검증 근거: [PLAN](./changes/2026-09-09-multilingual-template/03-PLAN.md)의 W-001~W-007과 검증 기록. tag·GitHub release는 T-002가 소유합니다.

- [x] **T-002 GitHub Releases 기반 v2.0.0 공개**
  - 변경-ID: `2026-09-18-github-releases-publication`
  - 통합 결과: `v2.0.0` tag commit `8bc8b1b`에서 생성한 기존 5개 draft asset을 재패키징·교체하지 않고 [immutable GitHub Release](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.0.0)로 공개했습니다. 게시 시 Origin·GitHub `main`은 `5eefc11`로 같았고 tag commit은 그 조상이었습니다.
  - 검증 근거: [PLAN](./changes/2026-09-18-github-releases-publication/03-PLAN.md)의 W-003·W-004 및 검증 기록. latest·exact-version의 en·ko install/export와 충돌 tree 불변 검증이 통과했습니다.

- [x] **T-003 프로젝트 전체 분석 skill 이관**
  - 변경-ID: `2026-09-18-project-analysis-skill`
  - 통합 결과: locale별 self-contained `project-analysis` skill과 README·manifest·checker 계약이 Origin PR #12 merge commit `5eefc11`에 통합됐습니다. 고정된 `v2.0.0` artifact는 변경하지 않았고 이 skill은 다음 release inventory에 포함됩니다.
  - 검증 근거: PR #12 exact-head 리뷰와 `main`의 root docs, stable locale, 전체 unittest 및 en·ko artifact 검사.

- [x] **T-004 기존 저장소 adoption 계약**
  - 변경-ID: `2026-09-18-existing-repository-adoption`
  - 통합 결과: 설계는 PR #14, adoption policy·release manifest schema 2·`adopt`는 PR #15, 기존 저장소 우선 문서는 PR #16, release 준비는 PR #18로 Origin `main`에 통합됐습니다. tag commit `36a123ff3bd939a99148e0f804f9e20924f6be0b`의 immutable GitHub Release `v2.1.0`으로 공개했습니다.
  - 검증 근거: [PLAN](./changes/2026-09-18-existing-repository-adoption/03-PLAN.md) W-004와 검증 기록. 원격 latest·exact의 install·export·adopt가 통과했습니다. `claude-review-e2e` baseline에서 대상 불변, PR #28과 같은 분류, report 반영 후 checker 통과를 확인했고, Claude·Codex·Cursor·OMP 로딩 probe가 통과했습니다.

- [x] **T-005 artifact `check-docs.py` 강화 반영**
  - 변경-ID: 없음 — 외부 계약을 바꾸지 않는 checker 결함 수정 묶음
  - 통합 결과: `claude-review-e2e` PR #28 head `719696f`의 강화분을 `template/common/`에 3-way merge로 반영했습니다. 미해결 P2 8건 중 7건을 수정하고 회귀 테스트 7개를 추가했습니다. Setext heading은 지원 범위 밖으로 명시하고 DFR-001로 기록했습니다. Origin PR #17 merge commit `6e664c374f87d26002124fa155c8345a121ba51f`에 통합됐습니다.
  - 검증 근거: 통합 후 `main`에서 전체 unittest 140개와 root docs·stable locale 검사가 통과했습니다. 공개된 `v2.1.0` ko artifact의 `scripts/check-docs.py`·`tests/test_check_docs.py`는 tag commit의 `template/common/` 파일과 byte-identical이고, 설치 tree에서 checker와 테스트 48개가 통과했습니다.

- [x] **T-006 consumer PR #28 마무리 (외부 저장소 `jaff2836/claude-review-e2e`)**
  - 통합 결과: `v2.1.0` `adopt` report를 반영한 PR #28 exact head `4b3987dad933142a192ebee08aea7c525a7681da`를 GitHub `main` merge commit `26c531beb65eaef8f524a00bcf8f06c52445c3d8`에 통합했습니다. 처리된 7개 review thread를 모두 해소했고 template 저장소로 이관한 P3는 T-009에 반영했습니다.
  - 검증 근거: exact head에서 Claude workflow #8과 jaff2836-pr-reviewer가 approve했고 네 job이 통과했습니다. 통합 `main`에서 checker test 48개, docs checker, Python compile과 `git diff --check`가 통과했으며 기존 `.github/`·`src/`는 PR에서 변경되지 않았습니다. 로컬 `.env`는 존재하지 않았고 통합된 `.gitignore`가 `.env`를 제외합니다.

완료 이력이 길어지면 기존 CHANGELOG 또는 마일스톤별 보관 문서로 연결하고 본문을 복제하지 않습니다.
