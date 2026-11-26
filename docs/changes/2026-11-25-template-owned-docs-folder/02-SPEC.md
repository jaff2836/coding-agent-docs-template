# 변경 명세: 템플릿 소유 문서를 `docs/template/`로 분리

## Metadata

- **Change ID:** `2026-11-25-template-owned-docs-folder`
- **Status:** Accepted
- **Intent:** [01-INTENT.md](./01-INTENT.md)
- **Parent:** [제품 기준](../../00-PROJECT.md)의 D-002, D-006, D-009. 기준 revision은 GitLab `main` `65e5f3d`
- **Decision:** PROJECT §8의 D-023
- **Approval:** Chae Sangwon, 2026-11-25 대화. §6의 질문 다섯 개에 "추천안대로". Q5의 `v3.3.0` 범위는 그 뒤 §7처럼 바로잡았습니다.
- **Execution:** [03-PLAN.md](./03-PLAN.md)

## 1. 요구사항과 시나리오

| 요구사항 ID | 요구사항 | 상황·입력 | 관찰 가능한 결과 | 검증 방법 |
|---|---|---|---|---|
| R-001 | 템플릿 소유 문서 네 개와 변경 양식 네 개가 `docs/template/` 아래에 있고 옛 경로에는 없다. en·ko가 같은 경로를 가진다 | en·ko export | inventory가 §3.1 표의 새 경로와 일치하고 옛 경로가 없다 | `tests/test_export_template.py`, `check-locales.py --require-stable` |
| R-002 | `docs/template/` 바로 아래의 안내 문서 네 개에는 프로젝트가 채우는 칸이 없다. 복사용 양식(`docs/template/changes/`)은 제외한다. 양식의 칸(`Owner` 등)은 복사한 변경 폴더에서 채우고 양식 자체는 고치지 않는다 | payload의 `docs/template/*.md`에 `Owner`, `Last reviewed`, `Template source`, `Template revision` 칸이나 「템플릿 적용 기록」 절을 다시 넣음 | locale 검사가 실패한다 | `tests/test_check_locales.py`의 새 사례(red-green) |
| R-003 | 프로젝트가 채우는 값은 프로젝트 소유 문서 `docs/TEMPLATE_RECORD.md`(§3.2)에 모이고 adoption policy는 `merge`다 | 새 프로젝트에 `install` | 그 문서에 source·revision·`Template release`·적용 기록 칸이 있고, DOCS_GUIDE의 placeholder 검색이 그 문서의 미작성 칸을 찾으며 검색 선언 자체는 찾지 않는다(§3.3) | export inventory, placeholder 검색 명령 실행 |
| R-004 | 적용 안내가 `docs/template/`을 artifact 판으로 통째로 바꾸는 폴더로 정의한다. 허용하는 차이는 `TEMPLATE_GUIDE.md` 삭제와 프로젝트 기록에 적은 수정 두 가지다(§3.3) | DOCS_GUIDE·TEMPLATE_GUIDE 읽기 | 문서 지도에 소유 구분이 있고, 업그레이드 절차가 폴더 교체로 적혀 있다 | 문서 검토 |
| R-005 | 변경 양식의 링크는 양식 위치와 복사한 위치(`docs/changes/<변경-ID>/`) 양쪽에서 같은 파일을 가리킨다 | 양식 네 개를 `docs/changes/example/`로 복사한 artifact | `check-docs.py`가 통과한다 | `template/common/tests/test_check_docs.py`의 새 사례 |
| R-006 | 검사기가 `docs/template/`의 문서를 짧은 이름으로 찾는다. 옛 경로를 가리키는 파일명 참조는 새 문서로 풀리지 않고 실패한다(§3.4의 대체 규칙) | `DESIGN §3` 같은 이름 참조, `docs/template/DESIGN.md`만 있는 저장소의 `01-DESIGN.md §1`, `docs/changes/x/`에서 쓴 `00-PROJECT.md §8` | 첫째는 절 번호까지 검사되고, 둘째는 "document target does not exist"로 실패하고, 셋째는 지금처럼 `docs/00-PROJECT.md`로 풀린다 | `template/common/tests/test_check_docs.py`의 새 사례(red-green) |
| R-007 | 판 번호 검사와 release 이력 검사가 새 경로를 읽고, `TEMPLATE_GUIDE.md`를 지운 저장소에서도 동작한다 | `docs/template/DOCS_GUIDE.md`만 있는 artifact | `Template version` 검사가 DOCS_GUIDE만으로 통과한다 | 기존 생략 허용 테스트의 경로 갱신 |
| R-008 | installer, packager, release 검증기, locale 검사기가 새 경로를 쓴다 | `adopt` 실행, `package-release.py`, `verify-release.py candidate` | plan의 `guide`가 `artifact/docs/template/TEMPLATE_GUIDE.md §2`이고, packager가 두 guide의 판 번호를 새 경로에서 읽는다 | `tests/test_install_release.py`, `tests/test_package_release.py`, `tests/test_verify_release.py` |
| R-009 | root 유지관리 영역도 같은 구조이며 root skill 사본은 ko payload와 byte 동일하다. 과거 기록은 검사기가 따라가는 참조의 경로·파일명만 바뀐다 | 무인자 `scripts/check-docs.py` | 통과한다. 이력 문서의 diff는 링크 목적지와 절 번호 앞의 경로·파일명에만 있다 | 무인자 source 검사, diff 검토 |
| R-010 | 이전 판을 base로 한 업그레이드에서 옛 경로와 새 경로가 모두 report에 나오고, 대상 상태별 분류가 §5의 표와 같다 | v3 적용 저장소에 `adopt --base-version <v3 판>`. 옛 문서를 고치지 않은 저장소, 고친 저장소, `TEMPLATE_GUIDE.md`를 지운 저장소, 새 경로에 이미 파일이 있는 저장소 | 각 경우가 §5 표의 분류로 나온다 | 로컬 package로 만든 E2E(PLAN W-005) |
| R-011 | `docs/template/` 아래 문서는 지울 수 있는 경로를 Markdown 링크로 가리키지 않고, 그 경로나 파일명 뒤에 절 번호를 붙이지도 않는다. 지울 수 있는 경로는 `decide` 정책 파일(`LICENSE`, `docs/10-EXTENSION.md`, `.cursor/BUGBOT.md`, `.omp/WATCHDOG.md`)과 `docs/template/TEMPLATE_GUIDE.md`다 | 이 파일들을 모두 지운 en·ko artifact | `docs/template/`을 고치지 않고도 `check-docs.py`가 통과한다 | locale 검사의 새 사례(링크와 경로·파일명 절 참조를 모두 거부)와 지운 artifact의 검사 실행(red-green) |

`R-nnn`은 이 변경 폴더 안에서만 고유합니다. R-010의 분류는 `scripts/installer.py`의 `_upgrade_status`를 읽고 낸 추론이었고, 2026-11-26 PLAN W-005에서 실행해 확인했습니다.

## 2. 대안과 선택 이유

- **변경하지 않음(기각):** 섞여 보이는 문제가 그대로입니다. 업그레이드 때 `copy` 문서의 칸을 손으로 옮기는 일도 남습니다.
- **소유 열만 추가(대안으로 남김):** 경로는 두고 DOCS_GUIDE 문서 지도에 "소유(템플릿/병합/프로젝트)" 열을 더합니다. 계약이 바뀌지 않아 minor 안에서 할 수 있습니다. 파일 트리는 여전히 섞여 보이고, 칸을 옮기는 업그레이드 부담도 그대로입니다. 사용자가 비용을 줄이기로 하면 이 안으로 바꿉니다.
- **칸을 그대로 두고 옮기기만 함(기각):** 폴더 안 문서를 프로젝트가 계속 고치므로 "읽기만 한다"가 사실이 아니고, 통째로 바꿀 수도 없습니다.
- **템플릿이 준 절차 문서를 모두 옮김(기각):** `REVIEW.md`, `REVIEW_ROUND.md`, `CI.md`는 `merge` 정책이고 프로젝트 절이 있습니다(REVIEW §6·§9, REVIEW_ROUND §2.1). `docs/REVIEW.md`는 §1.4의 고정 경로입니다.
- **내용으로 지은 이름(`docs/process/`, `docs/guides/`)(기각):** `REVIEW_ROUND.md`도 절차인데 밖에 남습니다. 나누는 기준이 소유이므로 이름도 소유를 나타냅니다.
- **숨김 폴더(`.template/` 등)(기각):** 사람과 도구가 문서를 덜 보게 되고, `AGENTS.md`의 링크가 숨김 경로를 가리킵니다.
- **선택:** `docs/template/`에 템플릿 소유 문서와 양식을 모으고, 프로젝트가 채우는 칸은 프로젝트 소유 문서로 뺍니다. 사용자가 제안한 이름입니다.

## 3. 설계와 계약

이 절의 DOCS_GUIDE·TEMPLATE_GUIDE는 locale payload의 문서입니다. root의 같은 이름 문서는 maintainer 보충 문서이며 §3.5에서 따로 다룹니다.

### 3.1 경로

| 지금 | 옮긴 뒤 | policy |
|---|---|---|
| `docs/01-DESIGN.md` | `docs/template/DESIGN.md` (Q3) | `copy` |
| `docs/DOCS_GUIDE.md` | `docs/template/DOCS_GUIDE.md` | `copy` |
| `docs/TEMPLATE_GUIDE.md` | `docs/template/TEMPLATE_GUIDE.md` | `copy` |
| `docs/CHANGELOG_GUIDE.md` | `docs/template/CHANGELOG_GUIDE.md` | `copy` |
| `docs/changes/_template/01-CHANGE.md` 외 세 개 | `docs/template/changes/01-CHANGE.md` 외 세 개 (Q2) | `copy` |
| 없음 | 프로젝트 기록 문서 `docs/TEMPLATE_RECORD.md` (Q1) | `merge` |

- `docs/`에 남는 것: `00-PROJECT.md`, `02-TODO.md`, `10-EXTENSION.md`(선택), `REVIEW.md`, `REVIEW_ROUND.md`, `CI.md`, 프로젝트 기록 문서, `changes/<변경-ID>/`.
- `01`을 비워 둡니다. `02-TODO.md`를 `01`로 당기지 않습니다(§3.6의 참조 수).
- `docs/template/changes/`는 `docs/changes/<변경-ID>/`와 깊이가 같습니다. 양식이 `../../00-PROJECT.md`와 `../../template/DESIGN.md`로 쓰면 두 위치에서 같은 파일을 가리킵니다(R-005).
- 옮기는 문서 안의 상대 링크는 한 단계 깊어집니다(예: `./00-PROJECT.md` → `../00-PROJECT.md`, `../README.md` → `../../README.md`).

### 3.2 프로젝트가 채우는 칸

| 칸 | 지금 | 옮긴 뒤 |
|---|---|---|
| `Template version` | DOCS_GUIDE·TEMPLATE_GUIDE Metadata. 템플릿이 씁니다 | 그대로. 폴더 내용의 판 번호입니다 |
| `Template source`, `Template revision` | 두 guide Metadata. 프로젝트가 채웁니다 | 프로젝트 기록 문서 |
| 「템플릿 적용 기록」 절 | DOCS_GUIDE | 프로젝트 기록 문서 |
| TEMPLATE_GUIDE를 지울 때 보관하는 placeholder 검색 선언 | "DOCS_GUIDE 같은 프로젝트 소유 문서"([ko TEMPLATE_GUIDE](../../../locales/ko/docs/template/TEMPLATE_GUIDE.md) §5) | 보관할 필요가 없어집니다. 선언과 두 검색 명령을 DOCS_GUIDE로 옮깁니다(§3.3) |
| `Owner`, `Last reviewed` | 네 문서 Metadata | 지웁니다. D-009에서 `project-analysis`의 프로젝트별 Metadata를 지운 것과 같은 이유입니다 |
| `Status`, `Review cadence` | 네 문서 Metadata | 그대로. 템플릿이 정한 값입니다 |

- `Template version`은 폴더 안에만 둡니다. 폴더를 바꾸면 판 번호도 함께 바뀌고, 프로젝트 기록에는 판 번호를 다시 적지 않습니다(두 곳에 두면 어긋납니다).
- 적용한 원본이 exact release가 아닐 수 있습니다. tag 이후 commit, tag 없는 원본, source checkout에서 export한 artifact, 미커밋 변경을 포함한 경우입니다. 이때 폴더 안의 `Template version`은 원본 파일에 적힌 값 그대로 두고, 프로젝트 기록의 `Template release` 칸에 그 사실을 적습니다. 값은 지금 TEMPLATE_GUIDE의 규칙과 같습니다(`미릴리스 (최근 tag: v1.2)` 또는 `미릴리스 (tag 없음)`). 미커밋 변경은 `Template revision`의 `미확정 (…)`으로 적습니다. exact release면 `release`로 둡니다.
- 프로젝트 기록의 `Template source`·`Template revision`은 지금 적용한 판의 원본을 가리킵니다. 업그레이드할 때 이전 값은 「이전 기준」에 남기고 두 칸을 새 원본으로 고칩니다(§5).
- DOCS_GUIDE의 Metadata Convention과 체크리스트의 "Owner·검토 주기·날짜를 기록했다"는 프로젝트 소유 문서에만 적용하도록 고칩니다.

### 3.3 소유 규칙

- `docs/template/` 아래는 artifact와 byte 단위로 같습니다. 업그레이드는 이 폴더의 파일을 새 artifact 판으로 바꾸는 것입니다. 이 폴더에는 artifact의 파일만 두고 프로젝트 파일은 두지 않습니다. 업그레이드 전부터 있던 inventory 밖 파일은 옮깁니다(§5).
- 허용하는 차이는 두 가지입니다. 하나는 `TEMPLATE_GUIDE.md` 삭제(지금의 생략 허용을 유지)이고, 다른 하나는 프로젝트 기록의 「템플릿 소유 파일의 수정」에 적은 수정(아래 넷째 항목)입니다. 수정한 파일은 업그레이드 때 artifact 판에서 시작해 그 수정을 다시 적용합니다(§5 4단계). 그 밖의 차이는 두지 않습니다.
- 선택 파일을 지우는 보통의 적용에서는 이 폴더를 고칠 일이 없어야 합니다. 그래서 이 폴더의 문서는 지울 수 있는 경로를 링크 대신 코드 경로(`` `docs/10-EXTENSION.md` ``)로 적습니다(R-011). 2026-11-25 `65e5f3d`의 ko 기준으로 지금 그렇게 링크하는 곳은 18개입니다(`01-DESIGN.md` 3개, `DOCS_GUIDE.md` 4개, `TEMPLATE_GUIDE.md` 11개). en도 같은 수입니다.
- 코드 경로라도 뒤에 절 번호가 붙으면 검사기가 따라갑니다. `SECTION_PATH_RE`는 inline code 안의 `` `<경로>.md` §n``을, `SECTION_FILENAME_RE`는 `TEMPLATE_GUIDE.md §n`을 찾고, 대상이 없으면 실패로 보고합니다. 그래서 지울 수 있는 문서의 절은 제목(예: TEMPLATE_GUIDE의 「외부 방법론·행동 규칙 도구」)이나 짧은 이름(`TEMPLATE_GUIDE §4`)으로 가리킵니다. 짧은 이름 참조는 대상이 없으면 검사기가 건너뜁니다(§3.4). 지금 `01-DESIGN.md`의 `[TEMPLATE_GUIDE.md](./TEMPLATE_GUIDE.md) §4`가 이 경우입니다.
- 선택 파일을 지울 때 "들어오는 링크도 지운다"는 지금의 안내(DOCS_GUIDE 「번호와 파일 수」와 체크리스트, TEMPLATE_GUIDE §2 5단계와 §5)는 프로젝트 소유 문서의 링크만 가리키도록 고칩니다.
- 그 밖의 이유로 이 폴더의 파일을 고쳐야 했다면 프로젝트 기록의 「템플릿 소유 파일의 수정」에 남기고, 다음 업그레이드에서 다시 적용합니다. 예를 들어 기존 `REVIEW.md`와 병합해 절 번호가 바뀌어, `DESIGN.md`의 `REVIEW.md §6` 참조를 고쳐야 하는 경우입니다. 지금 DOCS_GUIDE에 있는 규칙과 같습니다.
- 이 규칙은 검사로 강제하지 않습니다. 적용 저장소에는 비교할 artifact가 없습니다. [ko TEMPLATE_GUIDE](../../../locales/ko/docs/template/TEMPLATE_GUIDE.md) §4의 CODEOWNERS 목록에 `docs/template/`을 넣어 보호를 권합니다.
- [ko TEMPLATE_GUIDE](../../../locales/ko/docs/template/TEMPLATE_GUIDE.md) §3의 placeholder 검색은 두 guide 파일 대신 `docs/template/`을 통째로 제외합니다. 프로젝트 기록 문서는 검색 대상에 남습니다.
- 검색 선언(`template_placeholder_pattern`)과 두 검색 명령은 TEMPLATE_GUIDE §3에서 DOCS_GUIDE로 옮기고, TEMPLATE_GUIDE는 그 절을 가리킵니다. 선언 문자열에는 패턴 자체(`프로젝트에 맞게 작성` 등)가 들어 있어 검색 대상 문서에 두면 자기 자신이 걸립니다. DOCS_GUIDE는 지울 수 없고 검색에서 제외되므로 그런 일이 없고, TEMPLATE_GUIDE를 지울 때 따로 보관할 것도 없어집니다. `check_locales.py`가 선언을 정확히 한 번 찾는 문서도 DOCS_GUIDE로 바꿉니다(§3.4).

### 3.4 검사기와 도구

| 위치 | 바뀌는 것 |
|---|---|
| `template/common/scripts/check-docs.py` | `HISTORY_PATH`, `check_versions`의 두 guide 경로와 오류 문구, `doc_short_names`가 `docs/template/*.md`도 모음, 파일명 참조의 대체 규칙(아래) |
| `scripts/check-docs.py` (root wrapper) | 인자가 있을 때 되돌리는 `HISTORY_PATH` |
| `scripts/check_locales.py` | `design` skill 계약의 `skill_links`·`document`, guide 대조 경로, root maintainer guide가 가리키는 locale guide 경로, placeholder 검색 선언을 찾는 문서(TEMPLATE_GUIDE → DOCS_GUIDE), R-002·R-011 검사 |
| `locales/manifest.json` | localized inventory(옛 경로 여덟 개 → 새 경로 여덟 개와 프로젝트 기록 문서), adoption policy, `contracts.skills`의 `design` 문서 경로, `contracts.section_markers`의 `release-history`와 `contracts.required_commands` 일곱 항목이 가리키는 두 guide 경로 |
| `scripts/installer.py` | `ADOPTION_GUIDE` 상수. adoption plan의 `guide` 값이 바뀝니다(plan 형식은 `stability: experimental`) |
| `scripts/package_release.py` | 판 번호를 읽는 두 guide 경로 |
| `scripts/verify_release.py` | plan `guide` 대조 값 |
| `tests/`, `template/common/tests/` | 경로 갱신과 R-002·R-005·R-006·R-011의 새 사례 |

- `doc_short_names`는 `docs/*.md`와 `docs/template/*.md`만 봅니다. `docs/template/changes/`의 양식은 넣지 않습니다. 문서에서 `SPEC §3`이라고 쓰면 각 변경의 SPEC을 뜻하므로, 양식으로 풀면 다른 파일의 절을 검사하게 됩니다. 지금의 `docs/changes/_template/`도 짧은 이름에 들어가지 않습니다.
- 새 짧은 이름(`DESIGN`, `DOCS_GUIDE`, `TEMPLATE_GUIDE`, `CHANGELOG_GUIDE`)은 `docs/`의 이름과 겹치지 않습니다. 적용 저장소가 옛 `docs/01-DESIGN.md`를 남겨 두면 `DESIGN`이 두 파일을 가리켜, 이름 참조가 있는 곳에서 기존 "ambiguous document name" 오류가 납니다.
- 지금 검사기는 대상을 못 찾은 이름 참조(`DESIGN §3`)를 조용히 건너뜁니다. 그래서 `doc_short_names`를 고치지 않으면 옮긴 문서의 이름 참조가 검사 없이 지나갑니다.
- 파일명 참조는 경로로 못 찾으면 앞의 번호를 떼고 짧은 이름으로 다시 찾습니다(`check_section_refs`의 `kind == "filename"` 분기). 이 대체를 그대로 두고 `DESIGN`을 등록하면 옛 `01-DESIGN.md §1`이 새 `DESIGN.md`로 풀려, 남은 옛 이름이 검사를 통과합니다. 그래서 대체 규칙을 바꿉니다. 참조한 파일명에 번호가 붙어 있으면 `docs/*.md`·`docs/template/*.md` 가운데 파일 이름이 정확히 같은 문서로만 풉니다. 번호가 없는 파일명(`DESIGN.md §3`)만 지금처럼 짧은 이름으로 찾습니다. `docs/changes/x/`에서 쓴 `00-PROJECT.md §8`처럼 이름이 같은 파일이 있는 참조는 지금처럼 풀립니다(R-006).

### 3.5 root 유지관리 영역

- root skill 사본은 ko payload와 byte 동일해야 하므로 root도 같은 경로를 가집니다(Q4). root `docs/template/`에는 `DESIGN.md`(지금도 ko와 같음), 양식 네 개(지금도 ko와 같음), maintainer 보충 문서인 `DOCS_GUIDE.md`·`TEMPLATE_GUIDE.md`가 들어갑니다. root에는 `CHANGELOG_GUIDE.md`와 프로젝트 기록 문서가 없습니다.
- root의 `docs/template/`은 이 저장소가 템플릿을 적용한 결과가 아니라 템플릿 공통 절차의 원본 사본입니다. root DOCS_GUIDE 보충 문서에 이 차이를 적습니다.
- 과거 변경 문서와 완료 기록(`docs/changes/*`, `docs/TODO_ARCHIVE.md`)에서 검사기가 따라가는 참조 가운데 옮기는 파일을 가리키는 것은 `65e5f3d` 기준으로 두 종류입니다. 링크 27개(파일 8개)와, 경로나 번호 붙은 파일명 뒤에 절 번호를 붙인 참조 10개(파일 3개)입니다. 그 경로·파일명만 새 이름으로 고치고 나머지 본문은 그대로 둡니다(INTENT §4).
- 번호 없는 파일명 참조(`TEMPLATE_GUIDE.md §5`)와 짧은 이름 참조(`DESIGN §3`)는 §3.4의 규칙으로 새 문서에 풀리므로 고치지 않습니다. root CHANGELOG에는 이런 참조가 없습니다.
- 이 변경 폴더에도 ko TEMPLATE_GUIDE를 가리키는 링크가 4개 있습니다(SPEC 3개, PLAN 1개). 구현에서 함께 고칩니다. 구현할 때 옮기는 파일을 가리키는 링크를 다시 세어, 그 뒤에 생긴 링크도 빠뜨리지 않습니다.

### 3.6 참조 수정 범위

2026-11-25 `65e5f3d` 기준으로 파일 이름 문자열의 출현 수를 셌습니다(출현 수/파일 수). 본문 설명, 자기 참조, 과거 기록을 포함한 수이므로 실제로 고칠 곳은 이보다 적습니다.

| 이름 | en | ko | common | root 문서 | root 도구·테스트 | root 이력 |
|---|---|---|---|---|---|---|
| `01-DESIGN` | 49/11 | 49/11 | 1/1 | 19/8 | 16/3 | 14/8 |
| `DOCS_GUIDE` | 68/9 | 68/9 | 13/2 | 41/12 | 4/2 | 80/12 |
| `TEMPLATE_GUIDE` | 32/6 | 31/6 | 21/2 | 46/8 | 52/10 | 78/16 |
| `CHANGELOG_GUIDE` | 13/4 | 13/4 | 0/0 | 5/3 | 0/0 | 6/5 |
| `_template` | 34/11 | 34/11 | 2/1 | 23/11 | 16/8 | 5/4 |

- root 이력은 `docs/changes/*`, `docs/TODO_ARCHIVE.md`, root CHANGELOG입니다. 이 가운데 고치는 것은 §3.5의 링크 27개와 절 참조 10개입니다.
- `02-TODO`는 ko payload와 common에만 90번(파일 23개) 나옵니다. 그래서 번호를 당기지 않습니다(§3.1).

## 4. 상위 설계에 미치는 영향

- D-002의 locale artifact inventory를 바꿉니다. common+locale 합성과 locale 간 같은 경로 집합이라는 계약은 유지합니다.
- D-006의 adoption policy 표를 바꿉니다. policy의 종류와 의미(`copy`, `merge`, `decide`)는 유지합니다.
- D-009의 문서 소유권을 확장합니다. 템플릿 소유 문서에서 프로젝트 칸을 빼는 원칙을 `project-analysis`에서 `copy` 문서 전체로 넓힙니다. locale guide가 artifact 정본이고 root guide가 maintainer 보충 문서라는 구분은 유지합니다.
- D-021의 root↔ko skill byte 동일 규칙은 유지합니다. 그래서 root 구조도 바뀝니다(§3.5).
- 대체하는 결정은 없습니다.

## 5. 위험·호환성·rollback

- **적용 저장소의 링크:** 프로젝트 문서, README, 변경 문서가 옛 경로를 가리키면 깨집니다. 새 `check-docs.py`가 깨진 링크와 옛 파일명 참조를 보고합니다. release 이력에 옛 경로→새 경로 표를 둡니다.
- **업그레이드 절차(locale TEMPLATE_GUIDE의 release 이력에 적을 내용):**
  1. `adopt --base-version <이전 판>`을 돌립니다. 옛 경로 여덟 개와 새 경로 아홉 개가 아래 표처럼 나옵니다(R-010). 네 문서는 프로젝트가 Metadata를 채웠으므로 대부분 `diverged`일 것입니다(추론).
  2. report의 `blocked`와 `diverged`를 먼저 봅니다. `blocked` 경로는 정리한 뒤 다시 돌립니다. 새 경로에 이미 있는 파일은 policy에 따라 다르게 다룹니다.
     - `docs/template/` 아래(`copy`): 다른 내용의 파일(`diverged`)을 프로젝트 소유 위치로 옮겨 보존하고 프로젝트 기록의 「보존·제외」에 적습니다. inventory 밖 파일(예: 프로젝트가 만든 `docs/template/notes.md`)도 같습니다. 이런 파일은 report에 나오지 않습니다. `scripts/installer.py`의 upgrade report는 base와 current inventory의 합집합만 보므로(1244행) 폴더를 직접 훑어 찾습니다.
     - `docs/TEMPLATE_RECORD.md`(`merge`): 기존 문서를 제자리에 두고 템플릿 절을 병합합니다. 다른 `merge` 문서와 같습니다.
  3. 옛 문서의 「템플릿 적용 기록」과 의도한 수정을 프로젝트 기록 문서로 옮깁니다. 옛 `Template source`·`Template revision`은 「이전 기준」에 남기고, 두 칸은 이번 artifact의 원본 위치와 commit으로 새로 씁니다. locale TEMPLATE_GUIDE의 「템플릿 개정 반영하기」와 같은 규칙입니다.
  4. 옛 파일을 지우고 artifact의 `docs/template/` 파일을 그대로 넣습니다. 옛 `docs/TEMPLATE_GUIDE.md`를 지웠던 저장소(옛 경로가 `converged`)는 새 `docs/template/TEMPLATE_GUIDE.md`도 넣지 않을 수 있습니다(§3.3의 허용 차이). 그 선택을 「보존·제외」에 적습니다. 나머지 `copy` 정책 파일(`.agents/`·`.claude/`의 skill과 Codex 설정, `scripts/check-docs.py`, `tests/test_check_docs.py`)은 지금의 `copy` 처리처럼 artifact 판에서 시작해, 프로젝트 기록의 「템플릿 소유 파일의 수정」에 적은 의도한 수정만 다시 적용합니다. `docs/template/` 안의 수정(§3.3)도 같습니다. 옛 검사기는 `docs/DOCS_GUIDE.md`를 필수로 읽고, 옛 `design` skill은 `docs/01-DESIGN.md`가 없으면 절차를 적용하지 않으므로 이 파일들은 한 번에 바꿉니다.
  5. `merge` 정책 문서(`AGENTS.md`, `README.md`, `02-TODO.md`, `CI.md`, `REVIEW_ROUND.md`)의 바뀐 링크를 평소처럼 병합하고, 프로젝트가 직접 단 링크를 고칩니다.
  6. `check-docs.py`와 테스트를 돌립니다.
- **업그레이드 분류(R-010):** `scripts/installer.py`의 `_upgrade_status`를 읽고 낸 추론이었고, 2026-11-26 W-005에서 아래 표대로 나오는 것을 실행해 확인했습니다(PLAN §3).

  | 경로 | 대상 상태 | 분류 |
  |---|---|---|
  | 옛 경로 | base 판 그대로 | `template-only`(제거) |
  | 옛 경로 | 프로젝트가 고침(Metadata 채움 등) | `diverged` |
  | 옛 경로 | 이미 없음(예: 지운 `TEMPLATE_GUIDE.md`) | `converged` |
  | 새 경로 | 없음 | `template-only`(추가) |
  | 새 경로 | 같은 내용의 파일이 이미 있음 | `converged` |
  | 새 경로 | 다른 내용의 파일이 이미 있음 | `diverged` |
  | 어느 경로든 | symlink, 일반 파일이 아님 등 | `blocked` |
  | `docs/template/` 아래의 inventory 밖 파일 | 있음 | report에 나오지 않음. 2단계에서 직접 찾음 |

- **순서 의존:** 새 `check-docs.py`는 새 경로를, 옛 검사기와 옛 skill은 옛 경로를 요구합니다. 한쪽만 바꾸면 검사가 실패하거나 `design` skill이 멈추므로, 업그레이드 안내는 4단계에서 모든 `copy` 파일을 한 번에 바꾸라고 적습니다.
- **version:** artifact 경로와 adoption plan의 `guide` 값이 바뀌고 적용 저장소의 링크가 깨지므로 `v4.0.0`(major)으로 냅니다(Q5). v2(artifact 구조 변경)와 v3(Python 하한, installer 명령 계약 변경)를 major로 낸 선례가 있습니다.
- **root README의 release 안내:** README가 `latest` release로 받은 artifact 안의 경로(`artifact/docs/TEMPLATE_GUIDE.md`)를 안내하는 문장은, 구현 MR이 아니라 `v4.0.0`이 Latest로 공개된 뒤의 기록 작업에서 바꿉니다. 그 전까지 `latest`는 옛 경로의 artifact를 받습니다. README에서 source 문서로 가는 링크는 파일과 함께 옮겨야 깨지지 않으므로 구현 MR에서 바꿉니다.
- **리뷰 부담:** 바뀌는 파일이 많습니다. 구현 MR은 이동만 하는 commit과 내용을 고치는 commit을 나눠 rename을 따로 볼 수 있게 합니다.
- **rollback:** release 전에는 구현 MR을 revert합니다. release 뒤에는 게시한 판을 바꾸지 않고 patch로 고칩니다(D-004). 적용 저장소는 v3 판을 계속 쓸 수 있습니다.
- **확인하지 못한 것:** 템플릿 밖 도구가 `docs/changes/_template/`이나 `docs/01-DESIGN.md`를 고정 경로로 읽는지는 확인하지 않았습니다. 이 저장소의 코드에서는 §3.4의 위치뿐입니다.

## 6. 완료 조건과 미해결 사항

- **설계 완료:** 2026-11-25 이 문서와 INTENT가 `Accepted`가 됐고 결정은 D-023입니다.
- **시작과 통합 순서:** 구현은 `v3.3.0` release(TODO T-076)가 `main`에 통합된 뒤 그 `main`에서 시작합니다. release 준비가 두 guide의 `Template version`과 release 이력을 고치므로, 먼저 옮기면 같은 파일이 충돌합니다. `v3.3.0`은 `main`의 exact commit으로 내므로 이 변경이 먼저 merge되면 경로 이동이 `v3.3.0`에 섞입니다.
- **구현 완료:** PLAN의 W-002~W-005가 끝나고 `check-locales.py --require-stable`, `check-docs.py`(무인자와 en·ko export 결과물), `unittest discover -s tests`, `unittest discover -s template/common/tests`가 통과합니다.
- **통합 완료:** MR 리뷰와 필수 CI, GitLab `main` 반영.
- **공개:** 이 변경의 완료 조건이 아닙니다. 별도 release 작업에서 version·release 이력·CHANGELOG와 함께 합니다.

2026-11-25 사용자가 다섯 질문을 모두 추천안으로 정했습니다("추천안대로"). 남은 질문은 없습니다.

| ID | 질문 | 결정(추천안) | 기각한 안 |
|---|---|---|---|
| Q1 | 프로젝트가 채우는 값을 어디에 둘까 | 새 프로젝트 소유 문서 `docs/TEMPLATE_RECORD.md`(`merge`). 템플릿 적용 기록만 담아 제품 기준과 섞이지 않습니다 | `00-PROJECT.md`에 절 추가. 파일은 늘지 않지만 제품 기준 문서에 적용 이력이 들어갑니다 |
| Q2 | 변경 양식 폴더 | `docs/template/changes/`. `docs/changes/`에 실제 변경만 남고, 깊이가 같아 복사한 뒤에도 양식의 링크가 맞습니다(§3.1) | `docs/changes/_template/` 유지. "template"이 두 곳에 남습니다 |
| Q3 | `01-DESIGN.md`의 이름 | `docs/template/DESIGN.md`. 번호는 `docs/`의 탐색 순서용입니다 | `docs/template/01-DESIGN.md` 유지 |
| Q4 | root 구조 | payload와 같은 경로(§3.5). root skill byte 동일 규칙 때문입니다 | 다른 경로를 쓰려면 root skill 사본 규칙(D-021)을 바꿔야 합니다 |
| Q5 | release 순서와 version | `v3.2.0` 뒤 main에 통합된 미공개 payload 변경 T-071~T-074를 먼저 `v3.3.0`으로 공개하고, 이 변경은 `v4.0.0`으로 따로 공개. 새 skill과 검사기 수정만 받으려는 적용 저장소가 경로 이동을 함께 하지 않아도 됩니다 | 모두 묶어 `v4.0.0` |

## 7. 명세 변경 기록

- 2026-11-25: 최초 작성(Draft).
- 2026-11-25: §6의 질문 다섯 개가 "추천안대로" 정해져 Status를 `Accepted`로 바꾸고 D-023에 연결했습니다. §6에 시작과 통합 순서를 더했습니다.
- 2026-11-25: Q5의 `v3.3.0` 범위를 바로잡았습니다. Draft에는 미공개 작업을 T-073·T-074로 적었는데, `git log v3.2.0..65e5f3d`를 보면 T-071·T-072의 검사기 수정도 공개되지 않았습니다. "미공개 payload 변경을 먼저 `v3.3.0`으로, 이 변경은 `v4.0.0`으로"라는 결정은 그대로입니다.
- 2026-11-25: MR !12 리뷰 라운드 1(head `b4faf83`, prview)의 지적 다섯 건을 반영했습니다.
  - §5 업그레이드 절차에 모든 `copy` 파일 교체를 넣고, 대상 상태별 분류 표를 더해 R-010을 고쳤습니다.
  - 파일명 참조의 대체 규칙을 §3.4에 정하고 R-006을 고쳤습니다.
  - 지울 수 있는 경로를 링크하지 않는 R-011과 §3.3의 규칙을 더했습니다.
  - §3.5와 PLAN W-004에 이 폴더의 링크를 넣었습니다.
  - R-011, §3.3의 링크 규칙, §3.4의 대체 규칙은 승인("추천안대로") 뒤에 더한 요구라 그 승인에 들어 있지 않습니다. merge 확인 때 함께 확인받습니다.
- 2026-11-25: MR !12 리뷰 라운드 2(head `2f4108d`, prview)의 지적 다섯 건을 반영했습니다.
  - 이력 문서에서 검사기가 따라가는 절 참조 10개를 이동 범위에 넣고, 경로·파일명만 고치도록 INTENT §4를 바꿨습니다. 사용자가 "허용하고 계속"으로 승인했습니다(§3.5, R-009).
  - §5 업그레이드 절차에 `blocked`·`diverged` 처리, 의도한 수정의 재적용, `Template source`·`Template revision` 갱신을 넣었습니다(§3.2).
  - R-011과 §3.3에 "지울 수 있는 문서에는 경로·파일명 뒤 절 번호도 쓰지 않는다"를 더했습니다.
  - §3.4 manifest 행에 `section_markers`·`required_commands`의 guide 경로를 넣었습니다.
  - R-011 확장은 1라운드 추가분과 같이 merge 확인 때 함께 확인받습니다.
- 2026-11-25: MR !12 리뷰 라운드 3(head `f324158`, prview)의 지적 세 건을 반영했습니다.
  - placeholder 검색 선언과 두 명령을 DOCS_GUIDE로 옮기도록 §3.2·§3.3·§3.4와 R-003을 고쳤습니다. 프로젝트 기록에 두면 선언이 자기 자신을 검출합니다.
  - R-002의 금지 범위를 안내 문서 네 개로 좁히고 복사용 양식을 제외했습니다. 양식의 칸은 복사한 변경 폴더에서 채웁니다.
  - PROJECT §6에 D-023의 목표 구조를 넣었습니다(1라운드 P3 지적과 같은 원인).
  - 선언을 옮기는 것도 승인 뒤 추가분이라 merge 확인 때 함께 확인받습니다.
- 2026-11-25: MR !12 리뷰 라운드 4(head `a7d540f`, prview)의 지적 세 건을 §3.3과 §5 업그레이드 절차에 반영했습니다.
  - `docs/template/`의 inventory 밖 파일을 직접 찾아 옮깁니다. report에 나오지 않습니다.
  - `docs/TEMPLATE_RECORD.md`가 이미 있으면 제자리에서 병합합니다.
  - 지웠던 `TEMPLATE_GUIDE.md`는 새 경로에도 넣지 않을 수 있습니다.
- 2026-11-25: MR !12 리뷰 라운드 5(head `cf9287a`, prview)의 지적 두 건을 반영했습니다.
  - release가 아닌 원본에서 적용한 사실을 프로젝트 기록의 `Template release` 칸에 적도록 §3.2와 R-003을 고쳤습니다.
  - 허용하는 차이를 `TEMPLATE_GUIDE.md` 삭제와 기록한 수정 두 가지로 맞췄습니다(§3.3, R-004, PROJECT D-023, INTENT §2).
  - `Template release` 칸도 승인 뒤 추가분이라 merge 확인 때 함께 확인받습니다.
- 2026-11-25: MR !12 리뷰 라운드 6(head `9defe44`, prview)의 지적을 반영했습니다. root README의 release artifact 안내는 `v4.0.0` 공개 뒤에 바꾸도록 §5와 PLAN W-004·§5에 적었습니다.
- 2026-11-25: T-076의 판을 `v3.3.1`로 바꿨습니다. 2026-11-25 `v3.3.0` tag가 판 번호를 올리기 전 commit에 잘못 만들어져 그대로 두었기 때문입니다(TODO T-076). 이 문서의 `v3.3.0`은 그 release(T-076)를 가리킵니다.
- 2026-11-26: 구현(PLAN W-002~W-005)에서 R-010의 분류를 실행으로 확인해 §1과 §5의 "추론" 표시를 고쳤습니다. 계약은 바뀌지 않았습니다.
