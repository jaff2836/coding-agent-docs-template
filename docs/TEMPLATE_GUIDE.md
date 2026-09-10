# Template Guide

이 문서는 문서 중심 프로젝트 템플릿의 source 관리와 적용 안내입니다. 이 템플릿 저장소의 소개는 루트 [README.md](../README.md)에 있고, 한국어 적용 프로젝트의 소개·설치·실행 양식은 [locales/ko/README.md](../locales/ko/README.md)입니다.

v2 source root는 적용 payload가 아니므로 직접 복사하지 않습니다. locale별 exporter·installer가 완성되기 전에는 `v1.7.1` 기준 commit `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`을 사용합니다. 특정 CI 제품의 pipeline 파일은 포함하지 않으며 품질 게이트의 순서와 연결 확인은 [CI.md](./CI.md)를 따릅니다.

## Metadata

- **Status:** Active
- **Template version:** 1.7.1
- **Template source:** 템플릿 원본 저장소의 URL 또는 다시 접근할 수 있는 보관 위치를 프로젝트에 맞게 작성
- **Template revision:** 복사 기준인 원본 commit의 전체 SHA를 프로젝트에 맞게 작성 (§5)
- **Owner:** 프로젝트에 맞게 작성
- **Last reviewed:** YYYY-MM-DD
- **Review cadence:** 템플릿 구조 또는 도구 연결 방식 변경 시

`Template version`은 복사 기준 판, `Template source`와 `Template revision`은 그 원본 위치와 정확한 commit을 남깁니다. 적용 저장소에서 일반적인 문서 수정만 했다면 이 값을 바꾸지 않습니다. 원본 템플릿의 source·revision 안내 문구는 복사 시 채우며, 자기 자신의 commit SHA를 미리 문서에 넣으려 하지 않습니다. 기록 규칙은 §5, 판별 변경 내용은 §6에 있습니다.

## 1. 포함된 구조

```text
.
├── README.md                  # source 저장소 소개, artifact 제외
├── AGENTS.md                  # source 저장소 유지관리 지침, artifact 제외
├── docs/                      # source 저장소 설계·TODO, artifact 제외
├── template/common/           # 언어 비의존 payload source
├── locales/
│   ├── manifest.json          # locale 상태와 닫힌 output inventory
│   └── ko/                    # 한국어 payload source
│       ├── README.md          # artifact root README
│       ├── AGENTS.md
│       ├── docs/
│       ├── scripts/
│       └── tests/
├── scripts/                   # source 저장소 검사·향후 exporter/packager
└── tests/                     # source 저장소 회귀 테스트
```

## 2. 새 프로젝트에 적용하기

1. v2 exporter·installer가 구현되기 전에는 source root를 복사하지 말고 `v1.7.1` 기준 commit `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`을 사용합니다. 구현 후에는 exact version과 locale을 지정한 검증된 artifact만 적용합니다.
2. locale artifact의 root `README.md`는 이미 적용 프로젝트용 양식입니다. source 저장소 소개문이나 maintainer 문서는 artifact에 포함하지 않습니다.
3. artifact의 `AGENTS.md` 프로젝트 정보와 명령을 실제 저장소에 맞게 작성합니다. README의 실행 방법과 서로 일치하도록 확인하세요.
4. 아래 placeholder와 예시 항목을 교체합니다.
5. [00-PROJECT.md](./00-PROJECT.md)에 현재 제품 기준과 승인된 목표를 구분하고 기존 설계의 정본을 연결합니다. [02-TODO.md](./02-TODO.md)에 통합 대상과 첫 마일스톤의 변경 단위 항목을 작성합니다. 변경별 PLAN이 있으면 상세 작업·검증 상태는 PLAN에만 둡니다. 장기 확장이 없으면 `10-EXTENSION.md`와 들어오는 링크를 제거합니다.
6. [REVIEW.md](./REVIEW.md)에 프로젝트 고유 불변조건과 실제 승인된 예외만 기록합니다.
7. [REVIEW_ROUND.md](./REVIEW_ROUND.md)의 기본 라운드 수와 통과 임계값을 확인하고, §2.1에 이 저장소에서 도는 리뷰어를 전부 기록합니다. 임계값은 사용자가 변경할 수 있으며 실제 라운드에서는 확정한 값을 적용합니다. 통과 후 인계와 다음 작업의 문서 반영은 §6·§7·§9를 따릅니다. 아래 「리뷰어 조사 힌트」를 참고하되 실제 동작은 직접 확인하세요.
8. Cursor Bugbot을 쓴다면 [.cursor/BUGBOT.md](../.cursor/BUGBOT.md)의 불변조건·확정 결정 절을 [REVIEW.md](./REVIEW.md), [00-PROJECT.md](./00-PROJECT.md)와 같은 내용으로 채웁니다. OMP advisor를 쓴다면 [.omp/WATCHDOG.md](../.omp/WATCHDOG.md)의 import가 동작하는지 확인하고, 두 도구를 쓰지 않으면 해당 파일을 삭제합니다.
9. [01-DESIGN.md](./01-DESIGN.md)는 공통 절차입니다. Metadata는 적용 프로젝트에 맞추되 제품 설계 내용을 적지 않습니다. §1·§2에 따라 필요한 산출물만 만들고 `_template/`을 실제 작업으로 취급하지 않습니다. 승인된 단계 구현에 INTENT·SPEC을 재작성하지 않습니다.
10. 사용하는 개발 도구에서 공통 지침과 관련 문서를 의도대로 읽는지 확인합니다.
11. 외부 방법론·행동 규칙 도구를 함께 쓴다면 아래 §4 「외부 방법론·행동 규칙 도구」의 공존 규칙을 먼저 적용합니다.
12. [문서 운영 안내](./DOCS_GUIDE.md)의 Template Adoption Checklist로 적용 완료 여부를 확인합니다.
13. CI를 쓰는 저장소는 [CI.md](./CI.md)의 워크플로와 체크리스트로 기존 러너에 품질 게이트를 연결합니다. GitHub Actions·Buildkite 등 특정 제품의 pipeline 파일은 이 템플릿이 포함하지 않습니다. 사용자가 러너를 지정하기 전에는 YAML을 새로 만들지 마세요. CI가 없으면 같은 게이트를 로컬에서 실행하고 미사용 이유를 기록합니다.

기존 프로젝트에 적용할 때는 같은 이름의 파일을 덮어쓰지 말고 기존 지침·문서·ignore 규칙과 비교하여 병합하세요. 기존 코드나 사용자 변경은 보존합니다. 기존 `REVIEW.md`와 병합해 절 번호가 바뀌거나 [00-PROJECT.md](./00-PROJECT.md)의 조건부 절을 삭제하면, 절 번호로 참조하는 [REVIEW_ROUND.md](./REVIEW_ROUND.md), [01-DESIGN.md](./01-DESIGN.md), [.cursor/BUGBOT.md](../.cursor/BUGBOT.md), [.omp/WATCHDOG.md](../.omp/WATCHDOG.md)의 참조도 실제 헤딩에 맞게 고치세요. 도입 전부터 큰 설계 문서가 있는 저장소는 [01-DESIGN.md](./01-DESIGN.md) §6을 먼저 읽으세요. 기존 문서는 기본적으로 유지하고 사용자가 통합을 요청한 경우에만 근거와 참조를 보존해 병합합니다.

### 번호 체계로 이관하기

| 이전 파일 | 새 기본 파일 | 이관 범위 |
|---|---|---|
| `docs/PLAN.md` | `docs/00-PROJECT.md` | 제품 맥락·현재 구조·기본 설계·결정과 정본 링크 |
| `docs/DESIGN.md` | `docs/01-DESIGN.md` | 공통 절차. 실제 설계 산출물과 구분 |
| `docs/TODO.md` | `docs/02-TODO.md` | 전역 변경 목록. 상세 PLAN이 있으면 링크로 전환 |
| 기존 제품·확장 설계 | 기본적으로 기존 경로 유지 | PROJECT 인덱스에서 연결. 합의 없이 재작성·이동하지 않음 |
| 기존 변경 설계 | 기존 승인 기록 보존 | 새 변경부터 Intent·Spec·선택적 Plan 형식 사용 |

- 번호와 대문자·하이픈은 정렬과 역할 식별을 돕습니다. 번호만으로 설계 우선순위나 승인을 정하지 않고 기존 결정 ID를 재번호하지 않습니다.
- 이전 파일명을 일괄 치환하지 않습니다. 변경별 `03-PLAN.md`, 도구 생성 파일, 과거 이력의 `PLAN.md`는 역할이 다릅니다. 링크·import·스킬·검사 코드·고정 정책 경로를 조사해 실제 이관 대상만 바꿉니다.
- `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `docs/REVIEW.md` 등 진입점·계약 경로는 그대로 둡니다. 이름을 바꾸려면 소비자 호환성과 도구 설정을 별도 검토합니다.
- 기존 제품 설계를 통합한다면 실행 상태는 TODO/PLAN, 완료 이력은 기존 CHANGELOG로 정리합니다. 계약·결정 이유·승인 근거는 보존합니다. 확장 설계에는 상위 문서의 유지·확장·대체 범위를 명시합니다.
- 과거 변경 파일의 본문 동결 규칙은 그 기록에 유지합니다. 새 형식은 01-DESIGN.md §4의 승인 버전 보존과 갱신 규칙을 적용합니다. 미커밋 상태에서도 기존 승인 내용을 보존합니다.
- PR 수만으로 규모를 정하지 않습니다. 로컬 Git은 검토 가능한 변경 단위로 나누고, 전역 TODO에 통합 대상 또는 로컬 완료 대상을 적습니다. 원격 서비스나 자동 commit은 필수가 아닙니다.
- 실제 작업이 양식 폴더를 정본으로 가리키지 않는지 확인합니다. 작은 작업·상위 설계 구현에는 필요한 양식만 사용합니다.

### 리뷰어 조사 힌트

§2.1 표는 저장소마다 다르므로 템플릿이 채워 주지 않습니다. 다만 GitHub에서 널리 쓰이는 공개 리뷰어는 제품 수준에서 동작이 정해져 있어, 조사 시작점으로 다음이 관찰되었습니다(2026-09 기준, 사용 중인 버전에서 직접 확인).

| 리뷰어 | 관찰된 특성 | 재리뷰 요청 방법 (공식 문서 기준) |
|---|---|---|
| Codex (`chatgpt-codex-connector`) | PR review 본문의 `Reviewed commit:`으로 head 식별. 자동 리뷰는 PR이 리뷰 요청 상태로 열릴 때 1회이며 push마다 돌지 않습니다. 지적이 없어도 본문은 남깁니다. 인라인 finding에 `AGENTS.md` 줄 번호를 인용하므로 `AGENTS.md`의 Code Review Rules가 출력 형식에 영향을 줍니다 | PR 댓글 본문을 정확히 `@codex review`로. 접수 확인은 댓글에 붙는 👀 반응. **`review` 뒤에 다른 말을 붙이지 마세요** — `@codex`에 다른 문장이 이어지면 리뷰가 아니라 PR을 컨텍스트로 한 클라우드 태스크가 시작되어 branch에 push할 수 있습니다 |
| Copilot (`copilot-pull-request-reviewer`) | **PR당 1회**, head 표시 없음. 저신뢰 코멘트는 review 본문의 접힌 `<details>` "Suppressed comments"에도 있습니다 | 아래 「Copilot 재요청 명령」을 §2.1에 옮겨 실행. push마다 자동은 repository ruleset의 "Review new pushes"만 |
| 자체 호스팅 GitHub App 리뷰어 (예: webhook 기반 봇) | `pull_request`의 opened·reopened·ready_for_review·synchronize를 받아 push마다 돌고, PR 코멘트에 `<!-- <이름>:v1 head:<SHA> -->` 같은 마커 주석으로 head를 남기는 구성이 일반적입니다. head마다 새 코멘트인지 하나를 덮어쓰는지는 봇마다 다르므로 표의 `게시 위치`에 적으세요 | `push 자동` — 트리거 이벤트를 함께 적습니다. 문제가 없을 때도 결과를 남기는지 확인하세요. §4 타임아웃 처리가 달라집니다 |

**Copilot 재요청 명령** (`<n>`은 PR 번호. `rereview = request`가 되려면 §2.1 표에 이 명령 또는 이 블록 참조가 있어야 합니다. bot id `BOT_kgDOCnlnWA`는 2026-09 기준이며 `gh api users/copilot-pull-request-reviewer%5Bbot%5D --jq .node_id`로 다시 확인하세요. 이 REST URL만 `[bot]`을 씁니다):

```bash
gh api graphql \
  -f query='mutation($pr:ID!,$bot:ID!){ requestReviews(input:{pullRequestId:$pr, botIds:[$bot], union:true}) { pullRequest { reviewRequests(first:10) { nodes { requestedReviewer { ... on Bot { login } } } } } } }' \
  -f pr="$(gh pr view <n> --json id --jq .id)" \
  -f bot="BOT_kgDOCnlnWA"
```

접수 확인은 응답 `reviewRequests`의 GraphQL `Bot.login`이 `copilot-pull-request-reviewer`인지 봅니다(`[bot]` 없음). REST `requested_reviewers`는 200이어도 no-op일 수 있어 쓰지 마세요. 리뷰가 시작되면 요청 목록에서 빠지므로 뒤늦은 `gh pr view`는 비어 있을 수 있습니다.

자체 호스팅 봇이나 GitHub Actions 기반 리뷰어는 저장소·버전마다 다르므로 마커 주석과 트리거 조건을 직접 확인해 적으세요. 앞의 두 공개 리뷰어는 기본 구성에서 push마다 돌지 않으므로, 이들만 등록된 저장소는 `rereview = request`가 아니면 2라운드부터 상시 리뷰어의 결과를 받을 수 없습니다.

## 3. 교체할 값

교체 대상은 `{{...}}` 형식만이 아닙니다. 안내 문구형 placeholder도 함께 남아 있으므로 다음 명령으로 한 번에 찾으세요.

```bash
rg --hidden -n --glob '*.md' --glob '!**/.git/**' --glob '!docs/TEMPLATE_GUIDE.md' --glob '!docs/DOCS_GUIDE.md' \
  "\{\{|프로젝트에 맞게 작성|간단히 작성|YYYY-MM-DD|\| 예시|예시 결정|예시 완료|\*\*예시:\*\*" .
```

`rg`가 없으면 다음을 사용하세요.

```bash
grep -rnE "\{\{|프로젝트에 맞게 작성|간단히 작성|YYYY-MM-DD|\| 예시|예시 결정|예시 완료|\*\*예시:\*\*" \
  --include='*.md' --exclude=TEMPLATE_GUIDE.md --exclude=DOCS_GUIDE.md \
  --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.venv .
```

이 검사는 **복사 후 프로젝트 값을 채운 저장소**를 대상으로 합니다. 원본 템플릿에는 placeholder와 예시가 의도적으로 남아 있습니다. `--hidden`으로 `.cursor/BUGBOT.md` 같은 숨김 폴더도 검색하되 `.git` 내부는 제외합니다.

이 두 안내 문서는 placeholder를 설명하기 위해 그 문구를 포함하므로 검색에서 제외합니다. 대신 두 문서의 Metadata는 직접 확인하세요. `changes/_template/`의 placeholder는 복사용으로 유지할 수 있지만 실제 변경 폴더에 남은 값은 교체해야 합니다. 결과가 0건이어도 이 패턴에 없는 README 안내 문구, 담당자·마일스톤·태스크 예시, 명령의 실행 가능성과 완료 주장의 근거까지 검증된 것은 아닙니다. [DOCS_GUIDE.md](./DOCS_GUIDE.md)의 Template Adoption Checklist와 함께 확인합니다.

적용을 마쳤거나 문서를 옮긴 뒤에는 `scripts/check-docs.py`를 실행하세요. 상대 링크, `.agents`/`.claude` 스킬 사본과 Codex 명시 호출 정책값, `CLAUDE.md`와 `.omp/WATCHDOG.md`의 `@` import, [REVIEW.md](./REVIEW.md) §6과 [.cursor/BUGBOT.md](../.cursor/BUGBOT.md)의 불변조건 목록, 문서를 지목한 절 번호 참조, 안내 문서의 `Template version`을 한 번에 확인하고, 실패하면 종료 코드가 0이 아닙니다. 표준 라이브러리만 사용합니다.

```bash
python3 scripts/check-docs.py
```

템플릿 원본의 검사 스크립트를 바꿀 때는 실패 경로 회귀 테스트도 실행합니다.

```bash
python3 -m unittest discover -s tests -p 'test_check_docs.py' -v
```

위 명령은 `python3`을 기준으로 합니다. 파일 이동은 내용이 바뀌지 않아도 링크를 깨뜨립니다. 이 문서를 §5에 따라 삭제한 저장소에서도 검사는 그대로 동작하며, 판 기록은 [DOCS_GUIDE.md](./DOCS_GUIDE.md)에서만 확인합니다. 절 번호 검사는 문서를 지목한 참조(`REVIEW.md §6`, `PROJECT §8` 등)만 대상으로 하며, 대상이 모호한 같은 파일 안의 `§4` 같은 참조와 §6 릴리스 이력의 옛 절 번호는 제외합니다. 생성물 디렉터리(`dist`, `build`, `target`, `vendor` 등)는 검사에서 건너뜁니다. 이 검사는 원본 템플릿의 placeholder 잔존을 실패로 보지 않습니다. placeholder 검색은 위의 `rg`/`grep` 명령을 사용하세요.

| Placeholder | 작성할 내용 |
|---|---|
| `{{PROJECT_NAME}}` | 프로젝트 이름 |
| `{{PROJECT_DESCRIPTION}}` | 해결하는 문제와 핵심 기능 |
| `{{CHANGE_ID}}`, `{{CHANGE_TITLE}}` | 실제 변경 폴더의 고유 ID와 변경 제목. `_template/`에서는 복사용으로 유지 |
| `{{RUN_COMMAND}}` | 개발 또는 실행 명령 |
| `{{BUILD_COMMAND}}` | 빌드 명령 |
| `{{TEST_COMMAND}}` | 테스트 명령 |
| `{{LINT_COMMAND}}` | 린트 명령 |
| `{{TYPECHECK_COMMAND}}` | 타입 검사 명령 |
| `{{PROJECT_INVARIANT_1}}`, `{{PROJECT_INVARIANT_2}}` | 반드시 지켜야 할 프로젝트 고유 규칙. [REVIEW.md](./REVIEW.md) §6과 [.cursor/BUGBOT.md](../.cursor/BUGBOT.md) 두 곳에 같은 내용으로 |

- 사용하지 않는 명령은 `N/A`로 표시하고 [AGENTS.md](../AGENTS.md)에 이유를 남깁니다. 존재하지 않는 명령을 실행 가능한 예시처럼 남기지 마세요.
- `프로젝트에 맞게 작성`, `YYYY-MM-DD`, 담당자·마일스톤·태스크 예시도 실제 정보로 바꿉니다.
- 전역 TODO와 변경별 양식의 예시는 실제 완료 이력이 아닙니다. 전역 완료에는 통합 대상과 필요한 검증을, PLAN에는 해당 브랜치의 구현·검증 근거를 구분해 기록하세요.
- [00-PROJECT.md](./00-PROJECT.md)의 미정 사항은 미정으로 유지하고, 제안을 이미 합의된 결정으로 바꾸지 마세요. 예시 결정 행(`D-001`)도 삭제하거나 실제 결정으로 교체하세요. 필수 절은 §1~§5·§8·§11이며 나머지는 해당 사항이 없으면 삭제할 수 있습니다. 들어오는 절 참조를 함께 정리하세요. 빈 절을 placeholder 채로 남기지 마세요.
- [REVIEW.md](./REVIEW.md)의 예시 불변조건과 주석 처리된 예외는 프로젝트 정책으로 자동 채택하지 않습니다.
- `Last reviewed`는 실제 내용을 검토한 날짜를 **UTC 기준**으로 작성합니다. 템플릿을 복사한 것만으로 검증 완료를 표시하지 마세요. 로컬 시간대로 적으면 GitHub이 표시하는 PR 시각보다 미래 날짜가 되어 리뷰어가 지적합니다.
- 아직 정하지 않은 라이선스, 보안 신고 채널 및 운영 정보를 임의로 만들어 넣지 마세요. 템플릿에 포함된 `LICENSE`는 템플릿 자체의 MIT 라이선스입니다. 프로젝트 라이선스가 정해지면 교체하고, 정해지지 않았다면 삭제하고 README License 절에 미정으로 남기세요.

### `@` 토큰 주의

Claude Code는 `CLAUDE.md`와 그 import 대상에서 `@`로 시작하는 토큰을 파일 import로 해석합니다. `Owner` 필드나 연락처에 이메일 주소나 `@handle`을 적을 때는 backtick으로 감싸세요. 코드 스팬과 코드 블록 안의 `@`는 import되지 않습니다.

## 4. 개발 도구 연결 파일

공통 규칙의 원본은 [AGENTS.md](../AGENTS.md)입니다. 같은 규칙을 도구마다 복제해 관리하지 않는 구성을 사용합니다.

### 지침 파일

- [CLAUDE.md](../CLAUDE.md)에는 `@AGENTS.md`만 둡니다. 이 템플릿은 심볼릭 링크 생성을 요구하지 않습니다. Windows에서는 심볼릭 링크에 관리자 권한이나 개발자 모드가 필요하므로 import 방식이 더 안전합니다.
- Codex와 Cursor는 루트 `AGENTS.md`를 직접 읽습니다. Claude Code는 `CLAUDE.md`만 읽으므로 위 import가 필요합니다.
- **OMP를 쓰는 저장소**에서는 `.claude/CLAUDE.md`, `.agents/AGENTS.md`, `.github/copilot-instructions.md`를 만들지 마세요. OMP는 같은 디렉터리 depth에서 우선순위가 높은 provider가 낮은 provider를 가리는데, 루트 `AGENTS.md`는 가장 낮은 우선순위입니다. 이 중 하나라도 있으면 OMP에서 루트 `AGENTS.md`가 로드되지 않을 수 있습니다. (근거: OMP `docs/context-files.md`의 provider 우선순위표. 사용 중인 버전에서 직접 확인하세요.)
- **OMP를 쓰지 않는 저장소**에서는 해당 도구가 요구하는 전용 지침 파일을 둘 수 있습니다. 공통 규칙은 루트 `AGENTS.md`에 두고, 전용 파일에는 도구가 루트 파일을 읽지 못할 때만 필요한 연결(import 또는 한 줄 참조)을 남기며 본문을 복제하지 마세요. 나중에 OMP를 도입하면 이 파일들이 루트 `AGENTS.md`를 가리는지 먼저 확인하세요.
- `.cursorrules`와 `.omp/AGENTS.md`는 이 템플릿에 포함하지 않습니다. 기존 프로젝트에 도구 전용 지침이 있다면 공통 규칙과 중복·충돌하는지 확인하세요.
- CODEOWNERS를 쓰는 저장소라면 `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, `.cursor/`, `.omp/`, `docs/REVIEW.md`, `docs/REVIEW_ROUND.md`, `docs/01-DESIGN.md`, `docs/CI.md`를 owner 규칙에 추가하세요. 이 파일들은 에이전트의 commit·merge 권한과 리뷰 판정 기준을 정하므로 소스 코드와 같은 수준으로 보호해야 합니다. 이 템플릿은 CODEOWNERS 파일 자체를 포함하지 않습니다.

### 리뷰 관련 파일

- [.cursor/BUGBOT.md](../.cursor/BUGBOT.md)는 Cursor Bugbot 전용 파일입니다. Bugbot은 `.cursor/rules/`도 링크된 문서도 읽지 않고 이 파일만 프로젝트 규칙으로 사용하므로, [REVIEW.md](./REVIEW.md)의 판정 기준을 의도적으로 복제해 두었습니다. 판정 기준만이 아니라 **§6 불변조건과 §9 Accepted Deferrals, 되돌리지 않을 확정 결정**도 복제해야 Bugbot이 canonical 정책과 같은 blocking 판정을 냅니다. 리뷰 정책을 바꿀 때는 두 파일을 함께 수정하세요.
- [.omp/WATCHDOG.md](../.omp/WATCHDOG.md)는 OMP advisor(주 에이전트를 감시하는 두 번째 모델) 전용 파일입니다. OMP는 이 파일을 advisor의 system prompt에만 붙이고 주 에이전트 컨텍스트에는 넣지 않으며, `AGENTS.md`와 달리 context file로 취급하지 않습니다. Bugbot과 다르게 `@path` import를 확장하므로 [REVIEW.md](./REVIEW.md)를 복제하지 않고 `@../docs/REVIEW.md`로 import합니다. 발견 위치는 `<dir>/WATCHDOG.md` 또는 `<dir>/.omp/WATCHDOG.md`이며, 루트를 어지르지 않기 위해 후자를 택했습니다. `.omp/` 디렉터리에 `AGENTS.md`를 두지는 마세요(위 지침 파일 절). 함께 두는 `WATCHDOG.yml`(advisor 명단·모델·도구)은 모델과 비용에 관한 프로젝트별 선택이라 템플릿에 포함하지 않습니다. (근거: OMP `docs/advisor-watchdog.md`. import 경로의 `..` 해석을 사용 중인 버전에서 확인하세요.)
- 스킬(`review-round`, `design`)은 같은 내용을 두 경로에 둡니다. `.agents/skills/`는 Codex, Cursor, OMP가 읽고 `.claude/skills/`는 Claude Code가 읽습니다. 모든 파일은 `docs/`의 절차 문서를 가리키는 어댑터이며 절차 자체를 담지 않습니다. Cursor는 두 경로를 모두 로드하므로 슬래시 명령이 중복 표시될 수 있습니다. 내용이 같아 동작 차이는 없으며, Claude Code를 쓰지 않는 저장소라면 `.claude/skills/` 복제본을 생략해도 됩니다.
- `review-round`는 명시 호출 전용입니다. Claude Code·Cursor·OMP는 `disable-model-invocation: true`를 사용하고 Codex는 아래 별도 설정을 사용합니다. `design`은 합의 전까지 읽기 전용이라 자동 호출을 차단하지 않습니다. 모델이 설명 문구에 맞는 변경에서 스스로 절차를 시작할 수 있으며, 적용 조건은 [01-DESIGN.md](./01-DESIGN.md) §1이 가릅니다.
- 자동 호출 차단 키는 Cursor·Claude Code 모두 `disable-model-invocation`이고 OMP는 이 표기를 그대로 인식합니다. Codex는 [.agents/skills/review-round/agents/openai.yaml](../.agents/skills/review-round/agents/openai.yaml)의 `policy.allow_implicit_invocation: false`로 자동 호출을 차단하며 명시적 `$review-round` 호출은 허용합니다([공식 문서](https://learn.chatgpt.com/docs/build-skills)). 이 설정은 Codex 전용이므로 `.claude/skills/`에 복제하지 않습니다. 두 `SKILL.md`의 내용은 동일하게 유지하며 본문에도 명시 호출 조건을 남깁니다. `argument-hint`는 Claude Code 전용 필드이며 다른 도구는 무시합니다.
- Codex의 GitHub 리뷰는 인라인 finding에 `AGENTS.md` 줄 번호를 인용하고 finding 형식(`confidence`, `blocking`)도 그 절을 따릅니다. `AGENTS.md`의 Code Review Rules는 로컬 에이전트만이 아니라 GitHub 리뷰어의 출력 형식에도 영향을 주므로, 링크만 남기고 본문을 줄이지 마세요. Codex가 링크된 `docs/REVIEW.md`까지 읽는지는 확인되지 않았습니다.

### 외부 방법론·행동 규칙 도구

공통으로 항상 적용할 짧은 규칙은 루트 `AGENTS.md`에, 조건부로 읽는 절차는 `docs/`에 둡니다. 스킬은 그 절차를 가리키는 어댑터이며 본문을 담지 않습니다. 외부 방법론이나 행동 규칙 도구를 함께 쓸 때도 이 소유권을 유지하세요.

- `AGENTS.md`와 `CLAUDE.md`는 이 템플릿이 소유합니다. 외부 초기화·갱신이 이 파일을 바꾸면 그 기능을 끄거나 도입을 재고하세요. 추가 지침 파일은 위 「지침 파일」 절을 따릅니다.
- 도구 산출물은 INTENT·SPEC·PLAN의 같은 역할을 대체할 수 있습니다. 결정 인덱스(PROJECT)와 변경 단위 계획(TODO)은 유지하고, 계약·상세 상태는 한곳에만 둡니다.
- 도구가 자체 지침 디렉터리나 관리 블록을 만들면 `AGENTS.md`와 충돌하는지 확인하세요. 그 런타임·갱신은 `Template version`이 추적하지 않으므로, 지침 파일을 다시 쓰는 diff는 검토하세요.

### 공통

- 도구 버전과 로컬 설정에 따라 지침 로딩 결과를 직접 확인하세요. Markdown 링크만으로 모든 연결 문서가 자동 로드된다고 가정하지 마세요.
- [PROJECT_ANALYSIS.md](./PROJECT_ANALYSIS.md)는 전체 프로젝트 분석을 명시적으로 요청할 때 사용하는 절차입니다. 공통 지침에 전체 내용을 자동 import하지 않습니다.
- [01-DESIGN.md](./01-DESIGN.md)도 절차 문서입니다. `AGENTS.md`에는 적용 조건과 산출물 위치만 두고 단계 자체는 import하지 않습니다. 모든 작업에 설계 절차가 실려 있으면 모델이 작은 요청을 절차로 부풀립니다.

## 5. 적용 후 관리

- 일상적인 문서 관리 방법과 문서별 수정 권한은 [문서 운영 안내](./DOCS_GUIDE.md)를 기준으로 합니다.
- [DOCS_GUIDE.md](./DOCS_GUIDE.md)의 이름은 의도적으로 `README.md`가 아닙니다. 루트 README의 번역본을 `docs/README.ko.md`처럼 `docs/`에 두는 관행과 파일명이 충돌하기 때문입니다. `docs/README.md`로 되돌리지 마세요.
- 모든 저장소 내부 Markdown 링크는 해당 파일을 기준으로 한 상대 경로를 사용합니다. 파일을 옮기거나 이름을 바꾸면 참조하는 링크도 함께 수정하세요.
- 이 문서는 템플릿 적용 기록으로 남겨도 됩니다. 적용 후 필요 없어 삭제한다면 적용 프로젝트 [README.md](../README.md)와 [문서 운영 안내](./DOCS_GUIDE.md)에 있는 이 문서 링크도 함께 제거하세요.
- Cursor Bugbot을 사용하지 않아 [.cursor/BUGBOT.md](../.cursor/BUGBOT.md)를, 또는 OMP를 사용하지 않아 [.omp/WATCHDOG.md](../.omp/WATCHDOG.md)를 제거한다면 이 안내와 [DOCS_GUIDE.md](./DOCS_GUIDE.md)의 해당 링크와 구조 설명도 정리하세요.

### Git으로 복사 기준 기록하기

복사 전에 **템플릿 원본 checkout에서** 다음을 확인합니다. 적용 프로젝트의 HEAD는 원본 revision이 아닙니다.

```bash
git rev-parse HEAD
git describe --tags --always --dirty
git status --short --untracked-files=all
```

- `Template source`에는 원본을 다시 열 수 있는 저장소 URL 또는 보관 위치를, `Template revision`에는 첫 명령의 **전체 commit SHA**를 기록합니다.
- `Template version`은 릴리스 tag와 정확히 일치하는 원본이면 판 번호(예: tag `v1.2` → `1.2`)를 기록합니다. tag가 가리키는 commit은 `git rev-parse 'v1.2^{commit}'`으로 확인해 원본 SHA와 대조합니다. tag 이후 commit은 `미릴리스 (최근 tag: v1.2)`, tag가 없으면 `미릴리스 (tag 없음)`으로 구분하고 정확한 SHA를 함께 남깁니다.
- `git describe`는 tag 이후 commit 수와 축약 SHA를 보여 주는 확인 보조값입니다. 전체 SHA를 대신하지 않습니다. `-dirty`가 없더라도 새 파일이 빠질 수 있으므로 `git status`의 미추적 파일도 확인합니다. 미커밋 변경을 포함해 복사하면 `Template revision`을 `미확정 (기준 commit: <전체 SHA>, 미커밋 변경 포함)`으로 표시하고 포함한 변경을 기록합니다. SHA 하나로 복사본 전체가 재현된다고 주장하지 않습니다. 원본 이력을 확보하지 못한 경우도 `미확정`으로 남깁니다. ([Git describe](https://git-scm.com/docs/git-describe), [Git status](https://git-scm.com/docs/git-status))
- 두 안내 문서가 있으면 source·version·revision을 같게 유지합니다. 이 문서를 삭제할 경우에는 [DOCS_GUIDE.md](./DOCS_GUIDE.md)에 기록과 일부 반영 내역을 남깁니다. 이 값은 원본 문서의 식별자이며 도구 호환성 검증을 뜻하지 않습니다. 도구 로딩을 확인했다면 해당 도구 버전·확인 날짜·결과를 별도로 기록하세요.
- 템플릿 관리자는 릴리스 시 판 번호와 변경 이력을 갱신한 commit에 `v<판 번호>` tag를 붙입니다. 게시한 tag는 옮기지 않고 후속 변경은 새 commit과 다음 판으로 남깁니다. 이 절차를 읽거나 템플릿을 복사하는 것만으로 commit·tag 생성·push가 위임되지는 않습니다.

### 템플릿 행동 검증 사례

지침·스킬·검사 스크립트를 바꿀 때 아래가 여전히 성립하는지 확인합니다. `scripts/check-docs.py`가 대체하지 않으며, 실패하면 해당 문장이나 스킬 description을 고칩니다.

| 사례 | 기대 행동 | 실패로 보는 것 | 근거 |
|---|---|---|---|
| 작은 버그 수정 | 설계 파일 없이 수정 | INTENT·SPEC을 강제 | [01-DESIGN.md](./01-DESIGN.md) §1 |
| 승인된 설계의 구현 | 상위 절을 연결하고 필요한 PLAN만 작성. 재승인 없음 | 전체 설계 절차나 재승인을 요구 | [01-DESIGN.md](./01-DESIGN.md) §1·§3.6 |
| PLAN 체크 완료 | 해당 브랜치의 구현·검증 완료로만 보고 | 통합·릴리스·지원 검증 완료로 표시 | [DOCS_GUIDE.md](./DOCS_GUIDE.md), [01-DESIGN.md](./01-DESIGN.md) §4 |
| OMP를 쓰지 않는 저장소의 도구 전용 지침 | 공통 규칙을 복제하지 않는 전용 파일은 허용 | 모든 프로젝트에 생성 금지 | 이 문서 §4 |
| 러너를 지정하지 않은 CI 요청 | [CI.md](./CI.md)의 워크플로·체크리스트만 작성·연결 | GitHub Actions·Buildkite 등 제품 YAML을 새로 생성 | [CI.md](./CI.md) §4·§6 |

### 템플릿 개정 반영하기

- §6의 변경 이력을 읽고 반영할 변경을 고릅니다. 이력은 요약이므로 **원본 저장소에서** 기록된 이전 SHA와 새 SHA를 `git diff <이전 원본 SHA> <새 원본 SHA> -- <파일>`로 비교합니다. 두 기준이 정확히 tag와 일치하면 `git diff v1.1 v1.2 -- <파일>`처럼 비교해도 됩니다. 기존 기록이 판 번호뿐이라면 해당 tag의 SHA를 확인해 보완하되, 당시 미릴리스 변경을 포함했는지 알 수 없으면 확정된 복사 기준으로 단정하지 않습니다.
- 그 결과를 적용 저장소의 파일과 대조합니다(`git diff --no-index <템플릿 파일> <적용 파일>`). 프로젝트가 의도적으로 바꾼 부분까지 되돌리지 마세요. 이력에 없는 차이는 템플릿 쪽 누락인지 프로젝트의 의도적 변경인지 구분합니다.
- 반영한 뒤 두 안내 문서의 version·revision을 새 복사 기준으로 갱신합니다. 같은 판 안의 다른 commit을 반영해도 revision은 갱신합니다. 일부만 반영했다면 적용·제외한 항목과 이유를 [DOCS_GUIDE.md](./DOCS_GUIDE.md)에 함께 남겨 해당 SHA 전체를 적용한 것으로 오해하지 않게 합니다. `CHANGELOG.md`가 있으면 새 기준과 반영 항목을 요약합니다.

## 6. 템플릿 변경 이력

<!-- template-section:release-history -->

적용 저장소가 어느 변경을 아직 반영하지 않았는지 확인하는 용도입니다. 각 항목은 "무엇이 바뀌었고, 적용 저장소에서 무엇을 확인해야 하는지"만 적습니다. 템플릿 저장소는 각 판을 git tag(`v1.1`, `v1.2`, …)로 남기므로, 이력이 요약한 내용의 원문은 `git diff v1.1 v1.2`로 봅니다. `v1.1` 이전 판은 tag가 없습니다.

### v1.7.1 — 문서 게이트 정본과 회귀 테스트 범위 교정

- G-docs와 G-docs-test 명령을 `AGENTS.md`와 적용 프로젝트 README 양식에 명시해 [CI.md](./CI.md)의 명령 정본 규칙과 일치시켰습니다.
- G-docs-test가 적용 프로젝트의 다른 `test*.py`를 함께 실행하지 않도록 `test_check_docs.py`로 discovery pattern을 제한했습니다.
- 적용 저장소에서 확인할 것: 문서 검사 파일을 유지한다면 두 명령을 프로젝트 지침과 README에 같은 문자열로 남기고, 기존 CI의 G-docs-test도 제한된 pattern으로 갱신하세요.

### v1.7 — 템플릿 소개 README 분리와 러너 불문 CI 게이트

- 루트 `README.md`를 이 템플릿 저장소 소개로 두고, 적용 프로젝트 README 양식은 `README-PROJECT.md`로 분리했습니다. Origin 등 호스트에서 원본 저장소를 열면 프로젝트 placeholder가 아니라 템플릿 설명이 보입니다.
- 적용 절차 §2 2단계: `README-PROJECT.md`를 `README.md`로 바꿔 넣고 상단 적용 안내 주석을 삭제한 뒤 placeholder를 채웁니다. 적용 저장소에 템플릿 소개 README와 `README-PROJECT.md`를 남기지 않습니다.
- [DOCS_GUIDE.md](./DOCS_GUIDE.md) 적용 체크리스트에 README 교체 항목을 추가했습니다.
- [CI.md](./CI.md) 신설: GitHub Actions·Buildkite 등 제품 YAML 없이 품질 게이트 워크플로와 연결 체크리스트만 둡니다. 적용 절차 §2 13단계, AGENTS.md, 적용 체크리스트에서 이 문서를 가리킵니다.
- 적용 저장소에서 확인할 것: 이미 채운 프로젝트 `README.md`를 이 판의 템플릿 소개문으로 바꾸지 마세요. 새 복사본만 `README-PROJECT.md` → `README.md` 교체 절차를 따릅니다. 이미 적용한 저장소는 자기 README를 유지합니다. CI를 쓰면 기존 러너에 [CI.md](./CI.md) 게이트를 연결했는지, 사용자가 제품을 지정하기 전에 워크플로 파일을 새로 만들지 않았는지 확인하세요.

### v1.6.1 — v1.6 리뷰 후속 수정

- 잘못 표기한 `v1.31` tag와 이력을 `v1.3.1`로 교정해 숫자 버전 정렬에서 `v1.6`보다 최신으로 선택되지 않게 했습니다.
- `scripts/check-docs.py`가 Codex의 `policy.allow_implicit_invocation: false` boolean을 확인하고, 저장소 밖 경로의 제외 디렉터리명에 영향받지 않으며, 여러 줄 불변조건·깊은 절 번호·없는 문서 대상을 검사합니다.
- `tests/test_check_docs.py`에 위 실패 경로와 합본형 양식의 단독 사용을 고정했습니다.
- `_template/`의 네 양식은 템플릿 적용 시 모두 유지하되, 실제 변경 폴더에서는 필요한 형식만 사용하도록 소유권을 명확히 했습니다.

### v1.6 — 문서 검사 확대와 합본형 변경 양식

- `scripts/check-docs.py`: 저장소 루트 판별을 `AGENTS.md`로 바꾸고, 이 문서를 §5에 따라 삭제한 저장소에서도 동작하도록 판 대조를 선택 검사로 만들었습니다. 이전에는 이 문서가 없으면 검사가 종료 코드 2로 끝났습니다.
- `scripts/check-docs.py`: 링크 검사를 `.md` 외의 상대 링크까지 확대하고, `review-round` 스킬이 있는데 Codex 명시 호출 설정(`agents/openai.yaml`)이 없으면 실패합니다. 이 설정이 빠지면 Codex에서 암묵 호출이 열립니다.
- `scripts/check-docs.py`: [REVIEW.md](./REVIEW.md) §6과 [.cursor/BUGBOT.md](../.cursor/BUGBOT.md)의 불변조건 목록을 대조합니다. 절 번호가 아니라 헤딩 문구로 절을 찾으므로 병합으로 번호가 바뀐 저장소에서도 동작합니다.
- `scripts/check-docs.py`: 문서를 지목한 절 번호 참조(`REVIEW.md §6`, `PROJECT §8` 등)를 실제 헤딩과 대조합니다. 대상이 모호한 같은 파일 안의 참조와 §6 릴리스 이력의 옛 번호는 검사하지 않습니다. 생성물 디렉터리(`dist`, `build`, `target`, `vendor` 등)는 건너뜁니다.
- [`docs/changes/_template/01-CHANGE.md`](./changes/_template/01-CHANGE.md) 신설: [01-DESIGN.md](./01-DESIGN.md) §4가 규정한 합본형 절 구성을 양식으로 제공합니다. 분리형 INTENT·SPEC의 변경 기록 절은 하나로 합쳤습니다.
- [DOCS_GUIDE.md](./DOCS_GUIDE.md): 적용 체크리스트에 `LICENSE` 교체 항목을 추가했습니다. 템플릿 자체의 MIT 고지를 프로젝트 라이선스로 두지 않도록 확인합니다.
- 적용 저장소에서 확인할 것: `scripts/check-docs.py`를 새 판으로 교체했는지, 새 검사가 보고하는 불변조건·절 번호 불일치가 실제 문서 불일치인지(오탐이 아니라 그동안 잡히지 않던 차이일 수 있습니다), 합본형을 쓰지 않는다면 `01-CHANGE.md`와 들어오는 링크를 제거했는지, `LICENSE`를 교체했는지 확인하세요.

### v1.5.1 — 공존 안내 일반화, Copilot 힌트 정리

- `docs/TEMPLATE_GUIDE.md` §4: 외부 방법론·행동 규칙 절에서 특정 도구 사례를 빼고, 상시 규칙은 `AGENTS.md`·조건부 절차는 `docs/`·스킬은 어댑터라는 소유권만 남겼습니다.
- Copilot 재요청 힌트를 표와 명령 블록으로 나눴습니다. GraphQL 요청·접수 확인과 REST no-op 주의는 유지합니다.
- 적용 저장소에서 확인할 것: 공존 절이 특정 제품명에 묶여 있지 않은지, §2.1에 Copilot을 쓸 때 명령 블록(또는 그 참조)이 있는지 확인하세요.

### v1.5 — 도구 조건, 문서 검사, 식별자·수명

- `docs/TEMPLATE_GUIDE.md` §4: `.claude/CLAUDE.md` 등 추가 지침 파일 금지를 OMP 사용 시의 조건부 안내로 바꿨습니다. OMP를 쓰지 않으면 도구 전용 파일을 허용하되 공통 규칙은 복제하지 않습니다.
- `scripts/check-docs.py`: 상대 링크, 스킬 사본, `CLAUDE.md`/WATCHDOG import, 두 안내 문서의 Template version을 표준 라이브러리만으로 검사하고 실패 시 0이 아닌 종료 코드로 끝냅니다. 인라인 링크 검사 예시를 대체합니다.
- 변경-ID·`D-nnn`·`T-nnn`·변경 내부 ID의 발급 범위와 병렬 브랜치 충돌 처리를 정했습니다. 완료·취소·보류 변경 폴더는 유지하고, 구현된 계약은 통합 후 PROJECT 현재 기준에만 반영합니다.
- 지침·스킬 변경 때 확인할 행동 검증 사례를 추가했습니다.
- 적용 저장소에서 확인할 것: OMP를 쓰지 않는데도 전용 지침 파일을 일괄 금지하는 문장이 남아 있지 않은지, `scripts/check-docs.py`를 복사했는지, `D-`/`T-` ID를 변경 내부 ID와 섞지 않는지, 완료된 SPEC을 현재 제품 기준으로 읽지 않는지 확인하세요.

### v1.4 — 번호 문서와 변경별 산출물

- 공통 문서를 `00-PROJECT.md`, `01-DESIGN.md`, `02-TODO.md`로 이관했습니다. PROJECT는 기본 제품 설계와 기존 설계 인덱스를 수용합니다.
- 선택형 `10-EXTENSION.md`와 `changes/_template/`의 대문자 INTENT·SPEC·PLAN 양식을 추가했습니다. 작은 작업은 최소 문서, 승인된 단계 구현은 상위 설계 참조를 사용합니다.
- 전역 변경 목록과 상세 실행 상태의 소유권, 로컬 Git·병렬 브랜치·통합 완료·승인 근거를 정의했습니다. 새 형식은 승인 버전을 보존하면서 명세와 실행 계획의 갱신을 구분합니다.
- 지침·스킬·리뷰·분석의 경로와 인계 대상을 함께 갱신했습니다. 리뷰 라운드 통과 후에는 PLAN도 동결하고 다음 관련 작업에서 기록을 반영합니다.
- 적용 저장소에서는 §2 이관 표에 따라 고정 정책 경로·검사 코드·스킬 참조와 상태 중복 여부를 확인하세요.

아래 릴리스 이력의 옛 파일명·절 번호는 당시 구조를 설명합니다. 현재 경로로 실행할 지침이 아니며 위 이관 표와 현재 절차를 따릅니다.

### v1.3.1

- `docs/DESIGN.md`: §5의 프로젝트 고유 정보 금지에 §6의 기존 설계 문서 경로 한 줄 예외를 명시해 문언상 충돌을 해소했습니다.
- `.agents/skills/review-round/`, `.claude/skills/review-round/`: 스킬 description이 기본 `on_pass`를 반영하도록 갱신했습니다. PR은 사용자 확인 후 merge하고, PR이 없으면 `merge 안 함`으로 종료합니다. 두 `SKILL.md`는 동일하게 유지합니다.
- 적용 저장소에서 확인할 것: 기존 설계 문서 경로 외의 프로젝트 고유 정보가 `DESIGN.md`에 남아 있지 않은지, 두 review-round 스킬 description이 `on_pass` 기본값과 일치하는지 확인하세요.

### v1.3

- `docs/REVIEW_ROUND.md`: 기본 통과 조건을 `모든 P0 = 0, 모든 P1 = 0, blocking P2 = 0`으로 변경. 기본값에서는 유효하고 미해소인 P0·P1이 `blocking=false`이거나 승인된 deferral이어도 통과를 막습니다. 사용자가 지정한 임계값은 기본값보다 우선하며 수정·이관·조기 중단·소진 보고도 확정값을 따릅니다. 진행 중 명시적 변경의 기록·재평가 규칙과 기본 판정표를 추가했습니다.
- `.agents/skills/review-round/`, `.claude/skills/review-round/`: 기본 임계값을 갱신했습니다. 두 `SKILL.md`는 동일하게 유지합니다.
- `docs/REVIEW.md` (`Policy version` 1.2), `.cursor/BUGBOT.md`, `AGENTS.md`: 검증된 기존 P0·P1의 보고 예외와 라운드 통과 조건을 일치시켰습니다. `blocking` 분류와 단일 리뷰의 verdict 규칙은 유지합니다.
- `.agents/skills/review-round/agents/openai.yaml`: Codex에서 명시 호출만 허용하도록 `policy.allow_implicit_invocation: false`를 추가했습니다. Claude·Cursor·OMP용 frontmatter와 두 `SKILL.md`의 일치는 유지합니다.
- `docs/REVIEW_ROUND.md`, 두 `review-round/SKILL.md`: `self`는 리뷰어 등록·외부 요청·대기 없이 실행하고 세션에 원장을 남깁니다. `merge 안 함`은 통과·미병합으로 종료하며, PR 없는 실행의 기본값입니다.
- `docs/TEMPLATE_GUIDE.md`, `docs/DOCS_GUIDE.md`: placeholder 검색에 숨김 폴더를 포함하고 원본 템플릿과 적용 저장소의 검사를 구분했습니다. 검색 0건을 적용 완료로 간주하지 않습니다.
- `docs/REVIEW_ROUND.md`, 두 `review-round/SKILL.md`: 통과한 head를 유지하고 남은 finding과 판정 근거를 세션 인계 목록으로 전달합니다. 병합 직전에는 상태와 새 결과만 확인하며, 기록용 추가 push를 하지 않습니다. §9의 저장소 문서 반영은 사용자가 시작한 다음 관련 구현·문서 수정 작업으로 옮기고, `AGENTS.md`에 라운드 재시작 없이 §9만 적용하는 진입 조건을 추가했습니다.
- `docs/TEMPLATE_GUIDE.md`, `docs/DOCS_GUIDE.md`: 원본 위치·판·전체 SHA를 함께 기록하도록 `Template revision`과 Git 확인 절차를 추가했습니다. 미릴리스·미커밋 변경·일부 반영을 구분하고 개정 비교는 원본 SHA를 기준으로 합니다.
- 적용 저장소에서 확인할 것: 기본값에서 비차단 P0·P1을 제외하는 예외가 남지 않았는지, 사용자 지정 임계값이 수정·이관에도 반영되는지, 통과 후 즉시 TODO를 갱신하는 조항이 남지 않았는지 확인하세요. 두 스킬과 Bugbot 복제본, 원본 revision 기록도 함께 갱신합니다. 원본 템플릿의 `Template version`은 다음 판을 릴리스할 때 올립니다.

### 1.2

- `docs/DESIGN.md`: §1 제외 조건을 "확정으로 기록된 설계의 구현"으로 일반화(PLAN.md §8 `Accepted` 또는 기존 설계 문서의 확정 단계). §3.4에 조건부 절을 삭제한 저장소의 대조 대상 안내. §6 「기존 설계 문서가 있는 저장소」 신설 — 옮기지 않음, PLAN.md가 인덱스인 저장소의 산출물 해석, 자체 체크리스트와의 관계. 기존 §6 외부 스펙 도구는 §7로.
- `.agents/skills/design/`, `.claude/skills/design/`: description에 "이미 확정으로 기록된 설계의 구현에는 쓰지 않음" 추가. 자동 호출 조건이므로 적용 저장소의 두 파일도 갱신할 것.
- `.agents/skills/review-round/`, `.claude/skills/review-round/`: 3번 기본값에 `rereview = auto` 추가.
- `docs/REVIEW_ROUND.md`: §1 위임되지 않는 것에 릴리스 게시·tag 생성. §2.1 `게시 위치`에 코멘트 덮어쓰기(sticky) 여부 기록. §3 4단계 검증에 Build와 생성물 재생성 포함. §7에 덮어쓰는 리뷰어의 finding은 판정 기록에 남긴다는 규칙.
- `docs/DOCS_GUIDE.md`: 절 번호 참조 대조 항목을 `DESIGN.md`·`WATCHDOG.md`와 PLAN.md 조건부 절 삭제까지 확대. 기존 설계 문서 항목 추가. 리뷰어 표 항목에 `재리뷰 요청 방법` 열 언급. Maintenance에 tag 대조와 CHANGELOG 기록.
- `docs/TEMPLATE_GUIDE.md`: §2 병합 안내에 네 파일 절 참조와 DESIGN.md §6 안내. 리뷰어 힌트 표에 자체 호스팅 GitHub App 행. §5에 tag 간 `git diff` 대조와 CHANGELOG 기록. 이 이력 절에 tag 안내.
- 템플릿 저장소를 git으로 관리 시작. `v1.1`은 1.1 최종 상태, `v1.2`는 이 판.
- 첫 적용 PR(claude-code-pr-review #33)의 리뷰 라운드 2회에서 나온 수정을 같은 판에 포함:
  - `docs/REVIEW_ROUND.md`: §1 위임에 "처리한 finding의 인라인 스레드 해소 표시" 추가(§6이 요구하는데 위임 목록에 없었음). §2.1 접수 확인 예시를 REST `requested_reviewers`/GraphQL `reviewRequests`로 구분하고 확인 시점 명시. §3 `request`에서 접수 확인된 리뷰어를 그 라운드 정족수에 포함. push 없는 라운드의 예외로 base 변경 처리. §4 base 변경에서 위임되는 것은 non-force merge만이며 rebase는 제외. §7에 PR이 있을 때 판정 기록의 위치(세션 + §10 보고).
  - `AGENTS.md`: DESIGN 예외를 canonical §1과 같은 조건("원인이 구조 문제가 아닌 버그", "외부 계약이 바뀌지 않는 단일 모듈")으로 한정. 위임 조항에 스레드 해소 표시 추가.
  - `.agents/skills/design/`, `.claude/skills/design/`: description의 예외에도 같은 조건.
  - `docs/DESIGN.md` §4: `docs/changes/` 파일의 `Status`에 `Superseded by <링크>` 허용. 본문만 동결.
  - `docs/DOCS_GUIDE.md`: Metadata에 `Template source` 필드 — 템플릿 저장소 위치와 tag 규칙. 없으면 §5의 tag 비교를 재현할 수 없습니다.
  - `docs/TEMPLATE_GUIDE.md`: Copilot 재요청은 GraphQL `requestReviews`를 1차로. REST no-op이 실제 관찰됨. 복사해 실행할 수 있는 `gh api graphql` 명령 블록 추가.
  - 3라운드 추가분: `docs/REVIEW_ROUND.md` §1의 "push 없이는 라운드가 시작되지 않는다" 단정 제거(base 변경과 상충). §4에 「중요도 정규화」 — P 척도를 쓰지 않는 리뷰어의 finding은 REVIEW.md Severity 정의로 재판정하고 원 라벨을 원장에 남김. `docs/DESIGN.md` 머리말에 `docs/changes/`를 설계 상세 위치로 명시, §2에 「두 규모 공통」 — 리뷰 판정에 영향을 주는 결정은 규모와 무관하게 REVIEW.md §6·§9와 BUGBOT.md를 같은 커밋에서 갱신.
  - 후속 라운드: `docs/REVIEW_ROUND.md` §3 1라운드에서 `rereview = request`이면, 확정한 `reviewers`에 들어 있고 명시적 요청 방법이 있으며 현재 head 결과가 없는 리뷰어에게만 push 없이 요청한다. `push 자동`만 있는 리뷰어는 요청하지 않는다. 접수 확인이 요청 응답 밖 신호(댓글 반응 등)이면 즉시 실패로 보지 않고 기본 2분 한도까지 다시 확인한다. 확인 식별자는 그 API의 필드 값을 쓰며 REST `[bot]` username과 GraphQL `Bot.login`을 같은 문자열로 취급하지 않는다. `docs/DESIGN.md` §1은 명시적 `design` 호출이 예외 목록보다 우선한다.
- 적용 저장소에서 확인할 것: `design` 스킬 description이 갱신되었는지, `REVIEW_ROUND.md` §2.1 표의 PR 코멘트형 리뷰어에 덮어쓰기 여부가 적혀 있는지, 절 번호로 참조하는 네 파일의 참조가 실제 헤딩과 맞는지, `DOCS_GUIDE.md`에 `Template source`가 채워져 있는지.

### 1.1

- `AGENTS.md`: 리뷰 라운드 위임 범위에 non-force push, 파라미터로 지정된 재리뷰 요청, 사용자 확인을 거친 merge를 명시. 그 외 PR 댓글 게시는 위임 제외. 명령 표의 `{{...}}` placeholder 실행 금지 문구 추가. Document System에 `docs/DESIGN.md` 항목 추가. Change Rules에 재사용 순서·최소 코드·원인 수정·최소화 제외 규칙 4줄 추가(ponytail 규칙을 옮김).
- `docs/DESIGN.md` 신설: 구조·계약 변경의 구현 전 설계 절차(적용 조건, 규모 판정, 6단계, 산출물 규칙). `.agents/skills/design/`, `.claude/skills/design/` 어댑터 추가. `docs/changes/`는 큰 변경에서만 생성.
- `.omp/WATCHDOG.md` 신설: OMP advisor 전용 리뷰 우선순위. `REVIEW.md`를 `@` import.
- `docs/REVIEW_ROUND.md`: `reviewers = self` 옵션, 리뷰어 표 미등록 시 시작 거부, `REVIEW.md` 절 참조에 제목 병기, 접힌 `<details>` 블록 수집, base 변경 시 새 라운드, 리뷰어의 부분 검토 자기 보고를 `부분 결과`로 기록하고 merge 확인에 제시. `rereview` 파라미터(`auto` 기본, `request`는 사용자 지정 시) 추가와 §2.1 표에 `재리뷰 요청 방법` 열 추가, §3 1단계를 라운드별 요청 규칙으로 재작성.
- `docs/REVIEW.md`: 변경 없음 (`Policy version` 1.1 유지).
- `.cursor/BUGBOT.md`: 프로젝트 불변조건과 확정된 설계 결정·승인된 deferral 절 추가.
- `docs/PLAN.md`: 필수 절과 조건부 절 구분 안내 추가.
- `docs/DOCS_GUIDE.md`: `Last reviewed`를 UTC 기준으로 명시, 적용 체크리스트에 `BUGBOT.md` 불변조건, 절 번호 대조, CODEOWNERS, 링크 검사 추가.
- `docs/DOCS_GUIDE.md`: Document Map·Flow·Source-of-truth에 `DESIGN.md` 추가, 체크리스트에 `WATCHDOG.md` import 확인, `design` 스킬, 외부 방법론 도구 공존 확인 추가. CODEOWNERS 목록에 `.omp/`, `docs/DESIGN.md` 추가.
- `docs/TEMPLATE_GUIDE.md`: placeholder 검색 명령 보정, 링크 검사 스크립트, `disable-model-invocation`·Cursor 이중 경로 설명, 리뷰어 조사 힌트, CODEOWNERS 안내, §4 「외부 방법론·행동 규칙 도구」(ponytail·OpenSpec·BMAD·Kiro 공존 규칙), 이 변경 이력 추가.
- `LICENSE`: 템플릿 자체를 MIT로 배포. 적용 저장소는 프로젝트 라이선스로 교체.
- 적용 저장소에서 확인할 것: `.agents/skills/`와 `.claude/skills/`의 각 `SKILL.md`가 byte-identical한지, `REVIEW_ROUND.md` §2.1 리뷰어 표가 채워져 있고 `재리뷰 요청 방법` 열이 있는지, `BUGBOT.md` 불변조건이 `REVIEW.md` §6과 같은지, OMP를 쓰면 `.omp/WATCHDOG.md`의 import가 확장되는지.

### 1.0

- 최초 배포 판. 이 판 이전의 이력은 기록하지 않았습니다.
