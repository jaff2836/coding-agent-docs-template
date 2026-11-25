# 변경 의도: 템플릿 소유 문서를 `docs/template/`로 분리

## Metadata

- **Change ID:** `2026-11-25-template-owned-docs-folder`
- **Status:** Accepted
- **Originator:** Chae Sangwon
- **Source:** 2026-11-25 대화. 사용자 질문: "혹시 실제 프로젝트에서 사용될 파일이 아닌, 템플릿에 의해 설치되고 읽기만 하는 파일에 대해서는 /docs 가 아니라 /docs/template 폴더 안에 넣을 수 있나? 아니면 폴더 위치/이름 추천해 줘. 같이 있으니 헷갈리는데." 분석 결과를 보고한 뒤 "이 안으로 변경 문서 초안을 쓸까요?"라는 질문에 사용자가 "초안 쓰기"로 답했습니다.
- **Parent:** [제품 기준](../../00-PROJECT.md)의 D-002(locale artifact 구조), D-006(adoption policy), D-009(문서 소유권)
- **Approval:** Chae Sangwon, 2026-11-25 대화. Draft를 보고한 뒤 "SPEC의 질문 다섯 개를 추천안대로 정할까요?"라는 질문에 "추천안대로"로 답했습니다.
- **Spec:** [02-SPEC.md](./02-SPEC.md)

## 1. 문제

- 적용 저장소의 `docs/`에는 프로젝트가 쓰는 문서와 템플릿이 설치만 하는 문서가 섞여 있습니다. 파일 트리만으로는 어느 쪽인지 알 수 없습니다. 구분 기준은 `locales/manifest.json`의 adoption policy인데, 적용 저장소에는 manifest가 없습니다.
- 템플릿 소유(`copy`) 문서 네 개(`01-DESIGN.md`, `DOCS_GUIDE.md`, `TEMPLATE_GUIDE.md`, `CHANGELOG_GUIDE.md`)에도 프로젝트가 채우는 칸이 있습니다. `Owner`, `Last reviewed`, `Template source`, `Template revision`과 DOCS_GUIDE의 「템플릿 적용 기록」 절입니다. 그래서 업그레이드할 때 이 문서들을 artifact 판으로 통째로 바꿀 수 없습니다. 지금은 artifact 판에서 시작해 이 칸들을 손으로 옮겨야 합니다.
- 복사용 양식 `docs/changes/_template/`이 실제 변경 폴더와 같은 디렉터리에 있습니다. 그래서 `project-analysis`, `bugfix`, `refactor` skill과 DOCS_GUIDE가 "양식은 실제 작업으로 집계하지 않는다"는 예외를 따로 적어야 합니다.

## 2. 기대 결과

- `docs/` 바로 아래에는 프로젝트가 쓰는 문서만 남습니다. 템플릿이 설치하고 프로젝트가 읽기만 하는 문서는 한 폴더에 모입니다.
- 그 폴더는 artifact와 byte 단위로 같습니다. 업그레이드는 폴더를 새 판으로 바꾸는 것으로 끝나고, 프로젝트가 채운 값은 폴더 밖에서 그대로 유지됩니다.
- `docs/changes/` 아래에는 실제 변경 폴더만 있습니다.
- 위 구분을 파일 트리와 문서 지도 양쪽에서 확인할 수 있습니다.

## 3. 범위와 비범위

### 범위

- en·ko payload의 `copy` 문서 네 개와 변경 양식 네 개의 위치, 그 문서들에서 프로젝트가 채우는 칸을 옮길 곳
- 이 경로를 쓰는 skill, `AGENTS.md`, `README.md` 양식, 안내 문서, `merge` 정책 문서(`02-TODO.md`, `CI.md`, `REVIEW_ROUND.md`)의 링크, `.omp/WATCHDOG.md`, root README의 참조
- manifest의 inventory·adoption policy·skill 계약, payload 검사기(`check-docs.py`), locale 검사기, installer의 안내 경로 상수, packager·release 검증기와 테스트
- 이 저장소 root 유지관리 영역의 같은 구조와 이력 문서의 링크
- 기존 적용 저장소의 업그레이드 안내

### 비범위

- `merge` 정책 문서(`REVIEW.md`, `REVIEW_ROUND.md`, `CI.md`, `00-PROJECT.md`, `02-TODO.md`)와 `decide` 정책 문서(`10-EXTENSION.md`)의 위치
- `docs/` 밖의 템플릿 소유 파일(skill, `scripts/check-docs.py`, `tests/test_check_docs.py`)의 위치. 도구가 고정 경로로 읽습니다.
- installer가 경로 이동을 자동으로 처리하는 기능. 지금처럼 report만 만들고 자동 merge·삭제를 하지 않습니다.
- 이 변경의 release 자체. version·release note·CHANGELOG는 별도 release 작업에서 합니다.

## 4. 제약

- `docs/REVIEW.md`는 고정 경로입니다. Bugbot 사본 대조(`check-docs.py`의 `INVARIANT_SOURCE`), OMP의 `@../docs/REVIEW.md` import, `pr-review`의 base 정책 읽기가 이 경로를 씁니다.
- en·ko artifact는 같은 경로 집합을 가집니다. 두 도구 경로의 skill 사본은 byte 동일하고, root skill 사본은 ko payload와 byte 동일합니다(D-021).
- installer는 기존 파일을 덮어쓰지 않고, `adopt`는 대상 저장소에 쓰지 않습니다(D-006, D-008).
- 이미 게시한 tag와 release asset은 바꾸지 않습니다(D-004).
- production dependency를 더하지 않습니다.
- 과거 변경 문서와 완료 기록의 본문은 고치지 않습니다. 검사기가 따라가는 참조의 경로·파일명만 새 이름으로 고칩니다. 링크 목적지와, 경로나 파일명 뒤에 절 번호를 붙인 참조입니다(2026-11-25 변경, §6).

## 5. 미해결 질문

남은 질문은 없습니다. 프로젝트 기록의 위치, 양식 폴더, `01-DESIGN.md`의 이름, root 구조, release 순서와 version은 2026-11-25 사용자가 [02-SPEC.md](./02-SPEC.md) §6의 추천안으로 정했습니다.

## 6. 변경 기록

- 2026-11-25: 최초 작성(Draft).
- 2026-11-25: SPEC §6의 질문 다섯 개가 "추천안대로" 정해져 Status를 `Accepted`로 바꿨습니다. 결정은 PROJECT §8의 D-023입니다.
- 2026-11-25: §4의 이력 문서 제약을 바꿨습니다. 처음에는 "깨지는 링크의 목적지만 고친다"였는데, 이력 문서에는 링크가 아니어도 검사기가 따라가는 참조(`` `docs/TEMPLATE_GUIDE.md` §2`` 같은 경로·파일명 뒤 절 번호)가 있어 파일을 옮기면 root 검사가 실패합니다. MR !12 리뷰 라운드 2의 지적입니다. 사용자가 "이력 문서의 참조 경로 수정을 허용하고 라운드를 이어갈까요?"에 "허용하고 계속"으로 승인했습니다.
