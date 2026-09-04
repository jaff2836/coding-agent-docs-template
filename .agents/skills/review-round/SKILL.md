---
name: review-round
description: 리뷰 라운드를 실행합니다. 리뷰 대기 → 리뷰 확인 → 수정 → commit을 반복하고, 통과 임계값을 충족하면 사용자 확인 후 merge합니다. 사용자가 명시적으로 호출한 경우에만 실행합니다.
argument-hint: "[라운드 수]"
disable-model-invocation: true
---

# Review Round

**사용자가 이 스킬을 명시적으로 호출한 경우에만 실행하세요.** 모델 판단으로 자동 실행하지 마세요. 이 절차는 commit과 merge를 수행합니다.

1. `docs/REVIEW_ROUND.md`를 읽고 그 절차를 그대로 적용합니다. → [docs/REVIEW_ROUND.md](../../../docs/REVIEW_ROUND.md)
2. 판정 기준은 `docs/REVIEW.md`입니다. → [docs/REVIEW.md](../../../docs/REVIEW.md)
3. 인자가 없으면 기본값을 사용합니다: 5라운드, 임계값 `blocking P0·P1·P2 = 0`, `rereview = auto`, branch 삭제 없음. 리뷰어 표(§2.1)가 비어 있으면 시작하지 않고 등록을 요청합니다.
4. 확정한 파라미터를 사용자에게 되읽어 준 뒤 시작하세요.

이 파일은 어댑터입니다. 절차와 정책은 위 두 문서가 canonical이며, 충돌하면 문서를 우선합니다.
