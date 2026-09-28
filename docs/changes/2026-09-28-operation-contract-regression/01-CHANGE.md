# 변경: 문서 운영 계약 회귀 방지

## Metadata

- **Change ID:** `2026-09-28-operation-contract-regression`
- **Status:** Accepted
- **Originator:** Chae Sangwon
- **Source:** 기존 T-013, PR #28 version 2의 비차단 운영 권고(`cmt_01m33dxsvpenytt4nndy29hwz9`), 2026-09-28 사용자의 PR #47 리뷰 후 다음 작업 진행 요청
- **Parent:** [제품 기준](../../00-PROJECT.md) D-005·D-009, [문서 소유권 설계](../2026-09-22-documentation-ownership/01-CHANGE.md) R-001·R-002·R-004·R-005
- **Decision:** [PROJECT D-012](../../00-PROJECT.md#8-decisions) — T-013 A 검사·회귀 강화. D-005·D-009를 보강하며 기존 source/artifact 경계는 유지합니다.
- **Approval:** Chae Sangwon, 2026-09-28 선택 응답 “A: 검사·회귀 강화 (권고)” — PR #48 version 1 head `7af3e86c1e6d82a556c3b82efdef9d376133934e`의 A안, R-001~R-007·§2.3 구성·§2.4의 두 구현 PR 순서를 승인했습니다. B안은 미선택이며 release version·게시 시점은 별도 작업입니다.
- **Execution:** [전역 TODO](../../02-TODO.md)의 T-013이 상세 실행·검증·통합 상태를 소유합니다.

## 1. Intent

### 1.1 문제와 현재 근거

D-009는 runtime skill의 Metadata 제거, locale guide 정본, source/artifact별 이력
검사를 정했습니다. PR #28의 실제 결함은 수정됐지만 다음 변경에서 같은 경계가
다시 어긋나는지 확인하는 범위가 남았습니다. 이번 작업은 T-013의 네 항목을 다룹니다.

조사 기준은 PR #47 merge `ed3438f45977167390fd44aeddc6227d774fbccd`입니다.
Linux에서 이 exact tree를 임시 디렉터리에 복사하고 현재 checker·exporter를 호출했습니다.
변경한 fixture는 삭제했고 저장소의 source·checker·tests는 변경하지 않았습니다.

| 확인한 사실·fixture | 현재 관찰 | 해석 |
|---|---|---|
| root와 ko의 각 `.agents`/`.claude` skill 비교 | 각 pair는 같고, root↔ko는 `project-analysis`만 byte-identical | `design`·`review-round`는 maintainer adapter와 locale 계약 본문의 차이가 정당함 |
| root `project-analysis` 두 사본에 같은 Metadata를 추가 | root docs와 stable locale 검사 모두 통과; ko와는 다름 | 두 영역을 잇는 검사 없음; 과거 Metadata 회귀를 재현 가능 |
| en guide의 `grep` 패턴에서 `Customize for the project`만 제거 | locale·root docs 모두 통과; 해당 Owner 줄은 grep 패턴에서 누락 | rg/grep 어휘 중복이 현재 검사로 잡히지 않음 |
| 현재 version의 plain `unpublished candidate` heading | root docs 통과; 다른 version heading은 실패 | 구조 검사는 공개 사실을 확인하지 않음 |
| source wrapper로 en·ko export에 `--root` 실행 | 각 30-member artifact 통과; artifact history 선택 | D-009 CLI 계약이 동작함 |
| artifact에 `locales/en/BROKEN.md`의 깨진 링크 추가 | 두 locale 모두 실패 | artifact CLI에는 source의 top-level 제외가 적용되지 않음 |
| wrapper에 `--root <source>` 뒤 무인자 실행 | 전자는 artifact history marker 부재로 실패, 후자는 source history로 복원·통과 | source 검사 명령은 무인자 경로임; 전역 상태 누수는 관찰되지 않음 |
| 대표 root·common·ko 경로에 `git check-attr text eol` | `text=auto`, `eol=lf` | root `.gitattributes`가 maintainer checkout에 적용됨 |

기존 `tests/test_check_docs.py`의 wrapper 테스트 두 개는 delegation을 mock으로
확인합니다. canonical artifact suite에는 materialized root·top-level 제외와 version
검사가 이미 있습니다. LF는 locale checker가 common·locale payload를 UTF-8·LF·최종
newline로 검사합니다. 위 probe는 Linux에서 실행했으며 새 검사나 native Windows
probe를 실행한 근거로 사용하지 않습니다.

### 1.2 기대 결과·범위

기존 도구를 유지하며 root↔ko 분석 스킬 drift, CLI 경계와 반복 placeholder 어휘를
회귀로 확인합니다. source 준비 단계의 이력과 공개 완료 기록도 구분해 안내합니다.

범위는 `project-analysis`에 한정한 source 연결, source wrapper 회귀, maintainer
LF·미공개 heading 안내, en·ko placeholder 검색 정본과 검증입니다. 이번 PR은 설계와
PR #47 인계만 다루며 실행 계획은 TODO에서 추적합니다.

새 CLI 옵션·checker, locale/manifest schema·artifact inventory 변경, skill 본문 생성,
모든 root↔locale skill 동등성 강제, 전체 Markdown parser, 새 dependency·CI runner,
installer 동작·기존 immutable release 변경은 포함하지 않습니다.

### 1.3 제약과 선택 범위

- locale guide가 적용 프로젝트의 정본이며 root guide는 maintainer 보충 규칙만 소유합니다.
- 기존 검사 실패를 숨기거나 원본 template의 의도된 placeholder를 adoption 실패로 취급하지 않습니다.
- `.gitattributes`를 artifact에 새로 넣거나 적용 저장소의 Git 설정을 바꾸지 않습니다.
- source의 미공개 entry를 공개 증거로 사용하지 않고 D-007 candidate/published gate를 유지합니다.
- **사용자가 T-013 A 검사·회귀 강화안을 선택했습니다.** 선택에 관한 미해결 질문은 없으며 B는 미선택 비교 근거입니다.

## 2. Spec

### 2.1 대안과 선택 이유

| 안 | 내용 | 비용·결과 |
|---|---|---|
| **T-013 A — 검사·회귀 강화(선택)** | 기존 source gate에 분석 스킬 연결과 placeholder 검증을 보강하고 실제 CLI 회귀·maintainer 안내를 추가 | 두 구현 PR 필요; 재현된 drift를 merge 전에 거부; CLI·schema·inventory 유지 |
| **T-013 B — 설명 보강(미선택)** | CLI·LF·미공개 heading과 수동 사본·검색 확인을 root 안내에 명시 | 구현은 작은 문서 PR; root↔ko와 rg/grep의 기계적 검사 공백은 유지 |

현재 검사는 정상 경로를 확인하지만 두 pair를 함께 바꾸거나 한 검색 어휘만 누락하면
놓칩니다. 공개 계약을 재설계할 필요 없이 기존 gate에서 이 범위를 검사할 수 있으므로
A를 권고했고 사용자가 이를 선택했습니다. B는 추가 검사 유지비를 줄이지만 같은 누락을 수동으로 찾아야 합니다.
별도 공통 생성기·JSON 설정·전체 placeholder lint는 현재 규모에 필요하지 않습니다.

### 2.2 A의 요구사항과 검증

| ID | 요구사항 | 상황·입력 | 관찰 가능한 결과·검증 |
|---|---|---|---|
| R-001 | `project-analysis` root↔ko 연결을 source에서만 검사 | root 또는 ko의 두 pair가 함께 drift; 파일 누락·읽기 실패·영역 밖 경로 | source gate 비제로와 경로 진단; 정상 네 사본 byte 동일이면 통과. `design`·`review-round`의 정당한 차이는 허용 |
| R-002 | wrapper 공개 CLI 계약 유지 | 무인자, `--root` en/ko artifact, `--root` source, 실패하는 실제 checker, 반복 호출 | source만 top-level 제외·`CHANGELOG.md`; 인자 경로는 artifact 의미·history·비제로 전달. mock 외 실제 checker fixture 회귀 |
| R-003 | source 공개 전 이력 예외를 명확히 안내 | 준비 중 version heading, 공개 전후 entry | source 준비 entry는 미공개 후보임을 명시하고 공개 때 실제 release 링크·결과 기록. checker의 heading 통과를 게시 완료로 해석하지 않음 |
| R-004 | maintainer LF의 목적·범위 보존 | Windows checkout, payload export, attribute 제거 | root `* text=auto eol=lf`는 source용; 실제 Git attribute 조회와 기존 payload LF 회귀로 확인. artifact에 `.gitattributes` 추가 없음 |
| R-005 | locale별 검색 어휘를 한 곳에서 정의 | en/ko rg·grep, Owner만 교체 후 남은 `YYYY-MM-DD`, 예시·`{{` 토큰 | 두 명령이 같은 literal pattern을 참조; 각 sentinel과 일치. pattern·참조 누락은 source gate 실패 |
| R-006 | 검색의 기존 책임·한계 유지 | 적용 후 실제 문서, 숨김 지침, `.git`, 설명 guide·복사용 `_template`, TG 삭제 | 숨김 Markdown 확인·Git 내부 제외·guide Metadata 수동 확인 유지. `_template` 결과는 복사용으로 판정하고 실제 변경은 교체. 삭제 전에 검색 설정·명령 보존; 검색 0건을 완전 검증으로 설명하지 않음 |
| R-007 | 변경을 source/artifact 검증으로 연결 | source 전체 gate, 두 locale export와 artifact 자체 checker·tests | 기존 Windows/Linux CI·전체 unittest, en/ko export inventory·byte 검증 통과; 소비자 CLI에 maintainer 파일 의존성 없음 |

미선택 B안은 R-002~R-004·R-006의 안내와 수동 사본·검색 확인만 보강하는 대안입니다.
R-001·R-005의 새 gate와 추가 CLI 회귀를 제외하는 이 대안은 이번 승인·실행 범위가 아닙니다.

### 2.3 구성·책임과 실패 처리

**분석 스킬:** root `scripts/check-docs.py`의 무인자 maintainer 경로가 root와
`locales/ko`의 `.agents`·`.claude` 네 사본을 byte로 대조합니다. 고정된 분석 스킬
경로만 확인하고 기존 canonical checker의 실패를 그대로 전달합니다. missing·unsafe·
unreadable 경로를 같다고 간주하지 않습니다. artifact 인자 경로와 배포 checker에는
이 연결을 넣지 않습니다. 기존 locale pair 검사는 그대로 유지합니다.

**CLI:** 두 기존 wrapper 테스트를 보존하고 실제 checker fixture를 추가합니다.
top-level 제외가 `docs/locales/`까지 확대되지 않는 기존 회귀를 재사용합니다.
source·artifact 호출을 교차해 `HISTORY_PATH`·root·제외 범위가 다음 실행에 새지
않음을 확인합니다. CLI 옵션이나 canonical checker API를 새로 만들지 않습니다.

**LF·이력:** root [TEMPLATE_GUIDE.md](../../TEMPLATE_GUIDE.md) §3·§6과 필요한 maintainer checklist에
무인자/인자 경계·LF 목적·source 준비 entry 예외를 설명합니다. source의 준비 entry는
plain current-version heading에 미공개 후보 표시를 붙이고 공개 때 링크·완료 근거로
갱신합니다. 빈 `Unreleased` 절을 기본으로 만들지 않습니다. 적용 프로젝트의
`CHANGELOG_GUIDE.md`가 요구하는 공개 후 기록 원칙은 유지합니다. heading checker를
원격 release 존재 검사로 확장하지 않습니다.

**Placeholder:** 각 locale `TEMPLATE_GUIDE.md`의 교체 값 절에서
`template_placeholder_pattern`을 단일 literal shell 변수로 정의하고 rg·grep이
`"$template_placeholder_pattern"`을 사용합니다. 먼저 같은 shell에서 정의를 실행하도록
안내하며, TG 삭제 전 설정과 명령을 함께 보관합니다. 언어별 정본은 이 선언 하나입니다.
root guide는 locale 정본으로 연결해 축약된 별도 검색 어휘를 유지하지 않습니다.

기존 `scripts/check_locales.py`가 선언·두 참조와 en/ko의 주요 placeholder sentinel을
검증합니다. 정규식 전체 문자열을 검사 코드에 복제하거나 Markdown의 shell 코드를
실행하지 않습니다. sentinel은 `{{`·날짜·Owner 안내·간단 설명·예시를 독립적인 기대
입력으로 두어 pattern에서 토큰을 지우면 실패해야 합니다. 향후 공식 locale 확대 시
그 locale의 어휘·검증 사례는 별도로 합의합니다. 이는 skill fixture의 자연어 본문
동등성 검사로 확대하지 않습니다.

### 2.4 PR 순서와 검증 경계

| 단위 | 예상 범위 | 선행조건·완료 조건 |
|---|---|---|
| 설계 PR | 이 문서, PROJECT 인덱스·질문, TODO, PR #47 fixture 표기 인계 | A안 승인 기록·문서 gate·수동 리뷰·필수 CI·Origin/GitHub 통합 |
| A 구현 1 | source wrapper·`tests/test_check_docs.py`, maintainer CLI·LF·준비 이력 안내와 필요한 attribute 회귀 | 승인 설계 통합; R-001~R-004·R-007, 기존 docs/locale/full suite와 Windows/Linux exact head |
| A 구현 2 | en/ko 검색 선언·호출·보관 안내, source locale checker·회귀, root 검색 안내 연결 | 구현 1 통합; R-005~R-007, pattern drift 실패·전체 source gate·두 artifact export/check/tests |

각 구현 PR을 먼저 통합하고 다음 PR의 기준으로 사용합니다. 단위 2가 locale payload를
바꾸므로 실제 공개는 후속 release 후보·published gate에서 확인하며 이번 설계에서
version이나 게시 시점을 정하지 않습니다. B안의 문서 PR은 실행 계획에 포함하지 않습니다.
상세 체크박스와 각 실제 revision은 TODO만 소유합니다.

### 2.5 호환성·위험·rollback

- A는 source checkout의 drift를 새 실패로 만듭니다. 근거 없는 maintainer/ko 분기를
  허용하는 자동 예외는 두지 않으며, 의도적 분리가 필요하면 계약을 별도로 재설계합니다.
- shell 변수 선언 없이 fallback만 복사하면 빈 pattern으로 과도하게 검색할 수 있으므로
  같은 shell에서 선언부터 실행하는 순서와 TG 삭제 시 보관 항목을 안내·검증합니다.
- regex는 현행 rg/grep 공통 범위와 언어별 어휘를 보존합니다. 새 자동 placeholder lint나
  검색 결과 기반의 completion 판정은 추가하지 않습니다.
- source 안내·회귀 변경은 D-009를 보강하며 artifact 경계·비파괴 adoption을 유지합니다.
  locale 검색 안내 변경은 다음 artifact의 문서 byte 변경이며 기존 immutable asset에는 영향이 없습니다.
- 문제가 생기면 해당 source 검사·회귀와 연결된 안내를 함께 되돌립니다. 공개된 검색
  안내 수정은 새 release로 배포하고 기존 tag·asset을 교체하지 않습니다.

### 2.6 완료 조건

설계 PR은 승인 기록·문서 검증·exact head의 수동 리뷰와 필수 Windows/Linux CI를
확인하고 Origin/GitHub에 통합한 뒤 완료합니다. T-013은 두 구현 PR의 R-001~R-007
검증과 통합까지 확인해야 완료합니다. Status `Accepted`는 설계 승인 상태이며 구현이나
통합 완료를 뜻하지 않습니다. locale 안내의 공개는 별도 release 작업에서 확인합니다.

## 3. 변경 기록

- 2026-09-28: PR #47 version 2의 세 리뷰·Windows #52·Linux #37 통과와 Origin merge
  `ed3438f`·GitHub fast-forward를 확인했습니다. T-021은 A 유지로 통합됐고, 선택 권고인
  fixture 표의 `SHA256SUMS` 404 명시는 이번 문서 변경에 반영합니다. 기존 PR #28
  운영 권고를 확인하고 T-013 비교 설계를 준비했습니다. 검사 강화의 사용자 합의는 대기 중입니다.
- 2026-09-28: 사용자가 PR #48 version 1 head `7af3e86`의 T-013 A안을 선택했습니다.
  Status를 `Accepted`로 바꾸고 승인 범위를 D-012와 연결했습니다. source 검사·회귀
  구현 1 뒤 placeholder 정본·검증 구현 2를 진행하며 상세 검증·통합 상태는 TODO가 소유합니다.
