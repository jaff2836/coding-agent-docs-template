# 변경: 문서 소유권과 changelog 안내

## Metadata

- **Change ID:** `2026-09-22-documentation-ownership`
- **Status:** Accepted
- **Originator:** Chae Sangwon
- **Source:** 2026-09-22 사용자 대화 — T-010의 `project-analysis` Metadata 전체 제거, maintainer guide 축약과 `docs/` changelog 안내 제안
- **Parent:** [제품 기준](../../00-PROJECT.md)과 D-003 locale artifact 구조
- **Decision:** [PROJECT D-009](../../00-PROJECT.md#8-decisions)
- **Approval:** Chae Sangwon, 2026-09-22 사용자 대화 — PR #27 merge 뒤 세 범위를 `v2.3.0`으로 함께 진행하고 Origin PR 게시 승인
- **Execution:** [전역 TODO](../../02-TODO.md)의 T-010

## 1. Intent

### 1.1 문제

`project-analysis` skill은 독립 실행 절차인데 프로젝트별 `Owner`와 검토일
placeholder를 포함해 적용 직후 불필요한 수정과 두 사본 동기화를 요구합니다.
또한 root maintainer guide가 locale artifact guide의 큰 부분을 수동 복제해
source 운영 규칙과 적용 프로젝트 규칙의 소유권이 불명확합니다. 적용
artifact에는 README·TODO·릴리스 이력의 경계를 설명하는 changelog 안내도
없습니다.

### 1.2 기대 결과

- 독립 skill에서 프로젝트별 Metadata를 제거하고 행동 계약은 유지합니다.
- locale guide를 artifact 정본으로 삼고 root guide는 maintainer addendum으로
  줄입니다.
- 각 locale artifact에 실제 프로젝트 changelog를 덮어쓰지 않는
  `docs/CHANGELOG_GUIDE.md`를 제공합니다.
- source와 artifact checker가 각 영역의 정본 릴리스 이력을 검증합니다.

### 1.3 범위와 비범위

범위는 source root와 en·ko skill 사본, locale 안내·README·AGENTS, manifest
inventory와 adoption policy, root maintainer guide·CHANGELOG, 문서 checker와
회귀 테스트, `v2.3.0` 문서 provenance입니다.

적용 프로젝트의 실제 `CHANGELOG.md` 자동 생성·변환, 기존 changelog 형식
강제, 새 locale, 특정 CI runner 설정과 release 공개는 이번 branch 구현
범위가 아닙니다. release 공개는 Origin 통합 뒤 별도 gate로 진행합니다.

### 1.4 제약

- 기존 저장소의 프로젝트 소유 문서와 결정을 보존합니다.
- artifact inventory는 manifest에 닫혀 있고 en·ko가 같은 경로를 제공합니다.
- `.agents`와 `.claude`의 locale별 skill 사본은 byte-identical합니다.
- README는 현재 동작, changelog는 공개 완료 이력, TODO·PLAN은 미래 작업을
  소유합니다.
- 비어 있는 `Unreleased` 절을 기본으로 만들지 않습니다.
- production dependency와 특정 CI runner 설정을 추가하지 않습니다.

## 2. Spec

### 2.1 요구사항

| ID | 요구사항 | 검증 |
| -- | -------- | ---- |
| R-001 | source root 두 사본과 locale 네 사본의 `project-analysis`에서 `Metadata` 절 전체를 제거하고 각 사본 계약을 유지합니다. | skill equality·fixture·placeholder 검색 |
| R-002 | locale `TEMPLATE_GUIDE.md`·`DOCS_GUIDE.md`가 artifact 적용 안내의 정본이고 root guide는 maintainer 전용 addendum입니다. | 링크·절 참조·중복 범위 검토 |
| R-003 | en·ko에 `docs/CHANGELOG_GUIDE.md`를 추가하고 manifest inventory와 `copy` adoption policy에 등록합니다. | stable locale·export inventory 검사 |
| R-004 | guide는 README=현재, 선택형 root CHANGELOG=공개 이력, TODO/PLAN=미래, guide Metadata=template provenance 경계를 정의하고 기존 형식을 보존합니다. | locale parity·artifact 문서 검사 |
| R-005 | root checker는 root `CHANGELOG.md`, artifact checker는 `docs/TEMPLATE_GUIDE.md`의 표시된 이력을 읽으며 둘 다 현재 version heading을 검증합니다. | alternate-path·linked-heading 회귀 테스트 |
| R-006 | 새 artifact 문서 때문에 공개 payload가 늘어나므로 `v2.3.0` minor로 기록하며 기존 저장소에는 자동 changelog 생성·덮어쓰기를 하지 않습니다. | package manifest·adopt policy·docs 검토 |

### 2.2 선택한 설계

canonical checker의 기본 `HISTORY_PATH`는 artifact 호환을 위해
`docs/TEMPLATE_GUIDE.md`로 유지합니다. source wrapper의 인자 없는 maintainer
실행만 `CHANGELOG.md`를 지정하고, `--root` 등 artifact CLI 경로는 기본값을
복원합니다. checker는 표시된 section에서 plain 또는 linked Markdown version
heading을 허용하되 fenced·comment decoy는 계속 제외합니다.

locale changelog guide는 artifact에 항상 포함하지만 실제 root changelog는
project-owned optional 문서로 둡니다. adoption은 guide를 `copy`하고 기존
changelog에는 손대지 않습니다.

### 2.3 대안

- **root·locale guide를 계속 수동 복제:** 기존 구조를 유지하지만 drift 원인을
  남기므로 기각합니다.
- **root guide에서 locale guide를 생성:** 중복은 줄지만 단순 Markdown 저장소에
  새 생성 계층과 번역 결합을 추가하므로 기각합니다.
- **changelog guide를 root에만 둠:** release artifact 사용자가 안내를 받지
  못하므로 기각합니다.
- **artifact가 root `CHANGELOG.md`를 자동 생성:** 새 프로젝트에는 편하지만 기존
  release note와 충돌하고 비파괴 adoption 경계를 어기므로 기각합니다.

### 2.4 호환성과 rollback

기존 artifact 경로는 유지되고 안내 문서 하나만 추가됩니다. `project-analysis`
행동 계약과 marker는 바뀌지 않습니다. 문제가 생기면 새 guide를 inventory에서
제거하고 checker wrapper를 artifact 기본값으로 되돌릴 수 있으며, 기존
프로젝트 파일을 되돌릴 migration은 없습니다.

### 2.5 완료 조건

- branch 구현: source docs·tests·stable locale 검사, en·ko export와 artifact
  자체 검사·tests를 통과합니다.
- 통합: Origin PR이 merge되고 GitHub `main`이 fast-forward됩니다.
- 공개: clean exact commit으로 `v2.3.0` candidate·published gate와 consumer
  경로를 확인합니다.

branch 구현, Origin 통합과 공개 완료를 별도 상태로 기록합니다. 현재 미해결
계약 질문은 없습니다.

## 3. 변경 기록

- 2026-09-22: 사용자가 T-010의 두 정책과 `docs/` changelog 안내를 함께
  채택하고 `v2.3.0` 구현·Origin PR 진행을 승인했습니다.
- 2026-09-22: PR #28 version 1 리뷰 후 source root 두 skill 사본까지 R-001
  범위를 명확히 해 Metadata를 제거하고, README 정본 안내와 changelog guide의
  placeholder 어휘를 보완했습니다. version 2 재리뷰에는 새 finding이 없었습니다.
- 2026-09-22: PR #28 merge `5066d821084545554588182f5250cc9dea12e444`을
  Origin·GitHub `main`에 동기화하고 같은 exact source의 annotated tag와 검증한
  5개 asset을 immutable Latest `v2.3.0`으로 공개했습니다. candidate와
  `published --base-version 2.2.0` 검증이 통과했습니다.
