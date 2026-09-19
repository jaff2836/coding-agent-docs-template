# 변경 명세: 기존 저장소 적용을 위한 안전한 adoption 계약

## Metadata

- **Change ID:** `2026-09-18-existing-repository-adoption`
- **Status:** Accepted
- **Intent:** [01-INTENT.md](./01-INTENT.md)
- **Parent:** [제품 기준](../../00-PROJECT.md) D-002·D-004, [다국어 템플릿 SPEC](../2026-09-09-multilingual-template/02-SPEC.md) §3.3·§3.4
- **Decision:** D-006
- **Approval:** Chae Sangwon, 2026-09-19 사용자 대화 — 결정 1~7 권고안 승인
- **Execution:** [03-PLAN.md](./03-PLAN.md)

## 1. 요구사항과 시나리오

| 요구사항 ID | 요구사항 | 상황·입력 | 관찰 가능한 결과 | 검증 방법 |
|---|---|---|---|---|
| R-001 | 기존 저장소가 주 adoption 흐름으로 안내됩니다. | 기존 코드·README가 있는 저장소 | root landing README와 en·ko 적용 가이드가 `adopt` 기반 검토 흐름을 새 프로젝트 `install`보다 먼저 설명하고, `install`·`export`도 계속 안내합니다. | en/ko 문서 parity, docs·locale checker |
| R-002 | `adopt`는 release를 기존 installer와 동일하게 검증합니다. | `latest` 또는 exact version, locale, repo root, 빈 output | exact release의 installer·manifest·checksum·archive가 모두 일치해야 plan을 만들고, 하나라도 다르면 output 없이 실패합니다. | fake release 성공·실패 테스트, 원격 HTTPS E2E |
| R-003 | adoption은 대상 tree를 수정하지 않습니다. | 충돌·symlink·기존 파일이 있는 저장소, 검증 실패와 output 게시 실패 | 대상의 before/after 경로·mode·byte가 같습니다. output이 대상 안이거나 대상이 output 안이면 거부합니다. | tree snapshot 비교, failure injection |
| R-004 | 각 artifact 경로의 처리를 결정적으로 설명합니다. | artifact와 대상 비교 | report가 경로마다 policy, `missing`·`identical`·`merge`·`decision`·`blocked` 중 하나의 status, 대상 상태, artifact·대상 hash와 이유를 기록합니다. 같은 입력이면 byte가 같습니다. | report fixture, 두 번 실행 byte 비교 |
| R-005 | 민감한 경로는 명시적 결정을 요구합니다. | `LICENSE`, 선택 파일, 사용자 README·지침·결정 문서 | `decide` 경로는 대상 상태와 무관하게 `decision`, 프로젝트 소유 문서는 충돌 시 기존 내용을 보존하는 `merge`입니다. 자동 대체를 제안하지 않습니다. | policy fixture |
| R-006 | 병합 후 기존 checker로 구조를 검증합니다. | 사람 또는 agent가 staging 결과를 반영 | `check-docs.py`, placeholder 검색, Template Adoption Checklist와 도구 로딩 probe가 통과하거나 구체적 미완료를 보고합니다. | 기존 저장소 consumer E2E |
| R-007 | 새 저장소 계약과 rollback을 유지합니다. | 새 대상, 충돌 대상, adoption 중단 | `install`·`export`의 인자와 fail-closed 동작은 유지하고 충돌 오류는 `adopt`를 안내합니다. adoption 취소는 output 삭제뿐입니다. | installer 회귀 테스트 |
| R-008 | 모든 artifact 경로에 policy가 정확히 하나 있습니다. | inventory에 경로 추가·삭제, policy 누락·잉여·오타 | locale checker와 packager가 실패하고 release를 만들지 않습니다. release manifest의 각 member가 policy를 가집니다. | locale checker·packager negative 테스트 |
| R-009 | report가 실험적 형식임을 드러냅니다. | report 소비자 | report가 `format_version`과 `stability: experimental`을 포함하고 문서가 호환 비보장을 명시합니다. 절대 경로·시각을 기록하지 않습니다. | report fixture, 문서 검사 |

## 2. 대안과 선택 이유

### 2.1 해결 범위

- **현재 `export` 문서만 유지 또는 문서 계약만 보강:** 가장 작고 안전하며 PR #28에서도 문서만으로 `LICENSE`를 올바르게 제외했습니다. 그러나 충돌 분류가 비구조적이고 선택 파일 판단이 리뷰에서야 드러나 Intent의 문제를 해결하지 못해 기각했습니다.
- **기존 저장소에 없는 파일을 자동 추가:** 빠르지만 부분 적용 tree, adapter 의존성, 라이선스 오판을 만들 수 있어 기각합니다.
- **자동 overwrite 또는 3-way merge:** 문서 의미와 프로젝트 결정을 일반적으로 안전하게 병합할 수 없고 rollback 부담이 커 기각합니다.
- **검증된 staging tree + adoption report:** 대상 무변경을 유지하면서 사람과 coding agent가 재현 가능한 입력으로 병합할 수 있어 채택했습니다.

### 2.2 Policy 위치

- **`installer.py` 내부 표:** release manifest schema를 유지하지만 inventory와 policy의 정본이 둘이 되고 파일 추가 때 두 곳을 고쳐야 해 기각했습니다.
- **`locales/manifest.json` 정본 + release manifest materialization:** 닫힌 inventory 옆에서 누락을 즉시 검사하고, 이미 `SHA256SUMS`로 결합된 release manifest가 installer에 policy를 전달해 채택했습니다.

### 2.3 Report 형식

- **공개 JSON schema와 호환 보장:** 소비자가 아직 E2E 저장소 하나뿐이라 필드를 고정할 근거가 부족해 기각했습니다.
- **Markdown report만:** 사람이 읽기 쉽지만 결정적 검증과 agent 입력에 불리해 기각했습니다.
- **실험적 JSON + stdout 요약:** 결정적 fixture와 agent 입력을 지원하면서 다음 minor release에서 형식을 조정할 수 있어 채택했습니다.

### 2.4 Agent용 병합 prompt

- **locale별 병합 prompt 포함:** 병합 절차가 적용 가이드와 prompt 두 곳의 en·ko 정본으로 갈라지고 특정 agent 비의존 제약과 충돌해 기각했습니다.
- **경로별 이유와 적용 가이드 참조만 제공:** 병합 절차의 정본을 artifact 안 `docs/TEMPLATE_GUIDE.md` §2에 유지해 채택했습니다.

### 2.5 `decide` 범위

- **`LICENSE`만:** 규칙이 가장 작지만 PR #28에서 선택 파일 유지·삭제가 실제 판단 대상이었으므로 기각했습니다.
- **`LICENSE`와 선택 파일 세 개:** 적용 가이드가 사용 여부에 따라 삭제하라고 안내하는 파일을 명시적 결정으로 드러내 채택했습니다.

### 2.6 완료 기준과 E2E

- **`main` 통합까지만 완료:** 원격 release에서 `adopt`를 검증하지 못하고 이미 병합된 `project-analysis` skill도 계속 미공개로 남아 기각했습니다.
- **PR #28을 닫고 `adopt`로 재적용:** 원격 consumer 저장소를 다시 변경해야 하고 기존 수동 병합의 비교 기준을 잃어 기각했습니다.
- **`v2.1.0` 게시와 적용 전 baseline의 읽기 전용 E2E:** 사람이 이미 수행한 병합 결과를 정답지로 report 분류를 대조할 수 있어 채택했습니다.

## 3. 설계와 계약

### 3.1 CLI

```text
python3 installer.py adopt \
  --release-url https://github.com/jaff2836/coding-agent-docs-template/releases \
  --version <latest-or-semver> \
  --locale <bcp47-tag> \
  --repo-root <existing-repository> \
  --output <empty-staging-directory>
```

- release URL·version·locale 검증과 artifact 다운로드는 `export`와 같은 함수를 사용합니다.
- `--repo-root`는 존재하는 실제 디렉터리여야 하며 symlink이면 거부합니다. 새 프로젝트는 `install`을 사용합니다.
- `--output`은 `export`와 같이 비어 있거나 존재하지 않는 non-symlink 디렉터리이고 부모가 존재해야 합니다. 해석한 output이 repo root와 같거나 그 안에 있거나, repo root가 output 안에 있으면 거부합니다.
- `--force`, 누락 파일 적용 옵션, 자동 commit은 제공하지 않습니다.
- 성공하면 종료 코드 0과 stdout 요약을 출력합니다. `blocked`가 있어도 plan 생성은 성공입니다. 검증·입력·게시 오류는 종료 코드 1이며 output을 남기지 않습니다.

### 3.2 Adoption policy

`locales/manifest.json`의 `artifact.adoption_policy`는 inventory의 모든 output 경로를 key로, `copy`·`merge`·`decide` 중 하나를 값으로 가집니다. key 집합은 `common_paths`와 `localized_paths`의 합집합과 정확히 같아야 합니다.

| Policy | 의미 | 초기 대상 |
|---|---|---|
| `decide` | 대상 상태와 무관하게 프로젝트가 채택 여부를 결정 | `LICENSE`, `docs/10-EXTENSION.md`, `.cursor/BUGBOT.md`, `.omp/WATCHDOG.md` |
| `merge` | 프로젝트 소유. 충돌 시 기존 내용을 보존하고 템플릿 절을 병합 | `README.md`, `.gitignore`, `AGENTS.md`, `CLAUDE.md`, `docs/00-PROJECT.md`, `docs/02-TODO.md`, `docs/REVIEW.md`, `docs/REVIEW_ROUND.md`, `docs/CI.md` |
| `copy` | 템플릿 소유 절차·도구. 충돌 시 artifact 판을 기준으로 의도한 프로젝트 수정만 다시 적용 | `.agents/`·`.claude/` skill 사본과 `openai.yaml`, `docs/01-DESIGN.md`, `docs/DOCS_GUIDE.md`, `docs/TEMPLATE_GUIDE.md`, `docs/changes/_template/` 네 양식, `scripts/check-docs.py`, `tests/test_check_docs.py` |

packager는 이 값을 release manifest의 각 member record에 `policy`로 복사합니다. 이에 따라 release manifest는 `schema_version` 2가 되고 member record key는 `path`, `sha256`, `bytes`, `mode`, `timestamp`, `policy`입니다. `schemas/release-manifest.schema.json`, packager와 installer 검증을 함께 갱신합니다. 나머지 필드와 transport는 D-004 계약 그대로입니다.

### 3.3 분류

대상 저장소 전체를 순회하지 않고 artifact 경로만 검사합니다. 검사는 `lstat`·디렉터리 목록·읽기만 사용하고 대상에 쓰지 않습니다.

1. 경로의 각 상위 구성요소가 symlink, 디렉터리가 아닌 항목, 또는 대소문자만 다른 기존 이름이면 `blocked`입니다.
2. 대상 경로가 symlink, 일반 파일이 아닌 항목, 대소문자만 다른 기존 이름, 읽을 수 없는 파일이면 `blocked`입니다.
3. policy가 `decide`이면 대상 상태와 무관하게 `decision`입니다.
4. 대상이 없으면 `missing`, byte가 같으면 `identical`, 다르면 `merge`입니다.

`blocked`가 policy보다 우선합니다. 대상 상태 값은 `absent`, `file`, `symlink`, `special`, `unreadable`, `parent-symlink`, `parent-not-directory`, `case-variant`입니다.

### 3.4 Adoption report

output은 다음 두 항목만 가집니다. 임시 디렉터리에서 모두 만든 뒤 원자적으로 게시합니다.

```text
<output>/artifact/            # export와 같은 검증된 artifact tree
<output>/adoption-plan.json   # 아래 report
```

```json
{
  "format": "coding-agent-docs-template/adoption-plan",
  "format_version": 1,
  "stability": "experimental",
  "release": {"repository": "OWNER/NAME", "version": "2.1.0", "source_commit": "<40 hex>", "locale": "ko"},
  "guide": "artifact/docs/TEMPLATE_GUIDE.md §2",
  "summary": {"missing": 0, "identical": 0, "merge": 0, "decision": 0, "blocked": 0},
  "paths": [
    {"path": "README.md", "policy": "merge", "status": "merge", "target": "file",
     "artifact_sha256": "<64 hex>", "target_sha256": "<64 hex or null>", "reason": "..."}
  ]
}
```

- `paths`는 path 순으로 정렬하며 JSON은 key 정렬, UTF-8, LF, 마지막 개행으로 씁니다. 대상 절대 경로, 실행 시각, 사용자 이름은 기록하지 않습니다.
- `target_sha256`은 대상이 읽을 수 있는 일반 파일일 때만 값을 가집니다.
- `reason`은 policy·status·대상 상태로 정해지는 고정 영어 문장입니다. locale별 prompt나 병합 지시문은 넣지 않습니다.
- `stability: experimental`인 동안 필드는 minor release에서 바뀔 수 있습니다. 호환을 보장하는 schema 파일은 공개하지 않습니다.
- stdout은 release·locale, status별 개수, `identical`이 아닌 경로 목록과 대상이 변경되지 않았다는 문장을 출력합니다.

### 3.5 문서와 기존 명령

- root landing README(`README.md`, `README.ko.md`)와 en·ko `docs/TEMPLATE_GUIDE.md` §2는 기존 저장소의 `adopt` 흐름을 먼저, 새 프로젝트 `install`과 저수준 `export`를 그다음에 설명합니다.
- `install`의 충돌 오류는 `adopt`를 안내합니다. 인자와 동작은 바꾸지 않습니다.
- 적용 가이드는 report의 status별 처리와 `decide` 파일의 결정 기준을 설명합니다. 이것이 병합 절차의 유일한 정본입니다.

## 4. 상위 설계에 미치는 영향

- D-002: 비파괴 설치 원칙은 유지하고, “기존 프로젝트는 export 후 수동 merge”로 둔 최소 계약을 검증된 staging과 구조화된 report로 확장합니다. 자동 update·overwrite 비범위는 바꾸지 않습니다. [다국어 템플릿 SPEC](../2026-09-09-multilingual-template/02-SPEC.md) §3.3의 release manifest에 member `policy`를 추가하고 §3.4 installer에 `adopt`를 추가합니다.
- D-004: GitHub Releases transport, `latest`→exact 선택, redirect 경계는 그대로입니다. release manifest `schema_version`만 1에서 2로 올립니다.
- PROJECT §6 목표 구조에 adoption 흐름을 추가하고 구현·게시 후 §5 현재 구조로 옮깁니다.

## 5. 위험·호환성·rollback

| 위험 | 영향 | 완화·rollback |
|---|---|---|
| report를 자동 병합 승인으로 오해 | 사용자 문서·정책 손상 | 대상 무변경, `decision` 분류, 명시적 검토 문구 |
| policy가 새 파일 역할을 놓침 | 잘못된 copy/merge 안내 | 닫힌 inventory와 policy 누락 release gate(R-008) |
| release manifest schema 2 | 외부 manifest reader 영향 | installer는 자기 hash를 exact manifest와 대조하므로 `v2.0.0` installer는 원래 다른 version을 설치하지 못합니다. release note에 schema 변경을 기록하고 공개된 `v2.0.0` asset은 바꾸지 않습니다. |
| report 형식 조기 고정 | 다음 release 호환 부담 | `stability: experimental`, schema 파일 미공개 |
| output을 대상 안에 두어 대상 변경 | R-003 위반 | output·repo root 포함 관계 거부 |
| 기존 CLI 회귀 | 새 프로젝트 설치 실패 | `install`·`export` 인자 유지, 공통 검증 계층 재사용, 기존 회귀 테스트 |
| adoption 구현 결함 | 적용 지연 | 새 명령과 policy만 제거한 patch release로 기존 export·수동 병합에 rollback. 공개 release는 교체하지 않습니다. |

`v2.1.0`은 `adopt` 추가와 이미 `main`에 통합된 `project-analysis` skill, T-005 checker 강화를 포함하는 minor release입니다. tag·release 게시는 D-004 절차를 따르며 별도 사용자 위임이 필요합니다.

## 6. 완료 조건과 미해결 사항

- **설계 완료:** 이 INTENT·SPEC·PLAN과 PROJECT D-006, 전역 TODO가 Origin `main`에 통합된 상태
- **구현 완료:** PLAN W-001~W-003이 각 PR로 Origin `main`에 통합되고 전체 unittest, docs·stable locale checker, en·ko export의 checker와 결정적 package가 통과한 상태
- **공개 완료:** `v2.1.0` immutable GitHub Release의 latest·exact `adopt`·`install`·`export`가 원격 HTTPS에서 통과한 상태
- **지원 완료:** `jaff2836/claude-review-e2e`의 적용 전 baseline `4d9c0dfa9d39276e871592e350b772bba1863549` 임시 clone에서 대상 무변경 plan을 만들고, report 분류가 PR #28의 수동 병합 결과(`README.md`·`.gitignore` 병합, `LICENSE` 제외, 선택 파일 결정)와 일치하며, report에 따라 반영한 tree가 checker와 Claude·Codex·Cursor·OMP 로딩 probe를 통과한 상태

남은 미해결 질문은 없습니다.

## 7. 명세 변경 기록

- 2026-09-18: 합본형 Draft(`5eefc11`의 `01-CHANGE.md` Spec 절)에 R-001~R-007과 권고 설계를 작성했습니다.
- 2026-09-19: 사용자 결정에 따라 분리형으로 전환하고 policy 정본·release manifest schema 2(R-008), 실험적 report(R-009), output 위치 제약(R-003), 완료 기준과 consumer E2E를 확정해 Accepted로 기록했습니다.
