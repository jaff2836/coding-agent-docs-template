# Bugbot Review Rules

Bugbot은 이 파일만 프로젝트 리뷰 규칙으로 읽습니다. 그래서 [`docs/REVIEW.md`](../docs/REVIEW.md)의 판정 기준을 아래에 복제합니다. 두 문서가 충돌하면 `docs/REVIEW.md`가 canonical입니다. 정책을 바꿀 때는 두 파일을 함께 수정하세요.

## 언어

- 모든 리뷰 설명과 요약은 한국어로 작성합니다.
- 코드 식별자, 파일 경로, 설정 키 및 코드 인용은 원문을 유지합니다.

## Severity

- **P0:** 데이터 손실, 데이터 손상, 보안 구멍 또는 일반 경로의 크래시.
- **P1:** 일반적인 사용 조건에서 사용자에게 실제로 영향을 주는 결함 — 잘못된 결과, hang, leak, 멈춘 상태 기계, 현재 구성으로는 production에서 동작할 수 없는 기능.
- **P2:** 영향 범위가 좁거나 발생 조건이 드문 결함, 또는 의미 있는 robustness 격차.
- **P3:** 알아둘 가치는 있으나 병합을 막을 정도는 아닌 사항.

P0와 P1은 발생 조건부터 영향까지 end-to-end로 추적한 경우에만 부여합니다.

## Confidence

코드를 읽은 뒤 그 결함이 실재한다고 확신하는 정도를 판단합니다.

- `0.9` 이상: end-to-end로 추적했고 성립합니다.
- `0.6` 미만: 추측입니다. 보고하지 말고 버리세요.

## Blocking

모든 finding에 blocking 여부를 표시합니다. 중요도와 독립적인 값입니다.

- **blocking:** 이번 PR이 결함을 새로 만들었거나, 기존 결함을 직접 건드려 악화시켰습니다.
- **non-blocking:** 기존 결함을 건드리지 않았거나, 표면적인 문제이거나, 저장소 지침에 known·deferred·planned follow-up으로 기록된 항목입니다.

non-blocking finding도 보고합니다. 유용한 맥락입니다. 기본 리뷰 라운드의 통과 조건은 모든 P0·P1과 blocking P2가 0개인 것이므로, 기본값에서는 P0·P1이 non-blocking이어도 통과를 막습니다. 사용자는 임계값을 변경할 수 있으며, 실제 통과·수정·이관은 라운드 실행 주체가 확정한 값으로 판단합니다. 통과를 막는다는 이유로 blocking 분류를 바꾸지는 않습니다. 작성자가 이미 이월 작업으로 추적 중인 결함은 반드시 non-blocking입니다. 아래 「확정된 설계 결정과 승인된 deferral」에 기록된 항목을 finding과 대조하세요. 승인된 deferral도 기본 임계값의 P0·P1 예외가 되지 않습니다. 지침이 여러 PR에 걸쳐 의도적으로 단계화했다고 밝힌 설계는 다시 논쟁하지 않습니다.

## 이 저장소의 불변조건

<!-- template-section:project-invariants -->

Bugbot은 `docs/REVIEW.md` §6을 읽지 못하므로 같은 목록을 여기에 둡니다. 각 항목은 잘못된 동작, 영향 및 안전한 경로를 포함해야 하며, 두 파일의 목록은 항상 같아야 합니다. `scripts/check-docs.py`가 두 목록을 대조합니다.

- **Artifact 경계:** 저장소 root의 maintainer 문서나 source landing README를 사용자 artifact에 포함하지 않습니다. 포함하면 저장소 로드맵이 적용 프로젝트 정책으로 오염되므로, 안전한 경로는 `locales/manifest.json`의 닫힌 inventory에 따라 `template/common/`과 locale 하나만 합성하는 것입니다.
- **Locale 완전성:** 서로 다른 locale의 자연어 정책·스킬을 한 artifact에 섞거나 미완료 locale을 안정판으로 게시하지 않습니다. agent 행동과 사용자 검수가 언어별로 달라질 수 있으므로, 안전한 경로는 `en`·`ko` complete gate와 locale별 artifact 검사를 통과한 immutable asset만 게시하는 것입니다.
- **Adoption 읽기 전용:** `installer.py adopt`는 대상 저장소에 파일을 만들거나 수정·삭제하지 않고, artifact 경로를 policy 없이 배포하지 않습니다. 대상 안에 staging을 쓰거나 충돌 파일을 덮어쓰면 사용자 문서와 라이선스 결정이 손상되므로, 안전한 경로는 `locales/manifest.json`의 닫힌 adoption policy를 release manifest에 결합하고 대상 밖의 빈 output에 검증된 artifact와 report만 원자적으로 게시하는 것입니다.

## 확정된 설계 결정과 승인된 deferral

`docs/REVIEW.md` §9 Accepted Deferrals와 `docs/00-PROJECT.md` §8 Decisions 중 리뷰 판정에 영향을 주는 항목을 여기에 복제합니다. 여기 있는 결정을 **되돌리라는** 지적은 새 정보가 아니므로 보고하지 않습니다. 결정의 **전제가 깨졌다는 증거**(문서가 약속한 것과 코드가 실제로 하는 것이 다름, 결정이 가정한 조건이 더 이상 성립하지 않음)는 새 정보이므로 보고합니다.

- 승인된 deferral: 실제로 승인된 `DFR-*` 항목이 없으면 이 목록은 비워 둡니다
- 확정된 결정: D-001 — 저장소 root 유지관리 영역과 배포 payload source를 분리하고 source root를 직접 복사하지 않습니다.
- 확정된 결정: D-006 — 기존 저장소 adoption은 `adopt`가 대상 밖 output에 검증된 staging과 실험적 report만 만들며, 자동 적용·overwrite·3-way merge와 공개 report schema는 제공하지 않습니다.

## Finding 필수 항목

중요도, confidence, blocking 여부와 그 근거, 정확한 변경 위치, 재현 가능한 발생 조건, 영향, 최소 수정 방향, 증거가 되는 코드 줄.

## Do Not Report

- formatter나 lint가 결정적으로 검출하는 문제
- 구체적 발생 조건이 없는 추측 (confidence 0.6 미만)
- 개인적인 스타일 또는 아키텍처 취향
- 이번 PR과 관련 없는 기존 문제 (단, 발생 조건부터 영향까지 검증된 P0·P1은 non-blocking으로 보고합니다)
- 동작 영향이 없는 명명·주석 선호
- 단순히 테스트 수가 적다는 이유만으로 만든 finding
- 승인된 상위 설계의 구현에 INTENT·SPEC 파일이 없다는 사실만으로 만든 finding
- 같은 원인의 중복 finding
- 위 「확정된 설계 결정과 승인된 deferral」에 기록된 결정을 되돌리라는 요구

설계 문서의 파일명·체크박스만으로 승인이나 완료를 추정하지 않습니다. 완료 주장은 코드와 검증 근거로 확인하며, 변경별 PLAN의 브랜치 구현·검증 완료와 전역 TODO의 통합·릴리스·지원 검증 완료를 구분합니다.

중대한 문제가 없다면 문제를 만들어내지 말고 확인한 범위와 한계를 설명합니다.
