# 프로젝트 작업 목록

> 프로젝트 전체의 변경·마일스톤·우선순위·의존성을 관리합니다. 제품 기준과 결정은 [00-PROJECT.md](./00-PROJECT.md), 상세 상태의 소유권은 [DOCS_GUIDE.md](./DOCS_GUIDE.md)를 따릅니다.
>
> 이 branch에서는 템플릿 저장소 자체의 다국어 변경을 추적합니다. 기존 사용자용 한국어 TODO 양식은 구현 시 `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`에서 `locales/ko/docs/02-TODO.md`로 이관하며, 이 maintainer 작업은 locale artifact에 포함하지 않습니다.

## Metadata

- **Status:** Active
- **Owner:** Chae Sangwon
- **Last reviewed:** 2026-10-07 (KST)
- **Review cadence:** 작업 범위·우선순위·의존성·통합 결과 변경 시
- **Integration target:** local `main`; 공개 저장소 target `jaff2836/coding-agent-docs-template`; v1.7.1 payload 기준 `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`

## Current Milestone

- **Name:** 남은 작업 순차 진행 (T-040 평가 → T-044 → T-046)
- **Goal:** 2026-10-08 사용자가 승인한 순서대로 남은 작업을 PR 단위로 끝냄
- **Target:** 아래 Backlog 29·30·32행
- **Status:** In Progress — T-041·T-042는 끝났고, T-043은 보류, T-045는 취소했습니다. T-040 시범은 이 변경의 PR까지 4/5입니다.

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

- [ ] **T-040 문서·주석 필터 root 시범**
  - 출처: 2026-10-07 외부 자료 분석(anti-slop)과 2026-10-08 사용자 선택. 방향은 root 시범이고 대상은 추적 문서와 코드 주석입니다. 채팅 보고·PR 본문·리뷰 prose는 대상이 아닙니다.
  - 측정 근거: 2026-10-08 추적 문서(ko 116k자, en 210k자, root 171k자)에서 상투 표현 패턴 검사에서 걸린 것은 `다음과 같습니다` 4회(ko·root)와 `ensure` 12회(en)였고(함께 걸린 일반 서술 `할 수 있습니다` 33회는 상투 표현으로 보지 않음) 코드 주석의 장식 구분선·단계 나레이션은 0건이었습니다. `—`와 굵게 표시는 이 저장소의 관례라 필터 대상에서 뺐습니다.
  - [x] 도입: root [문서·주석 필터](./DOC_FILTER.md)(문서 규칙 D1~D7, 주석 규칙 C1~C6, 적용 절차, 평가 기준)를 추가하고 root `AGENTS.md`·[DOCS_GUIDE.md](./DOCS_GUIDE.md) §1에 연결했습니다. locale artifact는 바꾸지 않습니다. 통합: PR #63.
  - [x] PR #63 인계 C63-B-001(Codex, P3): 필터 대상이 `docs/`·`locales/`·`template/`·root README·CHANGELOG로 열거돼 root `AGENTS.md`·`CLAUDE.md`·스킬·`.cursor/BUGBOT.md`·`.omp/WATCHDOG.md`가 빠졌습니다. 대상을 추적 Markdown 전체(`git ls-files '*.md'`)로 고쳤습니다. 통합: PR #64.
  - [x] 시범 1/5 결과 정정과 절차 보완: PR #64의 "후보 0"은 패턴 검색 0건을 줄 단위로 읽은 결과처럼 적은 과소 보고였습니다. 다시 읽으니 후보 1건(D6)이 있었습니다. [문서·주석 필터](./DOC_FILTER.md) §4에 줄 단위 읽기, 방법 기록, 실질·문장 채택 구분을, §5에 측정할 수 있는 이관 기준과 조기 중단 조건을 넣었고, §1의 보관 문서 제외 범위를 좁혔습니다. 통합: PR #65.
  - [ ] 시범 적용: 추적 문서나 코드 주석을 바꾸는 이 저장소 PR 5개에서 작성자가 필터를 적용하고 결과를 PR 본문에 남깁니다. 진행: 4/5(PR #64, PR #65, PR #66, 이 변경의 PR).
  - [ ] 평가와 결정: 다섯 PR의 채택·오탐으로 중단, 규칙 조정, payload 이관 설계 중 하나를 사용자와 정합니다.

## Next

T-040 시범 평가(5/5)를 진행합니다. 새 작업은 사용자와 정한 뒤 PR 단위로 수동 리뷰·필수 CI·통합을 거칩니다.

## Blocked

- [ ] **T-043 community locale 설계 (보류)** — 2026-10-08 사용자 결정으로 보류합니다.
  - 보류 이유: 지금 계약에서는 manifest의 모든 locale이 `en`과 구조 parity를 유지해야 합니다(`check_locales.py`의 `_check_structural_parity`, `experimental` 포함). locale을 하나 추가하면 이후 payload PR마다 그 locale에도 구조 변경을 반영해야 합니다. 또 `stale`·`baseline_version`은 manifest 기준 판 `1.7.1`(v1 이관 시점)에 묶여 있어 현재 release와 번역 사이의 차이를 표현하지 못합니다.
  - 재개 조건: 실제 수요가 생기거나 사용자가 다시 정하는 경우입니다. 후보 locale은 중국어(`zh-Hans`)와 일본어(`ja`)이고, 번역 검수는 사용자 본인이 할 수 있습니다. 다시 시작하면 먼저 상태 장치를 고칠지(뒤처진 locale을 parity에서 빼고 현재 release 기준으로 `stale`을 표시) 정한 뒤 locale을 추가합니다.
  - 등록 당시 설명은 [완료 작업 보관](./TODO_ARCHIVE.md)에 있습니다.

## Backlog

아래 순서는 위험과 선행조건을 고려한 권고 PR 순서이며, Backlog 항목을 시작하는 권한은 아닙니다.
설계 결과에 따라 필요한 구현은 해당 설계 PR과 분리합니다. `v2.3.3`의 candidate 검증과 공개·published 검증은 D-007 경계에 따라 단계와 기록 PR을 분리합니다.

통합된 순서 1~27의 기록은 [완료 작업 보관](./TODO_ARCHIVE.md)에 있습니다.

| 순서 | PR 단위 | 작업 | 선행조건·통합 경계 |
| --- | --- | --- | --- |
| 28 | `claude/t041-t043-records` | T-041 완료, T-042 결과, T-043 보류·T-045 취소 기록 | **In Progress** — 이 변경의 PR. 시범 4/5 |
| 29 | `claude/t040-filter-evaluation` | T-040 시범 평가와 결정 | 28 통합 뒤. 시범 5/5 |
| 30 | `claude/t044-doc-filter-payload-*` | T-044 문서 필터 payload 이관(설계·구현) | 29에서 이관을 정했을 때만 |
| 32 | `claude/v2.6.0-release-prep` 등 | T-046 `v2.6.0` release | 30 통합 뒤. payload 변경이 없으면 생략 |

- [ ] **T-044 문서 필터 payload 이관 (조건부)** — T-040 평가에서 이관을 정하면 en·ko 문서 필터의 설계와 구현을 진행합니다.
- [ ] **T-046 `v2.6.0` release** — T-044의 payload 변경을 D-007 단계로 공개합니다(T-045는 취소). 바뀐 payload가 없으면 생략합니다.

## Cancelled

취소한 변경만 둡니다. 변경-ID, 취소 이유, Intent/Spec의 `Rejected` 근거, 유지 중인 변경 폴더 경로를 남깁니다. 완료·진행 항목과 섞지 않으며 폴더는 삭제하지 않습니다.

- **T-045 community locale 구현** — 2026-10-08 취소. 선행 설계 T-043을 보류해 구현할 계약이 없습니다. 변경 폴더는 만들지 않았습니다. T-043을 다시 시작하면 그 설계에서 구현 항목을 새로 등록합니다.

## Completed

실제 완료 항목만 추가합니다. 변경-ID, 통합 대상, 확인한 revision 또는 작업 트리 범위, 검증 근거의 위치를 남깁니다. 변경 폴더는 유지하고, 구현된 계약이 현재 지원 범위가 되면 PROJECT를 갱신합니다. PR이 있으면 실제 병합 결과를 확인하며, 로컬 작업에 가상의 PR·merge SHA를 만들지 않습니다.

상세 기록은 [완료 작업 보관](./TODO_ARCHIVE.md)에 있습니다. 새 완료 항목은 한 줄로 적고 상세 근거는 PR과 변경 문서에 둡니다.

- [x] **T-042 Origin 원격 branch 정리** — 2026-10-08 사용자 승인으로, `main`을 뺀 Origin 원격 branch 66개(`claude/*`·`codex/*`·`cursor/*`)를 지웠습니다. 삭제 직전에 모든 head가 `origin/main`의 조상인지 다시 확인했고, 삭제 뒤 `git ls-remote origin`에는 `refs/heads/main`만 남았습니다. 열린 PR은 없었습니다. PR 없는 원격 작업이라 이 기록은 다음 PR(이 변경)에 담았습니다.
- [x] **T-041 native Windows published 검증** — `v2.5.0`을 사용자가 Windows 10에서 직접 검증했고(PR #66 기록), Buildkite `windows-ci`의 수동 published 검증 step(PR #66)이 실환경에서 통과했습니다. Build #112(`main` `e105412`, `v2.5.0` 변수)는 Origin check에서 success로 조회됩니다. 상세는 [완료 작업 보관](./TODO_ARCHIVE.md)과 [CI.md](./CI.md) §6에 있습니다.
- [x] **T-035 release 신뢰 루트 검토** — 2026-10-08 검토: 재검토 조건(게시 권한 구조 변경, 외부 배포 요구, 표준 라이브러리만으로 검증할 경로)은 모두 충족되지 않았습니다. `v2.0.0`~`v2.5.0`의 모든 release에 GitHub release attestation이 있어 `gh release verify`로 검증했습니다. 이 서명은 GitHub가 공개 시점에 기록한 digest를 증명할 뿐 게시 계정 탈취는 막지 못합니다. 사용자 선택에 따라 root README(영·한)에 `gh release verify-asset` 선택 검증 안내와 그 한계를 추가했습니다. maintainer 독립 서명은 게시 권한 구조가 바뀌거나 외부 배포 요구가 생기면 새 항목으로 제안합니다. 통합: PR #63.
- [x] **T-039 `v2.5.0` locale release** — 준비는 PR #61로 통합됐습니다. 2026-10-07 사용자가 exact source `6d04b97`에 annotated tag와 draft를 만들어 immutable Latest로 공개했고, candidate와 published(`--base-version 2.4.0`) 검증이 통과했습니다. 상세는 [완료 작업 보관](./TODO_ARCHIVE.md)에 있습니다.
- [x] **T-036·T-037·T-038 보고·검증 규범 구현** — D-015~D-017을 en·ko locale과 root 사본의 `AGENTS.md`(보고 형식, 기본값 명시, 지시의 출처, 완료 근거, red-green), `docs/REVIEW.md` §5, `docs/REVIEW_ROUND.md` §1·§4~§7(위임 경계, 원본 재조회, 원장 `확인` 열), `.cursor/BUGBOT.md`에 반영했습니다. PR #59의 인계 C59-B-001(Codex, P3)도 [완료 작업 보관](./TODO_ARCHIVE.md)에서 해소했습니다. 통합: PR #60. R-002의 요청 안내는 T-039 준비에서 보완했습니다(C60-B-001). 공개는 T-039입니다.
- [x] **T-036·T-037·T-038 보고·검증 규범 설계** — Accepted D-015~D-017([설계](./changes/2026-10-07-agent-reporting-and-verification/01-CHANGE.md)). 통합: PR #59. 공개는 T-039입니다.
- [x] **T-034 `v2.4.0` locale release** — 준비는 PR #58로 통합됐습니다. 2026-10-07 사용자가 exact source `4fe3f76`에 annotated tag와 draft를 만들어 immutable Latest로 공개했고, candidate와 published(`--base-version 2.3.3`) 검증이 통과했습니다. 상세는 [완료 작업 보관](./TODO_ARCHIVE.md)에 있습니다.
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
