# 프로젝트 작업 목록

> 프로젝트 전체의 변경·마일스톤·우선순위·의존성을 관리합니다. 제품 기준과 결정은 [00-PROJECT.md](./00-PROJECT.md), 상세 상태의 소유권은 [DOCS_GUIDE.md](./DOCS_GUIDE.md)를 따릅니다.
>
> 이 branch에서는 템플릿 저장소 자체의 다국어 변경을 추적합니다. 기존 사용자용 한국어 TODO 양식은 구현 시 `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`에서 `locales/ko/docs/02-TODO.md`로 이관하며, 이 maintainer 작업은 locale artifact에 포함하지 않습니다.

## Metadata

- **Status:** Active
- **Owner:** Chae Sangwon
- **Last reviewed:** 2026-09-22 (UTC)
- **Review cadence:** 작업 범위·우선순위·의존성·통합 결과 변경 시
- **Integration target:** local `main`; 공개 저장소 target `jaff2836/coding-agent-docs-template`; v1.7.1 payload 기준 `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`

## Current Milestone

- **Name:** `v2.3.1` Windows release 도구 호환성 patch
- **Goal:** T-015의 Windows packaging·검증·checkout·test portability 수정과 native Windows 근거를 patch release로 공개
- **Target:** Origin `main` 통합과 동기화된 GitHub `main`, immutable Latest `v2.3.1`, Windows published E2E
- **Status:** In Progress — Origin PR #30 merge `3b4bf674da8f7e8c13b2a69c45b2cf1f8ce54756`을 양쪽 `main`에 동기화했고 `codex/v2.3.1-release-prep`에서 source version·release history를 정렬 중입니다.
- **다음 마일스톤:** T-016은 Draft 설계 합의 뒤 진행합니다. T-013·T-014·T-017과 community locale은 Backlog로 유지합니다.

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

- [ ] **T-015 Windows release 도구 호환성 수정**
  - 기준: Origin `main` merge `430de821db02d63808bcf520e7f1a6f8706db264`에서 `codex/t015-windows-release-compatibility` 작업 트리로 진행합니다.
  - 출처: 2026-09-22 사용자 제공 전체 프로젝트 리뷰, 기준 `5066d821084545554588182f5250cc9dea12e444`의 F-001·F-002와 검증 보완 항목
  - 확인된 증상: F-001은 Windows의 `Path` 정렬이 POSIX 상대 경로 문자열 inventory 순서와 달라 정상 source에서도 `exported member inventory differs`로 packaging이 중단됩니다. F-002는 정상 Windows 파일 mode가 `0666`으로 관찰될 때 verifier가 POSIX `0644`와 무조건 비교해 `verification file mode is not 0644`로 실패합니다.
  - [x] artifact member를 POSIX 상대 경로 문자열로 정렬하고 native path 정렬 차이를 모사하는 회귀를 추가했습니다.
  - [x] 설치·export tree는 Windows에서 writable 의미를, 그 밖의 플랫폼에서 정확한 `0644`를 검사하며 ZIP의 Unix mode `0644` 계약은 유지했습니다.
  - [x] `.gitattributes`로 text checkout의 LF를 고정하고 LF fixture·materialized mode assertion을 플랫폼 의미에 맞췄습니다.
  - [x] symlink fixture는 `NotImplementedError`와 Windows `WinError 1314`만 skip하고 다른 `OSError`는 실패시키며, artifact checker의 symlink 검증을 일반 경로 검증과 분리했습니다.
  - [x] Linux 관련 회귀, 전체 unittest, root docs, stable locale과 `git diff --check`를 통과했습니다.
  - [x] commit `556c434`의 native Windows·Python 3.14.7에서 문서·stable locale·LF checkout·file mode와 en·ko package 2회 5개 asset byte 동일성을 확인했습니다.
  - [x] head `a64a889`의 native Windows·Python 3.14.7에서 전체 unittest 174개(실패·오류 0, symlink 관련 skip 16), en·ko export artifact checker·test와 `git diff --check`를 확인했습니다. skip된 symlink 보호 동작 자체는 검증하지 않았지만 분리한 일반 경로 검증은 실행됐습니다.
  - [ ] 후속 patch release 공개 뒤 그 release의 native Windows published E2E를 확인합니다. immutable `v2.3.0`은 수정 전 artifact test를 포함하므로 이 branch의 완료 gate로 소급 사용하지 않습니다.
  - [x] Origin PR #30 merge `3b4bf674da8f7e8c13b2a69c45b2cf1f8ce54756`을 양쪽 `main`에 동기화하고 후속 release를 `v2.3.1` patch로 확정했습니다.
  - [ ] clean exact source의 `v2.3.1` candidate를 검증하고 같은 5개 asset을 immutable Latest release로 공개한 뒤 published·Windows E2E를 확인합니다. 특정 CI runner 설정 추가는 범위 밖입니다.

## Next

- [ ] **T-016 새 프로젝트 `install` 대상 계약 정합화**
  - 변경-ID: `2026-09-22-install-target-contract`, [Draft 변경 설계](./changes/2026-09-22-install-target-contract/01-CHANGE.md)
  - 출처: 같은 리뷰의 F-003. root landing README는 새 대상 또는 빈 디렉터리를 요구하지만, locale guide는 새·빈 대상을 권장하면서 실제 구현과 같은 artifact 경로 충돌 조건을 설명합니다. 구현은 겹치지 않는 기존 파일을 보존하면서 새 파일을 추가합니다.
  - 다음 단계: 기존 저장소는 `adopt`, 새 프로젝트만 `install`로 분리한 현재 제품 경계에 따라 비어 있지 않은 대상 전체를 거부하는 권고안을 사용자와 합의합니다. 승인 전에는 구현하지 않습니다.

## Blocked

없음.

## Backlog

- [ ] **T-013 D-009 운영 계약 회귀 방지** — `project-analysis`에 한정한 source root↔`locales/ko` 사본 동등성 검사, source/artifact checker CLI 경계와 source changelog의 공개 전 heading 예외, root `.gitattributes`가 maintainer checkout의 LF를 고정하는 목적, locale별 placeholder 검색 어휘의 단일 출처·검증 방식을 함께 설계합니다. `design`·`review-round` skill 사본은 같은 동등성 계약으로 일반화하지 않습니다.
- [ ] **T-014 병렬 리뷰 finding ID 충돌 방지 방식 검토** — reviewer-qualified ID와 종합 단계 canonical ID 부여를 우선 검토하고, 반복 근거와 사용자 승인 없이 `REVIEW.md`·`REVIEW_ROUND.md` 계약을 바꾸지 않습니다.
- [ ] **T-017 Windows junction 경계 검증** — `Path.is_symlink()`가 Windows directory junction을 탐지하지 못해 installer의 `install`·`adopt`·`export` 대상 경계를 우회할 수 있다는 PR #30 C30-002를 native Windows에서 재현합니다. 최소 지원 Python 범위를 먼저 정하고 그 범위에서 symlink와 junction을 함께 fail-closed로 처리하는 방법과 회귀 테스트를 설계한 뒤 별도 변경으로 진행합니다.
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

- [x] **T-007 이미 적용한 저장소의 업그레이드를 위한 `adopt` 분류 개선**
  - 변경-ID: `2026-09-20-adopt-upgrade-classification`
  - 통합·공개 결과: base 전용 schema 1·2 검증, 3-way upgrade 분류, format 2 report와 공개 검증은 Origin PR #24, review 후속은 PR #25, release 준비는 PR #26 merge `70a5a7a9e97fa5a89609a120ad69bced7e8ae1ac`에 통합됐습니다. 같은 exact source를 annotated tag와 [immutable `v2.2.0` release](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.2.0)로 공개했습니다.
  - 검증 근거: [PLAN](./changes/2026-09-20-adopt-upgrade-classification/03-PLAN.md) W-001~W-005. candidate·published gate와 en·ko `v2.1.0` base-aware 원격 E2E가 통과했습니다. `claude-review-e2e@26c531beb65eaef8f524a00bcf8f06c52445c3d8`에서 생성 report와 base·current·target byte를 독립 대조했고 format 1 `missing 0`·`identical 10`·`merge 15`·`decision 4`·`blocked 0`이 format 2 `unchanged 11`·`template-only 2`·`project-only 14`·`converged 0`·`diverged 2`·`blocked 0`으로 분해되며 target tree는 불변임을 확인했습니다.

- [x] **T-008 release 검증 절차 스크립트화**
  - 변경-ID: `2026-09-20-release-verification`
  - 통합·운영 결과: Origin PR #20 merge `40306b65fe211402090d7a11b5c3ffafcb3689eb`의 검증 CLI로 `v2.1.1` exact source `0cfcc896ee92ec018d12c88f3f2638a154b35720`과 `v2.2.0` exact source `70a5a7a9e97fa5a89609a120ad69bced7e8ae1ac`의 실제 draft candidate·immutable published 경로를 확인했습니다. 두 release 모두 검증한 5개 asset을 게시 전후 교체하지 않았습니다.
  - 검증 근거: 두 release의 candidate·published가 통과했고, `v2.2.0` published는 latest·exact의 en·ko `list-locales`·`install`·`export`·`adopt`, `v2.1.0` base-aware upgrade, source export와 target 불변을 확인했습니다. release는 `isDraft=false`, `isImmutable=true`, Latest입니다.

- [x] **T-009 checker·installer 확정 결함 수정**
  - 통합·공개 결과: checker의 선택 파일 경계와 installer schema mismatch 복구 진단을 포함한 exact source `0cfcc896ee92ec018d12c88f3f2638a154b35720`을 annotated tag `v2.1.1`과 immutable GitHub Release로 공개했습니다.
  - 검증 근거: exact source의 전체 unittest 154개, root docs, stable locale, Python compile, `git diff --check`, 두 번 생성한 5개 package byte 동일성과 T-008 candidate·published gate가 통과했습니다.

- [x] **T-010 문서 소유권·skill Metadata·changelog 안내 정리**
  - 변경-ID: `2026-09-22-documentation-ownership`, 결정 D-009
  - 통합·공개 결과: locale artifact 가이드 정본화, root maintainer addendum, source root 두 사본과 locale 네 사본의 `project-analysis` Metadata 제거, en·ko `docs/CHANGELOG_GUIDE.md`와 source/artifact별 release history 검사를 Origin PR #28 merge `5066d821084545554588182f5250cc9dea12e444`에 통합했습니다. 같은 exact source를 annotated tag와 [immutable `v2.3.0` release](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.3.0)로 공개했습니다.
  - 검증 근거: exact source의 전체 unittest 167개, root docs, stable locale, 두 package와 draft 5개 asset byte 동일성, candidate와 `published --base-version 2.2.0`이 통과했습니다. published gate는 latest·exact의 en·ko `list-locales`·`install`·`export`·`adopt`, source export와 target 불변을 확인했습니다.

- [x] **DFR-001 `v2.2.0` 준비 재검토**
  - 결과: 공식 locale source는 적용 가이드 §3의 지원 Markdown 범위만 사용하고 full CommonMark parser가 필요한 새 결함 근거가 없어 현재 범위를 유지합니다. 범위 밖 구문이 공식 source에 들어가거나 적용 consumer에서 검증된 P1/P2 결함으로 재현되면 다시 검토합니다.

- [x] **T-011 release verifier adoption plan 진단 강화**
  - 통합 결과: malformed `adoption-plan.json`을 일관된 `VerificationError`로 진단하고 공개 plan v1의 status 계약을 verifier checkout의 installer와 분리한 구현을 Origin PR #22 merge commit `62d1de45d9eb9c8c0387b3f2c4007fcc17480a21`에 통합했습니다. 리뷰에서 확인한 기존 ancestry 진단 결함은 T-012로 분리했습니다.
  - 검증 근거: PR #22 exact code head `c2bf788288c4ad1b61d69597614b3918e537dae6`에서 verifier test 14개와 전체 unittest 156개, root docs, stable locale, Python compile, `git diff --check`, 공개 `v2.1.0` `published` 검증이 통과했습니다. 최종 문서 증분 `7721962976ac80a276398e2ce993b80dfe411c9b`은 T-012 추적만 추가했습니다. 이 구현 작업의 완료 범위는 Origin·GitHub 통합이며 다음 candidate·published 운영 검증은 T-008이 소유합니다.

- [x] **T-012 release verifier의 remote `main` 객체·history 진단**
  - 통합 결과: remote `main` 객체 부재, shallow history 부족, 충분한 shallow history와 실제 비조상 관계를 구분하는 진단을 Origin PR #25 merge `d821dec23b0e34295b96f9af0690ba15f2d33edb`에 통합했습니다.
  - 검증 근거: PR #25 head의 verifier test 16개와 전체 unittest 166개가 통과했고, 후속 exact source `70a5a7a9e97fa5a89609a120ad69bced7e8ae1ac`의 `v2.2.0` candidate·published 성공 경로에서 동기화된 두 remote `main`과 tag ancestry를 추가 fetch 없이 확인했습니다.

완료 이력이 길어지면 기존 CHANGELOG 또는 마일스톤별 보관 문서로 연결하고 본문을 복제하지 않습니다.
