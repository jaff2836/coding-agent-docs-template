---
name: review-round
description: 리뷰 라운드를 실행합니다. 리뷰 대기 → 리뷰 확인 → 수정 → commit을 반복하고, 통과 시 on_pass 기본값(PR은 사용자 확인 후 merge, PR이 없으면 merge 안 함)에 따라 종료합니다. 사용자가 명시적으로 호출한 경우에만 실행합니다.
argument-hint: "[라운드 수]"
disable-model-invocation: true
---

# Review Round

**사용자가 이 스킬을 명시적으로 호출한 경우에만 실행하세요.** 모델 판단으로 자동 실행하지 마세요. 이 절차는 commit과 merge를 수행합니다.

1. `docs/REVIEW_ROUND.md`를 읽고 그 절차를 그대로 적용합니다. → [docs/REVIEW_ROUND.md](../../../docs/REVIEW_ROUND.md)
2. 판정 기준은 `docs/REVIEW.md`입니다. → [docs/REVIEW.md](../../../docs/REVIEW.md)
3. 사용자가 별도 지정하지 않은 파라미터에만 기본값을 사용합니다: 5라운드, 임계값 `모든 P0 = 0, 모든 P1 = 0, blocking P2 = 0`, `rereview = auto`, branch 삭제 없음. 외부 리뷰어를 사용하는데 리뷰어 표(§2.1)가 비어 있으면 시작하지 않고 등록을 요청합니다. `reviewers = self`는 등록 없이 시작하며 외부 리뷰를 요청하거나 기다리지 않습니다. PR이 없으면 `on_pass = merge 안 함`을 기본으로 합니다.
4. 사용자가 지정한 임계값을 포함해 확정한 파라미터를 되읽어 준 뒤 시작하세요. 진행 중 사용자가 명시적으로 바꾸면 §2에 따라 기록하고 재평가하며, 임의로 기본값을 강제하거나 완화하지 않습니다.
5. 통과하면 head를 동결하고 남은 항목은 세션 인계 목록에 기록합니다. 현재 PR에 기록용 commit·push를 추가하지 않으며, 저장소 문서 반영은 §9에 따라 다음 작업에서 수행합니다.

이 파일은 어댑터입니다. 절차와 정책은 위 두 문서가 canonical이며, 충돌하면 문서를 우선합니다.
