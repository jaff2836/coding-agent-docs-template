# 프로젝트 기준과 설계

> 제품 개요·현재 구조·기본 설계·결정과 상세 설계의 인덱스입니다. 기존 제품 설계를 통합할 때는 결정·계약·근거를 보존하고 중복 설명과 작업 상태를 정리합니다. 실행 계획은 [02-TODO.md](./02-TODO.md) 또는 변경별 PLAN에서 관리합니다.
>
> §1~§5, §8, §11은 필수입니다. 나머지 절은 해당 사항이 있을 때만 유지합니다. 기존 상세 설계를 유지한다면 본문을 복제하지 않고 §13에서 정본을 연결합니다. 절을 제거하거나 번호를 바꾸면 들어오는 절 참조도 갱신하세요.

## Metadata

- **Project:** {{PROJECT_NAME}}
- **Status:** Draft
- **Owner:** 프로젝트에 맞게 작성
- **Last reviewed:** YYYY-MM-DD
- **Review cadence:** 아키텍처·범위 변경 시 또는 마일스톤 종료 시

## 1. Context

### Problem

{{PROJECT_DESCRIPTION}}

### Target Users

- 주요 사용자와 운영 주체

### Current State

- 현재 구현 상태
- 기존 시스템 또는 대체 수단
- 확인된 제약

현재 구현·검증된 지원 범위와 그 근거를 기록합니다. 설계 승인·코드 구현·통합·릴리스·지원 검증을 구분합니다. 열린 PR이나 브랜치별 상세 상태를 여기에 복제하지 않습니다.

## 2. Goals

- 달성해야 하는 측정 가능한 결과

## 3. Non-goals

- 이번 범위에서 의도적으로 다루지 않는 사항

## 4. Constraints

- 기술적 제약
- 보안 및 규제 제약
- 호환성 요구사항
- 일정 또는 운영 제약

## 5. Current Architecture

현재 코드와 실제 배포 구성에 존재하는 구조를 기록합니다. 아직 구현되지 않은 목표 상태를 현재 구조처럼 작성하지 않습니다.

### Components

| Component | Responsibility | Dependencies | Owner |
| --------- | -------------- | ------------ | ----- |
| 예시      | 예시           | 예시         | 예시  |

### Data Flow

대표 요청 또는 작업이 입력부터 결과까지 이동하는 흐름을 작성합니다.

### External Boundaries

- 데이터베이스
- 외부 API
- 메시지 큐 또는 스케줄러
- 파일 및 object storage
- 인증·권한 시스템

### Contracts and Core Design

공개 계약·데이터 모델·오류 처리·주요 신뢰 경계와 기본 설계를 작성합니다. 설정 레퍼런스나 보안 모델 등 별도 정본이 있으면 링크로 연결합니다. 결정 이유는 §8 또는 거기서 지정한 상세 문서에 한 번만 기록합니다.

## 6. Target Architecture

합의되었지만 아직 완전히 구현되지 않은 목표 구조를 기록합니다. **제안만 있고 합의되지 않은 항목은 여기 두지 않습니다.** 미합의 항목은 §11 Open Questions 또는 §12 Rejected or Deferred Ideas에 두고, 결정이 내려진 뒤에만 이 표로 옮깁니다. 이 표만 읽는 사람은 여기 있는 것을 이미 결정된 것으로 읽습니다.

### Target Components

| Component | Intended Responsibility | Replaces/Extends | Completion Signal |
|---|---|---|---|
| 예시 | 목표 책임 | 현재 구성요소 | 완료를 확인할 근거 |

### Target Data Flow

목표 상태의 대표 흐름과 현재 구조에서 달라지는 경계를 작성합니다.

### Compatibility Requirements

- 전환 중 유지해야 하는 API·데이터·운영 호환성
- 병행 운영 또는 단계적 rollout 조건
- 제거할 legacy 경로와 제거 가능 조건

## 7. Transition Plan

현재 구조에서 목표 구조로 이동하는 순서와 안전 조건을 작성합니다. 단계 정의·완료 조건을 다루며, 상세 실행 체크박스는 TODO 또는 변경별 PLAN에서 관리합니다. 확장 문서가 같은 전환을 정의하면 그 절을 참조합니다.

| Phase | Change | Preconditions | Compatibility/Rollback | Completion Evidence |
|---|---|---|---|---|
| 1 | 전환 작업 | 선행 조건 | 호환성·rollback 방법 | 테스트·배포 근거 |

## 8. Decisions

결정 상태는 `Proposed`, `Accepted`, `Superseded`, `Rejected` 중 하나를 사용합니다.

| ID | Date | Status | Decision | Rationale / Canonical source | Alternatives / Consequences | Approval |
|---|---|---|---|---|---|---|
| D-001 | YYYY-MM-DD | Proposed | 결정 요약 | 이유 또는 상세 SPEC·기존 설계의 정본 링크 | 대안·영향 또는 정본 참조 | 미승인 |

중요한 결정이 많아지면 개별 ADR 문서로 분리하고 여기에는 링크와 요약만 남깁니다.

결정 상태와 정본 위치는 이 표가 기준입니다. `D-nnn`은 이 표에 등재할 때 전역으로 발급합니다. 표의 `D-001` 행은 자리 표시이므로 적용 시 삭제하거나 실제 결정으로 교체하세요. 변경 폴더의 `R-001` 등과 같은 번호대가 아닙니다. 상세 설계에 이유·대안·영향이 있으면 여기에는 링크와 요약만 남깁니다. 승인한 사람·범위·확인 가능한 근거를 연결하고, 기존 결정을 대체하면 삭제하지 않고 `Superseded`로 남깁니다. 기존 결정 ID를 파일 번호에 맞춰 재번호하지 않습니다.

## 9. Delivery Strategy

### Phase 1

- 목표
- 산출물
- 완료 조건

### Phase 2

- 목표
- 산출물
- 완료 조건

## 10. Risks

| Risk | Likelihood | Impact | Mitigation | Trigger/Signal |
| ---- | ---------- | ------ | ---------- | -------------- |
| 예시 | Medium     | High   | 대응 방법  | 관찰 신호      |

## 11. Open Questions

- [ ] 아직 결정되지 않은 질문

## 12. Rejected or Deferred Ideas

현재 계획으로 오인되지 않도록 기각·보류 이유와 재검토 조건을 기록합니다.

## 13. 설계 문서 인덱스

| 범위 | 정본 | 상위 설계와의 관계 | 적용 조건 |
|---|---|---|---|
| 기본 제품 설계 | 이 문서 또는 유지하는 기존 설계 문서 | 기본 계약·구조 | 실제 적용 범위 |
| 장기 확장 (선택) | [10-EXTENSION.md](./10-EXTENSION.md) 또는 기존 확장 문서 | 유지·확장·대체하는 결정·절 | 승인 범위와 선행조건 |

선택형 문서를 사용하지 않으면 해당 행과 링크를 제거합니다. 개별 변경 SPEC은 §8의 결정에서 연결합니다. 문서 번호나 작성일만으로 다른 설계 전체를 대체하지 않습니다.
