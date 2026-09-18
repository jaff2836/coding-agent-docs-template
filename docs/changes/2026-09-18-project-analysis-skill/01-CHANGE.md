# 변경: 프로젝트 전체 분석을 번들 스킬로 이관

## Metadata

- **Change ID:** `2026-09-18-project-analysis-skill`
- **Status:** Accepted
- **Originator:** Chae Sangwon
- **Source:** 2026-09-18 사용자 대화 — 번들 스킬 설명을 README에 추가하고 프로젝트 전체 분석도 스킬로 옮겨 하나의 Origin PR로 게시하도록 요청
- **Parent:** [제품 기준](../../00-PROJECT.md) D-002의 locale별 skill 계약과 artifact inventory
- **Decision:** PROJECT §8 D-005
- **Approval:** Chae Sangwon, 2026-09-18 사용자 대화 — `project-analysis` skill 이관과 README 설명 추가 승인
- **Execution:** [전역 TODO](../../02-TODO.md)의 T-003

## 1. Intent

### 1.1 문제

전체 프로젝트 분석은 명시 요청에서만 사용하는 독립 절차지만 `docs/PROJECT_ANALYSIS.md`에만 있어, skill discovery를 사용하는 Claude Code·Codex·Cursor·OMP가 조건에 맞춰 직접 선택하기 어렵습니다. README도 현재 번들에 포함된 skill의 이름만 나열해 각 skill의 용도와 호출 경계를 빠르게 이해하기 어렵습니다.

### 1.2 기대 결과

- `project-analysis`를 `design`, `review-round`와 함께 공식 번들 skill로 제공합니다.
- 전체 분석 절차의 정본은 self-contained skill 하나가 소유하고 별도 문서와 중복하지 않습니다.
- 영어·한국어 README가 License 바로 위에서 세 skill의 용도와 호출 경계를 짧게 설명합니다.
- locale artifact와 checker가 새 skill의 두 경로·행동 계약을 검증합니다.

### 1.3 범위와 비범위

범위는 root maintainer 지침, `en`·`ko` skill source, artifact inventory, locale/check-docs 계약, README·가이드와 회귀 테스트입니다. 분석 방법론 자체의 확대, 일반 PR 리뷰 정책, installer의 기존 저장소 적용 동작, release 게시와 tag 생성은 포함하지 않습니다.

### 1.4 제약

- locale별 `.agents/skills/project-analysis/SKILL.md`와 `.claude/skills/project-analysis/SKILL.md`는 byte-identical해야 합니다.
- skill은 사용자의 명시적인 전체 분석 요청에서만 적용하며 기본 동작은 읽기 전용입니다.
- `review-round`와 달리 자연어의 명시 요청에서 자동 선택할 수 있으므로 `disable-model-invocation`이나 Codex 차단 설정을 추가하지 않습니다.
- 이미 고정된 `v2.0.0` tag와 draft artifact를 변경하지 않으며 다음 release의 source 변경으로 취급합니다.

### 1.5 미해결 질문

없습니다. 실제 도구별 loading probe와 release version 선택은 후속 release 작업에서 확인합니다.

## 2. Spec

### 2.1 요구사항과 시나리오

| 요구사항 ID | 요구사항 | 상황·입력 | 관찰 가능한 결과 | 검증 방법 |
|---|---|---|---|---|
| R-001 | 전체 분석 절차는 `project-analysis` skill 하나가 소유합니다. | 전체 프로젝트 분석을 명시적으로 요청 | skill이 근거 수집·위험 분류·도입 판단 절차 전체를 제공하고 `docs/PROJECT_ANALYSIS.md`는 artifact에 없음 | manifest inventory, 링크 검사 |
| R-002 | 일반 작업에서 전체 분석을 자동 확대하지 않습니다. | 기능 구현·버그 수정·질문·PR 리뷰 | skill description과 본문이 비적용 범위를 명시 | stable skill fixture |
| R-003 | 분석은 기본 읽기 전용이며 증거 상태를 구분합니다. | 분석 실행 | `verified`, `inference`, `unverified`를 구분하고 외부 변경은 별도 요청 없이는 수행하지 않음 | stable skill fixture, locale parity |
| R-004 | 네 도구가 locale별 동일 계약을 찾습니다. | `en` 또는 `ko` artifact 적용 | `.agents`와 `.claude` 복제본이 동일하고 manifest에 두 경로가 존재 | `check-locales.py`, `check-docs.py` |
| R-005 | README가 세 번들 skill을 간략히 설명합니다. | 사용자가 source 또는 적용 README 확인 | `design`, `project-analysis`, `review-round`의 목적과 호출 경계를 License 바로 위에서 확인 | root·artifact 문서 검사 |

### 2.2 대안과 선택 이유

- **기존 문서만 유지:** 중복 변경이 없지만 tool의 skill discovery를 활용하지 못하므로 기각했습니다.
- **문서와 얇은 adapter skill 병행:** 기존 `design`·`review-round`와 일관되지만 전체 분석 정본이 별도 문서에 남아 명시 요청마다 추가 로딩이 필요합니다.
- **self-contained skill로 이관:** 한 번의 조건부 로딩으로 전체 절차를 제공하고 문서·skill 이중 정본을 제거하므로 선택했습니다. 긴 skill 파일은 대가지만 전체 분석 요청에만 로드되어 상시 context 비용을 만들지 않습니다.

### 2.3 설계와 계약

`project-analysis`는 locale별 skill source가 prose 전체를 소유합니다. manifest의 skill marker와 세 fixture가 명시 요청, 읽기 전용 기본값, 증거 상태 구분을 고정합니다. artifact checker는 세 skill의 `.agents`/`.claude` 사본을 대조합니다. `AGENTS.md`는 적용 조건만 남기고 본문을 복제하지 않습니다.

### 2.4 상위 설계에 미치는 영향

D-002의 locale별 skill S2와 고정 tool path를 확장합니다. `docs/`에 있던 조건부 절차가 반드시 adapter 뒤에 있어야 한다는 기존 가이드 표현은, 별도 문서 정본이 없는 self-contained skill도 허용하도록 좁게 대체합니다.

### 2.5 위험·호환성·rollback

| 위험 | 영향 | 완화·rollback |
|---|---|---|
| tool이 일반 작업에서 긴 분석을 잘못 호출 | 요청 범위 확대 | description·fixture에 명시 요청과 비적용 범위를 고정; 문제 시 skill을 제거하고 기존 문서 경로를 복원 |
| locale skill 의미 drift | 분석 결과 불일치 | stable assertion·토큰, 두 경로 byte 대조, en/ko 구조 parity |
| 기존 `docs/PROJECT_ANALYSIS.md` 링크 단절 | artifact 검사 실패 | 모든 현재 참조를 skill 경로로 옮기고 문서 링크 검사 실행 |
| v2.0.0 artifact와 main의 inventory 차이 | release 혼동 | v2.0.0 tag·asset은 불변으로 유지하고 다음 release에서만 새 inventory 게시 |

### 2.6 완료 조건과 미해결 사항

브랜치 구현 완료는 root 문서 검사, stable locale 검사, checker 회귀와 전체 테스트, en/ko export artifact 검사 통과입니다. Origin 통합은 PR merge 뒤 별도 확인하며, 실제 도구 loading과 release 지원 완료는 다음 release consumer probe에서 확인합니다.

## 3. 변경 기록

- 2026-09-18: 사용자 승인에 따라 `PROJECT_ANALYSIS.md`를 self-contained `project-analysis` skill로 이관하고 README의 번들 skill 설명을 같은 변경으로 묶었습니다.
