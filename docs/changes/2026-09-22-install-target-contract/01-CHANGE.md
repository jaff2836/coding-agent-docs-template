# 변경: 새 프로젝트 install 대상 계약 정합화

## Metadata

- **Change ID:** `2026-09-22-install-target-contract`
- **Status:** Draft
- **Originator:** Chae Sangwon
- **Source:** 2026-09-22 사용자 제공 전체 프로젝트 리뷰 F-003과 후속 작업 정리 요청. 분석 기준은 `5066d821084545554588182f5250cc9dea12e444`입니다.
- **Parent:** [제품 기준](../../00-PROJECT.md) D-002·D-006과 [기존 저장소 adoption SPEC](../2026-09-18-existing-repository-adoption/02-SPEC.md)
- **Decision:** 미정 — 사용자 합의 뒤 필요한 경우 PROJECT §8에 등재
- **Approval:** 미승인 — 권고안과 대안을 기록했으며 구현 승인이 아닙니다.
- **Execution:** [전역 TODO](../../02-TODO.md)의 T-016

## 1. Intent

### 1.1 문제

root README와 locale 적용 가이드는 새 프로젝트의 `install` 대상이 존재하지 않거나
비어 있어야 한다고 설명합니다. 구현은 artifact member와 겹치는 경로만 충돌로
검사하므로, `existing.txt`처럼 겹치지 않는 파일이 있는 디렉터리에는 기존 파일을
보존하면서 template 파일을 추가합니다. 기존 저장소는 읽기 전용 `adopt`를 먼저
사용한다는 제품 경계와 실제 `install` 동작이 일치하지 않습니다.

### 1.2 기대 결과

`install`이 허용하는 대상 상태를 하나의 공개 계약으로 확정하고 코드·영문 및
한국어 문서·테스트를 일치시킵니다. 거부하는 경우에는 쓰기 전에 중단하고 기존
저장소용 `adopt`를 안내합니다.

### 1.3 범위와 비범위

범위는 `installer.py install`의 대상 preflight, 오류 진단, root·locale 적용 문서와
회귀 테스트입니다. `adopt`·`export`의 공개 계약, 기존 저장소 자동 병합·파일 추가,
과거 immutable release 변경은 포함하지 않습니다.

### 1.4 제약

- 기존 대상의 경로·내용·mode를 실패 전후 동일하게 보존합니다.
- symlink와 비정규 경로 거부, archive 검증과 원자적 rollback을 약화하지 않습니다.
- 새 production dependency나 특정 CI runner 설정을 추가하지 않습니다.
- 공개된 `v2.3.0` asset은 변경하지 않고 이후 release에서만 수정합니다.

### 1.5 미해결 질문

`install`을 존재하지 않거나 빈 대상에만 제한할지, artifact path와 겹치지 않는
기존 파일을 허용할지 사용자 결정이 필요합니다. 현재 문서와 D-006의 역할 분리는
전자(A안)를 지지합니다.

## 2. Spec

### 2.1 요구사항과 시나리오

| 요구사항 ID | 요구사항 | 상황·입력 | 관찰 가능한 결과 | 검증 방법 |
|---|---|---|---|---|
| R-001 | 선택한 대상 계약을 쓰기 전에 검사합니다. | 존재하지 않는 대상, 빈 디렉터리, 겹치지 않는 `existing.txt`가 있는 디렉터리 | A안이면 앞의 두 경우만 성공하고 비어 있지 않은 대상은 아무것도 쓰지 않습니다. B안이면 현재처럼 artifact path 충돌만 거부합니다. | CLI·함수 회귀와 before/after tree snapshot |
| R-002 | 거부 진단이 안전한 다음 경로를 안내합니다. | 비어 있지 않은 기존 저장소에 `install` | 오류가 `adopt` 또는 빈 대상 사용을 안내합니다. | stderr assertion |
| R-003 | 기존 안전 경계를 유지합니다. | symlink root·member 충돌·쓰기 중 실패, `adopt`·`export` | 기존 fail-closed·rollback·대상 불변 계약이 유지됩니다. | 기존 installer 전체 회귀 |
| R-004 | 양 locale 문서와 CLI가 같은 계약을 설명합니다. | README와 en·ko 적용 가이드에서 새 프로젝트 설치를 확인 | 허용·거부 대상과 기존 저장소 흐름이 구현과 일치합니다. | docs·stable locale 검사 |

### 2.2 대안과 선택 이유

- **A안 — 비어 있지 않은 대상을 전부 거부(권고):** README와 locale guide의 현재
  약속, 새 프로젝트=`install`·기존 저장소=`adopt`라는 D-006 경계를 코드로
  강제합니다. 겹치지 않는 기존 파일이 있는 대상에서 이전에는 성공하던 호출이
  실패하는 호환성 비용이 있지만, 문서만 보고 기대한 안전성을 복구합니다.
- **B안 — artifact path 충돌만 거부:** 현재 구현을 유지하고 문서를 완화합니다.
  부분 설치가 편하지만 기존 저장소에 자동으로 파일을 추가하지 않는 adoption
  경계가 흐려지고 `install`과 `adopt`의 역할이 겹칩니다.
- **변경하지 않음:** 문서와 구현의 모순을 유지하므로 기각합니다.

### 2.3 설계와 계약

A안을 선택하면 release와 archive 검증을 마친 뒤 첫 파일을 쓰기 전에 대상 root가
존재하지 않거나 비어 있는 실제 디렉터리인지 검사합니다. 비어 있지 않거나 읽을 수
없으면 fail-closed하고 `adopt`를 안내합니다. 기존 member별 충돌 검사는 race와
방어 심도를 위해 유지하며 쓰기·rollback 경로는 바꾸지 않습니다.

B안을 선택하면 코드는 유지하되 root·en·ko 문서가 비어 있지 않은 대상도 artifact
경로가 겹치지 않으면 파일을 추가한다는 사실과, 기존 저장소에는 여전히 `adopt`를
권장하는 이유를 명시해야 합니다.

### 2.4 상위 설계에 미치는 영향

A안은 D-002의 비파괴 installer와 D-006의 새 프로젝트 `install`·기존 저장소
`adopt` 역할을 명확히 하며 대체하지 않습니다. B안은 D-006의 역할 경계를
완화하므로 승인 시 PROJECT 결정 근거도 함께 갱신해야 합니다.

### 2.5 위험·호환성·rollback

| 위험 | 영향 | 완화·rollback |
|---|---|---|
| 기존 사용자가 겹치지 않는 파일이 있는 대상에 `install`을 사용 | A안 적용 뒤 실패 | 오류에서 `adopt` 또는 빈 대상 경로를 안내하고 기존 tree는 보존 |
| emptiness 검사와 실제 쓰기 사이의 경합 | 검사 뒤 외부 파일 생성 | member별 `xb`와 충돌 검사를 유지해 overwrite 없이 rollback |
| 문서만 수정해 구현 모순이 재발 | 사용자 기대와 실제 동작 불일치 | 두 경계 조건을 CLI 회귀로 고정하고 locale 문서 검사를 함께 실행 |
| 선택이 잘못됨 | 새 프로젝트 또는 기존 저장소 흐름 불편 | 공개 전에는 Draft를 폐기할 수 있고, 공개 뒤에는 후속 release에서 계약과 문서를 함께 변경 |

### 2.6 완료 조건과 미해결 사항

사용자가 A안 또는 B안을 승인한 뒤 구현합니다. branch 완료는 관련 installer 회귀,
전체 unittest, root docs, stable locale, en·ko export·artifact 검사와
`git diff --check` 통과입니다. 통합과 release 포함 여부는 구현 시 별도로 정하며,
공개된 `v2.3.0`의 완료 근거를 소급 변경하지 않습니다.

## 3. 변경 기록

- 2026-09-22: 전체 프로젝트 리뷰 F-003을 재현하고 공개 계약 선택이 필요해
  T-016과 Draft 설계로 분리했습니다. A안을 권고하지만 아직 승인되지 않았습니다.
