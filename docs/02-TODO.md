# 프로젝트 작업 목록

> 프로젝트 전체의 변경·마일스톤·우선순위·의존성을 관리합니다. 제품 기준과 결정은 [00-PROJECT.md](./00-PROJECT.md), 상세 상태의 소유권은 [DOCS_GUIDE.md](./DOCS_GUIDE.md)를 따릅니다.
>
> 이 branch에서는 템플릿 저장소 자체의 다국어 변경을 추적합니다. 기존 사용자용 한국어 TODO 양식은 구현 시 `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`에서 `locales/ko/docs/02-TODO.md`로 이관하며, 이 maintainer 작업은 locale artifact에 포함하지 않습니다.

## Metadata

- **Status:** Active
- **Owner:** Chae Sangwon
- **Last reviewed:** 2026-09-29 (KST)
- **Review cadence:** 작업 범위·우선순위·의존성·통합 결과 변경 시
- **Integration target:** local `main`; 공개 저장소 target `jaff2836/coding-agent-docs-template`; v1.7.1 payload 기준 `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`

## Current Milestone

- **Name:** T-031 CI 검색 도구 gate
- **Goal:** Windows·Linux CI에서 ripgrep·GNU grep 실명령 회귀가 도구 누락 때문에 skip된 채 통과하지 않도록 함
- **Target:** `claude/t031-ci-search-tools` (Origin·GitHub `main` `f066978fb78a1712d67ab2fd97d0a3f823079f4a` 기준)
- **Status:** Next — T-029는 통합됐고, 2026-09-29 전체 분석의 위험 목록을 T-030~T-035로 등록했습니다. T-031은 아직 시작 전입니다.
- **다음 마일스톤:** Backlog 순서에 따라 T-032 원격 운영 정리, T-030·T-014 기록·리뷰 계약 설계를 진행합니다.

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

없음. 다음 작업은 Current Milestone과 Backlog 순서를 따릅니다.

## Next

T-031부터 아래 Backlog 순서로 진행합니다. 각 항목은 PR 단위로 수동 리뷰·필수 CI·통합을 거칩니다. locale payload 공개의 version·candidate/published gate는 T-034에서 확정합니다.

## Blocked

없음.

## Backlog

아래 순서는 위험과 선행조건을 고려한 권고 PR 순서이며, Backlog 항목을 시작하는 권한은 아닙니다.
설계 결과에 따라 필요한 구현은 해당 설계 PR과 분리합니다. `v2.3.3`의 candidate 검증과 공개·published 검증은 D-007 경계에 따라 단계와 기록 PR을 분리합니다.

| 순서 | PR 단위 | 작업 | 선행조건·통합 경계 |
| --- | --- | --- | --- |
| 1 | `codex/t017-windows-junction-design` | T-017: native Windows에서 junction을 재현·설계 | **Integrated** — Origin PR #37 merge `9d53913`과 GitHub `main` fast-forward를 확인했습니다. Windows·Linux 전체 gate와 native 재현을 통과했고, 경계 범위는 D-011로 확정했습니다. |
| 2 | `codex/t017-junction-boundary-implementation` | T-017: 승인된 경계와 native 회귀를 구현 | **Integrated** — Origin PR #38 merge `b5a9c4e`와 GitHub `main` fast-forward를 확인했습니다. 정확한 head의 Windows #27·Linux #12 CI가 통과했습니다. |
| 3 | `codex/t023-release-verifier-contract-regression` | T-023: 실제 installer와 verifier의 설치 거부 계약을 release 전 회귀로 연결 | **Integrated** — Origin PR #39 merge `b40630a`와 GitHub `main` fast-forward를 확인했습니다. Windows #30·Linux #15 CI가 통과했습니다. |
| 4 | `codex/t020-install-onboarding-guidance` | T-020: C34-001과 parent-directory 안내 권고를 진단·문서·회귀로 평가 | **Integrated** — Origin PR #40 merge `f236bf2`와 GitHub `main` 반영 확인; `v2.3.3` asset에 포함 |
| 5 | `codex/t024-installer-stdout-encoding` | T-024: 비-UTF-8 stdout에서 설치 후 거짓 실패 방지 | **Integrated** — Origin PR #41 merge `2901f1a`와 GitHub `main` fast-forward 확인; `v2.3.3` asset에 포함 |
| 6 | `codex/v233-release-prep` | T-025: `v2.3.3` version·이력·package 후보 준비 | **Integrated** — Origin PR #42 merge `989698d`와 GitHub `main` fast-forward 확인 |
| 7 | `codex/v233-candidate-record` | T-027: tag·draft candidate 검증과 인계 기록 | **Integrated** — Origin PR #43 merge `da4d6ae`와 GitHub `main` fast-forward 확인 |
| 8 | `codex/v233-publication-record` | T-028: `v2.3.3` 공개·published 검증 | **Integrated** — Origin PR #44 merge `b423c12`와 GitHub `main` fast-forward 확인; immutable Latest·Linux published 통과 |
| 9 | `codex/t026-document-status-ownership` | T-026: PROJECT §11·설계 Status 중복 정리 | **Integrated** — Origin PR #45 merge `9a7764b`와 GitHub `main` fast-forward 확인; C44-001 해소 |
| 10 | `codex/t022-install-target-invariant` | T-022: 승인된 install 대상 계약을 REVIEW/BUGBOT 불변조건으로 등록 | **Integrated** — Origin PR #46 merge `4c743f1`와 GitHub `main` fast-forward 확인; C46-001 해소 |
| 11 | `codex/t021-install-preflight-order-design` | T-021: preflight 순서 유지·변경을 비교·합의 | **Integrated** — Origin PR #47 merge `ed3438f`와 GitHub `main` fast-forward 확인; A 유지·별도 구현 없음 |
| 12 | `codex/t013-operation-contract-design` | T-013: source/artifact checker·LF·placeholder 회귀 방지 범위를 설계 | **Integrated** — Accepted A(D-012), Origin PR #48 merge `4b8ccc1`·GitHub fast-forward 확인. 구현 1 PR #49 merge `f9df2fa`, 구현 2 PR #50 merge `8d56698`·Windows #60·Linux #45 통과; T-013 구현·통합 완료 |
| 13 | `codex/t029-root-search-command-forms` | T-029: C50-002·C51-001·C51-002 root 검색식 gate 보강 | **Integrated** — Origin PR #51 merge `f066978`·GitHub fast-forward 확인; Windows #64·Linux #49 통과 |
| 14 | `claude/t031-ci-search-tools` | T-031: CI 검색 도구 gate | 선행조건 없음. 두 worker의 rg와 Windows의 전체 Git for Windows 준비됨 |
| 15 | `claude/t032-remote-operations` | T-032: GitHub `main` 보호·Origin→GitHub 동기화 절차·tag 정책 | GitHub ruleset 적용은 사용자가 실행. 다음 release 전 |
| 16 | `claude/t030-t014-contract-design` | T-030·T-014: 기록 시점·리뷰 finding ID 계약 설계 | 같은 artifact 문서를 바꾸므로 한 설계 PR. 사용자 승인 필요 |
| 17 | `claude/t030-t014-contract` | T-030·T-014·T-033: 승인 계약 구현과 TODO 완료 이력 보관 | 16의 승인·통합 |
| 18 | `claude/<version>-release-prep` 등 | T-034: 다음 locale release | 공개 payload 변경을 한 release로 묶음. D-007에 따라 준비·candidate·published 단계 분리 |

- [ ] **T-030 TODO·PLAN 기록 시점 계약 (merge 결합 서술·PR 원장)**
  - 출처: 2026-09-29 전체 분석과 후속 논의. merge된 `main`의 TODO가 한 PR씩 늦게 완료를 반영합니다. 원인은 통합 확인 뒤에만 Completed로 옮기는 규칙, 리뷰를 통과한 head의 동결, merge 뒤 기록 commit 금지([DOCS_GUIDE.md](./DOCS_GUIDE.md) §3, [REVIEW_ROUND.md](./REVIEW_ROUND.md) §9)와, 자기 PR의 CI·리뷰 결과를 그 PR 안에 기록하는 관행이 겹친 것입니다.
  - 사용자 결정(2026-09-29): branch 문서는 그 branch의 최종 head가 merge되는 시점까지의 상태를 결합 서술할 수 있습니다. merge 이후 사건(release 공개, GitHub 동기화, 다른 PR, 외부 검증)을 서술하는 것은 기본적으로 위반이며, 사용자가 명시적으로 요청한 경우에만 허용합니다.
  - 설계 제안(미승인): 자기 head의 CI 번호·리뷰 판정·merge SHA는 TODO에 쓰지 않고 PR을 원장으로 삼아 기록 전용 commit을 없앱니다. 최종 head 리뷰에서 새로 나온 finding은 `문서 반영 대기`로 다음 PR이 받습니다. 예외 요청의 근거를 PR 본문에 남기는 방식과 release candidate·공개 기록 PR 통합도 설계에서 검토합니다.
  - 경계: locale `DOCS_GUIDE.md`·`02-TODO.md`·`REVIEW_ROUND.md` §9와 review-round skill은 artifact이므로 DESIGN 절차·사용자 승인·release가 필요합니다. 결정 ID는 승인 때 발급합니다.
- [ ] **T-031 CI 검색 도구 gate**
  - 출처: 2026-09-29 분석과 사용자 제공 CI 로그. 사용자가 두 Buildkite worker에 rg를 설치한 뒤 Linux #48·Windows #63에서 ripgrep 회귀가 실행됐습니다. Windows #63의 GNU grep 회귀는 `grep is unavailable`로 skip됐습니다. Windows worker에는 전체 Git for Windows가 설치돼 있습니다.
  - 범위: Linux·Windows pipeline에서 unittest 전에 `rg`와 GNU grep을 확인해 없으면 build를 실패시킵니다. Windows는 Git for Windows의 `usr\bin`을 그 단계 PATH 뒤에 붙여 Git Bash와 같은 GNU grep을 쓰며 System32 도구를 가리지 않게 합니다. [CI.md](./CI.md) §6에 도구 요구를 기록하고 테스트 코드와 artifact는 바꾸지 않습니다.
  - 완료 조건: exact head의 Windows·Linux 로그에서 ripgrep·GNU grep 회귀가 모두 실행·통과하고 통합됩니다.
- [ ] **T-032 원격 운영: GitHub `main` 보호·동기화 절차·tag 정책**
  - 출처: 2026-09-29 분석. GitHub에는 `v*` tag ruleset만 있고 `main` branch protection이 없습니다(branch protection API 404 확인). Origin→GitHub `main` non-force fast-forward 절차는 TODO 기록에만 있고 maintainer 문서에 없습니다. Origin에는 v2.2.0~v2.3.2 tag만 있으며, release verifier는 GitHub tag만 사용합니다.
  - 범위: GitHub `main`의 force push·삭제를 막고 fast-forward push는 허용하는 ruleset(사용자 실행), root maintainer 문서의 동기화 절차와 tag 정본 명시, Origin tag 동기화 여부 결정.
- [ ] **T-033 TODO 완료 이력 보관** — Completed에 PR별 검증 로그가 누적돼 이 문서가 커졌습니다. Completed 규칙의 "완료 이력이 길어지면 보관 문서로 연결"을 적용해 요약·링크만 남기며, TODO 구조를 함께 바꾸는 T-030 구현 PR에서 진행합니다.
- [ ] **T-034 다음 locale release** — `v2.3.3` 이후 payload 변경은 en·ko `docs/TEMPLATE_GUIDE.md`(T-013 검색 선언)입니다. PR #50의 인계대로 release 이력에 검색 선언 단일화·Bash 전제·TEMPLATE_GUIDE 삭제 전 보관과 변경 파일을 기록합니다. T-030의 artifact 변경과 한 release로 묶는 것을 기본으로 하되, T-030 설계가 길어지면 guide 변경만 먼저 patch로 공개합니다. version·시점은 준비 PR에서 정합니다.
- [ ] **T-035 release 신뢰 루트 검토 (서명·attestation)** — installer는 같은 release의 `SHA256SUMS`·manifest로 무결성을 확인하지만 게시 계정 탈취는 막지 못하며, immutable release와 tag ruleset으로 완화합니다. 게시 권한 구조가 바뀌거나 외부 배포 요구가 생기거나 표준 라이브러리만으로 GitHub release attestation을 검증할 경로가 확인되면 D-004 확장 설계로 재검토합니다.
- [ ] **T-014 병렬 리뷰 finding ID 충돌 방지 방식 검토** — reviewer-qualified ID와 종합 단계 canonical ID 부여를 우선 검토하고, 반복 근거와 사용자 승인 없이 `REVIEW.md`·`REVIEW_ROUND.md` 계약을 바꾸지 않습니다. T-030과 같은 문서를 바꾸므로 한 설계 PR에서 다룹니다. 2026-09-29부터 Claude가 개발, Codex가 리뷰를 맡는 등 리뷰어 구성이 바뀔 수 있으므로 모델명이 아닌 고정 리뷰어 슬롯 라벨을 기준으로 검토합니다.

2026-09-29 분석의 root §3 검색식 allowlist 권고는 T-029에서 해소됐고, 작업 트리의 로컬 `.swp` 파일은 저장소 작업이 아니어서 등록하지 않았습니다.
- [ ] `en`·`ko` 외 community locale — v2의 locale 추가 계약과 두 공식 locale 지원 검증 후 재검토

## Cancelled

취소한 변경만 둡니다. 변경-ID, 취소 이유, Intent/Spec의 `Rejected` 근거, 유지 중인 변경 폴더 경로를 남깁니다. 완료·진행 항목과 섞지 않으며 폴더는 삭제하지 않습니다.

## Completed

실제 완료 항목만 추가합니다. 변경-ID, 통합 대상, 확인한 revision 또는 작업 트리 범위, 검증 근거의 위치를 남깁니다. 변경 폴더는 유지하고, 구현된 계약이 현재 지원 범위가 되면 PROJECT를 갱신합니다. PR이 있으면 실제 병합 결과를 확인하며, 로컬 작업에 가상의 PR·merge SHA를 만들지 않습니다.

- [x] **T-029 root 검색식 gate 보강 (C50-002·C51-001·C51-002)**
  - 출처·판정: PR #50 version 2 head `61e730ff36f276b6a805d0c5ce240b61889c5456` / base `f9df2fac4554ef8997695122b200df576133410f`의 **C50-002**(P3·confidence 0.95·blocking=false). Claude 댓글 `cmt_01m3nnjh7afqbaqbmnfqegktsh`은 `egrep`·`fgrep`·경로·`.exe` 표기 우회를, Luna 댓글 `cmt_01m3nnv319ezy99582103nzzt8`은 같은 원인의 shell `-c` 우회를 추가 재현했습니다. 중복 finding ID나 영구 deferral은 만들지 않습니다.
  - 우선순위·권한: 2026-09-29 사용자의 리뷰 확인 후 다음 작업 진행 요청에서 남은 인계를 우선 처리합니다. PR #50은 기본 통과 임계값을 충족해 먼저 통합했으며, 범위가 작은 같은 checker의 후속 수정을 T-014 정책 설계보다 앞에 둡니다.
  - 상위 계약·범위: [D-012 설계](./changes/2026-09-28-operation-contract-regression/01-CHANGE.md) R-005·R-007과 C48-001의 root 정본 위임을 보강합니다. 구조 원인이 아닌 재현된 private 모듈 버그이므로 DESIGN §1의 예외에 따라 새 설계·승인 절차를 반복하지 않습니다. 상세 실행 상태는 이 항목만 소유합니다.
  - [x] 통합 기준 `8d56698033fd40a982c6cf0d6bad6dbdeaee94c1`의 임시 source fixture에서 두 별칭·POSIX 경로·`.exe`·`sh -c` 다섯 조건이 오류 없이 통과함을 재현했습니다. 실제 source gate가 호출되는 exporter·packager 경로도 대조했습니다.
  - [x] version 1(`8b9d1b092f439b2f336a8ca580a64cc1bee7c27a`)은 root §3 코드 토큰의 basename·`.exe` 정규화와 Bourne shell literal `-c` 재토큰화로 다섯 조건을 거부했습니다. 이 도구 판별 방식은 아래 C51-001 수정으로 대체했습니다.
  - [x] 기준 `8d56698`에서 시작한 작업 트리의 source docs(304 links/45 files·절 참조 77개·invariant 5개)·stable locale·문서 회귀 65건(Linux Windows 전용 1건 skip)·locale 회귀 59건·전체 unittest 210건(Linux Windows 전용 3건 skip)이 통과했습니다. rg/GNU grep 실명령 회귀도 모두 실행했습니다. en·ko의 각 30-member export inventory·byte를 기준 commit의 payload와 대조해 동일함을 확인했고 wrapper `--root`·artifact 자체 checker·tests 53건씩, maintainer 파일 미포함·diff 검사도 통과했습니다. 로컬 작업 트리 검증과 후속 exact head의 원격 CI·리뷰는 구분합니다.
  - [x] PR #51 version 1 리뷰: 사용자 review `rev_01m3nxa3m3f5qbmhqez1x0waz6`와 Luna `cmt_01m3nxjg5ke64r5p1n0nhtkz8x`는 finding이 없고, Claude `cmt_01m3nyhpd4ewet66f1b04s77pw`는 **C51-001**(P3·confidence 0.95·blocking=false)을 보고했습니다. exact head에서 `sed`·`awk`·`python3 -c`·`ugrep`·`Select-String`·`pwsh -c`와 inline `sed` 검색식이 gate를 통과했습니다. 원인이 C50-002와 같은 도구 denylist이므로 2026-09-29 사용자 요청에 따라 이 PR에서 수용합니다.
  - [x] C51-001: 도구 판별을 제거하고 root §3을 닫힌 문법으로 검사합니다. fenced code의 비어 있지 않은 비주석 줄은 AGENTS.md의 Docs·Docs test·Locale source 세 명령과 정확히 같아야 하고, fenced 밖 visible text는 version 2에서 모든 locale 검색식이 공유하는 `{{`·`YYYY-MM-DD`·`template-example`만 대조했습니다(아래 C51-002에서 교체). `template_placeholder_pattern=` 선언 거부는 유지하며 shell·Markdown 코드를 토큰화·실행하지 않습니다. root §3에 이 제약을 안내했습니다.
  - [x] 회귀: C51-001 12건(fenced 다른 도구·wrapper·허용 명령 변형, inline·들여쓴 줄·본문 어휘)을 추가해 수정 전 실패·수정 후 통과를 확인했습니다. C50-001·C50-002 조건은 새 문법에서도 거부되고, 도구 이름 언급·HTML 주석·`#` 주석·다른 절 예시는 통과합니다. 잘못된 quotation은 별도 진단 대신 허용되지 않은 코드 줄로 거부합니다.
  - [x] version 1 head에서 시작한 version 2 작업 트리의 source docs(304 links/45 files·절 참조 77개·invariant 5개)·stable locale·문서 회귀 65건(Linux Windows 전용 1건 skip)·locale 회귀 60건·전체 unittest 211건(Linux Windows 전용 3건 skip)과 diff 검사가 통과했습니다. ripgrep 14.1.1·GNU grep 실명령 회귀도 실행했습니다. en·ko의 각 30-member export는 version 1 export와 byte-identical이고 wrapper `--root` 검사가 통과했습니다. 로컬 작업 트리 검증과 version 2 exact head의 원격 CI·리뷰는 구분합니다.
  - [x] PR #51 version 2 리뷰: 사용자 review `rev_01m3nzyt1met4amk0jtex9gpaq`는 finding이 없고, Codex review `rev_01m3p0263ee2mbjrp7bx1xa8gf`(inline `cmt_01m3p0263yfr0bt8b7y4yqynv2`)는 **C51-002**(P3·confidence 0.99·blocking=true)를, Luna 재리뷰 `cmt_01m3p0dk24fm5b46a8hh0ahe5p`는 같은 조건을 확인했습니다. version 2가 코드 밖 text를 공통 세 토큰으로만 대조해 `Customize for the project`·`프로젝트에 맞게 작성`·`Adapt to the project`만 쓴 inline 검색식이 version 1과 달리 통과했습니다. 이번 변경이 만든 회귀이므로 수용합니다.
  - [x] C51-002: root 전용 어휘 목록을 두지 않고, locale 검사가 검증한 각 locale의 `template_placeholder_pattern` 선언을 그대로 root §3 fenced 밖 visible text에 대조합니다. 선언이 없거나 잘못된 locale은 기존 locale 오류로 실패합니다. root §3 안내 문구도 이에 맞췄습니다.
  - [x] 회귀: C51-002의 세 inline 사례와 ko 예시 어휘 본문 사례, locale 선언에 새 대안을 추가하면 root 본문에서도 거부되는 단일 출처 회귀를 추가했습니다. 새 C51-002 사례 4건과 단일 출처 회귀는 version 2 checker에서 실패하고 수정 후 통과합니다.
  - 검증 경계: root §3 코드 줄은 허용 목록, 코드 밖 text는 각 locale의 선언 패턴과 비교합니다. §3에 다른 명령을 두려면 이 checker 목록을 함께 갱신합니다. locale 선언 패턴에 걸리지 않는 텍스트는 placeholder 검색으로 보지 않으며, fenced 안 `#` 주석은 기존처럼 허용합니다. root §3 범위·source 전용 의존성과 artifact 공개 CLI·inventory·payload 계약은 상위 설계 그대로입니다.
  - [x] version 2 head에서 시작한 version 3 작업 트리의 source docs(304 links/45 files·절 참조 77개·invariant 5개)·stable locale·문서 회귀 65건(Linux Windows 전용 1건 skip)·locale 회귀 61건·전체 unittest 212건(Linux Windows 전용 3건 skip)과 diff 검사가 통과했습니다. ripgrep·GNU grep 실명령 회귀도 실행했습니다. en·ko의 각 30-member export는 version 1 export와 byte-identical이고 wrapper `--root` 검사가 통과했습니다. version 2 exact head의 Windows #63·Linux #48 성공은 version 3 통과 근거로 쓰지 않습니다.
  - 통합 결과: PR #51 version 3 head `d7a9f94912ac185cc8f248ff9528b99de55ce75a`을 Origin merge `f066978fb78a1712d67ab2fd97d0a3f823079f4a`에 통합하고 GitHub·로컬 `main`에도 non-force fast-forward했습니다. version 3의 사용자 review `rev_01m3p2547jevqv57eb12gc2c3e`, Codex review `rev_01m3p26k6qfwnrh5ahxem0cwx4`, Luna `cmt_01m3p28r5je3tvdt3zbsdc948k` 모두 새 finding이 없고 C50-002·C51-001·C51-002 해소를 확인했습니다. exact head의 Windows #64·Linux #49 CI가 통과했고 다섯 리뷰 스레드를 정리했습니다. Windows CI의 GNU grep 회귀 skip은 T-031이 소유합니다.

- [x] **T-013 D-009 운영 계약 회귀 방지**
  - 정본·범위: [2026-09-28-operation-contract-regression](./changes/2026-09-28-operation-contract-regression/01-CHANGE.md)가 Intent·대안·R-001~R-007·호환성·PR 순서를 소유합니다. 실행 상태는 이 항목에서 관리합니다. A안이 D-012로 승인됐으며 D-005·D-009와 기존 CLI·schema·inventory를 유지합니다. 설계 승인과 구현·통합을 구분합니다.
  - [x] PR #47 version 2 head `fc186b1` / base `4c743f1`의 세 리뷰와 exact CI 통과·실제 통합을 확인하고 T-021 완료를 아래에 기록했습니다. 선택 권고인 `SHA256SUMS` 404 표기는 정본에 반영했습니다.
  - [x] PR #28 version 2의 권고 `cmt_01m33dxsvpenytt4nndy29hwz9`와 D-009를 대조했습니다. 분석 스킬 source 연결·CLI 경계·placeholder 정본·source 이력 예외·LF 목적을 이번 설계에 포함하며 finding ID 정책은 T-014에 유지합니다.
  - [x] `ed3438f45977167390fd44aeddc6227d774fbccd` 임시 source에서 root 분석 pair의 동시 drift와 en grep 어휘 누락이 기존 검사를 통과함을 재현했습니다. 실제 en/ko export·wrapper 경계·실패 전달·반복 호출·준비 heading도 관찰했고 Git의 LF attribute를 확인했습니다. 제안 검사·Windows probe는 구현 전입니다.
  - [x] T-013 A 검사·회귀 강화(권고)와 B 설명 보강을 비교한 Draft를 준비했습니다. `design`·`review-round`의 root↔ko 차이는 강제 동등성 범위에서 제외했습니다.
  - [x] version 1 head `7af3e86c1e6d82a556c3b82efdef9d376133934e`에서 로컬 root docs·stable locale·docs 회귀 55건·diff 검사가 통과했습니다. 새 설계의 링크·절 참조와 기존 두 불변조건 5개 항목 동등성을 확인했습니다. exact head의 Windows #54·Linux #39 CI도 통과했습니다.
  - [x] 2026-09-28 사용자 선택 응답 “A: 검사·회귀 강화 (권고)”를 근거로 설계 Metadata를 Accepted로 바꾸고 PROJECT §8의 D-012에 승인 범위를 기록했습니다. B는 미선택 비교 근거입니다.
  - [x] 승인 기록을 반영한 작업 트리의 로컬 문서·stable locale·docs 회귀 55건·diff 검사가 통과했습니다.
  - [x] 설계 PR #48 version 2 head `8980c5ba685e175f751a5f61d6ba9e59618560c2` / base `ed3438f`의 세 수동 리뷰와 Windows #55·Linux #40 CI 통과를 확인했습니다. 차단 finding은 없고, Origin merge `4b8ccc1fae789b9555fc80a8fa90727a15b6830d`를 GitHub·로컬 `main`에도 non-force fast-forward했습니다. 통과 head는 동결하고 후속 인계만 이번 브랜치에 기록합니다.
  - [x] 구현 1: source 분석 스킬 연결·실제 wrapper 회귀와 CLI·LF·준비 entry 안내를 별도 PR로 구현·검증·통합했습니다.
    - [x] 무인자 wrapper에 고정된 `project-analysis` 네 사본 byte 검사와 missing·unreadable·영역 밖 경로 진단을 추가했습니다. 인자 경로와 배포 checker는 기존 계약을 유지합니다.
    - [x] 기존 mock 회귀 2건을 보존하고 실제 checker fixture·Git attribute 회귀 10건을 추가했습니다. pair 동시 drift, 파일 실패·외부 symlink/junction, source/artifact 교차 호출·제외·history·실패 코드와 미공개 후보 heading을 검증합니다. canonical 중첩 `docs/locales/` 회귀도 그대로 재사용합니다.
    - [x] maintainer CLI·LF·공개 준비 entry 안내와 체크리스트를 보강했습니다. `.gitattributes`·common·locale payload·manifest·version은 변경하지 않습니다.
    - [x] 기준 `4b8ccc1`에서 시작한 현재 브랜치 작업 트리의 source docs·stable locale·전체 unittest 194건(Linux에서 Windows 전용 3건 skip)이 통과했습니다. 문서 회귀 65건을 포함하며 en/ko의 30-member export는 기준 payload와 byte-identical합니다. 각 export에서 wrapper `--root`·artifact 자체 checker·tests 53건과 `.gitattributes` 미포함을 확인했습니다. 로컬 검증과 미확인 PR exact head의 원격 Windows/Linux CI는 구분합니다.
    - [x] PR #49 version 1 head `589eb9b431b77f37dcb7264c2d4826c5a6b4686e` / base `4b8ccc1`의 세 리뷰 모두 finding이 없고 Windows #57·Linux #42 CI가 통과했습니다. Origin merge `f9df2fac4554ef8997695122b200df576133410f`를 GitHub·로컬 `main`에도 non-force fast-forward했습니다. 비finding 참고(`cmt_01m3kk9zbyf17v4ea0tga11zmg`)인 fail-fast 진단 방식·저장소 안 symlink 동등성은 승인 계약과 맞아 현재 범위를 유지합니다.
  - [x] 구현 2: locale별 검색 선언·참조·보관 안내, source locale 검사·독립 sentinel 회귀를 별도 PR로 구현·검증·통합합니다.
    - PR #48 인계 **C48-001** (`cmt_01m3kgn45be4at0kt1q6tz0z1h`, head `8980c5b`, P2·confidence 0.92·blocking=false)를 수용합니다. R-005·R-007의 완료 조건에 root 검색 안내의 locale 정본 위임과 별도 검색식 부재를 확인하는 source gate·회귀를 포함합니다. 현재 브랜치에서 구현했고 PR 검증·통합 후 해소를 확정합니다.
    - PR #48의 비finding 권고(`cmt_01m3kgq9h0epssrvksdyqzw2zp`)도 구현 2에 인계합니다. rg·GNU grep-E·Python `re`에서 같은 의미를 유지하고 Bash(Windows에서는 Git Bash/WSL)·동일 shell에서 선언부터 실행하는 전제를 명시합니다.
    - [x] en·ko 가이드 §3에 단일 single-quoted literal 선언과 두 quoted 참조를 두고 §5에 TG 삭제 전 선언·명령 보관을 안내했습니다. root §3은 locale 정본에 위임합니다.
    - [x] 기존 locale 검사에 선언·순서·regex operand·독립 sentinel과 root 정본 위임 검사를 연결했습니다. 전체 regex 복제나 shell 실행 없이 확인하며 source export·package에도 같은 gate가 적용됩니다. source fixture에 필요한 root 안내를 포함했습니다.
    - [x] 회귀 11건을 추가해 어휘 누락·missing/duplicate/dynamic 선언·잘못된 참조·주석/fence decoy·root 독립 검색식·missing guide를 거부합니다. 실제 rg/GNU grep 명령을 인자 배열로 실행해 Owner 교체 후 남은 날짜·숨김 Markdown·Git 내부 제외·guide 제외·복사용 `_template` 결과를 확인합니다. 도구가 없는 환경은 명시적으로 skip하며 설치하거나 다른 도구로 통과를 가정하지 않습니다.
    - [x] 기준 `f9df2fa`에서 시작한 현재 브랜치 작업 트리의 source docs(303 links/45 files·절 참조 76개·invariant 5개)·stable locale·문서 회귀 65건·locale 회귀 54건·전체 unittest 205건이 통과했습니다. Linux에서는 Windows 전용 3건 skip이며 rg/GNU grep 실제 명령 회귀는 모두 실행했습니다. en/ko의 30-member export는 기준과 같은 inventory이고 `docs/TEMPLATE_GUIDE.md`만 byte가 달라졌습니다. 각 export에서 wrapper `--root`·artifact 자체 checker·tests 53건, maintainer 파일 미포함과 diff 검사를 확인했습니다. PR exact head의 원격 Windows/Linux CI·수동 리뷰·통합은 후속 확인합니다.
    - [x] PR #50 version 1 head `9bb68d2c786195e23cb25a13e772c01d76eb058d` / base `f9df2fa`의 세 수동 리뷰와 Windows #59·Linux #44 CI를 확인했습니다. 두 리뷰는 finding이 없고 Luna 댓글 `cmt_01m3nb0mf6f9f9zq9zbdy7pcm8`은 **C50-001**(P2·confidence 0.98·blocking=true)을 보고했습니다. root 검색 절에 `git grep`을 추가해도 통과하는 조건을 재현했으므로 병합하지 않고 수정합니다.
    - [x] C50-001: root 독립 검색 검사를 실제 §3으로 한정하고 shell 코드를 실행하지 않는 토큰 검사로 바꿨습니다. fenced·inline의 `git grep`, Git 옵션·줄 이어짐·wrapper·shell separator 형태를 거부하며 주석·단순 도구 이름 언급·다른 절의 무관한 검색 예시는 허용합니다. 잘못된 quotation은 오류로 진단합니다. 추가 회귀 2건은 수정 전 실패·수정 후 통과를 확인했습니다.
    - [x] 수정 작업 트리의 source docs·stable locale·문서 회귀 65건(Linux Windows 전용 1건 skip)·locale 회귀 56건·전체 unittest 207건(Linux Windows 전용 3건 skip)이 통과했습니다. rg/GNU grep 실명령 회귀는 모두 실행했으며 version 1 이후 locale·common payload byte와 inventory는 변경하지 않았습니다. 새 head의 원격 CI·재리뷰 결과는 이전 head의 성공과 구분합니다.
    - PR #50 Claude의 비finding 인계(`cmt_01m3nar359fxebfbewtjep1f39`): root 검사 범위 권고는 C50-001 수정에 반영합니다. 다음 release-prep의 locale guide 이력에 검색 선언 단일화·Bash 전제·TG 삭제 전 보관을 기록하고 artifact 변경 파일이 locale별 `docs/TEMPLATE_GUIDE.md`뿐임을 명시합니다. 공개 version·시점은 아직 확정하지 않았습니다.
    - [x] PR #50 version 2 head `61e730ff36f276b6a805d0c5ce240b61889c5456` / base `f9df2fa`의 세 수동 재리뷰가 C50-001 해소를 확인했습니다. P0·P1·Blocking P2는 없고 Windows #60·Linux #45 CI가 통과했습니다. 통과 head를 변경하지 않고 Origin merge `8d56698033fd40a982c6cf0d6bad6dbdeaee94c1`에 통합한 뒤 GitHub·로컬 `main`에도 non-force fast-forward했습니다. C48-001·C50-001의 구현·통합 해소를 확정하며 비차단 C50-002는 T-029에 인계합니다.
  - 완료 경계: 두 구현 PR의 검증과 Origin/GitHub 통합을 확인해 T-013의 구현·통합을 완료했습니다. locale payload 변경을 공개하는 후속 release·version·게시 시점은 별도 작업이며 설계 승인으로 완료 처리하지 않습니다.

- [x] **T-021 install preflight 순서 설계**
  - 정본·선택: [2026-09-28-install-preflight-order](./changes/2026-09-28-install-preflight-order/01-CHANGE.md). 2026-09-28 사용자가 PR #47 version 1 head `978be1788fd3e2fc15c72ac823b8c04815e5fc0e`의 A안을 선택해 D-010 §2.3의 현재 순서·오류 우선순위를 유지했습니다. 별도 구현·release 없이 설계 판단을 기록했으며 B는 미선택 비교 근거입니다.
  - 초기 근거: PR #46 merge `4c743f149d726c692684f8f626e31fd74db34a73`의 호출자·Linux fixture 6개와 PR #46의 C46-001 인계를 대조했습니다. version 1의 로컬 docs·stable locale·docs 회귀 55건·diff 검사와 Windows #51·Linux #36 CI가 통과했습니다.
  - 통합 결과: 승인 기록을 반영한 PR #47 version 2 head `fc186b11fb71236a26d64aecea4cdaf6b91bb435`을 Origin merge `ed3438f45977167390fd44aeddc6227d774fbccd`에 통합하고 GitHub `main`에도 non-force fast-forward했습니다. 세 리뷰 모두 새 finding이 없고 exact Windows #52·Linux #37 CI가 통과했습니다. 로컬 docs·stable locale·docs 회귀 55건·diff 검사와 두 독립 리뷰의 전체 unittest 184건(Linux에서 Windows 전용 2건 skip)·fixture 재현도 확인했습니다.
  - 인계 처리: PR #47의 선택 권고였던 “asset 404”를 `SHA256SUMS` 404로 명시해 HTTP 1회 표의 재현 조건을 고정했습니다. 원 코멘트 `cmt_01m3kcyck2ftf8hjwb5x33w05p`, 재확인 `cmt_01m3kdarb0e3br1njt1w8ybffa`는 finding이 아닌 표기 권고이며 T-013 문서 변경에서 반영합니다. 향후 순서 변경 시 REVIEW·BUGBOT 두 불변조건을 같은 구현 PR에서 갱신한다는 R-005도 비교 근거로 보존합니다.

- [x] **T-022 install 대상 불변조건 등록**
  - 출처·범위: 기존 T-022와 2026-09-28 사용자의 리뷰 후 다음 작업 진행 요청에 따라 승인된 D-010을 maintainer 리뷰 불변조건으로 등록합니다. 상위 계약은 [install 대상 설계](./changes/2026-09-22-install-target-contract/01-CHANGE.md) R-001·R-002·§2.3이며 D-011의 기존 symlink·junction 경계도 유지합니다.
  - 평가·선택: REVIEW의 일반 정확성·문서 계약 검사만으로 둘 수도 있지만, BUGBOT은 자신의 단일 파일에서 판단하므로 install 대상 보호를 두 불변조건 목록에 명시하는 안을 채택합니다. 기존 파일과 겹치지 않아도 비어 있지 않으면 거부하고, emptiness를 확인할 수 없으면 fail-closed합니다. 대상 검사 거부 시 tree를 보존하며, 빈 대상·읽기 전용 `adopt` 안내는 비어 있음 검사에서 거부한 경우로 한정합니다.
  - 설계 범위: 이미 승인·구현된 계약의 문서 등록이므로 DESIGN §1의 작은 문서 변경 예외를 적용하고 새 제품 결정·설계를 만들지 않습니다. 대상 preflight의 release·archive 검증 뒤 순서와 오류 우선순위는 D-010 그대로이며, 순서 재설계는 별도 T-021입니다.
  - 변경·검사: `docs/REVIEW.md` §6과 `.cursor/BUGBOT.md`의 `Install 대상 보존` 항목을 같은 문장으로 추가합니다. 기존 checker는 example을 제외한 전체 bullet 목록의 동등성을 검사하므로 코드·규칙 변경 없이 두 목록을 비교합니다. locale payload와 공개 asset은 이 maintainer 정책 변경에 포함되지 않습니다.
  - 최초 등록 검증: PR #46 version 1 head `dc571d9677de44bc72635a8eec7e2a4b6fa08bc4`에서 전체 unittest 184건(Linux의 Windows 전용 2건 skip), root docs의 두 목록 5개 항목 동등성, stable locale·diff 검사가 통과했습니다. 새·빈 대상 성공, 비어 있지 않은 대상과 `.git` 대상 거부·tree 보존, unreadable·uninspectable 대상 fail-closed 회귀를 포함합니다. 정책 문장과 `install` → `_resolve_target_root`·`_require_empty_install_target` → `_write_members`의 실제 순서를 대조했습니다. exact head의 Windows #48·Linux #33 CI도 통과했습니다.
  - C46-001 판정·수정: PR #46 version 1 head `dc571d9` / base `9a7764b`의 자동 리뷰와 Luna가 P3·confidence 0.90·blocking=true로 보고한 안내 범위 모호성을 수용했습니다. `_resolve_target_root`·`_link_kind`의 root·부모·검사 실패 메시지에는 `adopt` 안내가 없으므로, 두 불변조건에서 tree 보존은 대상 검사 거부에 적용하고 안내는 `_require_empty_install_target`의 비어 있음 검사 거부로 한정합니다. version 1은 기본 통과 기준을 충족했지만 같은 PR에서 문구를 수정했고, version 2의 세 재리뷰가 해소와 새 finding 없음을 확인했습니다.
  - 후속 문구 검증: root docs의 두 목록 5개 항목 일치, stable locale·docs 회귀 55건·diff 검사가 통과했습니다. installer 코드·locale payload는 수정하지 않았으며, version 2 exact head의 필수 CI와 두 독립 리뷰에서 전체 unittest 184건을 확인했습니다(Linux의 Windows 전용 2건 skip).
  - PR #45 인계: version 1 head `3281f0b` / base `b423c12`의 세 리뷰가 C44-001 해소와 새 finding 없음을 확인했습니다. T-026의 실제 Origin·GitHub 통합 완료는 아래 완료 항목에 반영합니다. 다음 release 기록에서는 PROJECT Metadata Status와 Current State의 공개 기준을 함께 확인하라는 권고를 유지합니다.
  - 통합 결과: PR #46 version 2 head `e113dd159a986633a87544866b164bbec6b2e7e5`을 Origin merge `4c743f149d726c692684f8f626e31fd74db34a73`에 통합하고 GitHub `main`에도 non-force fast-forward했습니다. exact head의 Windows #49·Linux #34 CI가 통과했습니다. C46-001은 해소됐으며 순서 변경 시 두 불변조건을 함께 갱신한다는 인계는 T-021 설계 범위에 연결합니다.

- [x] **T-026 문서 상태 중복 정리**
  - 출처·범위: PR #41 version 1 head `d86bee8`의 C41-001에서 파생한 기존 T-026과 PR #44 version 1 head `2165887a43aef91455cf7f493edc7d43282c41d3` / base `da4d6aef4b817e396cf1400e912b233a66b58601`의 C44-001을 함께 처리합니다. PROJECT §11과 T-017 설계 Metadata를 기존 [DOCS_GUIDE §2·§4](./DOCS_GUIDE.md)에 맞추는 maintainer 문서 변경입니다.
  - C44-001 판정·이관: T-017 설계 Status의 `다음 release 반영 전`은 공개 후 잘못된 현재 상태입니다. 세 리뷰가 같은 P3를 확인했고 confidence는 0.90~0.95, blocking 판정은 서로 달랐습니다. P0·P1·Blocking P2가 없어 PR #44를 통과시켰으며 T-026에서 해소했습니다. 영구 review deferral은 추가하지 않았습니다.
  - PR #45 정리 결과: 당시 PROJECT §11을 T-021·T-022·T-013·T-014의 미해결 판단과 TODO 링크로 줄였습니다. 완료·통합·CI 상세를 반복하는 방식은 상태 변경 시 동기화 지점을 늘리므로 채택하지 않았으며, 이미 지정된 실행·공개 기록과 확정된 제품 결정은 각 정본에서 보존했습니다.
  - 설계 Metadata: T-017 Status를 승인 상태 `Accepted`만 표시하도록 바꿉니다. D-011의 요구·승인·결정과 날짜별 변경 기록은 유지합니다. 공개 상태는 PROJECT의 현재 기준·CHANGELOG·T-028 기록에서 확인하며, Metadata를 release마다 고치는 사본으로 쓰지 않습니다.
  - 근거 보존: §11의 제품 결정은 PROJECT §1·§5·§8에, PR #37 final head `cc67e31`과 native CI 근거는 T-017 변경 기록·CI 문서에, T-020·T-023 등의 실제 통합은 해당 TODO 완료 항목에 이미 있습니다. 중복 문장을 제거해도 이 근거와 연결은 유지합니다.
  - 통합 결과: PR #45 version 1 head `3281f0b75b30138747e7d350704bf988b61fe056`을 Origin merge `9a7764bca550f828edad757b45150f735cb3d3f7`에 통합하고 GitHub `main`에도 non-force fast-forward했습니다. 세 리뷰 모두 새 finding이 없고 C44-001 해소를 확인했습니다. exact head의 Windows #46·Linux #31 CI가 통과했으며 root docs·stable locale·docs 회귀 55건·diff 검사도 통과했습니다. 전체 unittest 184건은 CI와 두 독립 리뷰에서 확인했습니다(Linux의 Windows 전용 2건 skip).

- [x] **T-028 `v2.3.3` 공개와 published 검증**
  - 범위·위임: 2026-09-28 사용자가 `v2.3.3` 공개부터 다음 기록 PR 게시까지 명시적으로 위임했습니다. D-007의 수동 게시 단계로 기존 draft를 공개하고, tag source의 읽기 전용 verifier로 published gate를 실행했습니다.
  - 공개 결과: [immutable Latest `v2.3.3`](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.3.3)을 2026-09-28 03:01:47 UTC(12:01:47 KST)에 공개했습니다. `isDraft=false`, `isImmutable=true`, `isPrerelease=false`이며 GitHub Latest identity도 일치합니다. 기존 draft asset 5개의 ID·SHA-256은 게시 전후 동일합니다.
  - source·ref: annotated tag의 exact source는 `989698d4070d7a9596117cf410362fea0b7f28bb`입니다. 공개·published 실행 시 Origin·GitHub `main`은 `da4d6aef4b817e396cf1400e912b233a66b58601`로 같았고 source는 그 조상이었습니다. 기록 PR의 source와 release의 source를 구분합니다.
  - published 검증: clean exact tag source에서 `python3 scripts/verify-release.py published --version 2.3.3 --source-commit 989698d4070d7a9596117cf410362fea0b7f28bb --repository jaff2836/coding-agent-docs-template --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --base-version 2.3.2`가 exit 0으로 통과했습니다. Linux에서 tag source 자신의 verifier로 5개 asset byte·immutable Latest, latest·exact의 en·ko list/install/export/adopt, source export와의 동등성, `v2.3.2` base-aware upgrade 및 비어 있지 않은 install 대상의 거부·tree 불변을 확인했습니다.
  - 검증 범위: 이번 원격 published E2E는 Linux에서 실행했습니다. Windows는 tag source와 같은 tree의 PR #42 head에서 Windows #40 CI·native junction 회귀가 통과한 근거를 유지하며, native Windows published E2E를 실행했다고 표시하지 않습니다.
  - PR #43 version 1 인계: head `cb4bd84`의 세 리뷰 모두 새 finding이 없었고 Windows #42·Linux #27 CI가 통과했습니다. PROJECT Status·현재 공개 기준·D-011 공개 범위·§11과 en·ko README·changelog를 갱신합니다. 선택 제안인 draft target 변경은 기존 annotated tag와 exact-source 검증으로 게시 대상을 확인할 수 있어 현 상태를 유지했습니다.
  - 통합 결과: PR #44 head `2165887a43aef91455cf7f493edc7d43282c41d3`을 Origin merge `b423c12db3a4d0771272736a81b5e67789a38293`에 통합하고 GitHub `main`에도 non-force fast-forward했습니다. exact head의 Windows #44·Linux #29 CI가 통과했습니다. 리뷰의 유일한 P3 C44-001은 T-026에서 해소하며 공개·published 성공 근거는 유지합니다.

- [x] **T-027 `v2.3.3` draft candidate 검증과 기록**
  - 범위·위임: 2026-09-28 사용자 대화의 다음 작업 진행 요청에 따라 D-007의 수동 release 준비 단계로 annotated tag·draft asset을 준비하고 candidate gate를 실행했습니다. PR #43은 source changelog·TODO만 변경했고, 공개와 published 검증은 T-028이 소유합니다.
  - 확인한 source·ref: exact clean source `989698d4070d7a9596117cf410362fea0b7f28bb`에 local·GitHub annotated `v2.3.3` tag를 결합했습니다. candidate 실행 시 Origin·GitHub `main`도 같은 commit이었습니다. source tree는 리뷰를 통과한 PR #42 head `cdbe374465f6b676416a4ce73d29631b11ebcaf1`과 같습니다.
  - candidate 검증: `python3 scripts/verify-release.py candidate --version 2.3.3 --source-commit 989698d4070d7a9596117cf410362fea0b7f28bb --repository jaff2836/coding-agent-docs-template`가 exit 0으로 통과했습니다. 전체 unittest·root docs·stable locale·diff 검사, 반복 package byte 동등성, 두 remote·annotated tag와 [당시 GitHub draft](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.3.3)의 5개 asset 동등성을 확인했습니다. candidate 당시 draft는 `isDraft=true`, `isImmutable=false`, `isPrerelease=false`, `publishedAt=null`입니다.
  - version 선택 근거: PR #42가 준비한 `v2.3.3` patch를 유지합니다. 명령 집합·manifest schema 2·locale artifact inventory는 유지하고, D-011 경계 강제와 출력 실패·안내·검증 회귀를 묶습니다. Windows Python 3.12 미만의 실행 중단은 호환성 변화이므로 changelog와 draft notes에 명시합니다. patch 선택을 모든 기존 환경의 호환성 보장으로 해석하지 않습니다.
  - PR #42 version 2 인계: C42-001·C42-002는 해소됐고 새 finding은 없습니다. 별도 비차단 권고였던 version 선택 근거는 이 항목에, Python 업그레이드 우선 안내와 구버전 대안의 수정 누락은 en·ko source changelog 및 draft notes에 반영했습니다. T-026은 release 완료 후의 다음 문서 정리 후보로 우선순위를 올립니다.
  - 통합 결과: PR #43 head `cb4bd842d52f1f62b065793e2d85c2df7ad01020`을 Origin merge `da4d6aef4b817e396cf1400e912b233a66b58601`에 통합하고 GitHub `main`에도 non-force fast-forward했습니다. 세 리뷰에서 새 finding이 없었고 exact head의 Windows #42·Linux #27 CI가 통과했습니다. 공개·published 검증은 T-028이 소유합니다.

- [x] **T-025 `v2.3.3` release 후보 준비**
  - 통합 결과: en·ko artifact version·release history와 source changelog를 정렬한 PR #42 head `cdbe374465f6b676416a4ce73d29631b11ebcaf1`을 Origin merge `989698d4070d7a9596117cf410362fea0b7f28bb`에 통합하고 GitHub `main`에도 non-force fast-forward했습니다. tag·draft candidate 검증은 후속 T-027, 공개·published 검증은 T-028이 소유합니다.
  - 검증 근거: exact PR head의 Buildkite Windows #40·Linux #25가 통과했고, root docs·stable locale·docs test 55건·en/ko export와 artifact docs 검사를 확인했습니다. 같은 source의 package 2회가 5개 asset 모두 byte-identical했고, version 2 리뷰에서 C42-001·C42-002 해소와 새 finding 없음이 확인됐습니다.

- [x] **T-024 installer stdout 인코딩 후속**
  - 통합 결과: 비-UTF-8 stdout에서 `install`·`export`·`adopt` 완료 메시지가 `UnicodeEncodeError`로 거짓 실패를 일으키지 않도록 한 PR #41 head `e06e823dd5d7401c9c6a6853096a788d24afb184`을 Origin merge `2901f1a545d40a14ea95ed243231acb7f3bfab34`에 통합하고 GitHub `main`에도 non-force fast-forward했습니다. 공개 `v2.3.2` asset은 변경하지 않았습니다.
  - 검증 근거: 정확한 PR head의 Buildkite Windows #37·Linux #22가 통과했고, 전체 unittest 184건(Linux에서 Windows 전용 2건 skip), root docs·stable locale·`git diff --check`가 통과했습니다. PR #41 version 3 재리뷰에서 C41-001·C41-002 해소와 새 finding 없음이 확인됐습니다.

- [x] **T-020 install onboarding 진단·안내 평가**
  - 통합 결과: `.git`만 있는 대상의 거부 안내, 새 프로젝트의 `git init` 순서와 직접 부모 조건을 Origin PR #40 merge `f236bf2278fcde83fe0c08ae1d9aa8e422d09a32`에 통합하고 GitHub `main`에도 반영했습니다. D-010의 새·빈 대상 계약과 공개 `v2.3.2` asset은 변경하지 않았습니다.
  - 검증 근거: PR #40 exact head `cd3608f`의 Buildkite Windows #33·Linux #18이 통과했습니다. 전체 unittest 183건, root docs·stable locale, en·ko export와 artifact docs 검사 결과는 PR #40에 기록됐습니다.

- [x] **T-023 release 후보의 verifier·installer 계약 회귀**
  - 통합 결과: 실제 installer와 verifier의 새·빈 대상 허용, 겹치거나 무관한 파일이 있는 대상 거부·tree 불변을 같은 local fixture로 대조하는 회귀를 Origin PR #39 head `930e393`에서 `b40630a`로 병합하고 GitHub `main`에도 non-force fast-forward했습니다. 공개 `v2.3.2` asset은 변경하지 않았습니다.
  - 검증 근거: PR #39 exact head의 Buildkite Windows #30·Linux #15가 통과했습니다. 두 환경에서 전체 unittest 181개와 실제 installer subprocess 회귀를 실행했고, Windows native junction 테스트와 probe도 통과했습니다. 다음 release candidate는 별도 준비·검증 작업입니다.

- [x] **T-017 Windows junction 경계 검증**
  - 통합 결과: 승인된 [D-011 경계](./changes/2026-09-23-windows-junction-boundary/01-CHANGE.md)를 구현한 Origin PR #38 head `42d9923`을 `b5a9c4e`에 병합하고 GitHub `main`에도 non-force fast-forward로 반영했습니다. 공개 `v2.3.2` asset은 변경하지 않았습니다.
  - 검증 근거: PR #38 exact head의 Buildkite Windows #27·Linux #12가 통과했고, Windows native junction probe와 전체 unittest 180개, root docs·stable locale gate를 확인했습니다. 다음 release 후보의 installer·verifier 계약 회귀는 T-023이 소유합니다.

- [x] **T-019 `v2.3.2` 공개 기록과 지원 검증**
  - 통합 결과: T-018 exact source `4c6a798885404fdf5170769e271f7d06f4959234`의 candidate가 통과한 5개 asset을 교체 없이 [immutable Latest `v2.3.2`](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.3.2)로 공개했습니다. verifier의 새 install 거부 문구 대응과 공개 기록은 Origin PR #36 merge `cc791be2370e76930184e473061312518d5fe221`에 통합하고 GitHub `main`에도 non-force fast-forward로 반영했습니다.
  - 검증 근거: clean exact source를 `--root`로 지정한 보완 verifier의 `published --base-version 2.3.1`이 통과했습니다. Latest·immutable metadata와 게시 전과 같은 5개 asset, latest·exact의 en·ko list/install/export/adopt, base-aware upgrade, artifact와 겹치거나 무관한 파일이 있는 install 대상의 거부·tree 불변을 확인했습니다. 두 remote `main`이 merge commit을 가리킵니다.

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
  - 통합·운영 결과: Origin PR #20 merge `40306b65fe211402090d7a11b5c3ffafcb3689eb`의 검증 CLI로 `v2.1.1`부터 `v2.3.3`까지 실제 draft candidate·immutable published 경로를 반복 확인했습니다. 각 release에서 검증한 5개 asset을 게시 전후 교체하지 않았으며 exact source는 [변경 기록](./changes/2026-09-20-release-verification/01-CHANGE.md)에 남겼습니다.
  - 검증 근거: 최신 `v2.3.3` published는 Linux에서 tag source 자신의 verifier로 latest·exact의 en·ko `list-locales`·`install`·`export`·`adopt`, `v2.3.2` base-aware upgrade, source export와 비어 있지 않은 target 불변을 확인했습니다. release는 `isDraft=false`, `isImmutable=true`, Latest입니다.

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

- [x] **T-015 Windows release 도구 호환성 수정**
  - 통합·공개 결과: POSIX 상대 경로 정렬, Windows materialized mode 의미, LF checkout과 제한된 symlink fixture skip을 Origin PR #30 merge `3b4bf674da8f7e8c13b2a69c45b2cf1f8ce54756`에 통합했습니다. release 준비 PR #31 merge `3460e4ccd0065bcd8a24fd64a6cd7135293926a0`의 5개 asset을 교체 없이 [immutable Latest `v2.3.1`](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.3.1)로 공개했습니다.
  - 검증 근거: PR head `a64a8897673924abe1c110baad3b2a6ecc8aa811`의 native Windows·Python 3.14.7에서 전체 unittest 174개(실패·오류 0, symlink 관련 skip 16)와 en·ko package·export artifact 검증이 통과했습니다. `v2.3.1` exact source의 `published --base-version 2.3.0`은 Linux와 native Windows 10.0.28000에서 모두 통과했고, Windows 실행은 synchronized `main` `969d1ed48414cee30e698067417d40122a1b8f59`과 5개 asset을 확인한 뒤 exit code 0으로 끝났습니다.

- [x] **T-016 새 프로젝트 `install` 대상 계약 정합화**
  - 변경-ID: `2026-09-22-install-target-contract`, 결정 D-010. Origin PR #34의 `f4004b727fc6e54ce40e7a05877ce74c20695aa4`은 merge commit `a105740ca16ea3e0b6092a7331bf60b89b06f4a3`으로 Origin `main`에 통합됐습니다.
  - 통합 근거: PR #34는 exact head의 installer 회귀 44개·전체 unittest 176개·root docs·stable locale·en/ko export artifact checker와 각 artifact test 53개·Python compile·`git diff --check`를 통과했습니다. 원격 CI runner는 이 템플릿이 제공하지 않아 `No checks reported`였고, 같은 gate를 로컬에서 실행했습니다.
  - release 경계: 공개 `v2.3.1` asset은 변경하지 않았습니다. D-010 계약을 포함한 `v2.3.2` 공개와 candidate·published 검증은 T-018·T-019가 소유합니다.

- [x] **T-018 `v2.3.2` release 준비**
  - 통합 결과: D-010·T-016이 포함된 source의 version·release history를 Origin PR #35 merge `4c6a798885404fdf5170769e271f7d06f4959234`에 통합하고 GitHub `main`에도 non-force fast-forward로 반영했습니다. 양쪽 `main`과 annotated `v2.3.2` tag가 같은 exact source를 가리킵니다.
  - 검증 근거: clean exact checkout의 root docs·stable locale·전체 unittest 176개, 2회 package byte 동일성, 같은 5개 asset의 GitHub draft와 candidate gate가 통과했습니다. 공개와 published 검증·기록은 T-019가 소유합니다.

완료 이력이 길어지면 기존 CHANGELOG 또는 마일스톤별 보관 문서로 연결하고 본문을 복제하지 않습니다.
