# 프로젝트 기준과 설계

> 제품 개요·현재 구조·기본 설계·결정과 상세 설계의 인덱스입니다. 기존 제품 설계를 통합할 때는 결정·계약·근거를 보존하고 중복 설명과 작업 상태를 정리합니다. 실행 계획은 [02-TODO.md](./02-TODO.md) 또는 변경별 PLAN에서 관리합니다.
>
> §1~§5, §8, §11은 필수입니다. 나머지 절은 해당 사항이 있을 때만 유지합니다. 기존 상세 설계를 유지한다면 본문을 복제하지 않고 §13에서 정본을 연결합니다. 절을 제거하거나 번호를 바꾸면 들어오는 절 참조도 갱신하세요.

## Metadata

- **Project:** coding-agent-docs-template
- **Status:** In Progress — 공개 v1.7.1 기준과 v2 locale source 전환을 구분
- **Owner:** Chae Sangwon
- **Last reviewed:** 2026-09-09
- **Review cadence:** 아키텍처·범위 변경 시 또는 마일스톤 종료 시

## 1. Context

### Problem

Claude, Codex, Cursor와 OMP가 같은 문서·설계·리뷰 계약을 사용하도록 하는 공개 템플릿입니다. v1.7.1까지는 저장소 root가 한국어 복사형 payload와 저장소 관리 문서를 겸했기 때문에 locale 확장 시 maintainer 작업이 사용자 템플릿에 섞이는 문제가 있습니다.

### Target Users

- 템플릿을 관리·번역·릴리스하는 maintainer
- AI 코딩 에이전트 협업 규칙을 새 프로젝트에 적용하는 개발자

### Current State

- 공개 기준은 한국어 복사형 `v1.7.1`이며 Origin `main`의 merge commit `113a6a58f9b03707fe8050b5673d3437b9895d03`에 반영되어 있습니다.
- W-001의 root 유지관리 영역과 `template/common/`·`locales/ko/` payload source 분리는 Origin PR #3 merge commit `2a735eb182662afa69ee2c6d67f4f03d09e56d38`에 통합됐습니다.
- W-002의 `locales/en`·locale별 skill S2 계약과 W-003 locale/artifact 검사는 각각 Origin PR #4·#5에 통합됐습니다. `en`·`ko` source는 모두 `complete`입니다.
- W-004에서 deterministic exporter·packager와 release manifest schema를 구현·로컬 검증했습니다. installer, 공식 release와 도구 지원 검증은 아직 완료되지 않았습니다.
- 기존 적용 저장소의 사용자 수정 문서는 자동 덮어쓰기나 locale 자동 전환 대상이 아닙니다.

현재 구현·검증된 지원 범위와 그 근거를 기록합니다. 설계 승인·코드 구현·통합·릴리스·지원 검증을 구분합니다. 열린 PR이나 브랜치별 상세 상태를 여기에 복제하지 않습니다.

## 2. Goals

- `en`·`ko` complete source에서 고정 경로의 단일-locale artifact를 재현 가능하게 생성합니다.
- artifact와 exact source commit·version·member hash를 결합하고 비파괴 installer로 검증 후 설치합니다.
- Claude, Codex, Cursor와 OMP에서 locale별 진입점·스킬·리뷰 계약이 동일하게 동작하는지 검증합니다.

## 3. Non-goals

- `en`·`ko` 외 locale의 공식 번역과 품질 보증
- 특정 CI runner pipeline 또는 자동 리뷰 실행 구성
- 기존 프로젝트 문서의 자동 update·overwrite
- GitHub 저장소 생성, tag·release 게시와 mirror 구성

## 4. Constraints

- Python 표준 라이브러리만 사용하고 새 production dependency를 추가하지 않습니다.
- locale은 BCP 47 tag를 사용하며 manifest allowlist에 등록된 값만 지원합니다.
- 적용 artifact의 `AGENTS.md`, `CLAUDE.md`, `docs/`, tool별 고정 경로는 v1 계약을 유지합니다.
- path traversal, symlink, 부분 설치, checksum 불일치와 기존 파일 충돌은 쓰기 전에 거부합니다.

## 5. Current Architecture

현재 코드와 실제 배포 구성에 존재하는 구조를 기록합니다. 아직 구현되지 않은 목표 상태를 현재 구조처럼 작성하지 않습니다.

### Components

| Component | Responsibility | Dependencies | Owner |
| --------- | -------------- | ------------ | ----- |
| root maintenance plane | 저장소 소개, 제품 결정, 변경 설계·TODO와 maintainer 도구 지침 | artifact source와 분리 | Chae Sangwon |
| `template/common/` | 현재 언어 비의존으로 확인된 payload source | `locales/manifest.json` inventory | Chae Sangwon |
| `locales/en/`, `locales/ko/` | complete locale별 prose·도구 계약 source | common source와 합성 | Chae Sangwon |
| `locales/manifest.json` | baseline, locale 상태, common/localized output inventory | checker·exporter·packager가 사용 | Chae Sangwon |
| locale exporter·packager | 단일-locale tree와 deterministic ZIP·manifest·checksum 생성 | complete locale source, 고정 installer source | Chae Sangwon |

### Data Flow

exporter는 manifest의 common과 선택 locale inventory만 외부 빈 디렉터리에 합성하고 artifact checker를 통과한 뒤 원자적으로 게시합니다. packager는 `complete` locale을 고정 ZIP metadata로 묶고 source commit·version·repository·member hash를 release manifest에 결합합니다. source root 자체는 배포하지 않으며 실제 installer를 포함한 release E2E는 W-005 이후에 수행합니다.

### External Boundaries

- Origin은 source branch와 PR을 보관하지만 artifact release host는 아직 결정하지 않았습니다.
- 파일시스템과 향후 release asset 다운로드가 신뢰 경계입니다. manifest·archive·member hash를 모두 확인해야 합니다.

### Contracts and Core Design

상세 요구사항·오류 처리·마이그레이션 계약은 [다국어 템플릿 SPEC](./changes/2026-09-09-multilingual-template/02-SPEC.md), 실행 상태는 [PLAN](./changes/2026-09-09-multilingual-template/03-PLAN.md)이 정본입니다.

## 6. Target Architecture

합의되었지만 아직 완전히 구현되지 않은 목표 구조를 기록합니다. **제안만 있고 합의되지 않은 항목은 여기 두지 않습니다.** 미합의 항목은 §11 Open Questions 또는 §12 Rejected or Deferred Ideas에 두고, 결정이 내려진 뒤에만 이 표로 옮깁니다. 이 표만 읽는 사람은 여기 있는 것을 이미 결정된 것으로 읽습니다.

### Target Components

승인된 목표 구성은 `template/common/`과 BCP 47 tag별 `locales/<tag>/` source, 닫힌 manifest inventory, locale 검사, deterministic exporter·packager와 비파괴 installer입니다. 첫 안정판은 `en`·`ko`가 모두 `complete`일 때만 만들며 skill prose와 출력 정책은 locale별 source가 소유합니다.

### Target Data Flow

common과 선택 locale 하나를 manifest inventory에 따라 표준 root 경로로 합성하고 검사합니다. exact source commit과 version에 결합된 locale별 archive·manifest를 만든 뒤 installer가 검증·stage·전체 충돌 검사를 거쳐 대상에 기록합니다. 상세 계약은 [SPEC §3](./changes/2026-09-09-multilingual-template/02-SPEC.md)을 따릅니다.

### Compatibility Requirements

- v1.7.1 한국어 payload는 `fb70176` 기준으로 보존합니다.
- source root를 직접 복사하지 않으며 locale artifact만 적용합니다.
- 이미 적용한 저장소는 자동 migration하지 않습니다.

## 7. Transition Plan

현재 구조에서 목표 구조로 이동하는 순서와 안전 조건을 작성합니다. 단계 정의·완료 조건을 다루며, 상세 실행 체크박스는 TODO 또는 변경별 PLAN에서 관리합니다. 확장 문서가 같은 전환을 정의하면 그 절을 참조합니다.

| Phase | Change | Preconditions | Compatibility/Rollback | Completion Evidence |
|---|---|---|---|---|
| W-001 | root maintainer 영역과 common/ko source 분리 | 사용자 승인, PR #2 병합 | `fb70176` payload 보존; 실패 시 source 분리 폐기 | PR #3 merge commit `2a735eb`, closed inventory와 path·byte 비교 |
| W-002 | en locale과 locale별 skill S2 | W-001 | v1.7.1 유지 | PR #4 merge commit `fa01b20`, 최종 번역 승인 |
| W-003 | locale/artifact 검사 | W-002 | marker·inventory 계약 유지 | PR #5 merge commit `7657d2c`, source/stable gate |
| W-004 이후 | deterministic export/package와 installer | W-003, complete locale | v1.7.1 유지; installer 전에는 release하지 않음 | 변경 PLAN의 gate |

## 8. Decisions

결정 상태는 `Proposed`, `Accepted`, `Superseded`, `Rejected` 중 하나를 사용합니다.

| ID | Date | Status | Decision | Rationale / Canonical source | Alternatives / Consequences | Approval |
|---|---|---|---|---|---|---|
| D-001 | 2026-09-09 | Accepted | 저장소 root 유지관리 영역과 배포 payload source를 분리하고 W-001을 PR #3에서 구현 | [SPEC §3.1](./changes/2026-09-09-multilingual-template/02-SPEC.md), Origin PR #3 리뷰 F-001 | source root 직접 복사 중단; v1.7.1 snapshot 보존 | Chae Sangwon, 2026-09-09 대화 |
| D-002 | 2026-09-09 | Accepted | common+locale 합성 artifact, locale별 skill S2 계약과 host-neutral installer를 포함한 v2 전체 구조 | [다국어 템플릿 SPEC](./changes/2026-09-09-multilingual-template/02-SPEC.md) | v2 breaking change; release host는 구현 중 확정 | Chae Sangwon, 2026-09-09 대화 |

중요한 결정이 많아지면 개별 ADR 문서로 분리하고 여기에는 링크와 요약만 남깁니다.

결정 상태와 정본 위치는 이 표가 기준입니다. `D-nnn`은 이 표에 등재할 때 전역으로 발급합니다. 표의 `D-001` 행은 자리 표시이므로 적용 시 삭제하거나 실제 결정으로 교체하세요. 변경 폴더의 `R-001` 등과 같은 번호대가 아닙니다. 상세 설계에 이유·대안·영향이 있으면 여기에는 링크와 요약만 남깁니다. 승인한 사람·범위·확인 가능한 근거를 연결하고, 기존 결정을 대체하면 삭제하지 않고 `Superseded`로 남깁니다. 기존 결정 ID를 파일 번호에 맞춰 재번호하지 않습니다.

## 9. Delivery Strategy

### Phase 1 — source boundary

- root maintainer plane과 `template/common`·`locales/ko`를 분리합니다.
- baseline inventory 보존과 root 직접 복사 금지를 검증합니다.

### Phase 2 — multilingual delivery

- 승인된 순서에 따라 `en`, locale parity 검사, deterministic packaging과 installer를 구현합니다.
- exact-head consumer E2E 후에만 지원 완료와 release를 별도로 판정합니다.

## 10. Risks

| Risk | Likelihood | Impact | Mitigation | Trigger/Signal |
| ---- | ---------- | ------ | ---------- | -------------- |
| maintainer 문서가 artifact에 포함됨 | Medium | High | manifest의 닫힌 inventory와 artifact 부재 검사 | root 전용 path가 archive member에 등장 |
| locale 번역의 행동 계약 drift | Medium | High | stable marker·fixture·사람의 최종 검수 | locale parity 또는 소비자 E2E 실패 |
| installer가 기존 문서를 덮어씀 | Low | High | 충돌 시 전체 중단, `--force` 미제공 | before/after tree hash 차이 |

## 11. Open Questions

- [ ] immutable release asset의 실제 host와 bootstrap URL을 구현 중 확정합니다.

## 12. Rejected or Deferred Ideas

- `en`·`ko` 외 공식 locale은 v2 계약과 두 필수 locale 지원 검증 후 재검토합니다.
- 기존 적용 저장소의 자동 update·overwrite는 사용자 문서 손실 위험 때문에 첫 버전에서 제외합니다.

## 13. 설계 문서 인덱스

| 범위 | 정본 | 상위 설계와의 관계 | 적용 조건 |
|---|---|---|---|
| 기본 제품 설계 | 이 문서 | 저장소 현재 상태와 승인된 결정 | root 유지관리 작업 |
| 다국어 배포 변경 | [2026-09-09-multilingual-template SPEC](./changes/2026-09-09-multilingual-template/02-SPEC.md) | D-001을 구현하고 D-002를 제안 | 연결된 PLAN의 승인 범위 |

선택형 문서를 사용하지 않으면 해당 행과 링크를 제거합니다. 개별 변경 SPEC은 §8의 결정에서 연결합니다. 문서 번호나 작성일만으로 다른 설계 전체를 대체하지 않습니다.
