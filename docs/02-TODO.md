# 프로젝트 작업 목록

> 프로젝트 전체의 변경·마일스톤·우선순위·의존성을 관리합니다. 제품 기준과 결정은 [00-PROJECT.md](./00-PROJECT.md), 상세 상태의 소유권은 [DOCS_GUIDE.md](./DOCS_GUIDE.md)를 따릅니다.
>
> 이 branch에서는 템플릿 저장소 자체의 다국어 변경을 추적합니다. 기존 사용자용 한국어 TODO 양식은 구현 시 `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`에서 `locales/ko/docs/02-TODO.md`로 이관하며, 이 maintainer 작업은 locale artifact에 포함하지 않습니다.

## Metadata

- **Status:** Active
- **Owner:** Chae Sangwon
- **Last reviewed:** 2026-10-01 (KST)
- **Review cadence:** 작업 범위·우선순위·의존성·통합 결과 변경 시
- **Integration target:** local `main`; 공개 저장소 target `jaff2836/coding-agent-docs-template`; v1.7.1 payload 기준 `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`

## Current Milestone

- **Name:** T-034 다음 locale release
- **Goal:** `v2.3.3` 이후 통합된 locale payload 변경(T-013 검색 선언, D-013·D-014 계약)을 한 release로 공개함
- **Target:** release 준비 PR과 D-007의 candidate·published 단계
- **Status:** Next — version·시점은 준비 PR에서 정합니다.
- **다음 마일스톤:** T-035는 조건부 재검토 항목이고, `en`·`ko` 외 locale은 보류 상태입니다.

## 운영 규칙

- 변경별 PLAN이 있으면 이 문서는 링크·우선순위·선행조건과 통합 여부만 관리합니다. 상세 체크박스·검증 로그를 복제하지 않습니다.
- PLAN이 없는 작은 작업은 아래 항목 안에서 범위·구현 순서·완료 조건·검증을 관리합니다.
- `In Progress`는 프로젝트가 선택한 진행 작업입니다. 다른 브랜치나 열린 PR의 실시간 상태를 보장하지 않습니다. 작업 시작 시 실제 Git·PR 상태와 해당 변경의 PLAN을 확인합니다.
- 각 브랜치는 자기 변경의 상세 기록을 갱신합니다. 다른 브랜치 작업을 오래된 사본만 보고 완료·미완료로 되돌리지 않습니다.
- 공통 항목은 범위·의존성·통합 결과가 달라질 때만 수정합니다. 충돌은 최신 기준과 변경-ID를 대조해 해결하고, 영향받은 계약·검증 전제를 재확인합니다.
- `Completed`는 필요한 검증과 지정한 대상에의 반영을 확인한 항목, 또는 작업 브랜치에서 자기 최종 head의 통합과 동시에 완료되는 항목(결합 서술)을 담습니다. 릴리스·지원 검증처럼 통합 뒤에 일어나는 완료는 그 일이 끝난 뒤에만 기록합니다. 브랜치 구현 완료·리뷰 통과·병합·릴리스·지원 검증을 구분하고 해당 작업의 완료 조건으로 판단합니다.
- 자기 PR의 CI build·리뷰 판정·merge SHA는 PR을 원장으로 두고 이 문서에는 PR 참조만 둡니다. 상세 규칙과 사용자 요청 예외는 [DOCS_GUIDE.md](./DOCS_GUIDE.md)의 로컬 Git과 병렬 브랜치 절을 따릅니다.
- `T-nnn`은 이 문서의 전역 작업 ID입니다. 변경-ID·PROJECT의 `D-nnn`·변경 폴더의 `R-nnn`/`W-nnn`과 범위가 다릅니다. 발급·충돌 처리는 [DOCS_GUIDE.md](./DOCS_GUIDE.md)의 식별자 범위를 따릅니다. 아래 `T-001` 등은 자리 표시입니다.
- 취소한 변경은 Cancelled에 두고 변경 폴더는 유지합니다. 완료된 SPEC을 현재 제품 기준으로 읽지 않으며, 구현된 계약은 통합 후 PROJECT에 반영합니다.
- 원격 저장소나 PR은 필수가 아닙니다. 로컬 작업은 기준 revision과 대상 브랜치 또는 검토한 작업 트리 범위로 근거를 남깁니다. 미커밋 결과를 commit SHA로 재현된다고 표현하지 않습니다.
- 문서 갱신은 commit·push·merge 권한이 아닙니다. 리뷰 라운드 통과 후 반영은 [REVIEW_ROUND.md](./REVIEW_ROUND.md) §9를 따릅니다.

## In Progress

없음. 다음 작업은 Current Milestone과 Backlog 순서를 따릅니다.

## Next

T-034 release를 준비합니다. 각 항목은 PR 단위로 수동 리뷰·필수 CI·통합을 거칩니다.

## Blocked

없음.

## Backlog

아래 순서는 위험과 선행조건을 고려한 권고 PR 순서이며, Backlog 항목을 시작하는 권한은 아닙니다.
설계 결과에 따라 필요한 구현은 해당 설계 PR과 분리합니다. `v2.3.3`의 candidate 검증과 공개·published 검증은 D-007 경계에 따라 단계와 기록 PR을 분리합니다.

통합된 순서 1~18의 기록은 [완료 작업 보관](./TODO_ARCHIVE.md)에 있습니다.

| 순서 | PR 단위 | 작업 | 선행조건·통합 경계 |
| --- | --- | --- | --- |
| 19 | `claude/<version>-release-prep` 등 | T-034: 다음 locale release | 공개 payload 변경을 한 release로 묶음. D-007에 따라 준비·candidate·published 단계 분리 |

- [ ] **T-034 다음 locale release** — `v2.3.3` 이후 통합된 payload 변경을 한 release로 공개합니다. 대상은 T-013 검색 선언(en·ko `docs/TEMPLATE_GUIDE.md`)과 D-013·D-014 계약(en·ko `docs/DOCS_GUIDE.md`·`docs/02-TODO.md`·`docs/REVIEW.md`·`docs/REVIEW_ROUND.md`·`.cursor/BUGBOT.md`)입니다. PR #50의 인계대로 release 이력에 검색 선언 단일화·Bash 전제·TEMPLATE_GUIDE 삭제 전 보관과 변경 파일을 기록합니다. version·시점은 준비 PR에서 정하고, D-007에 따라 준비·candidate·published 단계를 나눕니다.
- [ ] **T-035 release 신뢰 루트 검토 (서명·attestation)** — installer는 같은 release의 `SHA256SUMS`·manifest로 무결성을 확인하지만 게시 계정 탈취는 막지 못하며, immutable release와 tag ruleset으로 완화합니다. 게시 권한 구조가 바뀌거나 외부 배포 요구가 생기거나 표준 라이브러리만으로 GitHub release attestation을 검증할 경로가 확인되면 D-004 확장 설계로 재검토합니다.

- [ ] `en`·`ko` 외 community locale — v2의 locale 추가 계약과 두 공식 locale 지원 검증 후 재검토

## Cancelled

취소한 변경만 둡니다. 변경-ID, 취소 이유, Intent/Spec의 `Rejected` 근거, 유지 중인 변경 폴더 경로를 남깁니다. 완료·진행 항목과 섞지 않으며 폴더는 삭제하지 않습니다.

## Completed

실제 완료 항목만 추가합니다. 변경-ID, 통합 대상, 확인한 revision 또는 작업 트리 범위, 검증 근거의 위치를 남깁니다. 변경 폴더는 유지하고, 구현된 계약이 현재 지원 범위가 되면 PROJECT를 갱신합니다. PR이 있으면 실제 병합 결과를 확인하며, 로컬 작업에 가상의 PR·merge SHA를 만들지 않습니다.

상세 기록은 [완료 작업 보관](./TODO_ARCHIVE.md)에 있습니다. 새 완료 항목은 한 줄로 적고 상세 근거는 PR과 변경 문서에 둡니다.

- [x] **T-033 TODO 완료 이력 보관** — Completed 상세와 통합된 Backlog 행을 [완료 작업 보관](./TODO_ARCHIVE.md)으로 옮기고 이 문서에는 한 줄 목록만 남겼습니다. PR #56의 인계 C56-005(P3: sticky 게시물의 짧은 인용이 head를 버림)를 en·ko·root `REVIEW.md` §7과 설계 R-006에서 해소했습니다. 통합 근거: 이 변경의 PR(D-013 결합 서술).
- [x] **T-030·T-014 기록 시점·리뷰 finding ID 계약 구현** — 통합: PR #56(D-013·D-014). 공개는 T-034.
- [x] **T-030·T-014 기록 시점·리뷰 finding ID 계약 설계**
- [x] **T-032 원격 운영: GitHub `main` 보호·동기화 절차·tag 정책**
- [x] **T-031 CI 검색 도구 gate**
- [x] **T-029 root 검색식 gate 보강 (C50-002·C51-001·C51-002)**
- [x] **T-013 D-009 운영 계약 회귀 방지**
- [x] **T-021 install preflight 순서 설계**
- [x] **T-022 install 대상 불변조건 등록**
- [x] **T-026 문서 상태 중복 정리**
- [x] **T-028 `v2.3.3` 공개와 published 검증**
- [x] **T-027 `v2.3.3` draft candidate 검증과 기록**
- [x] **T-025 `v2.3.3` release 후보 준비**
- [x] **T-024 installer stdout 인코딩 후속**
- [x] **T-020 install onboarding 진단·안내 평가**
- [x] **T-023 release 후보의 verifier·installer 계약 회귀**
- [x] **T-017 Windows junction 경계 검증**
- [x] **T-019 `v2.3.2` 공개 기록과 지원 검증**
- [x] **T-001 다국어 템플릿 source와 선택형 배포 도입**
- [x] **T-002 GitHub Releases 기반 v2.0.0 공개**
- [x] **T-003 프로젝트 전체 분석 skill 이관**
- [x] **T-004 기존 저장소 adoption 계약**
- [x] **T-005 artifact `check-docs.py` 강화 반영**
- [x] **T-006 consumer PR #28 마무리 (외부 저장소 `jaff2836/claude-review-e2e`)**
- [x] **T-007 이미 적용한 저장소의 업그레이드를 위한 `adopt` 분류 개선**
- [x] **T-008 release 검증 절차 스크립트화**
- [x] **T-009 checker·installer 확정 결함 수정**
- [x] **T-010 문서 소유권·skill Metadata·changelog 안내 정리**
- [x] **DFR-001 `v2.2.0` 준비 재검토**
- [x] **T-011 release verifier adoption plan 진단 강화**
- [x] **T-012 release verifier의 remote `main` 객체·history 진단**
- [x] **T-015 Windows release 도구 호환성 수정**
- [x] **T-016 새 프로젝트 `install` 대상 계약 정합화**
- [x] **T-018 `v2.3.2` release 준비**

완료 이력이 길어지면 기존 CHANGELOG 또는 마일스톤별 보관 문서로 연결하고 본문을 복제하지 않습니다.
