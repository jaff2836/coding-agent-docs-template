# Documentation Guide

## Metadata

- **Status:** Active
- **Template version:** 1.2
- **Owner:** 프로젝트에 맞게 작성
- **Last reviewed:** YYYY-MM-DD
- **Review cadence:** 문서 체계 변경 시

이 디렉터리는 프로젝트의 계획, 변경 설계 절차, 실행 상태, 리뷰 정책, 리뷰 라운드 절차 및 전체 분석 절차를 관리합니다. 각 문서는 서로 다른 질문에 답하며, 같은 정보를 여러 문서에 중복 기록하지 않습니다.

프로젝트 소개와 실행 방법은 [프로젝트 README](../README.md), 최초 복사·설정 방법은 [Template Guide](./TEMPLATE_GUIDE.md)를 참고하세요. 이 문서는 적용 후의 문서 운영 기준을 설명합니다.

## Document Map

| Document | Answers | Read When | Update When | Authority |
|---|---|---|---|---|
| [PLAN.md](./PLAN.md) | 왜 이렇게 설계했는가? 현재와 목표 구조는 무엇인가? | 구조·기술·범위 결정 전 | 결정이 합의되거나 실제 결정이 변경될 때 | 프로젝트 담당자 |
| [DESIGN.md](./DESIGN.md) | 구조·계약을 바꾸는 변경을 구현 전에 어떤 순서로 설계하고 합의하는가? | 구조·기술 스택·공개 계약 변경, 또는 대안 간 트레이드오프가 있을 때 | 설계 절차 자체가 변경될 때 | Maintainer |
| [TODO.md](./TODO.md) | 지금 무엇을 구현하고 있으며 완료 조건은 무엇인가? | 추적 중인 작업을 수행할 때 | 작업 상태 또는 검증 결과가 바뀔 때 | 작업 담당자 |
| [REVIEW.md](./REVIEW.md) | 무엇을 결함으로 판단하고 병합을 차단하는가? | PR·diff·commit 리뷰 시 | 리뷰 정책 변경이 합의될 때 | Maintainer |
| [REVIEW_ROUND.md](./REVIEW_ROUND.md) | 리뷰 결과를 받아 누가 언제 수정·commit·merge하는가? | 사용자가 리뷰 라운드를 시작할 때 | 라운드 절차나 권한 위임 범위가 변경될 때 | Maintainer |
| [PROJECT_ANALYSIS.md](./PROJECT_ANALYSIS.md) | 프로젝트 전체를 어떤 기준으로 평가하는가? | 전체 분석·기술 실사·도입 판단 요청 시 | 분석 절차 자체가 변경될 때 | Maintainer |

## Document Flow

```text
PLAN의 목표와 결정
        ↓
DESIGN의 변경 설계와 합의 (구조·계약 변경 시)
        ↓
TODO의 실행 작업과 완료 조건
        ↓
코드·테스트·배포 결과
        ↓
REVIEW의 변경 품질 판정
        ↓
REVIEW_ROUND의 수정·병합 진행
        ↓
PROJECT_ANALYSIS의 전체 정합성 평가
```

## Source-of-truth Rules

- 목표, 제약, 아키텍처와 결정 이유는 [PLAN.md](./PLAN.md)에 기록합니다.
- 변경 설계 절차는 [DESIGN.md](./DESIGN.md)에 기록합니다. 큰 변경의 설계 상세는 `docs/changes/` 파일에 두되, 결정 이유는 [PLAN.md](./PLAN.md), 작업 상태는 [TODO.md](./TODO.md)가 canonical이며 설계 파일에서 따로 관리하지 않습니다.
- 현재 작업, 차단 상태와 검증 결과는 [TODO.md](./TODO.md)에 기록합니다.
- 리뷰 중요도, `confidence`·`blocking` 기준, 프로젝트 불변조건과 승인된 deferral은 [REVIEW.md](./REVIEW.md)에 기록합니다.
- 라운드 절차, 통과 임계값과 위임되는 권한 범위는 [REVIEW_ROUND.md](./REVIEW_ROUND.md)에 기록합니다.
- 전체 분석 방법은 [PROJECT_ANALYSIS.md](./PROJECT_ANALYSIS.md)에 기록합니다.
- 저장소에 `CHANGELOG.md`가 있으면 릴리스 단위 완료 이력의 source of truth로 연결하고, [TODO.md](./TODO.md) `Completed`에는 검증 근거만 남깁니다. 저장소 구조나 공개 계약을 바꾸는 변경은 CHANGELOG에도 기록합니다.
- 문서가 코드·테스트·자동화와 다르면 불일치를 숨기지 말고 어느 쪽이 오래되었는지 확인합니다.
- 동일한 정책을 도구별 adapter에 요약할 수 있지만, 충돌할 경우 [REVIEW.md](./REVIEW.md)가 리뷰 정책의 canonical source입니다.

## Metadata Convention

각 관리 문서는 가능한 한 다음 metadata를 유지합니다.

- **Status:** Draft, Active, Superseded 또는 Archived
- **Owner:** 내용 정확성과 정기 검토 책임자
- **Last reviewed:** 내용을 실제 근거와 비교한 마지막 날짜
- **Review cadence:** 정기 또는 이벤트 기반 재검토 조건

일부 문서는 추가 필드를 가집니다. [REVIEW.md](./REVIEW.md)의 `Policy version`은 리뷰 정책 자체의 개정 번호이고, 이 문서와 [Template Guide](./TEMPLATE_GUIDE.md)의 `Template version`은 복사해 온 템플릿 판입니다. 둘은 독립적으로 움직입니다.

날짜만 갱신하지 말고 문서와 실제 상태를 비교한 경우에만 `Last reviewed`를 변경합니다.

날짜는 `YYYY-MM-DD` 형식의 **UTC 기준**으로 적습니다. 저장소가 다른 시간대를 관례로 쓴다면 이 문서에 그 시간대를 명시하고 모든 문서가 같은 기준을 따르게 하세요. GitHub은 커밋과 PR 시각을 UTC로 표시하므로, 로컬 시간대로 적은 날짜가 PR 생성 시각보다 미래가 되어 리뷰어가 메타데이터 오류로 지적하는 경우가 실제로 있습니다.

## Template Adoption Checklist

- [ ] [Template Guide](./TEMPLATE_GUIDE.md)의 placeholder 검색 명령으로 `{{...}}`와 안내 문구형 placeholder를 모두 찾아 교체했다.
- [ ] `Run`, `Build`, `Test`, `Lint`, `Typecheck` 명령을 실제로 검증했거나 `N/A`인 이유를 기록했다.
- [ ] [PLAN.md](./PLAN.md)에 현재 구조, 목표 구조 및 전환 전략을 작성했거나, 해당 없음으로 판단해 조건부 절(§5~§7, §9, §10, §12)을 삭제했다.
- [ ] [PLAN.md](./PLAN.md)의 예시 결정 행(`D-001`)과 예시 표 행을 제거하거나 실제 항목으로 교체했다.
- [ ] [TODO.md](./TODO.md)에 첫 마일스톤과 검증 가능한 완료 조건을 작성했다.
- [ ] [TODO.md](./TODO.md)의 예시 완료 항목(`- [x] 완료된 작업`)을 제거하거나 실제 완료 이력과 검증 근거로 교체했다.
- [ ] [REVIEW.md](./REVIEW.md)에 프로젝트 고유 불변조건을 작성했다.
- [ ] [REVIEW.md](./REVIEW.md)의 예시 deferral을 실제 정책으로 오인할 수 없도록 제거하거나 실제 승인 항목으로 교체했다.
- [ ] Cursor Bugbot을 쓴다면 [REVIEW.md](./REVIEW.md) §6 불변조건과 §9 Accepted Deferrals, [PLAN.md](./PLAN.md)의 확정 결정 중 리뷰 판정에 영향을 주는 항목을 [.cursor/BUGBOT.md](../.cursor/BUGBOT.md)에도 복제했다. Bugbot은 링크된 문서를 읽지 않습니다.
- [ ] OMP advisor를 쓴다면 [.omp/WATCHDOG.md](../.omp/WATCHDOG.md)의 `@../docs/REVIEW.md` import가 사용 중인 OMP 버전에서 실제로 확장되는지 확인했다. 쓰지 않는다면 파일을 삭제했다.
- [ ] 기존 저장소의 REVIEW.md와 병합해 절 번호가 바뀌었거나 [PLAN.md](./PLAN.md)의 조건부 절을 삭제했다면, 절 번호로 참조하는 네 파일 — [REVIEW_ROUND.md](./REVIEW_ROUND.md), [DESIGN.md](./DESIGN.md), [.cursor/BUGBOT.md](../.cursor/BUGBOT.md), [.omp/WATCHDOG.md](../.omp/WATCHDOG.md) — 의 참조를 실제 헤딩과 대조해 고쳤다.
- [ ] 도입 전부터 있던 큰 설계 문서가 있다면 [DESIGN.md](./DESIGN.md) §6에 따라 옮기지 않고, [PLAN.md](./PLAN.md) §8에서 그 문서를 결정 본문의 위치로 가리키게 했다.
- [ ] [REVIEW_ROUND.md](./REVIEW_ROUND.md)의 기본 라운드 수와 통과 임계값이 프로젝트 정책과 맞는지 확인했다.
- [ ] 이 저장소에서 도는 리뷰어를 전부 조사해 [REVIEW_ROUND.md](./REVIEW_ROUND.md) §2.1에 기록했다. 도착 주기(상시·간헐)를 빠뜨리면 정족수 판정이 틀리고, `재리뷰 요청 방법` 열이 비어 있으면 `rereview = request`가 동작하지 않습니다.
- [ ] 각 문서의 `Last reviewed`를 실제로 내용을 검토한 날짜로 UTC 기준으로 기입했다. 템플릿을 복사한 것만으로 날짜를 채우지 않았다.
- [ ] 저장소에 맞는 owner와 검토 주기를 각 문서에 지정했다.
- [ ] Codex, Claude Code, Cursor 및 OMP가 의도한 instruction 파일을 로드하는지 확인했다.
- [ ] 사용하는 도구가 `review-round`·`design` 스킬을 인식하는지 확인했다. `.agents/skills/`는 Codex·Cursor·OMP, `.claude/skills/`는 Claude Code가 읽습니다.
- [ ] [Template Guide](./TEMPLATE_GUIDE.md)의 링크 검사 명령으로 문서의 상대경로 링크가 저장소 내에서 정상적으로 열리는지 확인했다.
- [ ] CODEOWNERS를 쓰는 저장소라면 `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, `.cursor/`, `.omp/`, `docs/REVIEW.md`, `docs/REVIEW_ROUND.md`, `docs/DESIGN.md`를 owner 규칙에 추가했다.
- [ ] OpenSpec, BMAD 같은 외부 방법론 도구를 함께 쓴다면 [Template Guide](./TEMPLATE_GUIDE.md) §4 「외부 방법론·행동 규칙 도구」의 공존 규칙에 따라 문서 소유권을 나누고, 도구가 `AGENTS.md`나 금지된 지침 파일을 생성·수정하지 않는지 확인했다.

## Maintenance

- 문서를 옮기거나 이름을 바꾸면 그 파일 안의 상대 링크와 그 파일을 가리키는 링크를 함께 고칩니다. 내용 변경이 없는 순수 rename도 링크를 깨뜨립니다. [Template Guide](./TEMPLATE_GUIDE.md)의 링크 검사 명령을 PR 전에 실행하세요.
- 오래된 완료 작업은 [TODO.md](./TODO.md)에서 마일스톤별 archive로 이동할 수 있습니다.
- 결정 기록이 커지면 [PLAN.md](./PLAN.md)의 결정 항목을 `adr/` 디렉터리로 분리하고 PLAN에는 상대경로 링크와 요약만 남깁니다.
- Superseded 문서는 삭제하기보다 대체 문서와 이유를 명시해 과거 맥락을 보존합니다.
- 이 문서와 [Template Guide](./TEMPLATE_GUIDE.md)의 `Template version`은 복사해 온 템플릿 판을 나타냅니다. 템플릿 개정을 반영했을 때만 올리며, Template Guide §6의 변경 이력에서 반영할 항목을 고르고 템플릿 저장소의 해당 tag와 파일을 직접 대조합니다(Template Guide §5). Template Guide를 삭제한 저장소는 이 문서의 값이 유일한 기록입니다. 저장소에 `CHANGELOG.md`가 있으면 판을 올린 사실과 반영한 항목을 한 줄로 남기세요.
