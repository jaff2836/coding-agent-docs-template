# 변경: 기존 저장소 적용을 위한 안전한 adoption 계약

## Metadata

- **Change ID:** `2026-09-18-existing-repository-adoption`
- **Status:** Draft
- **Originator:** Chae Sangwon
- **Source:** 2026-09-18 사용자 대화 — 대부분의 사용자는 기존 저장소에 템플릿을 적용할 가능성이 높으므로 기존 저장소를 주 consumer 시나리오로 검토하고 계약 변경 설계를 요청
- **Parent:** [제품 기준](../../00-PROJECT.md) D-002의 비파괴 installer와 D-004의 GitHub Releases transport
- **Decision:** PROJECT §8 D-006 (Proposed)
- **Approval:** 문제·설계 문서 작성 범위 승인. `adopt` CLI·manifest schema·자동 적용 여부는 미승인
- **Execution:** [전역 TODO](../../02-TODO.md)의 T-004

## 1. Intent

### 1.1 문제

현재 `install`은 새 대상에 안전하지만 기존 저장소에서 artifact 경로 하나라도 충돌하면 전체를 중단합니다. 일반 저장소는 대개 `README.md`, `.gitignore`, `LICENSE` 또는 기존 agent 지침을 이미 가지므로 실제 주 사용자는 별도 `export` 후 수동 비교·병합을 해야 합니다. 안전성은 높지만 이 경로가 보조 설명에 머물러 있고, 어떤 파일을 보존·병합·결정해야 하는지 기계적으로 설명하지 않습니다.

`jaff2836/claude-review-e2e`의 임시 clone에 `ko` artifact를 대조한 결과 `README.md`와 `.gitignore`가 충돌했고 나머지 파일을 추가한 혼합 tree에서 문서 검사와 checker 회귀는 통과했습니다. 그러나 일반화된 “없는 파일 전부 복사”는 프로젝트가 선택하지 않은 `LICENSE`를 추가할 수 있어 안전한 공식 계약이 아닙니다.

### 1.2 기대 결과

- 기존 저장소 적용을 제품의 주 adoption 시나리오로 설명합니다.
- verified artifact와 대상 tree를 비교해 사용자가 보존·병합·결정할 경로를 명시적인 계획으로 제공합니다.
- 기본 동작은 대상 저장소를 수정하지 않으며, 사람 또는 coding agent가 검토 가능한 staging tree와 report를 사용합니다.
- 새 저장소의 fail-closed `install`과 기존 release 검증 계약은 유지합니다.

### 1.3 범위와 비범위

제안 범위는 향후 `adopt` 명령, path별 adoption policy, report 형식, README 순서, 기존 저장소 consumer E2E와 rollback입니다. 이번 PR은 설계만 기록하며 installer·release manifest·schema를 구현하지 않습니다. 자동 overwrite, semantic Markdown merge, 자동 commit·push·PR, locale 자동 전환과 기존 프로젝트의 라이선스 선택은 비범위입니다.

### 1.4 제약

- checksum, exact version, repository identity와 installer 자기 검증은 `install`·`export`와 같아야 합니다.
- 대상 파일은 기본적으로 한 byte도 바꾸지 않습니다.
- `LICENSE`, 사용자 README, 기존 agent 정책과 프로젝트 결정은 자동 대체하지 않습니다.
- Python 표준 라이브러리만 사용하며 특정 Git hosting 또는 coding agent에 병합 실행을 의존하지 않습니다.
- v2.0.0의 `install`·`export` CLI는 호환 유지합니다.

### 1.5 미해결 질문

- `adoption-plan.json`을 장기 호환 공개 schema로 고정할지, 첫 판에는 CLI 내부 report로 둘지
- staging report에 coding agent용 병합 prompt를 포함할지
- path별 `copy`·`merge`·`decide` 정책을 source manifest에 둘지 release manifest에만 materialize할지

## 2. Spec

### 2.1 요구사항과 시나리오

| 요구사항 ID | 요구사항 | 상황·입력 | 관찰 가능한 결과 | 검증 방법 |
|---|---|---|---|---|
| R-001 | 기존 저장소가 주 adoption 흐름으로 안내됩니다. | 기존 코드·README가 있는 저장소 | README가 `adopt`/export 기반 검토 흐름을 새 프로젝트 설치보다 먼저 설명 | en/ko 문서 parity |
| R-002 | `adopt`는 release를 기존 installer와 동일하게 검증합니다. | latest 또는 exact version, locale, repo root, 빈 output | exact release의 installer·manifest·checksum·archive가 모두 일치해야 plan 생성 | fake release와 원격 HTTPS E2E |
| R-003 | 기본 adoption은 대상 tree를 수정하지 않습니다. | 충돌·symlink·기존 파일이 있는 저장소 | target before/after hash가 동일하고 staging tree와 report만 output에 생성 | failure injection, tree hash |
| R-004 | 각 artifact path의 처리를 설명합니다. | artifact와 target 비교 | report가 `missing`, `identical`, `merge`, `decision`, `blocked`를 구분하고 이유·source hash·target 상태를 기록 | deterministic report fixture |
| R-005 | 민감한 경로는 명시적 결정을 요구합니다. | `LICENSE`, README, `.gitignore`, 기존 `AGENTS.md`·프로젝트 문서 | 라이선스는 항상 `decision`, 사용자 소유 문서는 충돌 시 `merge`; 자동 대체 제안 없음 | path-policy fixtures |
| R-006 | 병합 후 기존 checker로 구조를 검증합니다. | 사람 또는 agent가 staging 결과를 반영 | `check-docs.py`, placeholder/adoption checklist와 tool loading probe가 통과하거나 구체적 미완료를 보고 | 기존 저장소 consumer E2E |
| R-007 | 새 저장소 계약과 rollback을 유지합니다. | 새 대상 또는 adoption 중단 | `install`은 기존 fail-closed 동작을 유지하고 staging output 삭제만으로 adoption을 취소 가능 | installer 회귀, output cleanup |

### 2.2 대안과 선택 이유

- **현재 `export` 문서만 유지:** 가장 작고 안전하지만 충돌 분류와 검토 결과가 비구조적이라 주 사용 흐름의 경험을 개선하지 못합니다.
- **기존 저장소에 없는 파일을 자동 추가:** 빠르지만 부분 적용 tree, adapter 의존성, 라이선스 오판을 만들 수 있어 기각합니다.
- **자동 overwrite 또는 3-way merge:** 문서 의미와 프로젝트 결정을 일반적으로 안전하게 병합할 수 없고 rollback 부담이 커 기각합니다.
- **검증된 staging tree + adoption plan:** target 무변경을 유지하면서 사람과 coding agent가 재현 가능한 입력으로 병합할 수 있어 권고안으로 선택합니다.

### 2.3 설계와 계약

제안 CLI는 다음 형태입니다.

```text
python3 installer.py adopt \
  --release-url https://github.com/jaff2836/coding-agent-docs-template/releases \
  --version <latest-or-semver> \
  --locale <bcp47-tag> \
  --repo-root <existing-repository> \
  --output <empty-staging-directory>
```

`adopt`는 release 검증 후 artifact 전체를 output에 materialize하고 대상 tree와 비교한 deterministic report를 함께 생성합니다. target에는 쓰지 않습니다. path policy는 최소 `copy`, `merge`, `decide`를 표현하며 target 상태와 결합해 R-004의 결과를 만듭니다. `LICENSE`는 존재 여부와 관계없이 `decide`, 프로젝트 README와 기존 지침·결정 문서는 충돌 시 `merge`입니다. 첫 구현에는 `--force`, `--apply-new`, 자동 commit을 넣지 않습니다.

README는 기존 저장소 흐름을 먼저 보여 주되 새 저장소의 `install`과 저수준 `export`를 계속 제공합니다. coding agent는 report와 staging tree를 입력으로 사용할 수 있지만, 구체적인 agent 제품은 계약에 포함하지 않습니다.

### 2.4 상위 설계에 미치는 영향

D-002의 비파괴 설치 원칙과 D-004의 release transport는 유지합니다. D-002에서 “기존 프로젝트는 export 후 수동 merge”로 둔 최소 계약을 구조화된 adoption plan으로 확장하며, 자동 update·overwrite 비범위는 바꾸지 않습니다. 승인되기 전에는 PROJECT §6 목표 구조에 올리지 않습니다.

### 2.5 위험·호환성·rollback

| 위험 | 영향 | 완화·rollback |
|---|---|---|
| report를 자동 병합 승인으로 오해 | 사용자 문서·정책 손상 | target 무변경, `decision` 분류, 명시적 검토 문구 |
| path policy가 새 파일 역할을 놓침 | 잘못된 copy/merge 안내 | 닫힌 manifest inventory와 policy 누락 release gate |
| report schema 조기 고정 | 다음 release 호환 부담 | schema 공개 여부를 승인 전 미해결 질문으로 유지 |
| 기존 CLI 회귀 | 새 프로젝트 설치 실패 | `install`·`export` 코드를 유지하고 공통 검증 계층만 재사용 |
| adoption 구현 결함 | 적용 지연 | 새 명령만 제거하면 기존 export/manual merge로 rollback 가능 |

### 2.6 완료 조건과 미해결 사항

설계 완료에는 미해결 질문과 CLI/report 계약에 대한 사용자 승인이 필요합니다. 구현 완료에는 source/release manifest, installer, docs와 negative fixture가 통과해야 합니다. 지원 완료에는 비어 있지 않은 실제 consumer 저장소에서 target 무변경 plan, 사람 또는 agent 병합, checker와 Claude·Codex·Cursor·OMP loading probe가 exact release head에서 통과해야 합니다.

## 3. 변경 기록

- 2026-09-18: 기존 저장소가 실제 주 consumer라는 사용자 판단과 `claude-review-e2e` 임시 clone 관찰을 바탕으로 Draft를 작성했습니다. installer 구현은 승인 전 시작하지 않습니다.
