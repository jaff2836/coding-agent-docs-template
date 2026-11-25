# 변경 실행 계획: 템플릿 소유 문서를 `docs/template/`로 분리

## Metadata

- **Change ID:** `2026-11-25-template-owned-docs-folder`
- **Spec:** [02-SPEC.md](./02-SPEC.md) (Accepted, D-023)
- **Global task:** [02-TODO.md](../../02-TODO.md)의 T-075
- **Owner:** Chae Sangwon
- **Baseline:** 설계는 GitLab `main` `65e5f3d`(MR !11 merge). 구현은 T-076이 통합된 뒤의 `main`에서 시작하고, 그때 이 칸을 고칩니다.
- **Integration target:** GitLab `main`과 GitHub `main`의 같은 merge commit fast-forward([TODO Metadata](../../02-TODO.md))
- **Scope:** §1의 파일 범위. 이 변경이 바꾸는 파일을 다른 작업이 동시에 바꾸지 않습니다.

설계는 2026-11-25 합의됐습니다. W-002부터는 T-076(`v3.3.0` release)이 `main`에 통합된 뒤 시작합니다. 아래 체크 완료는 이 브랜치에서의 구현·검증 완료이며 병합·release·지원 검증 완료를 뜻하지 않습니다.

## 1. 구현 순서와 의존성

1. W-001 설계 합의. SPEC §6의 질문에 답을 받고 문서를 고칩니다.
2. 이 설계 branch는 root 문서만 바꾸고 artifact에 들어가지 않으므로 MR 하나로 따로 통합할 수 있습니다(설계 PR #70과 구현 PR #71·#72 선례). 구현은 T-076 `v3.3.0` release가 `main`에 통합된 뒤 그 `main`에서 새 branch로 시작합니다(SPEC §6의 시작과 통합 순서).
3. W-002~W-004는 MR 하나로 통합합니다. locale 검사가 manifest와 파일을, source 검사가 root와 ko skill 사본을 서로 대조하므로 어느 하나만 먼저 넣으면 검사가 실패합니다.
4. 구현 MR은 commit을 둘로 나눕니다. 첫 commit은 `git mv`로 이동만 하고, 둘째 commit이 링크·문구·도구·테스트를 고칩니다. 첫 commit 상태에서는 검사가 실패해도 됩니다.
5. W-005 검증 뒤 MR을 올립니다. 이 변경의 `v4.0.0` release는 별도 작업입니다(SPEC Q5).

## 2. 작업 체크리스트

- [x] **W-001 설계 합의**
  - 범위·변경 파일: 이 폴더의 세 문서, `docs/00-PROJECT.md` §8과 설계 인덱스, `docs/02-TODO.md`
  - 대응 요구사항·상위 완료 조건: SPEC §6 설계 완료
  - 선행조건: 없음
  - 검증 방법: 질문 Q1~Q5의 답과 승인 문구를 Approval에 기록
  - 결과·근거: 2026-11-25 사용자가 "추천안대로"로 답했습니다. INTENT·SPEC을 `Accepted`로 바꾸고 PROJECT에 D-023, TODO에 T-076을 더했습니다. branch `claude/t075-template-docs-folder`의 작업 트리에 기록했고 commit하지 않았습니다.
- [ ] **W-002 payload 이동과 칸 분리**
  - 범위·변경 파일: `locales/en`·`locales/ko`의 `docs/` 여덟 개 이동, 프로젝트 기록 문서(`Template release` 칸 포함) 추가, 네 문서의 Metadata 정리, DOCS_GUIDE 문서 지도·Metadata Convention·체크리스트, TEMPLATE_GUIDE §1 구조·§2 단계·§3 검색 명령·§4 CODEOWNERS·§5, `merge` 정책 문서 `02-TODO.md`·`CI.md`·`REVIEW_ROUND.md`의 링크, `AGENTS.md`, skill 여섯 개 중 경로를 쓰는 것(`design`, `project-analysis`, `bugfix`, `refactor`), `.omp/WATCHDOG.md`, `README.md` 양식. 옮기는 문서에서 지울 수 있는 경로로 가는 링크를 코드 경로로 바꾸고, 선택 파일 삭제 안내를 프로젝트 소유 문서의 링크로 좁힙니다(SPEC §3.3). placeholder 검색 선언과 두 명령을 TEMPLATE_GUIDE §3에서 DOCS_GUIDE로 옮기고, TEMPLATE_GUIDE §5의 "삭제 전에 선언을 보관한다" 안내를 지웁니다
  - 대응 요구사항·상위 완료 조건: R-001~R-005, R-011
  - 선행조건: W-001, T-076의 `main` 통합
  - 검증 방법: `check-locales.py --require-stable`, en·ko export 결과물의 `check-docs.py`
  - 결과·근거:
- [ ] **W-003 검사기와 도구**
  - 범위·변경 파일: SPEC §3.4의 표 전체, 파일명 참조의 대체 규칙(SPEC §3.4)과 해당 테스트
  - 대응 요구사항·상위 완료 조건: R-002, R-005~R-008, R-011
  - 선행조건: W-002와 같은 MR
  - 검증 방법: `unittest discover -s tests`, `unittest discover -s template/common/tests`. R-002·R-006·R-011의 새 사례는 규칙을 잠시 되돌려 실패를 확인(red-green). R-006에는 `docs/template/DESIGN.md`만 있는 저장소의 `01-DESIGN.md §1` 사례를 넣습니다
  - 결과·근거:
- [ ] **W-004 root 유지관리 영역**
  - 범위·변경 파일: root `docs/template/`, root skill 사본, root `README.md`·`README.ko.md`에서 source guide로 가는 링크, root DOCS_GUIDE·TEMPLATE_GUIDE 보충 문서, root `AGENTS.md`, 이력 문서의 링크 27개와 절 참조 10개, 이 변경 폴더의 링크 4개(SPEC §3.5). 구현할 때 다시 세어 그 뒤에 생긴 참조도 포함합니다. README의 `artifact/docs/TEMPLATE_GUIDE.md` 안내는 `latest` release로 받은 artifact 안의 경로라 여기서 바꾸지 않습니다. `v4.0.0` 공개 뒤의 기록 작업에서 바꿉니다(§5, T-051 선례)
  - 대응 요구사항·상위 완료 조건: R-009
  - 선행조건: W-002와 같은 MR
  - 검증 방법: 무인자 `scripts/check-docs.py`, 이력 문서 diff가 링크 목적지와 절 번호 앞의 경로·파일명에만 있는지 확인
  - 결과·근거:
- [ ] **W-005 업그레이드 E2E**
  - 범위·변경 파일: 없음(검증만)
  - 대응 요구사항·상위 완료 조건: R-010
  - 선행조건: W-002~W-004
  - 검증 방법: `v3.2.0`으로 만든 적용 저장소 사본에 이 head의 로컬 package로 `adopt --base-version 3.2.0`을 돌려, SPEC §5 표의 경우마다 분류를 확인합니다. 옛 문서를 고치지 않은 사본, 고친 사본, `TEMPLATE_GUIDE.md`를 지운 사본, 새 경로에 파일이 있는 사본, `docs/template/`에 inventory 밖 파일이 있는 사본, `docs/TEMPLATE_RECORD.md`가 이미 있는 사본, skill에 의도한 수정이 있는 사본이 대상입니다. 그 뒤 SPEC §5의 절차대로 옮기고 확인합니다. 새 경로의 기존 내용과 inventory 밖 파일이 보존됐는지, 기존 `TEMPLATE_RECORD.md`가 제자리에서 병합됐는지, 지웠던 `TEMPLATE_GUIDE.md`가 다시 생기지 않았는지, 의도한 수정이 다시 적용됐는지, 프로젝트 기록의 `Template source`·`Template revision`이 새 원본이고 이전 값이 「이전 기준」에 있는지, 그 저장소의 `check-docs.py`가 통과하는지입니다.
  - 결과·근거:

## 3. 검증 기록

| 대상 작업·요구사항 | 확인한 revision 또는 작업 트리 범위 | 실행한 검사 | 결과·남은 한계 |
|---|---|---|---|
| 없음 | — | — | 구현 전 |

## 4. 변경·재검증 기록

- 2026-11-25: 최초 작성. SPEC이 `Draft`라 구현을 시작하지 않았습니다.
- 2026-11-25: W-001 완료. SPEC Q5에 따라 §1에 T-076 선행 단계를 넣고 W-002의 선행조건과 Baseline을 고쳤습니다.
- 2026-11-25: MR !12 리뷰 라운드 1의 지적을 따라 W-002~W-005에 R-011, 파일명 참조 대체 규칙, 이 폴더의 링크, 업그레이드 경우별 분류를 더했습니다(SPEC §7).
- 2026-11-25: 리뷰 라운드 2의 지적을 따라 W-004에 이력 문서의 절 참조 10개를, W-005에 보존·재적용·원본 갱신 확인을 더했습니다(SPEC §7).
- 2026-11-25: 리뷰 라운드 3의 지적을 따라 W-002에 placeholder 검색 선언의 이동을 더했습니다(SPEC §7).
- 2026-11-25: 리뷰 라운드 4의 지적을 따라 W-005에 inventory 밖 파일, 기존 `TEMPLATE_RECORD.md`, 지웠던 `TEMPLATE_GUIDE.md`의 경우를 더했습니다(SPEC §7).
- 2026-11-25: 리뷰 라운드 5의 지적을 따라 W-002의 프로젝트 기록에 `Template release` 칸을 더했습니다(SPEC §7).
- 2026-11-25: 리뷰 라운드 6의 지적을 따라 root README의 release artifact 안내를 W-004에서 빼고 `v4.0.0` 공개 뒤로 옮겼습니다(§5, SPEC §5·§7).
- 2026-11-25: T-076의 판을 `v3.3.1`로 바꿨습니다. 2026-11-25 `v3.3.0` tag가 판 번호를 올리기 전 commit에 잘못 만들어져 그대로 두었기 때문입니다(TODO T-076). 이 문서의 `v3.3.0`은 그 release(T-076)를 가리킵니다.

## 5. 인계

- 선행 release는 TODO의 T-076(`v3.3.0`, T-071~T-074 공개)입니다.
- 이 변경의 `v4.0.0` release는 T-075가 통합된 뒤 TODO에 등록합니다. 그 작업이 [locale TEMPLATE_GUIDE](../../../locales/ko/docs/TEMPLATE_GUIDE.md) §6에 옛 경로→새 경로 표와 SPEC §5의 업그레이드 절차를 적습니다.
- root README의 `artifact/docs/TEMPLATE_GUIDE.md` 안내는 `v4.0.0`이 Latest로 공개된 뒤의 기록 작업에서 새 경로로 바꿉니다. 그 전까지 `latest`는 옛 경로의 `v3.3.0` artifact를 받기 때문입니다.
