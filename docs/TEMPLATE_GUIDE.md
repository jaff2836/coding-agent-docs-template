# Template Guide

이 문서는 문서 중심 프로젝트 템플릿의 최초 적용 안내입니다. 실제 프로젝트의 소개·설치·실행 방법은 루트 [README.md](../README.md)에 작성하세요.

초기화 스크립트, GitHub Actions용 리뷰 프롬프트 및 자동 리뷰 실행 구성은 포함하지 않습니다. 파일을 복사하고 프로젝트 값을 직접 채우는 방식입니다.

## Metadata

- **Status:** Active
- **Template version:** 1.2
- **Owner:** 프로젝트에 맞게 작성
- **Last reviewed:** YYYY-MM-DD
- **Review cadence:** 템플릿 구조 또는 도구 연결 방식 변경 시

`Template version`은 이 저장소가 어느 템플릿 판에서 복사되었는지를 남기는 값입니다. 프로젝트에서 문서를 고칠 때 바꾸지 말고, 템플릿 개정을 따라 반영했을 때만 올리세요. 판별 변경 내용은 §6에 있습니다.

## 1. 포함된 구조

```text
.
├── README.md                  # 실제 프로젝트 소개와 사용법
├── AGENTS.md                  # AI 개발 도구의 공통 프로젝트 지침
├── CLAUDE.md                  # @AGENTS.md 참조
├── LICENSE                    # 템플릿 자체의 MIT 라이선스. 프로젝트 라이선스로 교체
├── .gitignore
├── .agents/
│   └── skills/
│       ├── design/
│       │   └── SKILL.md       # 변경 설계 절차 진입점: Codex, Cursor, OMP
│       └── review-round/
│           └── SKILL.md       # 리뷰 라운드 진입점: Codex, Cursor, OMP
├── .claude/
│   └── skills/
│       ├── design/
│       │   └── SKILL.md       # 변경 설계 절차 진입점: Claude Code
│       └── review-round/
│           └── SKILL.md       # 리뷰 라운드 진입점: Claude Code
├── .cursor/
│   └── BUGBOT.md              # 선택 사항: 리뷰 판정 기준 복제본
├── .omp/
│   └── WATCHDOG.md            # 선택 사항: OMP advisor 전용 리뷰 우선순위. REVIEW.md를 import
└── docs/
    ├── DOCS_GUIDE.md          # 문서 인덱스·운영 규칙·적용 완료 체크리스트
    ├── TEMPLATE_GUIDE.md      # 이 문서: 최초 적용 방법
    ├── PLAN.md                # 목표·현재/목표 구조·전환 계획·결정
    ├── DESIGN.md              # 구조·계약을 바꾸는 변경의 구현 전 설계 절차
    ├── changes/               # 큰 변경의 설계 파일. 템플릿에는 없고 DESIGN.md §2에 따라 필요할 때 생성
    ├── TODO.md                # 현재 실행 작업과 검증 상태
    ├── REVIEW.md              # 공통 PR 리뷰 정책
    ├── REVIEW_ROUND.md        # 리뷰 라운드 절차와 권한 위임 범위
    └── PROJECT_ANALYSIS.md    # 요청 시 사용하는 전체 분석 절차
```

## 2. 새 프로젝트에 적용하기

1. 이 템플릿의 내용을 새 프로젝트 폴더로 복사합니다. 숨김 항목인 `.agents/`, `.claude/`, `.cursor/`, `.omp/`와 `.gitignore`도 확인하세요.
2. [프로젝트 README](../README.md)에 프로젝트 이름, 설명, 요구사항, 설치·실행·검증 방법, 보안 안내 및 라이선스를 작성합니다. 파일명을 바꿀 필요는 없습니다.
3. [AGENTS.md](../AGENTS.md)의 프로젝트 정보와 명령을 실제 저장소에 맞게 작성합니다. README의 실행 방법과 서로 일치하도록 확인하세요.
4. 아래 placeholder와 예시 항목을 교체합니다.
5. [PLAN.md](./PLAN.md)에 현재 구현된 구조와 합의된 목표 구조를 구분해 기록하고, [TODO.md](./TODO.md)에 첫 마일스톤의 실행 작업과 완료 조건을 작성합니다.
6. [REVIEW.md](./REVIEW.md)에 프로젝트 고유 불변조건과 실제 승인된 예외만 기록합니다.
7. [REVIEW_ROUND.md](./REVIEW_ROUND.md)의 기본 라운드 수와 통과 임계값을 확인하고, §2.1에 이 저장소에서 도는 리뷰어를 전부 기록합니다. 아래 「리뷰어 조사 힌트」를 참고하되 실제 동작은 직접 확인하세요.
8. Cursor Bugbot을 쓴다면 [.cursor/BUGBOT.md](../.cursor/BUGBOT.md)의 불변조건·확정 결정 절을 [REVIEW.md](./REVIEW.md), [PLAN.md](./PLAN.md)와 같은 내용으로 채웁니다. OMP advisor를 쓴다면 [.omp/WATCHDOG.md](../.omp/WATCHDOG.md)의 import가 동작하는지 확인하고, 두 도구를 쓰지 않으면 해당 파일을 삭제합니다.
9. [DESIGN.md](./DESIGN.md)는 절차 문서라 채울 값이 없습니다. §1 적용 조건이 프로젝트의 변경 규모 감각과 맞는지만 확인하세요.
10. 사용하는 개발 도구에서 공통 지침과 관련 문서를 의도대로 읽는지 확인합니다.
11. OpenSpec, BMAD 같은 외부 방법론 도구를 함께 쓴다면 아래 §4 「외부 방법론·행동 규칙 도구」의 공존 규칙을 먼저 적용합니다.
12. [문서 운영 안내](./DOCS_GUIDE.md)의 Template Adoption Checklist로 적용 완료 여부를 확인합니다.

기존 프로젝트에 적용할 때는 같은 이름의 파일을 덮어쓰지 말고 기존 지침·문서·ignore 규칙과 비교하여 병합하세요. 기존 코드나 사용자 변경은 보존합니다. 기존 `REVIEW.md`와 병합해 절 번호가 바뀌거나 [PLAN.md](./PLAN.md)의 조건부 절을 삭제하면, 절 번호로 참조하는 [REVIEW_ROUND.md](./REVIEW_ROUND.md), [DESIGN.md](./DESIGN.md), [.cursor/BUGBOT.md](../.cursor/BUGBOT.md), [.omp/WATCHDOG.md](../.omp/WATCHDOG.md)의 참조도 실제 헤딩에 맞게 고치세요. 도입 전부터 큰 설계 문서가 있는 저장소는 [DESIGN.md](./DESIGN.md) §6을 먼저 읽으세요 — 그 문서는 옮기지 않습니다.

### 리뷰어 조사 힌트

§2.1 표는 저장소마다 다르므로 템플릿이 채워 주지 않습니다. 다만 GitHub에서 널리 쓰이는 공개 리뷰어는 제품 수준에서 동작이 정해져 있어, 조사 시작점으로 다음이 관찰되었습니다(2026-09 기준, 사용 중인 버전에서 직접 확인).

| 리뷰어 | 관찰된 특성 | 재리뷰 요청 방법 (공식 문서 기준) |
|---|---|---|
| Codex (`chatgpt-codex-connector`) | PR review 본문의 `Reviewed commit:`으로 head 식별. 자동 리뷰는 PR이 리뷰 요청 상태로 열릴 때 1회이며 push마다 돌지 않습니다. 지적이 없어도 본문은 남깁니다. 인라인 finding에 `AGENTS.md` 줄 번호를 인용하므로 `AGENTS.md`의 Code Review Rules가 출력 형식에 영향을 줍니다 | PR 댓글 본문을 정확히 `@codex review`로. 접수 확인은 댓글에 붙는 👀 반응. **`review` 뒤에 다른 말을 붙이지 마세요** — `@codex`에 다른 문장이 이어지면 리뷰가 아니라 PR을 컨텍스트로 한 클라우드 태스크가 시작되어 branch에 push할 수 있습니다 |
| Copilot (`copilot-pull-request-reviewer`) | **PR당 1회**, head 표시 없음. 저신뢰 코멘트는 review 본문의 접힌 `<details>` "Suppressed comments"에 숨기므로 그 블록도 읽어야 합니다 | push마다 자동은 repository ruleset의 "Review new pushes"만. 요청은 아래 「Copilot 재요청 명령」을 §2.1 표에 그대로 옮겨 적고 실행합니다. 접수 확인은 mutation 응답의 `reviewRequests`에서 GraphQL `Bot.login`이 `copilot-pull-request-reviewer`인지 봅니다(`[bot]` 없음). REST username `copilot-pull-request-reviewer[bot]`은 같은 봇의 다른 API 표기입니다. 리뷰가 시작되면 요청 목록에서 빠지므로 뒤늦게 `gh pr view --json reviewRequests`로 보면 비어 있을 수 있습니다. **REST `POST /repos/{owner}/{repo}/pulls/{n}/requested_reviewers`(본문 `{"reviewers": ["copilot-pull-request-reviewer[bot]"]}`)는 200을 돌려주면서 no-op이 되는 것이 2026-09-04에 실제로 관찰되어 권하지 않습니다.** UI의 Reviewers 재요청 버튼은 사람이 누를 때의 대안입니다 |
| 자체 호스팅 GitHub App 리뷰어 (예: webhook 기반 봇) | `pull_request`의 opened·reopened·ready_for_review·synchronize를 받아 push마다 돌고, PR 코멘트에 `<!-- <이름>:v1 head:<SHA> -->` 같은 마커 주석으로 head를 남기는 구성이 일반적입니다. head마다 새 코멘트인지 하나를 덮어쓰는지는 봇마다 다르므로 표의 `게시 위치`에 적으세요 | `push 자동` — 트리거 이벤트를 함께 적습니다. 문제가 없을 때도 결과를 남기는지 확인하세요. §4 타임아웃 처리가 달라집니다 |

**Copilot 재요청 명령** (`<n>`은 PR 번호. bot node id `BOT_kgDOCnlnWA`는 2026-09 기준이며 REST `gh api users/copilot-pull-request-reviewer%5Bbot%5D --jq .node_id`로 다시 얻을 수 있습니다 — 이 URL만 `[bot]` 접미사를 씁니다. GraphQL `Bot.login`은 `copilot-pull-request-reviewer`입니다. §3의 "표에 적힌 방법을 그대로 실행"이 성립하려면 표에는 이 명령 자체 또는 이 블록으로의 참조가 있어야 합니다):

```bash
gh api graphql \
  -f query='mutation($pr:ID!,$bot:ID!){ requestReviews(input:{pullRequestId:$pr, botIds:[$bot], union:true}) { pullRequest { reviewRequests(first:10) { nodes { requestedReviewer { ... on Bot { login } } } } } } }' \
  -f pr="$(gh pr view <n> --json id --jq .id)" \
  -f bot="BOT_kgDOCnlnWA"
```

응답의 `nodes`에 GraphQL `Bot.login` `"copilot-pull-request-reviewer"`가 있으면 접수된 것입니다. REST username `copilot-pull-request-reviewer[bot]`과 같은 봇이지만, 이 확인은 GraphQL login만 사용합니다.

자체 호스팅 봇이나 GitHub Actions 기반 리뷰어는 저장소·버전마다 다르므로 마커 주석과 트리거 조건을 직접 확인해 적으세요. 앞의 두 공개 리뷰어는 기본 구성에서 push마다 돌지 않으므로, 이들만 등록된 저장소는 `rereview = request`가 아니면 2라운드부터 상시 리뷰어의 결과를 받을 수 없습니다.

## 3. 교체할 값

교체 대상은 `{{...}}` 형식만이 아닙니다. 안내 문구형 placeholder도 함께 남아 있으므로 다음 명령으로 한 번에 찾으세요.

```bash
rg -n --glob '*.md' --glob '!docs/TEMPLATE_GUIDE.md' --glob '!docs/DOCS_GUIDE.md' \
  "\{\{|프로젝트에 맞게 작성|간단히 작성|YYYY-MM-DD|\| 예시|예시 결정|예시 완료|\*\*예시:\*\*"
```

`rg`가 없으면 다음을 사용하세요.

```bash
grep -rnE "\{\{|프로젝트에 맞게 작성|간단히 작성|YYYY-MM-DD|\| 예시|예시 결정|예시 완료|\*\*예시:\*\*" \
  --include='*.md' --exclude=TEMPLATE_GUIDE.md --exclude=DOCS_GUIDE.md .
```

이 두 안내 문서는 placeholder를 설명하기 위해 그 문구를 포함하므로 검색에서 제외합니다. 결과가 0건이면 교체가 끝난 것입니다.

적용을 마쳤거나 문서를 옮긴 뒤에는 상대 링크도 확인하세요. 파일 이동은 내용이 바뀌지 않아도 링크를 깨뜨립니다.

```bash
python3 - <<'EOF'
import pathlib, re
pattern = re.compile(r"\]\(((?!https?://)[^)\s#]+?\.md)(?:#[^)]*)?\)")
broken = []
for md in pathlib.Path(".").rglob("*.md"):
    if ".git" in md.parts or "node_modules" in md.parts:
        continue
    for m in pattern.finditer(md.read_text(encoding="utf-8")):
        if not (md.parent / m.group(1)).exists():
            broken.append(f"{md}: {m.group(1)}")
print("\n".join(broken) or "no broken relative links")
EOF
```

| Placeholder | 작성할 내용 |
|---|---|
| `{{PROJECT_NAME}}` | 프로젝트 이름 |
| `{{PROJECT_DESCRIPTION}}` | 해결하는 문제와 핵심 기능 |
| `{{RUN_COMMAND}}` | 개발 또는 실행 명령 |
| `{{BUILD_COMMAND}}` | 빌드 명령 |
| `{{TEST_COMMAND}}` | 테스트 명령 |
| `{{LINT_COMMAND}}` | 린트 명령 |
| `{{TYPECHECK_COMMAND}}` | 타입 검사 명령 |
| `{{PROJECT_INVARIANT_1}}`, `{{PROJECT_INVARIANT_2}}` | 반드시 지켜야 할 프로젝트 고유 규칙. [REVIEW.md](./REVIEW.md) §6과 [.cursor/BUGBOT.md](../.cursor/BUGBOT.md) 두 곳에 같은 내용으로 |

- 사용하지 않는 명령은 `N/A`로 표시하고 [AGENTS.md](../AGENTS.md)에 이유를 남깁니다. 존재하지 않는 명령을 실행 가능한 예시처럼 남기지 마세요.
- `프로젝트에 맞게 작성`, `YYYY-MM-DD`, 담당자·마일스톤·태스크 예시도 실제 정보로 바꿉니다.
- [TODO.md](./TODO.md)의 완료 예시는 실제 완료 이력이 아닙니다. 예시를 삭제하거나 실제 작업과 검증 근거로 교체하세요.
- [PLAN.md](./PLAN.md)의 미정 사항은 미정으로 유지하고, 제안을 이미 합의된 결정으로 바꾸지 마세요. 예시 결정 행(`D-001`)도 삭제하거나 실제 결정으로 교체하세요. 조건부 절(§5~§7, §9, §10, §12)은 해당 사항이 없으면 삭제해도 됩니다. 빈 절을 placeholder 채로 남기지 마세요.
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
- **`.claude/CLAUDE.md`, `.agents/AGENTS.md`, `.github/copilot-instructions.md`를 만들지 마세요.** OMP는 같은 디렉터리 depth에서 우선순위가 높은 provider가 낮은 provider를 가리는데, 루트 `AGENTS.md`는 가장 낮은 우선순위입니다. 이 중 하나라도 있으면 OMP에서 루트 `AGENTS.md`가 로드되지 않을 수 있습니다. (근거: OMP `docs/context-files.md`의 provider 우선순위표. 사용 중인 버전에서 직접 확인하세요.)
- `.cursorrules`와 `.omp/AGENTS.md`는 이 템플릿에 포함하지 않습니다. 기존 프로젝트에 도구 전용 지침이 있다면 공통 규칙과 중복·충돌하는지 확인하세요.
- CODEOWNERS를 쓰는 저장소라면 `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, `.cursor/`, `.omp/`, `docs/REVIEW.md`, `docs/REVIEW_ROUND.md`, `docs/DESIGN.md`를 owner 규칙에 추가하세요. 이 파일들은 에이전트의 commit·merge 권한과 리뷰 판정 기준을 정하므로 소스 코드와 같은 수준으로 보호해야 합니다. 이 템플릿은 CODEOWNERS 파일 자체를 포함하지 않습니다.

### 리뷰 관련 파일

- [.cursor/BUGBOT.md](../.cursor/BUGBOT.md)는 Cursor Bugbot 전용 파일입니다. Bugbot은 `.cursor/rules/`도 링크된 문서도 읽지 않고 이 파일만 프로젝트 규칙으로 사용하므로, [REVIEW.md](./REVIEW.md)의 판정 기준을 의도적으로 복제해 두었습니다. 판정 기준만이 아니라 **§6 불변조건과 §9 Accepted Deferrals, 되돌리지 않을 확정 결정**도 복제해야 Bugbot이 canonical 정책과 같은 blocking 판정을 냅니다. 리뷰 정책을 바꿀 때는 두 파일을 함께 수정하세요.
- [.omp/WATCHDOG.md](../.omp/WATCHDOG.md)는 OMP advisor(주 에이전트를 감시하는 두 번째 모델) 전용 파일입니다. OMP는 이 파일을 advisor의 system prompt에만 붙이고 주 에이전트 컨텍스트에는 넣지 않으며, `AGENTS.md`와 달리 context file로 취급하지 않습니다. Bugbot과 다르게 `@path` import를 확장하므로 [REVIEW.md](./REVIEW.md)를 복제하지 않고 `@../docs/REVIEW.md`로 import합니다. 발견 위치는 `<dir>/WATCHDOG.md` 또는 `<dir>/.omp/WATCHDOG.md`이며, 루트를 어지르지 않기 위해 후자를 택했습니다. `.omp/` 디렉터리에 `AGENTS.md`를 두지는 마세요(위 지침 파일 절). 함께 두는 `WATCHDOG.yml`(advisor 명단·모델·도구)은 모델과 비용에 관한 프로젝트별 선택이라 템플릿에 포함하지 않습니다. (근거: OMP `docs/advisor-watchdog.md`. import 경로의 `..` 해석을 사용 중인 버전에서 확인하세요.)
- 스킬(`review-round`, `design`)은 같은 내용을 두 경로에 둡니다. `.agents/skills/`는 Codex, Cursor, OMP가 읽고 `.claude/skills/`는 Claude Code가 읽습니다. 모든 파일은 `docs/`의 절차 문서를 가리키는 어댑터이며 절차 자체를 담지 않습니다. Cursor는 두 경로를 모두 로드하므로 슬래시 명령이 중복 표시될 수 있습니다. 내용이 같아 동작 차이는 없으며, Claude Code를 쓰지 않는 저장소라면 `.claude/skills/` 복제본을 생략해도 됩니다.
- `review-round`는 commit·merge를 수행하므로 `disable-model-invocation: true`로 자동 호출을 막습니다. `design`은 합의 전까지 읽기 전용이라 이 키를 두지 않았습니다. 모델이 설명 문구에 맞는 변경에서 스스로 절차를 시작할 수 있으며, 적용 조건은 [DESIGN.md](./DESIGN.md) §1이 가릅니다.
- 자동 호출 차단 키는 Cursor·Claude Code 모두 `disable-model-invocation`이고 OMP는 이 표기를 그대로 인식합니다. Codex는 이 키를 문서화하지 않고 추가 키를 무시하므로, 본문에도 "사용자가 명시적으로 호출한 경우에만 실행"을 문장으로 남겼습니다. `argument-hint`는 Claude Code 전용 필드이며 다른 도구는 무시합니다.
- Codex의 GitHub 리뷰는 인라인 finding에 `AGENTS.md` 줄 번호를 인용하고 finding 형식(`confidence`, `blocking`)도 그 절을 따릅니다. `AGENTS.md`의 Code Review Rules는 로컬 에이전트만이 아니라 GitHub 리뷰어의 출력 형식에도 영향을 주므로, 링크만 남기고 본문을 줄이지 마세요. Codex가 링크된 `docs/REVIEW.md`까지 읽는지는 확인되지 않았습니다.

### 외부 방법론·행동 규칙 도구

이 템플릿은 "항상 적용되는 짧은 규칙은 `AGENTS.md`에, 절차는 `docs/`에, 진입점은 얇은 스킬 어댑터에" 두는 구조입니다. 설계 방법론이나 행동 규칙을 제공하는 외부 도구를 함께 쓸 때도 같은 원칙으로 판단하세요. 아래는 2026-09 기준으로 확인한 대표 사례이며, 도구 버전에 따라 다를 수 있습니다.

- **행동 규칙형 (예: ponytail)** — 작은 always-on 규칙 세트입니다. 이 템플릿의 `AGENTS.md` Change Rules에 있는 재사용 순서·최소 코드·원인 수정·최소화 제외 규칙은 [ponytail](https://github.com/DietrichGebert/ponytail)(MIT)의 규칙을 이 템플릿의 문맥에 맞게 옮긴 것입니다. 플러그인(hook, 강도 모드)까지 설치할 필요는 없습니다. ponytail의 instruction-only 어댑터가 안내하는 `.github/copilot-instructions.md` 복사는 위 지침 파일 절의 금지 항목과 충돌하므로 따르지 마세요. 참고: ponytail 자체 벤치마크에 따르면 terse reasoning 모델에서는 비용이 오히려 늘 수 있습니다.
- **스펙 워크플로우형 (예: OpenSpec, BMAD)** — 변경 단위 산출물(proposal·specs·design·tasks)을 자기 디렉터리에 생성하고 CLI로 갱신하는 시스템입니다. 도입하려면 다음을 먼저 정하세요.
  - **문서 소유권.** 결정 이유는 [PLAN.md](./PLAN.md), 작업 상태는 [TODO.md](./TODO.md)가 canonical입니다. 도구 산출물은 [DESIGN.md](./DESIGN.md) §2의 `docs/changes/` 파일을 대체하는 "변경 단위 설계 상세"로만 쓰고, PLAN.md 결정 ID를 산출물에 남깁니다. 같은 정보를 두 곳에서 관리하기 시작하면 어느 쪽이 오래되었는지 알 수 없게 됩니다.
  - **관리 블록.** OpenSpec은 `<!-- OPENSPEC:START -->`/`<!-- OPENSPEC:END -->` 마커로 관리 블록을 쓰는 구조이고, 과거 버전은 이 블록을 루트 `AGENTS.md`에도 썼습니다. 도입 전에 `openspec init`·`openspec update`가 어느 파일을 생성·수정하는지 확인하고, `AGENTS.md`·`CLAUDE.md`·`.claude/CLAUDE.md`·`.agents/AGENTS.md`·`.github/copilot-instructions.md`를 건드리면 그 기능을 끄거나 도입을 재고하세요. 이 파일들은 이 템플릿이 소유합니다.
  - **의존성과 갱신 주기.** 이들은 Node(BMAD는 Python·uv도) 런타임과 자체 갱신 명령을 가지며, 이 템플릿의 `Template version`이 추적하지 않습니다. 도구 갱신이 지침 파일을 다시 생성한다면 그 diff를 PR에서 검토하세요.
  - BMAD는 페르소나 기반 다중 에이전트와 전용 installer를 가진 무게 있는 방법론이라 이 템플릿의 기본 태도(작은 변경, 요청 범위 유지)와 결이 다릅니다. 큰 greenfield에서 팀이 합의한 경우에만 도입을 권합니다.
- **제품 내장형 (예: Kiro)** — 스펙 워크플로우가 IDE·CLI 제품에 내장되어 있고 산출물은 `.kiro/specs/`, 지침은 `.kiro/steering/`에 둡니다. 이 템플릿은 도구 비종속이므로 제품 전용 디렉터리를 포함하지 않습니다. Kiro는 루트 `AGENTS.md`를 항상 읽으므로 공통 지침은 그대로 동작합니다. `.kiro/steering/`에 별도 지침을 두면 `AGENTS.md`와 중복·충돌하는지 확인하세요. OMP가 `.kiro/` 디렉터리를 context로 읽는지는 확인되지 않았습니다.

### 공통

- 도구 버전과 로컬 설정에 따라 지침 로딩 결과를 직접 확인하세요. Markdown 링크만으로 모든 연결 문서가 자동 로드된다고 가정하지 마세요.
- [PROJECT_ANALYSIS.md](./PROJECT_ANALYSIS.md)는 전체 프로젝트 분석을 명시적으로 요청할 때 사용하는 절차입니다. 공통 지침에 전체 내용을 자동 import하지 않습니다.
- [DESIGN.md](./DESIGN.md)도 절차 문서입니다. `AGENTS.md`에는 적용 조건과 산출물 위치만 두고 단계 자체는 import하지 않습니다. 모든 작업에 설계 절차가 실려 있으면 모델이 작은 요청을 절차로 부풀립니다.

## 5. 적용 후 관리

- 일상적인 문서 관리 방법과 문서별 수정 권한은 [문서 운영 안내](./DOCS_GUIDE.md)를 기준으로 합니다.
- [DOCS_GUIDE.md](./DOCS_GUIDE.md)의 이름은 의도적으로 `README.md`가 아닙니다. 루트 README의 번역본을 `docs/README.ko.md`처럼 `docs/`에 두는 관행과 파일명이 충돌하기 때문입니다. `docs/README.md`로 되돌리지 마세요.
- 모든 저장소 내부 Markdown 링크는 해당 파일을 기준으로 한 상대 경로를 사용합니다. 파일을 옮기거나 이름을 바꾸면 참조하는 링크도 함께 수정하세요.
- 이 문서는 템플릿 적용 기록으로 남겨도 됩니다. 적용 후 필요 없어 삭제한다면 [프로젝트 README](../README.md)와 [문서 운영 안내](./DOCS_GUIDE.md)에 있는 이 문서 링크도 함께 제거하세요.
- Cursor Bugbot을 사용하지 않아 [.cursor/BUGBOT.md](../.cursor/BUGBOT.md)를, 또는 OMP를 사용하지 않아 [.omp/WATCHDOG.md](../.omp/WATCHDOG.md)를 제거한다면 이 안내와 [DOCS_GUIDE.md](./DOCS_GUIDE.md)의 해당 링크와 구조 설명도 정리하세요.
- 템플릿이 개정되면 §6에서 적용 저장소의 `Template version` 이후 항목을 읽고, 반영할 변경을 골라 적용한 뒤 이 문서와 [DOCS_GUIDE.md](./DOCS_GUIDE.md)의 `Template version`을 올립니다. 프로젝트가 의도적으로 바꾼 부분까지 템플릿으로 되돌리지 마세요.
- 변경 이력은 요약이라 항목이 빠질 수 있습니다. 반영할 때는 이력을 읽는 것과 함께, 템플릿 저장소의 두 판(적용 저장소의 현재 `Template version` tag와 목표 판 tag)을 `git diff v1.1 v1.2 -- <파일>`로 비교하고, 그 결과를 적용 저장소의 파일과 대조하세요. 적용 저장소 쪽은 `git diff --no-index <템플릿 파일> <적용 파일>`로 봅니다. 이력에 없는 차이가 나오면 템플릿 쪽 누락인지 적용 저장소가 의도적으로 바꾼 것인지 판단해 전자는 이력에 추가합니다.
- 적용 저장소에 `CHANGELOG.md`가 있으면 판을 올린 사실과 반영한 항목을 한 줄로 남깁니다.

## 6. 템플릿 변경 이력

적용 저장소가 어느 변경을 아직 반영하지 않았는지 확인하는 용도입니다. 각 항목은 "무엇이 바뀌었고, 적용 저장소에서 무엇을 확인해야 하는지"만 적습니다. 템플릿 저장소는 각 판을 git tag(`v1.1`, `v1.2`, …)로 남기므로, 이력이 요약한 내용의 원문은 `git diff v1.1 v1.2`로 봅니다. `v1.1` 이전 판은 tag가 없습니다.

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
