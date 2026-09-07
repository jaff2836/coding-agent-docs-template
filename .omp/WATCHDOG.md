# Advisor Review Priorities

이 파일은 OMP advisor(감시자 모델) 전용 지침입니다. 주 에이전트의 컨텍스트에는 들어가지 않으며, `AGENTS.md`처럼 동작하지도 않습니다. 리뷰 판정 기준의 canonical 문서는 `docs/REVIEW.md`이며 아래에서 그대로 import합니다. 정책을 바꿀 때는 `docs/REVIEW.md`만 수정하세요.

@../docs/REVIEW.md

## 이 세션에서 특히 볼 것

- `docs/REVIEW.md` §6 Project-specific Invariants를 깨는 변경. 주 에이전트가 불변조건을 언급하지 않고 지나가면 `concern`으로 짚어 주세요.
- `docs/00-PROJECT.md` §8에 `Accepted`로 기록된 결정을 근거 없이 되돌리는 변경. 결정의 전제가 깨졌다는 증거가 있으면 그 증거를 함께 적어 주세요.
- `AGENTS.md` Change Rules 위반 — 요청 범위를 넘는 리팩터링, 동의 없는 새 production dependency, 명시 요청 없는 commit·push, 비밀값을 코드·로그·문서에 남기는 것.
- 주 에이전트가 읽지 않은 코드에 대해 가정하고 진행하는 경우. 호출자를 확인하지 않은 함수 시그니처 변경이 대표적입니다.
- `docs/01-DESIGN.md` §1 적용 조건에 해당하는 변경을 설계 절차 없이 바로 구현하기 시작하는 경우.

## 보고하지 않을 것

- `docs/REVIEW.md` §8 Do Not Report에 해당하는 항목
- §9 Accepted Deferrals와 `docs/00-PROJECT.md` §12에 기록된 보류 항목을 되돌리라는 요구
- 주 에이전트가 이미 스스로 짚고 처리 중인 문제
