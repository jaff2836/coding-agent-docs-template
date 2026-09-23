# Maintainer 문서 운영 보충 안내

> 적용 프로젝트의 일반 문서 운영 정본은 locale별
> [영문](../locales/en/docs/DOCS_GUIDE.md)·[한국어](../locales/ko/docs/DOCS_GUIDE.md)
> 가이드입니다. 이 문서는 source 저장소 maintainer에게만 필요한 경계를
> 기록합니다.

## Metadata

- **Status:** Active
- **Template version:** 2.3.2
- **Template source:** https://github.com/jaff2836/coding-agent-docs-template
- **Template revision:** release 검증 시 exact source commit으로 확정
- **Owner:** Chae Sangwon
- **Last reviewed:** 2026-09-22
- **Review cadence:** maintainer 문서 체계 또는 source·artifact 소유권 변경 시

## 1. Maintainer 문서 지도

| 문서 | 책임 |
| ---- | ---- |
| [00-PROJECT.md](./00-PROJECT.md) | 현재 제품 기준, 결정과 상세 설계 인덱스 |
| [01-DESIGN.md](./01-DESIGN.md) | 구조·공개 계약 변경의 합의 절차 |
| [02-TODO.md](./02-TODO.md) | 전역 변경·마일스톤·통합 상태 |
| `docs/changes/<change-ID>/` | 변경별 Intent·Spec과 필요한 PLAN |
| [REVIEW.md](./REVIEW.md) | PR 리뷰 판단 기준 |
| [REVIEW_ROUND.md](./REVIEW_ROUND.md) | 명시적으로 시작한 리뷰 라운드 절차 |
| [CI.md](./CI.md) | runner 불문의 품질 게이트와 연결 확인 |
| [TEMPLATE_GUIDE.md](./TEMPLATE_GUIDE.md) | source·artifact·배포 유지관리 보충 규칙 |
| [CHANGELOG.md](../CHANGELOG.md) | 공개 완료된 영문 릴리스 이력 |
| [CHANGELOG.ko.md](../CHANGELOG.ko.md) | 공개 완료된 한국어 릴리스 이력 |

locale source의 가이드는 artifact 정본입니다. root maintainer 가이드는 locale
본문을 번역·복제하지 않습니다.

## 2. 식별자와 정보의 정본

- 전역 결정은 PROJECT §8의 `D-nnn`, 전역 작업은 TODO의 `T-nnn`, 변경 내부
  요구·작업은 해당 변경 폴더의 `R-nnn`·`W-nnn` 등으로 구분합니다.
- 병렬 branch가 같은 전역 번호를 사용하면 먼저 통합된 번호를 유지하고 다른
  branch만 재번호합니다. 변경-ID는 재번호하지 않습니다.
- 제품 현재 기준과 결정 위치는 PROJECT, 변경 요청·계약은 변경 문서, 상세
  실행 상태는 PLAN(없으면 TODO 항목), 공개 이력은 CHANGELOG가 소유합니다.
- README는 현재 사용법, TODO·PLAN은 미래 작업을 소유합니다. 같은 체크리스트나
  릴리스 이력을 여러 문서에 복제하지 않습니다.

## 3. 실행·통합·인계

- 설계 승인, branch 구현·검증, PR 통합, release 공개와 consumer 지원 검증을
  별도 상태로 기록합니다.
- PLAN 완료는 해당 branch의 구현·검증 완료입니다. 전역 TODO 완료는 지정한
  integration target에 실제 반영됐는지도 확인합니다.
- 문서 작성이나 check 완료는 commit·push·merge·배포 권한을 만들지 않습니다.
- 다른 branch가 먼저 통합됐으면 파일 충돌뿐 아니라 공유 계약과 검증 전제를
  대조합니다. 관련 없는 사용자 변경을 덮어쓰지 않습니다.
- 리뷰 라운드 통과 후 tracked head는 동결하고, 후속 기록은 다음 관련 작업의
  인계 절차에 따라 반영합니다.

## 4. Root와 locale 가이드 소유권

- locale `TEMPLATE_GUIDE.md`와 `DOCS_GUIDE.md`는 적용 프로젝트가 읽는 정본이며
  en·ko 의미 parity를 유지합니다.
- locale `CHANGELOG_GUIDE.md`는 적용 프로젝트의 선택형 release note 규칙을
  소유합니다. 실제 changelog는 프로젝트 소유이므로 artifact inventory에
  포함하지 않습니다.
- root의 두 guide는 maintainer 전용 addendum입니다. locale의 적용 절차,
  checklist 또는 version history를 root에 수동 복제하지 않습니다.
- `Template version`은 두 root guide와 각 locale의 두 guide에서 release 대상
  version을 맞춥니다. exact source revision은 release gate에서 검증합니다.
- 문서 Metadata는 그 문서의 상태·책임만 나타냅니다. 독립적으로 배포되는
  runtime skill에는 프로젝트별 Owner·검토일 placeholder를 넣지 않습니다.

## 5. Maintainer 체크리스트

- [ ] 사용자 승인 범위와 관련 change 문서·TODO만 갱신했다.
- [ ] manifest inventory와 adoption policy가 모든 locale에 닫혀 있다.
- [ ] en·ko 가이드 의미와 skill 사본 byte identity를 확인했다.
- [ ] root maintainer 문서가 locale 적용 안내를 복제하지 않는다.
- [ ] README·CHANGELOG·TODO/PLAN의 현재·과거·미래 경계를 유지했다.
- [ ] `python3 scripts/check-docs.py`와 checker 회귀 테스트를 통과했다.
- [ ] `python3 scripts/check-locales.py --require-stable`을 통과했다.
- [ ] en·ko artifact를 export하고 artifact 자체 checker·tests를 실행했다.
- [ ] release라면 clean exact commit의 candidate·published gate와 asset
  provenance를 각각 확인했다.

문서 이동·이름 변경 시 들어오는 링크와 코드·테스트·도구 참조를 함께
갱신합니다. source revision 비교와 비파괴 이관은
[TEMPLATE_GUIDE.md](./TEMPLATE_GUIDE.md) §5를 따릅니다.
