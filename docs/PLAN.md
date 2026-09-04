# Project Plan

> 이 문서는 목표와 결정 이유를 기록합니다. 일상적인 작업 체크리스트는 [TODO.md](./TODO.md)에서 관리합니다.
>
> §1~§4, §8, §11은 필수입니다. §5~§7, §9, §10, §12는 해당 사항이 있을 때만 유지하고, 없으면 절을 삭제하세요. 빈 절을 placeholder 채로 남기지 마세요.

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

현재 구조에서 목표 구조로 이동하는 순서와 안전 조건을 작성합니다.

| Phase | Change | Preconditions | Compatibility/Rollback | Completion Evidence |
|---|---|---|---|---|
| 1 | 전환 작업 | 선행 조건 | 호환성·rollback 방법 | 테스트·배포 근거 |

## 8. Decisions

결정 상태는 `Proposed`, `Accepted`, `Superseded`, `Rejected` 중 하나를 사용합니다.

| ID    | Date       | Status   | Decision  | Rationale | Alternatives | Consequences |
| ----- | ---------- | -------- | --------- | --------- | ------------ | ------------ |
| D-001 | YYYY-MM-DD | Proposed | 결정 내용 | 선택 이유 | 검토한 대안  | 예상 결과    |

중요한 결정이 많아지면 개별 ADR 문서로 분리하고 여기에는 링크와 요약만 남깁니다.

표와 별도의 상세 섹션을 함께 두는 구조라면 둘을 같이 갱신하세요. 표에는 있는데 상세가 없는 결정이 생기면 조회 경로가 결정마다 달라집니다.

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
