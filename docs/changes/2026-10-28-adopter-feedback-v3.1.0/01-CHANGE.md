# 변경: 적용 저장소 claude-code-pr-review의 v3.1.0 역제안

## Metadata

- **Change ID:** `2026-10-28-adopter-feedback-v3.1.0`
- **Status:** Accepted
- **Originator:** 적용 저장소 `jaff2836/claude-code-pr-review`의 유지자
- **Source:**
  - 2026-10-28 claude-code-pr-review 작업 세션에서 유지자가 "템플릿에 반영할 만한 내용 전체를 담은 문서를 만들라"고 요청했습니다. 근거는 그 저장소 `origin/main` `da34a08`과 이 저장소 `v3.1.0`(`3c5b13f`), `main` `9326c1e`의 비교입니다. 같은 내용이 루트 `Feedback.md`(미추적)로도 전달됐습니다.
  - 2026-10-28 이 저장소 세션에서 사용자가 `/design`으로 "프로젝트 전체를 분석·평가하고 `Feedback.md`의 내용을 검증해 공용 템플릿용 수정을 디자인하라"고 요청했습니다.
  - 적용 저장소 쪽 비교·검증은 §2.6.1, 이 저장소의 재검증은 §2.6.2에 있습니다.
- **Parent:** [제품 기준](../../00-PROJECT.md)과 v3.1.0 payload(`locales/ko/`, `locales/en/`, `template/common/`). 닿는 곳은 REVIEW_ROUND §1·§2.1·§3·§4·§6, REVIEW §5·§8, BUGBOT 「Do Not Report」 다음 문단, DOCS_GUIDE 「Metadata Convention」·「Template Adoption Checklist」, TEMPLATE_GUIDE §2·§5, Codex 명시 호출 정책 판정입니다. 공개는 D-007 절차를 따릅니다.
- **Decision:** PROJECT §8의 D-020
- **Approval:** Chae Sangwon, 2026-10-28 대화 — 이 문서의 미추적 Draft(§1.5 Q2~Q4)에 대한 선택 응답 "1. A. 2. A. 3. 넣자. 4. 좋아."입니다. R-005·R-010은 A, R-012는 포함, R-008은 §2.3.4 형식입니다. Q3의 남은 한계는 응답에 언급이 없어 권고안대로 이번 범위에서 뺐습니다. 같은 응답의 "문서 불일치도 고치자"는 TODO의 T-065 Backlog 행 정리입니다
- **Execution:** [전역 TODO](../../02-TODO.md)의 T-067(검사기), T-068(문구), T-066(`v3.2.0` release)

## 1. Intent

§1.1~§1.4는 적용 저장소 쪽 초안의 원문입니다. 이 저장소에서 확인한 정정·보완은 원문을 고치지 않고 §2.6.2에 적었습니다.

### 1.1 문제

claude-code-pr-review는 PR #37(merge `43acc77`, 2026-10-22)에서 한국어 v3.1.0을 기존 문서에 병합했습니다. 그 뒤 적용 저장소에서 찾은 공용 결함과 개선이 템플릿으로 돌아오지 않았습니다.

- **문서 검사기 결함 13건(확인됨).**
  - 적용 PR #37의 리뷰 라운드 1~6에서 `check-docs.py`의 Markdown 판정 결함 13건(그 PR의 finding F-037-2~14)을 고쳤습니다.
  - 이 저장소의 v3.1.0과 `main` `9326c1e`의 `template/common/scripts/check-docs.py`에는 어느 수정도 없습니다.
  - 적용 저장소가 더한 회귀 테스트 13개를 이 저장소 v3.1.0 검사기에 돌리면 13개 모두 assertion에서 실패합니다(§2.6).
  - 대부분은 깨진 상대 링크를 놓치거나, 코드 예시 안의 링크를 검사해 거짓 실패를 냅니다.
  - 하나는 Codex 명시 호출 정책 `false#note`를 boolean `false`로 받아들여, 지켜지지 않는 정책을 통과시킵니다. YAML에서 `false#note`는 문자열입니다.
- **리뷰 정책·라운드 문구(확인됨, 일부는 추론).**
  - 적용 저장소가 여러 PR의 리뷰 라운드를 돌리며 정한 운영 규칙 가운데 프로젝트와 무관한 것이 있습니다. 리뷰어 표를 언제 고치는지, 리뷰어가 결과를 언제 확정하는지, 빈 commit 재리뷰의 위임 경계, base가 다른 merge로 앞서 나간 경우가 그렇습니다.
  - 정본 정책과 사본이 어긋난 곳도 있습니다. `.cursor/BUGBOT.md`의 Do Not Report에는 "기록된 결정을 되돌리라는 요구"가 있지만 `docs/REVIEW.md` §8에는 없습니다.
- **적용 안내(확인됨).**
  - 적용 저장소는 기존 `PLAN.md`·`DESIGN.md`·`TODO.md`를 유지하고 번호형 경로를 그 파일에 연결했습니다.
  - 이때 이름을 일괄 치환해서 TEMPLATE_GUIDE의 템플릿 이력과 조건부 삭제 문장의 뜻이 틀어졌습니다.
  - 현재 안내의 "이전 파일명을 일괄 치환하지 않습니다"는 번호 체계로 **이관할 때**만 다룹니다.

### 1.2 기대 결과

- 공식 검사기가 §2.1 R-001의 13개 입력에서 적용 저장소 검사기와 같은 판정을 내고, 회귀 테스트가 그것을 고정합니다.
- 리뷰 정책·라운드·적용 안내에 아래 R-002~R-011 가운데 채택한 문구가 `ko`·`en` 양쪽에 들어갑니다.
- 채택하지 않은 항목은 이유와 함께 이 문서 §3에 남습니다.

### 1.3 범위와 비범위

- **포함:** §2.1의 R-001~R-011. 프로젝트 이름, 경로, 사례를 뺀 일반 규칙만 제안합니다.
- **비범위(프로젝트 고유):** 적용 저장소의 Overview·명령·불변조건, `REVIEW.md` D1~D15와 잔여 간극, 리뷰어 행과 Codex·Copilot 제거 기록, Bugbot·Watchdog 목록, CI 연결 절, 경로 적응, 보관 디렉터리 `ai-agent-docs-template/` 제외 래퍼와 그 테스트, Policy version.
- **비범위(반대 방향):** 이 저장소 `main`의 T-065(위임 입력 규칙)를 적용 저장소에 가져오는 일은 적용 저장소의 작업입니다.
- **비범위(이미 같음):** AGENTS의 보고 형식·완료 근거·red-green 규칙, REVIEW_ROUND의 §1·§3~§10 절차, DOCS_GUIDE 결합 서술 규칙은 v3.1.0과 문장 단위로 같아 제안할 것이 없습니다(확인됨).

### 1.4 제약

- 검사기는 표준 라이브러리만 씁니다. 수정은 판정을 CommonMark 쪽으로 좁히는 방향이라, 기존 적용 저장소에서 새 실패가 생길 수 있습니다. 숨어 있던 깨진 링크가 드러나는 경우입니다(추론). release note에 적어야 합니다.
- `ko`·`en` locale parity를 유지합니다. 문서 문구 제안(R-002~R-011)은 한국어 초안만 있으므로 영어 문구를 함께 만들어야 합니다.
- 적용 저장소 사례는 근거로만 쓰고 템플릿 본문에 프로젝트 이름을 넣지 않습니다.

### 1.5 미해결 질문

원문의 Q1~Q3을 검증 결과로 갱신하고 Q4를 더했습니다. 모두 해소했습니다.

- **Q1 (해소, 확인됨):** `v3.1.1` patch는 현재 release 계약으로는 낼 수 없습니다.
  - release source는 동기화된 `main`의 조상이어야 합니다(root TEMPLATE_GUIDE §5). `main`에는 지침 추가인 T-065가 이미 있어, `main`에서 자르는 release는 이 저장소의 관례(지침 추가는 minor, 예: `v2.5.0`·`v3.1.0`)상 minor입니다.
  - 그래서 2026-10-14 사용자 결정("그 전에 다른 payload 변경이 생기면 함께 묶음", T-066)대로 T-066에 묶어 `v3.2.0`으로 냅니다. 시작 시점은 사용자가 정합니다.
- **Q2 (해소):** R-005와 R-010 모두 A입니다(§2.3.2, §2.3.5). R-004의 별도 열은 만들지 않고 열 설명에 넣습니다(§2.3.2).
- **Q3 (해소):** R-012를 이번에 넣습니다. setext `===` heading을 포함한 Markdown 쪽 남은 한계(§2.3.1)는 이번 범위에서 빼고 PROJECT §12에 보류로 둡니다.
- **Q4 (해소):** R-008은 §2.3.4의 줄인 필드와 위치로 넣습니다.

## 2. Spec

### 2.1 요구사항과 시나리오

| 요구사항 ID | 요구사항 | 상황·입력 | 관찰 가능한 결과 | 검증 방법 | 판정 |
|---|---|---|---|---|---|
| R-001 | 검사기 판정 13건 수정 | §2.3.1 표의 입력 13개 | 깨진 링크는 보고하고 코드 예시 안 링크는 무시하며, `false#note`는 정책 위반으로 봅니다 | 부록 B의 회귀 테스트가 수정 전에는 assertion에서 실패하고 수정 뒤 통과 | 채택(원안) |
| R-002 | 리뷰어 표를 고치는 시점 | 운영 중 리뷰어 구성이 바뀜 | 라운드 밖에서 표를 먼저 고치고, 라운드 중에는 고치지 않음 | REVIEW_ROUND §2.1 문구 | 채택 |
| R-003 | `push 자동` 트리거 예시 보강 | GitHub App 리뷰어 | 트리거 예시에 webhook 이벤트가 있음 | 같은 절 문구 | 채택(효과 작음) |
| R-004 | 리뷰어의 결과 확정 신호 | 진행 중 표시를 같은 코멘트에서 결과로 바꾸는 리뷰어 | 완료로 판별된 뒤에만 결과로 읽음 | 같은 절 `게시 위치` 열 설명 | 수정 채택 |
| R-005 | 빈 commit 재리뷰의 위임 경계 | 코드 변경 없이 같은 tree를 다시 리뷰받아야 함 | 사용자 요청이 있을 때만 하고, 새 head이므로 새 라운드로 셈 | REVIEW_ROUND §1·§3 문구 | 채택(A) |
| R-006 | Do Not Report 정본과 사본 일치 | 확정된 결정을 되돌리라는 finding | REVIEW §8과 BUGBOT이 같은 항목을 가짐 | 두 파일 대조 | 채택(검사기 대조 확장은 기각) |
| R-007 | 반복 결함 유형 3개를 Required Checks에 | 결정 변경, 선언한 계약, 저장소 밖 사실 주장 | REVIEW §5 Tests and Documentation에 해당 확인 항목이 있음 | 문구 | 수정 채택 |
| R-008 | 적용 기록 형식 | 기존 저장소에 적용·업그레이드 | DOCS_GUIDE에 업그레이드 때 옮기는 「템플릿 적용 기록」 절과 필드가 있음 | 문구와 체크리스트 | 수정 채택 |
| R-009 | 기존 이름 유지 시 일괄 치환 금지 | 번호형 경로를 기존 `PLAN.md` 등에 연결 | TEMPLATE_GUIDE §6 이력과 템플릿 설명문은 바꾸지 않음 | 문구 | 수정 채택 |
| R-010 | base branch가 다른 merge로 앞서 나간 경우 | 승인한 PR 둘을 차례로 merge | tip만 바뀐 경우가 base 변경인지와 merge 직전 확인 방법이 정해져 있음 | REVIEW_ROUND §4·§6 문구 | 채택(A) |
| R-011 | 부분 결과의 예시 보강 | 리뷰어가 자기 검토 단계를 마치지 못했다고 보고 | 그 결과를 `부분 결과`로 기록 | REVIEW_ROUND §4 문구 | 채택 |
| R-012 | Codex 정책 판정의 남은 YAML 차이 | `allow_implicit_invocation:false`, `fAlSe`, `policy:#x` | 세 입력 모두 정책 위반으로 봄. `False`·`FALSE`는 계속 허용 | 회귀 테스트 red-green | 채택 |

R-001~R-011은 원안의 ID를 유지합니다. R-012는 이 저장소 검증(§2.6.2)에서 추가했습니다. `수정 채택`의 차이는 §2.3의 각 항목에 적었습니다.

### 2.2 대안과 선택 이유

- **변경하지 않음:** 모든 적용 저장소가 같은 검사기 결함을 따로 겪고 따로 고치게 됩니다. 적용 저장소마다 검사기가 갈라지면 다음 템플릿 갱신 때 병합 비용이 커집니다. 기각합니다.
- **검사기만 반영:** 가장 작고 위험이 낮습니다. 하지만 Q1에 따라 검사기만 따로 낼 release가 없고, 문구를 다음 release로 미루면 적용 저장소가 병합을 두 번 합니다. 기각합니다.
- **`v3.1.1` patch로 검사기만 먼저 공개:** 기각합니다(확인됨). release source는 동기화된 `main`의 조상이어야 하고 `main`에는 T-065가 있습니다. T-065를 빼려면 되돌리는 commit이 필요합니다.
- **검사기를 CommonMark parser로 교체:** 표준 라이브러리 제약(§1.4)을 깨고 새 dependency 동의가 필요합니다. 기각합니다.
- **기준 parser와의 차분 검사를 회귀 테스트로 추가:** 이번 검증에는 유효했습니다(§2.6.2). CI에 parser를 들이는 것은 dependency 추가라 이번에는 기각합니다. 남은 한계를 다루는 후속 작업에서 다시 판단합니다.
- **적용 저장소 문구를 그대로 복사:** 프로젝트 이름과 사례가 섞여 있어 기각합니다. §2.3은 일반화한 문구만 제안합니다.

### 2.3 설계와 계약

문구는 "현재 문장 → 새 문장"으로 적습니다. 현재 문장은 `9326c1e`의 payload에서 옮겼습니다. root 사본(`docs/REVIEW.md`, `docs/REVIEW_ROUND.md`, `.cursor/BUGBOT.md`)은 ko 문장을 그대로 받습니다(D-019).

#### 2.3.1 R-001 검사기 13건과 R-012

수정 위치는 `template/common/scripts/check-docs.py`입니다. 루트 `scripts/check-docs.py`는 이 파일을 불러 쓰므로 함께 바뀝니다. 회귀 테스트는 `template/common/tests/test_check_docs.py`에 넣습니다. 전체 diff는 부록 A(검사기)와 부록 B(테스트)입니다.

| #   | 결함                                                                  | 수정                                                        | 회귀 테스트                                             | 놓치는 방향                              |
| --- | --------------------------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------- | ---------------------------------------- |
| 1   | escaped backtick(`` \` ``)이 code span을 엽니다                       | escaped backtick은 자기 자신만 소비                         | `test_escaped_backtick_does_not_open_code_span`         | 뒤 링크를 가려 깨진 링크를 놓침          |
| 2   | code span이 빈 줄을 넘어 닫힙니다                                     | span은 문단 안에서만 닫힘                                   | `test_code_span_does_not_cross_blank_line`              | 문단 사이 링크를 가림                    |
| 3   | 들여쓴 코드 예시 안의 목록형 줄을 목록으로 봅니다                     | 들여쓰기 코드 판정을 목록 marker보다 먼저                   | `test_indented_list_examples_are_code_blocks`           | 예시 링크를 검사해 거짓 실패             |
| 4   | 목록 안 fence가 그 목록 항목이 끝나도 닫히지 않습니다                 | fence·HTML block은 담은 목록 항목·인용문이 끝나면 함께 닫힘 | `test_list_fence_ends_with_its_list_item`               | 뒤 문서 전체를 코드로 봄                 |
| 5   | Codex 정책 `false#note`를 `false`로 받습니다                          | YAML 주석은 앞에 공백이 있을 때만 인정                      | `test_codex_policy_must_be_boolean_false` 확장          | 지켜지지 않는 정책을 통과시킴            |
| 6   | HTML block이 담은 인용문·목록 항목과 함께 닫히지 않습니다             | 4번과 같은 container 종료 판정                              | `test_html_block_ends_with_its_container`               | 뒤 링크를 가림                           |
| 7   | info string에 backtick이 든 줄을 fence로 봅니다                       | backtick fence의 info string에는 backtick이 없어야 함       | `test_one_line_backtick_span_is_not_a_fence`            | 한 줄 code span 뒤 문서 전체를 코드로 봄 |
| 8   | 코드·HTML block 줄의 backtick이 주석 판정의 code span 짝에 들어갑니다 | 그 줄은 짝 찾기에서 건너뜀(`skip_line`)                     | `test_code_block_backticks_do_not_hide_comment_openers` | HTML 주석 시작을 잘못 가림               |
| 9   | 인용문 깊이가 바뀌어도 목록 상태가 남습니다                           | 깊이가 바뀌면 목록 상태를 비움                              | `test_quoted_list_ends_with_its_blockquote`             | 목록 기준 들여쓰기를 잘못 계산           |
| 10  | `- - -` 같은 구분선을 목록 항목으로 봅니다                            | 구분선이 목록보다 우선                                      | `test_thematic_breaks_are_not_list_items`               | 뒤 줄의 코드·목록 판정이 틀어짐          |
| 11  | code span이 heading·구분선·목록 항목 줄을 넘어 닫힙니다               | span은 그 줄들에서 끝나는 문단을 넘지 않음                  | `test_code_span_does_not_cross_block_starts`            | 링크를 가림                              |
| 12  | code span이 더 깊은 인용문이나 인용문 안 빈 줄을 넘습니다             | span은 같은 인용문 문단 안에서만 닫힘                       | `test_code_span_stays_in_its_blockquote_paragraph`      | 링크를 가림                              |
| 13  | heading·구분선 바로 뒤 들여쓴 줄을 코드로 보지 않습니다               | 빈 줄처럼 다음 줄의 코드 시작을 허용                        | `test_indented_code_may_follow_heading_or_break`        | 예시 링크를 검사해 거짓 실패             |

- 부록 A에는 타입 검사용 한 줄(`bullet_indent is not None`)도 들어 있습니다. 동작은 바뀌지 않습니다.
- 적용 저장소에서 각 수정이 생긴 라운드: 1·2번 라운드 1, 3번 라운드 2, 4·5번 라운드 3, 6~8번 라운드 4, 9~11번 라운드 5, 12·13번 라운드 6(적용 저장소 `docs/DOCS_GUIDE.md` 「프로젝트 적용 기록」의 「검사기 적응」).
- "놓치는 방향" 열은 테스트 입력과 실패 메시지에서 읽은 것입니다(추론). 예를 들어 1번 테스트는 v3.1.0에서 깨진 링크 `MISSING.md`를 보고하지 않습니다.
- 수정 전 검사기의 실패 메시지로 다시 분류하면 1·2·4·6·7·11·12번은 깨진 링크를 놓치고, 1·2·3·8·9·10·13번은 예시 링크를 검사합니다(확인됨, 1·2번은 둘 다).

**R-012(채택).** 5번과 같은 종류인 정책 판정 차이가 3건 남아 있습니다. 모두 수정 뒤 검사기가 `false`로 받아들이지만 YAML에서는 boolean `false`가 아닙니다(PyYAML 6.0.2로 확인).

| 입력 | YAML 해석 | 수정 |
|---|---|---|
| `allow_implicit_invocation:false`(`policy:` 아래 줄) | 콜론 뒤 공백이 없어 key가 아님. `policy` 값이 문자열 | key 뒤에 공백이나 줄 끝을 요구 |
| `allow_implicit_invocation: fAlSe` | 문자열 `fAlSe` | YAML 1.2 core 표기(`true`·`True`·`TRUE`·`false`·`False`·`FALSE`)만 인정, `re.IGNORECASE` 제거 |
| `policy:#x` | `policy` mapping이 아님. 다음 줄과 함께 YAML 오류 | `policy:` 줄의 주석도 앞에 공백을 요구 |

- 대상은 `read_implicit_invocation_policy`의 정규식 세 개입니다. scratch 사본에서 적용해 보니 위 세 입력은 `None`(위반)이 되고, 기존 허용 입력 다섯 개(`false`, `False`, `FALSE`, `false # c`, `policy: # c`)는 그대로 `false`였습니다. 그 사본에서 root·template 테스트와 `check-docs.py`가 통과했습니다.
- 회귀 테스트는 `test_codex_policy_must_be_boolean_false`의 거부 사례에 세 입력을, 허용 사례에 `False`·`FALSE`·`policy: # note`를 더합니다. 정규식 세 개를 하나씩 되돌리면 각각 대응하는 거부 사례에서 실패해야 합니다.
- maintainer 검사 `scripts/check_locales.py`의 `_read_implicit_invocation_policy`는 같은 판정의 사본입니다. 이 사본이 더 느슨하면 `check-locales.py --require-stable`은 통과하는데 artifact 검사기는 거부합니다(MR !1 리뷰 P3). 그래서 사본도 같은 규칙으로 맞춥니다. 값이 표기 규칙에 맞지 않는 key도 중복 판정에 셉니다. 회귀 테스트는 `test_common_implicit_invocation_policy_is_narrowly_validated`에 네 입력을 더합니다: `false#note`, `policy:#note`, `allow_implicit_invocation:false`, 따옴표 값 뒤의 `false`.

**남은 한계(이번 범위 밖, 확인됨).** 수정 뒤에도 CommonMark와 다른 판정입니다. 마지막 항목을 빼면 수정 전 검사기도 같아서 R-001이 만든 결함은 아닙니다. PROJECT §12에 보류로 둡니다.

- 깨진 링크를 놓치는 쪽
  - 인용문·목록 항목 안에서 닫히지 않은 `<!--`가 그 container가 끝나도 이어집니다. 4·6번의 HTML 주석판입니다.
  - 인용문·목록 항목 안의 reference definition(`> [r]: ./x.md`)을 검사하지 않습니다.
  - setext 밑줄 `===`가 code span을 끊지 않습니다(원문 Q3).
- 예시 링크를 검사하는 쪽
  - `<!-- c --> [l](./x.md)`처럼 주석으로 시작하는 줄의 나머지를 본문으로 봅니다. CommonMark에서는 줄 전체가 HTML block입니다.
  - fence 닫는 줄 바로 뒤의 들여쓴 줄을 코드로 보지 않습니다. 13번의 fence판입니다.
  - 문단을 끊지 못하는 `2.` 목록 marker도 code span을 끊습니다. R-001이 새로 만든 차이이며 더 엄격한 쪽입니다.

#### 2.3.2 R-002~R-005 REVIEW_ROUND §1·§2.1·§3

**R-002 — §2.1 도입문.** 두 locale 모두 정족수 문장 바로 뒤에 한 문장을 넣습니다.

- ko: "리뷰어를 누락하면 §4의 정족수 판정이 틀립니다. 라운드 실행 중에는 …" → "리뷰어를 누락하면 §4의 정족수 판정이 틀립니다. **리뷰어 구성이 바뀌면 라운드 밖에서 이 표를 먼저 갱신합니다.** 라운드 실행 중에는 …"
- en: "Omitting a reviewer makes the §4 quorum calculation incorrect. Do not edit this document during a round." → "Omitting a reviewer makes the §4 quorum calculation incorrect. **When the set of reviewers changes, update this table outside a round first.** Do not edit this document during a round."

**R-003 — `재리뷰 요청 방법`의 `push 자동`.** TEMPLATE_GUIDE 「리뷰어 조사 힌트」의 자체 호스팅 GitHub App 행이 이미 webhook 트리거를 적으라고 하므로 효과는 작습니다. 표 설명과 힌트를 맞추는 한 단어 수정입니다.

- ko: "트리거 조건(ruleset, workflow 이벤트 등)" → "트리거 조건(webhook 이벤트, ruleset, workflow 이벤트 등)"
- en: "such as a ruleset or workflow event" → "such as a webhook event, ruleset, or workflow event"

**R-004 — `게시 위치` 열 설명.** 별도 열(`완료 신호`)은 만들지 않습니다. 표의 열이 바뀌면 이미 표를 채운 적용 저장소가 모두 병합해야 하고, 대상 리뷰어는 진행 중 표시를 쓰는 리뷰어뿐입니다. 열 설명 끝에 두 문장을 더합니다.

- ko: "… 덮어쓰는 리뷰어는 §7의 원장 규칙이 달라집니다" → "… 덮어쓰는 리뷰어는 §7의 원장 규칙이 달라집니다. 진행 중 표시를 먼저 게시하고 같은 게시물을 결과로 바꾸는 리뷰어는 그 표시와 완료를 판별하는 방법을 적습니다. 완료로 판별되기 전의 게시물은 결과로 읽지 않습니다"
- en: "… Reviewers that overwrite have different ledger rules under §7" → "… Reviewers that overwrite have different ledger rules under §7. If a reviewer first posts an in-progress marker and later turns the same post into its result, record that marker and how to tell that the result is complete. Do not read a post as a result until it is complete"

**R-005 — 빈 commit 재리뷰(A 채택).** 지금 문서는 §1에서 "라운드별 commit"과 non-force push를 위임하고, §3에서 "같은 head에 대한 두 번째 리뷰는 라운드가 아닙니다"라고만 합니다. 코드 변경 없는 빈 commit이 위임 범위 안인지 정하지 않아 해석이 갈립니다.

| 선택지 | 내용 | 장단점 |
|---|---|---|
| A(권고) | 위임하지 않음. 사용자가 요청할 때만 하고 새 라운드로 셈 | 빈 commit으로 §3 규칙을 우회해 원하는 결과가 나올 때까지 리뷰를 다시 돌리는 일을 막습니다. 리뷰어 결과가 빠진 경우는 이미 §4 `결과 없음`과 §6 사용자 확인으로 넘어갑니다 |
| B | `push 자동`만 있는 상시 리뷰어가 현재 head에 결과를 남기지 않았을 때 한 번만 위임 | 사용자 개입이 줄지만 "결과가 오지 않음"의 판정을 실행 주체가 하게 됩니다 |
| C | 채택하지 않음 | 해석 차이가 그대로 남습니다 |

A에 따라 다음을 넣습니다.

- §1 「위임되지 않는 것」, "재리뷰 요청 이외의 PR 댓글 …" 항목 뒤
  - ko: "- 코드 변경 없이 재리뷰만 받으려는 빈 commit과 그 push. 사용자가 요청한 경우에만 하며, head가 바뀌므로 새 라운드로 셉니다"
  - en: "- An empty commit, and its push, made only to obtain another review without a code change. Make one only when the user asks, and count it as a new round because the head changes"
- §3 「push가 없었던 라운드」, "같은 head에 대한 두 번째 리뷰는 라운드가 아닙니다." 뒤
  - ko: "빈 commit으로 head만 바꿔 재리뷰를 받는 것도 위임되지 않습니다(§1)."
  - en: "Changing only the head with an empty commit to get another review is not delegated either (§1)."

`review-round` 스킬은 REVIEW_ROUND를 따르라고만 하므로 바꾸지 않습니다.

#### 2.3.3 R-006·R-007 REVIEW·BUGBOT

**R-006 — REVIEW §8 Do Not Report.** 마지막 항목 뒤에 더합니다. 승인된 deferral은 넣지 않습니다. REVIEW §9에 따라 deferral과 일치하는 finding은 `blocking=false`로 **보고하는** 대상이기 때문입니다.

- ko: "- `[00-PROJECT.md](./00-PROJECT.md)` §8 Decisions에 확정된 결정을 새 근거 없이 되돌리라는 요구. 결정의 전제가 깨졌다는 증거는 보고합니다"
- en: "- Requests to reverse a decision accepted in `[00-PROJECT.md](./00-PROJECT.md)` §8 Decisions without new evidence. Report evidence that the decision's premise no longer holds"
- BUGBOT은 이미 같은 뜻의 항목이 있어 바꾸지 않습니다. 두 목록은 표현이 달라(§ 참조, 백틱) 검사기가 문자열로 대조할 수 없으므로 대조 확장은 기각합니다. R-007의 첫 항목이 같은 종류의 어긋남을 리뷰에서 잡게 합니다.

**R-007 — REVIEW §5 Tests and Documentation.** 새 항목 하나를 더하고 기존 두 항목을 넓힙니다. 원안의 세 항목 중 둘은 기존 항목과 겹쳐서 합쳤습니다.

- 새 항목, "`[00-PROJECT.md](./00-PROJECT.md)`의 확정된 결정과 코드의 일치" 뒤
  - ko: "- 결정이나 정책을 바꾼 변경이 그것을 서술하는 다른 문서와 사본도 함께 고쳤는지 — 남은 곳이 폐기된 지침을 계속 지시하지 않는지"
  - en: "- Whether a change to a decision or policy also updates the other documents and copies that describe it, so that no remaining copy keeps directing readers to superseded guidance"
- 기존 항목 넓힘(선언한 계약)
  - ko: "- 문서가 불변조건이나 안전장치로 선언한 동작이 코드에 실제로 강제되어 있는지" → "- 문서가 불변조건이나 안전장치로 선언하거나 기록·검증한다고 적은 동작이 코드·schema·검사 절차로 실제로 강제되거나 구현되어 있는지"
  - en: "- Whether behavior declared by the documentation as an invariant or safeguard is actually enforced in code" → "- Whether behavior that the documentation declares as an invariant or safeguard, or says is recorded or verified, is actually enforced or implemented in code, a schema, or a check procedure"
- 기존 항목 넓힘(저장소 밖 사실)
  - ko: "… 마지막 변경 뒤에 실행하거나 조회한 근거를 갖는지" → "… 마지막 변경 뒤에 실행하거나 조회한 근거를 갖는지. release 게시, 외부 검증, CI 결과처럼 checkout만으로 확인할 수 없는 주장은 다시 조회할 수 있는 식별자(tag, digest, build·run ID, 실행 명령)를 함께 적었는지"
  - en: "… meaning evidence run or retrieved after the last change" → "… meaning evidence run or retrieved after the last change, and whether claims a checkout alone cannot confirm, such as a published release, external verification, or a CI result, carry an identifier that can be looked up again (tag, digest, build or run ID, or the command run)"
- BUGBOT 「Do Not Report」 다음 문단에 이 완료 근거 항목의 사본이 있으므로 함께 넓힙니다.
  - ko: "완료·통과·수정 주장에는 마지막 변경 뒤에 실행하거나 조회한 근거가 있어야 합니다." 뒤에 "checkout만으로 확인할 수 없는 주장에는 다시 조회할 수 있는 식별자(tag, digest, build·run ID, 실행 명령)가 있어야 합니다."
  - en: "Completion, passing, or fix claims need evidence run or retrieved after the last change." 뒤에 "Claims a checkout alone cannot confirm need an identifier that can be looked up again (tag, digest, build or run ID, or the command run)."

#### 2.3.4 R-008·R-009 DOCS_GUIDE·TEMPLATE_GUIDE

**R-008 — DOCS_GUIDE 「템플릿 적용 기록」.** `docs/DOCS_GUIDE.md`의 adoption policy는 `copy`(템플릿 소유)입니다. 그래서 기록 절을 두되, 업그레이드에서 artifact 판으로 다시 시작할 때 그 절을 옮긴다고 적습니다. 원안의 필드 중 셋은 뺐습니다.

- 적용 기준(판, 원본 SHA): Metadata의 `Template version`·`Template revision`과 같습니다.
- 슬롯 부여: REVIEW_ROUND §2.1 표가 정본입니다.
- 정본: PROJECT의 설계 인덱스가 정본입니다.

새 절은 「Metadata Convention」과 「Template Adoption Checklist」 사이에 둡니다.

- ko

  ```markdown
  ## 템플릿 적용 기록

  처음 적용할 때와 새 판으로 업그레이드할 때 채웁니다. 이 문서는 템플릿 소유(`copy`)이므로 업그레이드에서 artifact 판으로 다시 시작하면 이 절을 그대로 옮깁니다. 위 Metadata의 source·version·revision은 반복하지 않습니다. 해당 없는 항목은 `없음`으로 둡니다.

  - **이전 기준:** 업그레이드라면 이전 판과 원본 revision. `adopt --base-version`에는 이 판을 씁니다
  - **적용 시작 revision:** 병합을 시작한 이 프로젝트의 commit
  - **경로 적응:** 기존 이름을 유지했거나 다른 경로로 옮긴 템플릿 문서와 그 대응
  - **보존·제외:** 템플릿 판 대신 프로젝트 판을 유지했거나 적용하지 않은 경로와 이유
  - **템플릿 소유 파일의 수정:** `copy` 정책 파일(검사 스크립트·테스트 포함)을 고쳤다면 그 내용과 이유. 다음 업그레이드에서 다시 적용할 대상입니다
  - **미검증:** 확인하지 못한 도구 로딩·명령·CI 항목
  ```

- en

  ```markdown
  ## Template Adoption Record

  Fill this in at the first adoption and at each upgrade to a new release. This document is template-owned (`copy`), so when an upgrade starts again from the artifact version, carry this section over unchanged. Do not repeat the source, version, and revision from Metadata above. Write `None` for items that do not apply.

  - **Previous baseline:** For an upgrade, the previous version and source revision. Pass this version to `adopt --base-version`
  - **Starting revision:** The commit of this project where the merge started
  - **Path adaptations:** Template documents kept under existing names or moved elsewhere, and how they map
  - **Kept or excluded:** Paths where the project version was kept instead of the template version, or that were not applied, and why
  - **Changes to template-owned files:** If any `copy`-policy file (including the check script and its tests) was changed, what changed and why. These are reapplied at the next upgrade
  - **Unverified:** Tool loading, commands, or CI items that could not be confirmed
  ```

이 절을 가리키도록 기존 문장 네 곳을 고칩니다.

| 위치 | ko | en |
|---|---|---|
| DOCS_GUIDE 「Metadata Convention」 넷째 항목 | "일부만 반영했다면 이 문서에 적용·제외 내역을 남깁니다." → "일부만 반영했다면 적용·제외 내역을 아래 「템플릿 적용 기록」에 남깁니다." | "record inclusions and exclusions in this document." → "record inclusions and exclusions in the Template Adoption Record below." |
| DOCS_GUIDE 「Template Adoption Checklist」 | "- [ ] Template source·version·revision과 일부 반영 내역을 확인했다. …" → "- [ ] Template source·version·revision을 확인하고 「템플릿 적용 기록」을 채웠다. …" | "- [ ] Verified Template source, version, revision, and partial adoption details. …" → "- [ ] Verified Template source, version, and revision, and filled in the Template Adoption Record. …" |
| TEMPLATE_GUIDE §2 "기존 프로젝트에는 `install`을 바로 실행하지 말고" 문단 | "적용·제외한 파일을 Template revision 기록 옆에 남깁니다." → "적용·제외한 파일을 `[DOCS_GUIDE.md](./DOCS_GUIDE.md)`의 「템플릿 적용 기록」에 남깁니다." | "record included and excluded files next to the Template revision." → "record included and excluded files in the Template Adoption Record in `[DOCS_GUIDE.md](./DOCS_GUIDE.md)`." |
| TEMPLATE_GUIDE §5 「템플릿 개정 반영하기」 셋째 항목 | "… 이유를 `[DOCS_GUIDE.md](./DOCS_GUIDE.md)`에 함께 남겨 …" → "… 이유를 `[DOCS_GUIDE.md](./DOCS_GUIDE.md)`의 「템플릿 적용 기록」에 남겨 …" | "… the reason in `[DOCS_GUIDE.md](./DOCS_GUIDE.md)`, so …" → "… the reason in the Template Adoption Record in `[DOCS_GUIDE.md](./DOCS_GUIDE.md)`, so …" |

**R-009 — TEMPLATE_GUIDE 「번호 체계로 이관하기」 둘째 항목.** 별도 절을 만들지 않고 기존 항목을 두 방향으로 넓힙니다.

- ko: "- 이전 파일명을 일괄 치환하지 않습니다. 변경별 `03-PLAN.md`, 도구 생성 파일, 과거 이력의 `PLAN.md`는 역할이 다릅니다. 링크·import·스킬·검사 코드·고정 정책 경로를 조사해 실제 이관 대상만 바꿉니다." → "- 이전 파일명과 새 파일명은 어느 방향으로도 일괄 치환하지 않습니다. 번호 체계로 옮길 때도, 기존 `PLAN.md`·`DESIGN.md`·`TODO.md`를 유지하고 템플릿의 번호형 경로를 그 파일로 바꿀 때도 같습니다. 변경별 `03-PLAN.md`, 도구 생성 파일, 과거 이력의 `PLAN.md`는 역할이 다릅니다. 링크·import·스킬·검사 코드·고정 정책 경로를 조사해 실제 대상만 바꾸고, §6 변경 이력과 템플릿 자체를 설명하는 문장(위 표, `10-EXTENSION.md` 제거 같은 조건부 안내)은 고치지 않습니다. 기존 이름을 유지했다면 고친 템플릿 소유 파일을 `[DOCS_GUIDE.md](./DOCS_GUIDE.md)`의 「템플릿 적용 기록」에 남깁니다."
- en: "- Do not globally replace old filenames. … then change only the actual migration targets." → "- Do not globally replace old or new filenames in either direction. This applies both when migrating to the numbered system and when keeping existing `PLAN.md`, `DESIGN.md`, and `TODO.md` and changing the template's numbered paths to point at them. A change-specific `03-PLAN.md`, tool-generated files, and historical `PLAN.md` records have different roles. Search links, imports, skills, checker code, and fixed policy paths and change only the actual targets. Do not change the §6 revision history or sentences that describe the template itself, such as the table above or conditional guidance like removing `10-EXTENSION.md`. If existing names were kept, record the template-owned files you changed in the Template Adoption Record in `[DOCS_GUIDE.md](./DOCS_GUIDE.md)`."

#### 2.3.5 R-010·R-011 REVIEW_ROUND §4·§6

**R-010 — base branch의 tip만 앞서 나간 경우(A 채택).** §4 「base 변경」의 목록(retarget, base branch merge·rebase, stacked PR의 아래 PR 병합)에는 다른 PR이 base branch에 merge된 경우가 없습니다. §6 2단계의 "head·base가 승인 대상과 같은지"를 base tip으로 읽으면, 승인한 PR 둘을 차례로 merge할 때 두 번째 PR이 진행할 수 없습니다. PR diff는 merge base 기준이라 이 PR의 head가 그대로면 리뷰어가 본 diff도 같습니다.

| 선택지 | 내용 | 장단점 |
|---|---|---|
| A(권고) | tip만 바뀌면 base 변경이 아님. merge 직전에 새 tip의 병합 가능 여부와 필수 검사를 보고, 확인받은 tip과 다르면 다시 확인받음. 순서를 함께 확인받은 예상 tip은 확인된 것으로 봄 | 리뷰를 다시 돌리지 않고, 무엇을 무엇에 merge하는지는 사용자 확인 대상으로 남습니다. 새 tip과의 의미 충돌은 저장소의 필수 검사 설정에 맡기므로 남는 위험입니다 |
| B | tip이 바뀌어도 base 변경으로 보고 리뷰로 돌아감 | 지금 문장을 엄격히 읽은 것입니다. push가 없어 `push 자동` 리뷰어 결과가 오지 않고, merge가 잦은 저장소에서 진행이 막힙니다 |
| C | tip이 바뀌면 base branch를 대상 branch에 merge해 새 base에서 필수 검사를 다시 받음 | 의미 충돌을 가장 잘 막지만 head가 바뀌어 매번 새 라운드입니다. 플랫폼이 branch 최신 유지를 요구하는 저장소는 이미 이 경로이고 기존 §4 규칙으로 처리됩니다 |

A에 따라 다음을 넣습니다. `MUST_GATE_ON_EXACT_HEAD_AND_BASE`는 "확인받은 head와 base tip"으로 읽히므로 계약 토큰과 fixture는 바꾸지 않습니다.

- §4 「base 변경」 문단 끝
  - ko: "다른 PR이 base branch에 merge되어 base branch의 tip만 앞서 나가고 이 PR의 head와 merge base는 그대로라면, 리뷰어가 본 diff가 같으므로 base 변경이 아닙니다. 이 경우는 §6의 병합 직전 확인에서 다룹니다."
  - en: "If another PR merges into the base branch so that only the base branch tip advances while this PR's head and merge base stay the same, the diff reviewers examined is unchanged, so it is not a base change. §6's pre-merge check handles this case."
- §6 1단계
  - ko: "확인 요청에는 대상 head·base, …" → "확인 요청에는 대상 head·base(base branch와 그 시점의 tip), …"
  - en: "Include the target head and base, …" → "Include the target head and base (the base branch and its tip at that time), …"
- §6 2단계
  - ko: "head·base가 바뀌면 §3·§4에 따라 리뷰로 돌아갑니다." → "head나 merge base가 바뀌면 §3·§4에 따라 리뷰로 돌아갑니다. base branch의 tip만 앞서 나갔다면 리뷰로 돌아가지 않고, 새 tip에 충돌 없이 병합되는지와 필수 검사를 확인한 뒤 확인받은 tip과 다르면 새 tip을 알리고 다시 확인을 받습니다. 여러 PR의 merge 순서를 함께 확인받으면서 앞 PR merge 뒤의 예상 tip을 적었다면 그 tip은 확인받은 것으로 봅니다."
  - en: "If the head or base changed, return to review under §3 and §4." → "If the head or the merge base changed, return to review under §3 and §4. If only the base branch tip advanced, do not return to review: confirm that the PR still merges cleanly into the new tip and that required checks are satisfied, and if the tip differs from the one the user confirmed, report the new tip and ask for confirmation again. When the user confirmed the merge order of several PRs and the request listed the tip expected after the earlier merge, that tip counts as confirmed."

배경: 적용 저장소에서 2026-10-28에 승인한 PR 두 개를 차례로 merge했습니다. 두 번째 PR은 확인 요청에 base 변화를 미리 적어 승인받았습니다. A의 마지막 문장이 그 방식입니다.

**R-011 — §4 「검토 범위」.** 부분 검토 예시에 한 가지를 더합니다.

- ko: "diff 절단, 일부 파일만 검토, 파싱 실패 후 재구성(salvage) 같은" → "diff 절단, 일부 파일만 검토, 파싱 실패 후 재구성(salvage), 자기 검토 단계(후속 검증 단계 등)를 마치지 못함 같은"
- en: "such as a truncated diff, only some files reviewed, or reconstruction after a parsing failure (salvage)," → "such as a truncated diff, only some files reviewed, reconstruction after a parsing failure (salvage), or an unfinished stage of its own review (such as a follow-up verification stage),"

### 2.4 상위 설계에 미치는 영향

- R-001·R-012는 검사기 판정을 좁힙니다. 검사하는 파일·절, CLI와 출력 형식은 바뀌지 않습니다. `template/common`이 바뀌므로 release가 필요합니다.
- R-002~R-011은 문구 변경입니다. 기존 결정을 대체하지 않습니다. root 사본 셋은 D-019에 따라 ko 문장을 그대로 받고, root `scripts/check-docs.py`가 대조합니다.
- `review-round` 스킬의 계약 토큰 세 개와 fixture, `locales/manifest.json`의 adoption policy·section marker, release manifest schema와 installer는 바뀌지 않습니다.
- D-007 공개 절차를 유지합니다. T-066의 범위가 T-065에 이 변경을 더한 것으로 넓어집니다.
- R-005·R-010·R-012의 선택과 R-008 형식은 PROJECT §8의 D-020입니다. REVIEW §6 불변조건과 §9 deferral은 바뀌지 않습니다.

### 2.5 위험·호환성·rollback

- **검사기가 엄격해짐.** R-001 뒤에는 적용 저장소에서 숨어 있던 깨진 링크가 새로 보고될 수 있습니다. 이 저장소와 적용 저장소의 실제 문서 141개에서는 검사 대상 링크가 수정 전후 같았습니다(§2.6.2). 무작위 입력 차분에서 새로 생긴 차이는 대부분 더 엄격한 쪽이었습니다. release note에 "판정이 엄격해짐"을 적습니다.
- **정책 판정.** `false#note`(R-001)와 R-012의 세 입력은 새로 실패합니다. 의도한 변경입니다.
- **DOCS_GUIDE 업그레이드.** 새 절이 생겨 적용 저장소의 DOCS_GUIDE는 다음 `adopt`에서 `merge`(base 모드에서는 `diverged`)로 나옵니다. Metadata를 채운 저장소는 이미 그렇습니다. release note에 "적용 기록 절을 옮긴다"를 적습니다.
- **R-010 A의 남는 위험.** tip만 바뀐 경우 새 tip과의 의미 충돌은 저장소의 필수 검사 설정이 막지 않으면 남습니다. 템플릿은 새 base에서의 재실행을 강제하지 않습니다.
- **rollback.** 문구는 다음 release에서 되돌립니다. 적용 저장소는 이전 판 artifact를 다시 씁니다. 검사기는 `copy` 정책이므로 이전 판 검사기를 다시 복사합니다.

### 2.6 완료 조건과 미해결 사항

#### 2.6.1 적용 저장소 쪽 근거

적용 저장소 쪽 초안이 근거로 쓴 확인입니다. 모두 2026-10-28에 했습니다.

- **비교 범위:** 적용 저장소 `origin/main` `da34a08`의 템플릿 소유 파일과 이 저장소 `3c5b13f`의 `locales/ko/`·`template/common/`을 비교했습니다.
  - 적용 뒤(`43acc77..da34a08`)에 템플릿 소유 파일을 고친 commit은 5개이고, 모두 프로젝트 고유입니다.
  - 검사기와 테스트는 적용 PR 뒤로 바뀌지 않았습니다.
- **템플릿 쪽 상태:** 이 저장소의 마지막 tag는 `v3.1.0`(`3c5b13f`)입니다. 그 뒤 `main`에는 PR #85(T-064)와 PR #86(T-065)만 있습니다.
  - `git diff --quiet 3c5b13f 9326c1e -- template/common scripts tests`가 통과했습니다. 즉 검사기는 v3.1.0 그대로입니다.
- **red:** 적용 저장소 테스트 파일의 회귀 테스트 13개를 이 저장소 v3.1.0 검사기에 돌렸습니다.
  - 13개 모두 assertion에서 실패했습니다.
  - 예: 깨진 링크 `'MISSING.md' not found in ''`, 코드 예시 링크 `'EXAMPLE.md' unexpectedly found`, `[] is not true : false#note`.
  - 적용 저장소 검사기에서는 13개 모두 통과합니다.
- **적용 가능성:** `git archive 9326c1e`를 풀고 부록 A·B를 `patch -p1`로 적용한 뒤 실행했습니다. 모두 통과했습니다.
  - `python3 -m unittest discover -s tests`: 261 tests OK (skipped=3)
  - `python3 -m unittest discover -s template/common/tests`: 67 tests OK
  - `python3 scripts/check-docs.py`: All checks passed
- **하지 않은 것:**
  - 영어 문구 초안
  - 이 저장소 CI
  - setext `===` heading 등 남은 엣지 케이스 확인(Q3)

#### 2.6.2 이 저장소의 재검증

2026-10-28 이 저장소 세션에서 `9326c1e`의 `git archive` 사본으로 확인했습니다. 사본과 검증 스크립트는 세션 scratch에만 있고 저장소에는 넣지 않았습니다.

| 원문 주장 | 판정 | 근거 |
|---|---|---|
| 회귀 테스트 13개가 v3.1.0·`main` 검사기에서 모두 assertion 실패 | 확인됨 | 부록 B만 적용한 사본: `FAILED (failures=13)`, 13개 모두 `AssertionError`. `git diff --quiet 3c5b13f 9326c1e -- template/common scripts tests` 통과 |
| 부록 A·B 적용 뒤 전체 통과 | 확인됨 | Python 3.13.5와 CI 하한인 3.12.13 모두 root 261 OK(skip 3), template 67 OK, `check-docs.py` All checks passed, `check-locales.py --require-stable` 통과 |
| 부록 A가 적용 저장소 검사기와의 차이 전체 | 확인됨 | 부록 A를 적용한 파일이 `da34a08:scripts/check_docs.py`와 byte 단위로 같음 |
| 테스트의 기대 판정이 CommonMark와 같음 | 확인됨(추가) | markdown-it-py 4.2.0의 CommonMark preset과 대조: 수정 전 검사기는 12개 Markdown 테스트 입력 모두에서 다르고(놓친 링크 11개, 링크가 아닌데 검사한 링크 12개) 수정본은 차이 0. 대표 사례는 cmark-gfm 2025.10.22로 교차 확인 |
| `false#note`는 YAML 문자열 | 확인됨 | PyYAML 6.0.2: `'false#note'` |
| 기존 적용 저장소에서 새 실패가 생길 수 있음(추론) | 보완 | 이 저장소 `9326c1e`의 Markdown 98개와 적용 저장소 `da34a08`의 43개에서 검사 대상 링크 집합이 수정 전후 같고 CommonMark와도 같음. 13건은 두 저장소의 실제 문서에는 드러나지 않은 잠재 결함 |
| 적용 뒤 템플릿 소유 파일 commit 5개, 검사기·테스트 무변경 | 확인됨 | `43acc77..da34a08`: `7f694a8`, `9e873f1`, `b13c358`, `4da7a00`, `a15b831`. 검사기·테스트 commit 0 |
| REVIEW_ROUND §1·§3~§10은 v3.1.0과 같음 | 확인됨 | §3 이후 차이는 경로 이름(`TODO.md`·`PLAN.md`)과 원장 예시의 근거 한 칸뿐 |
| BUGBOT에만 결정 번복 항목 | 확인됨, 보완 | ko·en 모두 같음. BUGBOT에만 있는 다른 항목(INTENT·SPEC 부재만으로 만든 finding)은 REVIEW §3에 있어 어긋남이 아님 |
| R-002~R-005는 적용 저장소에서 쓰는 문구 | 확인됨 | 적용 저장소 `docs/REVIEW_ROUND.md` 77·86·94·103행. R-010·R-011은 그 문서에 없고 운영 경험에서 나온 제안 |
| R-003의 필요 | 보완 | TEMPLATE_GUIDE 「리뷰어 조사 힌트」의 자체 호스팅 GitHub App 행이 이미 webhook 트리거를 적으라고 함 |
| 일괄 치환 사례 | 확인됨 | 적용 저장소 `docs/TEMPLATE_GUIDE.md` 171행의 자기 매핑, 466~467행의 `README-PLAN.md`, 151행 조건부 삭제 문장이 그 저장소의 정본 확장 설계를 가리킴 |
| Q1: patch release로 먼저 낼 수 있음 | 정정 | §1.5 Q1 |
| R-008을 DOCS_GUIDE에 둠 | 보완 | DOCS_GUIDE adoption policy가 `copy`. 업그레이드 때 옮기는 절임을 적어야 함(§2.3.4) |
| setext `===` 등 남은 엣지 케이스(미확인) | 확인됨 | §2.3.1 「남은 한계」 |

**무작위 입력 차분.** 줄 앞 container(인용문·목록·들여쓰기·tab)와 줄 내용(fence, code span, escape, HTML block·주석, heading, 구분선, 목록 marker, 링크, reference definition)을 무작위로 조합한 문서 20,000개(seed 7)를 만들었습니다. 각 문서에서 검사기가 검사하는 로컬 링크 집합을 markdown-it-py가 링크로 해석한 집합과 비교했습니다. 일부러 드문 조합을 만든 입력이라 비율은 실제 문서의 빈도가 아닙니다.

| 지표 | 수정 전 | 수정 뒤(R-001) |
|---|---|---|
| CommonMark 링크 33,233개 중 놓친 링크 | 11,488 | 2,220 |
| 링크가 아닌데 검사한 링크 | 4,081 | 3,768 |
| 문서 판정: 둘 다 일치 / 수정으로 고쳐짐 / 둘 다 다름 / 수정으로 새로 틀림 | — | 10,923 / 4,734 / 4,010 / 333 |

- 새로 틀린 333건 중 311건은 링크가 아닌 것을 검사하는 쪽(더 엄격)입니다.
- 놓치는 쪽 22건 중 17건은 container 안의 닫히지 않은 `<!--`와 얽혀 있습니다. 최소화한 2건은 수정 전 검사기의 다른 결함(4번의 닫히지 않는 fence, 7번의 fence가 아닌 줄)이 그 주석을 우연히 가려 맞았던 경우였고, 나머지도 같다고 봅니다(추론).
- markdown-it-py와 cmark-gfm은 lazy continuation 한 사례에서 서로 달랐습니다. 그런 사례는 결론에 쓰지 않았습니다.

**하지 않은 것:** 이 저장소 CI(Buildkite API 토큰 인증 실패로 `9326c1e`의 build도 조회하지 못함), 영어 문구의 원어민 검수. R-012의 회귀 테스트는 설계 시점에는 없었고 T-067에서 작성합니다.

#### 2.6.3 작업 단위와 완료 조건

아래 단위는 [전역 TODO](../../02-TODO.md)의 항목입니다. 실행 상태는 TODO가 소유합니다.

| 단위 | 범위 | 완료 조건 |
|---|---|---|
| T-067 검사기 PR | 부록 A·B와 R-012의 수정·테스트 | 새 테스트마다 수정 전 검사기에서 assertion 실패·수정 뒤 통과(red-green). root·template 테스트, `check-docs.py`, `check-locales.py --require-stable`이 Windows·Linux 필수 CI에서 통과 |
| T-068 문구 PR | §2.3.2~§2.3.5의 채택 문구를 ko·en payload와 root 사본 셋에 반영 | `check-docs.py`(root 사본 대조 포함)와 `check-locales.py --require-stable` 통과. 바뀐 줄을 다시 읽어 ko·en 뜻과 절 참조 확인 |
| T-066 release | T-065·T-067·T-068을 `v3.2.0`으로 공개 | ko·en TEMPLATE_GUIDE §6 `v3.2.0` 항목과 CHANGELOG. D-007의 candidate·published 검증을 `--base-version 3.1.0`으로 통과 |

브랜치 구현·검증, `main` 통합, release와 published 검증은 각각 따로 완료로 기록합니다. 이 문서와 PROJECT·TODO 등재는 T-067 PR에 담고, T-068 PR은 그 위에 쌓습니다.

#### 2.6.4 미해결

없음. §2.3.1의 남은 한계는 PROJECT §12의 보류 항목입니다.

## 3. 변경 기록

- 2026-10-28: 적용 저장소 세션에서 초안을 작성했습니다.
- 2026-10-28: 이 저장소 세션에서 원문 주장을 다시 검증하고(§2.6.2) 판정, ko·en 문구 확정안, R-005·R-010 선택지, R-012를 더했습니다. 원문 §1.1~§1.4, §2.6.1과 부록은 그대로 두었습니다. 채택하지 않은 부분은 R-004의 별도 열, R-006의 검사기 대조 확장, R-008의 필드 세 개이며 이유는 §2.3에 있습니다.
- 2026-10-28: 사용자가 R-005·R-010 A, R-012 포함, R-008 형식을 승인해 Accepted로 바꾸고 D-020과 T-067·T-068로 등재했습니다. 공개는 T-066 `v3.2.0`입니다.

## 부록 A. 검사기 diff

`template/common/scripts/check-docs.py`(v3.1.0 = `main` `9326c1e`)에 대한 diff입니다. 적용 저장소 `scripts/check_docs.py`(`da34a08`)와 이 파일의 차이 전체이며, 13건 수정과 타입 검사용 한 줄로 이루어져 있습니다.

````diff
--- a/template/common/scripts/check-docs.py
+++ b/template/common/scripts/check-docs.py
@@ -49,8 +49,13 @@
 IMPORT_LINE_RE = re.compile(r"^@([^\s]+)\s*$")
 HEADING_RE = re.compile(r"^[ ]{0,3}(#{1,6})\s+(.*)$")
 HEADING_NUM_RE = re.compile(r"^[ ]{0,3}#{1,6}\s+(\d+(?:\.\d+)*)[.\s]")
-FENCE_LINE_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})(.*)$")
+# A backtick fence's info string has no backtick; otherwise it is a code span.
+FENCE_LINE_RE = re.compile(r"^[ ]{0,3}(`{3,}(?=[^`]*$)|~{3,})(.*)$")
 BLOCKQUOTE_MARKER_RE = re.compile(r"[ ]{0,3}>[ \t]?")
+# A one-line block: an ATX heading or a thematic break.
+LINE_BLOCK_RE = re.compile(
+    r"^[ ]{0,3}(?:#{1,6}(?:[ \t]|\r?$)|([-*_])(?:[ \t]*\1){2,}[ \t]*\r?$)"
+)
 # CommonMark HTML blocks: type 1 ends at its closing tag, type 6 at a blank line.
 HTML_BLOCK_RAW_RE = re.compile(
     r"^[ ]{0,3}<(pre|script|style|textarea)(?:[ \t>]|$)", re.IGNORECASE
@@ -64,7 +69,10 @@
     r"track|ul)(?:[ \t>]|/>|$)",
     re.IGNORECASE,
 )
-LIST_ITEM_RE = re.compile(r"^( *)(?:[-+*]|\d{1,9}[.)])([ \t]+)")
+# A thematic break such as `- - -` wins over a list item.
+LIST_ITEM_RE = re.compile(
+    r"^( *)(?!([-*_])(?:[ \t]*\2){2,}[ \t]*$)(?:[-+*]|\d{1,9}[.)])([ \t]+)"
+)
 REFERENCE_DEFINITION_RE = re.compile(
     r"^[ ]{0,3}\[((?:\\.|[^\]\r\n])+)\]:[ \t]*"
 )
@@ -313,7 +321,7 @@
         if key is None:
             continue
         value = re.fullmatch(
-            r"(true|false)\s*(?:#.*)?", key.group(1), re.IGNORECASE
+            r"(true|false)(?:\s+#.*)?\s*", key.group(1), re.IGNORECASE
         )
         values.append(
             value.group(1).lower() == "true" if value is not None else None
@@ -412,39 +420,42 @@
     return depth, line[cursor:]


+def leaves_container(line: str, blockquote_depth: int, list_indent: int) -> bool:
+    """Return whether *line* ends the blockquote or list item holding a block."""
+
+    depth, content = strip_blockquote_markers(line, blockquote_depth)
+    if depth < blockquote_depth:
+        return True
+    content = content.expandtabs(4)
+    leading = len(content) - len(content.lstrip(" "))
+    return bool(content.strip()) and leading < list_indent
+
+
 def indented_code_line_indexes(text: str) -> set:
     """Return line indexes belonging to ordinary or list-relative code blocks."""

     code_lines = set()
     list_items: List[Tuple[int, int]] = []
+    list_depth = 0
     in_code = False
     code_indent = 4
     previous_blank = True

     for index, raw_line in enumerate(text.splitlines()):
-        _, line = strip_blockquote_markers(raw_line)
+        depth, line = strip_blockquote_markers(raw_line)
         line = line.expandtabs(4)
+        # Lists live inside one blockquote level and end when it changes.
+        if depth != list_depth:
+            list_items.clear()
+            list_depth = depth
         if not line.strip():
             if in_code:
                 code_lines.add(index)
             previous_blank = True
             continue

+        # Code comes first: a list marker indented as code is example text.
         leading = len(line) - len(line.lstrip(" "))
-        list_item = LIST_ITEM_RE.match(line)
-        if list_item is not None:
-            marker_indent = len(list_item.group(1))
-            while list_items and marker_indent <= list_items[-1][0]:
-                list_items.pop()
-            while list_items and marker_indent < list_items[-1][1]:
-                list_items.pop()
-            list_items.append((marker_indent, list_item.end()))
-            in_code = False
-            previous_blank = False
-            continue
-
-        while list_items and leading < list_items[-1][1]:
-            list_items.pop()
         required_indent = (list_items[-1][1] if list_items else 0) + 4
         if in_code:
             if leading >= code_indent:
@@ -456,7 +467,22 @@
             code_indent = required_indent
             in_code = True
             code_lines.add(index)
-        previous_blank = False
+            previous_blank = False
+            continue
+
+        list_item = LIST_ITEM_RE.match(line)
+        if list_item is not None:
+            marker_indent = len(list_item.group(1))
+            while list_items and marker_indent <= list_items[-1][0]:
+                list_items.pop()
+            while list_items and marker_indent < list_items[-1][1]:
+                list_items.pop()
+            list_items.append((marker_indent, list_item.end()))
+        else:
+            while list_items and leading < list_items[-1][1]:
+                list_items.pop()
+        # Like a blank line, a heading or thematic break lets code start next.
+        previous_blank = list_item is None and LINE_BLOCK_RE.match(line) is not None
     return code_lines


@@ -466,55 +492,63 @@
     context = []
     fence_character: Optional[str] = None
     fence_length = 0
-    fence_blockquote_depth = 0
+    block_depth = 0
+    block_list_indent = 0
     in_html_comment = False
     html_block_end: Optional[str] = None
     indented_code_lines = indented_code_line_indexes(text)
     openers = CommentOpenerSearch(text)
     list_items: List[Tuple[int, int]] = []
+    list_depth = 0
     for index, line in enumerate(text.splitlines()):
         blockquote_depth, container_line = strip_blockquote_markers(line)
         container_line = container_line.expandtabs(4)
+        if (
+            html_block_end is not None or fence_character is not None
+        ) and leaves_container(line, block_depth, block_list_indent):
+            html_block_end = None
+            fence_character = None
         if html_block_end is not None:
             context.append((False, False))
+            openers.skip_line(index)
             if html_block_end == "" and not container_line.strip():
                 html_block_end = None
             elif html_block_end and html_block_end in line.lower():
                 html_block_end = None
             continue
         if fence_character is not None:
-            if blockquote_depth < fence_blockquote_depth:
+            _, closing_container = strip_blockquote_markers(line, block_depth)
+            closing_candidate = list_relative_line(
+                closing_container.expandtabs(4), list_items, update=False
+            )
+            context.append((False, False))
+            openers.skip_line(index)
+            stripped = closing_candidate.lstrip(" ")
+            if (
+                len(closing_candidate) - len(stripped) <= 3
+                and re.fullmatch(
+                    re.escape(fence_character) + "{%d,}[ \t]*" % fence_length,
+                    stripped,
+                )
+            ):
                 fence_character = None
                 fence_length = 0
-                fence_blockquote_depth = 0
-            else:
-                _, closing_container = strip_blockquote_markers(
-                    line, fence_blockquote_depth
-                )
-                closing_candidate = list_relative_line(
-                    closing_container.expandtabs(4), list_items, update=False
-                )
-                context.append((False, False))
-                stripped = closing_candidate.lstrip(" ")
-                if (
-                    len(closing_candidate) - len(stripped) <= 3
-                    and re.fullmatch(
-                        re.escape(fence_character) + "{%d,}[ \t]*" % fence_length,
-                        stripped,
-                    )
-                ):
-                    fence_character = None
-                    fence_length = 0
-                    fence_blockquote_depth = 0
-                continue
+            continue

         if not in_html_comment and index in indented_code_lines:
             context.append((False, False))
+            openers.skip_line(index)
             continue

+        if not in_html_comment and blockquote_depth != list_depth:
+            list_items.clear()
+            list_depth = blockquote_depth
         fence_candidate = list_relative_line(
             container_line, list_items, update=not in_html_comment
         )
+        # The container of a fenced or HTML block that opens on this line.
+        block_depth = blockquote_depth
+        block_list_indent = list_items[-1][1] if list_items else 0
         fence = (
             None
             if in_html_comment
@@ -524,8 +558,8 @@
             sequence = fence.group(1)
             fence_character = sequence[0]
             fence_length = len(sequence)
-            fence_blockquote_depth = blockquote_depth
             context.append((False, False))
+            openers.skip_line(index)
             continue

         raw_block = (
@@ -534,11 +568,13 @@
         if raw_block is not None:
             closing = "</%s>" % raw_block.group(1).lower()
             context.append((False, False))
+            openers.skip_line(index)
             if closing not in fence_candidate.lower()[raw_block.end() :]:
                 html_block_end = closing
             continue
         if not in_html_comment and HTML_BLOCK_TAG_RE.match(fence_candidate):
             context.append((False, False))
+            openers.skip_line(index)
             html_block_end = ""
             continue

@@ -586,6 +622,11 @@

         self.pairing_start = self.line_starts[index] + column

+    def skip_line(self, index: int) -> None:
+        """Keep backticks on code or raw HTML line *index* out of code spans."""
+
+        self.pairing_start = max(self.pairing_start, self.line_starts[index + 1])
+
     def find(self, index: int, column: int, end: int) -> int:
         """Return the first opener column in ``line[column:end]``, or ``-1``."""

@@ -674,18 +715,30 @@
     """Return the end of the backtick run at *start* and of its code span.

     The code span ends after the next run of the same length; without one the
-    run is literal text and its span end is ``None``.
+    run is literal text and its span end is ``None``. An escaped backtick is
+    literal and consumes only itself. A span stays in its paragraph or heading
+    line: it never closes past a line that ends the paragraph.
     """

+    if is_escaped(text, start):
+        return start + 1, None
     opening_end = start + 1
     while opening_end < len(text) and text[opening_end] == "`":
         opening_end += 1
     run_length = opening_end - start

+    line_start = text.rfind("\n", 0, start) + 1
+    line_end = text.find("\n", start)
+    if line_end < 0:
+        line_end = len(text)
+    depth, content = strip_blockquote_markers(text[line_start:line_end])
+    limit = line_end if HEADING_RE.match(content) else len(text)
     candidate = opening_end
-    while candidate < len(text):
-        closing_start = text.find("`", candidate)
-        if closing_start < 0:
+    while candidate < limit:
+        closing_start = text.find("`", candidate, limit)
+        if closing_start < 0 or paragraph_ends_between(
+            text, candidate, closing_start, depth
+        ):
             break
         run_end = closing_start + 1
         while run_end < len(text) and text[run_end] == "`":
@@ -696,6 +749,30 @@
     return opening_end, None


+def paragraph_ends_between(text: str, start: int, end: int, depth: int) -> bool:
+    """Return whether a line starting in ``text[start:end]`` ends a paragraph.
+
+    A paragraph at blockquote *depth* ends at a blank line, a deeper
+    blockquote, or a heading, thematic break or list item line. A shallower
+    line continues it lazily.
+    """
+
+    newline = text.find("\n", start, end)
+    while newline >= 0:
+        line_end = text.find("\n", newline + 1)
+        line = text[newline + 1 : len(text) if line_end < 0 else line_end]
+        line_depth, content = strip_blockquote_markers(line)
+        if (
+            line_depth > depth
+            or not content.strip()
+            or LINE_BLOCK_RE.match(content)
+            or LIST_ITEM_RE.match(content)
+        ):
+            return True
+        newline = text.find("\n", newline + 1, end)
+    return False
+
+
 def markdown_searchable_text(text: str, *, mask_inline_code: bool = False) -> str:
     """Mask non-prose Markdown constructs while preserving string offsets."""

@@ -711,6 +788,7 @@
         if not outside_fence:
             mask_text_range(characters, 0, content_end)
             masked_lines.append("".join(characters))
+            openers.skip_line(index)
             continue

         cursor = 0
@@ -1119,6 +1197,7 @@
             bullet_indent = len(bullet_match.group(1))
         if (
             bullet_match is not None
+            and bullet_indent is not None
             and len(bullet_match.group(1)) <= bullet_indent
         ):
             if current is not None and current_index is not None:
````

## 부록 B. 회귀 테스트 diff

`template/common/tests/test_check_docs.py`에 대한 diff입니다. 적용 저장소 테스트 파일에서 이 수정에 해당하는 hunk만 골랐고, 프로젝트 고유 변경(검사기 경로, 문서 이름, 보관 디렉터리 제외 테스트)은 뺐습니다. `patch -p1`로 부록 A와 함께 적용합니다.

````diff
--- a/template/common/tests/test_check_docs.py
+++ b/template/common/tests/test_check_docs.py
@@ -73,7 +75,7 @@
             config.parent.mkdir(parents=True)
             skill.write_text("skill", encoding="utf-8")

-            for value in ("true", '"false"', "missing"):
+            for value in ("true", '"false"', "false#note", "missing"):
                 if value == "missing":
                     config.write_text("policy: {}\n", encoding="utf-8")
                 else:
@@ -86,13 +88,15 @@
                     CHECK_DOCS.check_skill_configs(errors, [])
                 self.assertTrue(errors, value)

-            config.write_text(
-                "policy:\n  allow_implicit_invocation: false\n", encoding="utf-8"
-            )
-            errors = []
-            with patch.object(CHECK_DOCS, "ROOT", root):
-                CHECK_DOCS.check_skill_configs(errors, [])
-            self.assertEqual(errors, [])
+            for value in ("false", "false # explicit only"):
+                config.write_text(
+                    "policy:\n  allow_implicit_invocation: %s\n" % value,
+                    encoding="utf-8",
+                )
+                errors = []
+                with patch.object(CHECK_DOCS, "ROOT", root):
+                    CHECK_DOCS.check_skill_configs(errors, [])
+                self.assertEqual(errors, [], value)

             for duplicate in (
                 "policy:\n"
@@ -509,6 +513,346 @@
                 CHECK_DOCS.check_relative_links(errors, [])
             self.assertIn("MISSING.md", "\n".join(errors))

+    def test_escaped_backtick_does_not_open_code_span(self) -> None:
+        with tempfile.TemporaryDirectory() as directory:
+            root = Path(directory)
+            write(
+                root,
+                "docs/SOURCE.md",
+                "Use \\` as a literal delimiter.\n"
+                "[broken](./MISSING.md)\n"
+                "Use \\` again.\n"
+                "\n"
+                "A \\``span\n"
+                "[code](./CODE.md)` stays code.\n",
+            )
+
+            errors = []
+            with patch.object(CHECK_DOCS, "ROOT", root):
+                CHECK_DOCS.check_relative_links(errors, [])
+            self.assertIn("MISSING.md", "\n".join(errors))
+            self.assertNotIn("CODE.md", "\n".join(errors))
+
+    def test_code_span_does_not_cross_blank_line(self) -> None:
+        with tempfile.TemporaryDirectory() as directory:
+            root = Path(directory)
+            write(
+                root,
+                "docs/SOURCE.md",
+                "Open ` here.\n"
+                "\n"
+                "[missing](./MISSING.md)\n"
+                "\n"
+                "Then `code`.\n"
+                "\n"
+                "A `multi-line\n"
+                "[code](./CODE.md)` span.\n",
+            )
+
+            errors = []
+            with patch.object(CHECK_DOCS, "ROOT", root):
+                CHECK_DOCS.check_relative_links(errors, [])
+            self.assertIn("MISSING.md", "\n".join(errors))
+            self.assertNotIn("CODE.md", "\n".join(errors))
+
+    def test_indented_list_examples_are_code_blocks(self) -> None:
+        with tempfile.TemporaryDirectory() as directory:
+            root = Path(directory)
+            write(
+                root,
+                "docs/SOURCE.md",
+                "    - [top](./MISSING-TOP.md)\n"
+                "    - [continued](./MISSING-CONTINUED.md)\n"
+                "\n"
+                "Paragraph.\n"
+                "\n"
+                "    1. [ordered](./MISSING-ORDERED.md)\n"
+                "\n"
+                "- item\n"
+                "\n"
+                "      - [nested](./MISSING-NESTED.md)\n"
+                "\n"
+                "- [real](./MISSING-REAL.md)\n"
+                "  - [inner](./MISSING-INNER.md)\n",
+            )
+
+            errors = []
+            with patch.object(CHECK_DOCS, "ROOT", root):
+                CHECK_DOCS.check_relative_links(errors, [])
+            report = "\n".join(errors)
+            for example in ("TOP", "CONTINUED", "ORDERED", "NESTED"):
+                self.assertNotIn("MISSING-%s.md" % example, report)
+            self.assertIn("MISSING-REAL.md", report)
+            self.assertIn("MISSING-INNER.md", report)
+
+    def test_list_fence_ends_with_its_list_item(self) -> None:
+        with tempfile.TemporaryDirectory() as directory:
+            root = Path(directory)
+            write(
+                root,
+                "docs/SOURCE.md",
+                "- item\n"
+                "\n"
+                "  ```text\n"
+                "  [inside](./INSIDE.md)\n"
+                "\n"
+                "[after list](./MISSING-AFTER-LIST.md)\n"
+                "\n"
+                "- outer\n"
+                "  - inner\n"
+                "\n"
+                "    ```text\n"
+                "    [nested](./NESTED.md)\n"
+                "  [outer prose](./MISSING-OUTER.md)\n"
+                "\n"
+                "> - quoted\n"
+                ">\n"
+                ">   ```text\n"
+                ">   [quoted](./QUOTED.md)\n"
+                ">\n"
+                "> [quote prose](./MISSING-QUOTE.md)\n"
+                "\n"
+                "- closed\n"
+                "\n"
+                "  ```text\n"
+                "  [closed](./CLOSED.md)\n"
+                "  ```\n"
+                "  [after fence](./MISSING-AFTER-FENCE.md)\n",
+            )
+
+            errors = []
+            with patch.object(CHECK_DOCS, "ROOT", root):
+                CHECK_DOCS.check_relative_links(errors, [])
+            report = "\n".join(errors)
+            for example in ("INSIDE", "NESTED", "QUOTED", "CLOSED"):
+                self.assertNotIn("/%s.md" % example, report)
+            for prose in ("AFTER-LIST", "OUTER", "QUOTE", "AFTER-FENCE"):
+                self.assertIn("MISSING-%s.md" % prose, report)
+
+    def test_html_block_ends_with_its_container(self) -> None:
+        with tempfile.TemporaryDirectory() as directory:
+            root = Path(directory)
+            write(
+                root,
+                "docs/SOURCE.md",
+                "> <pre>\n"
+                "> [quoted](./QUOTED.md)\n"
+                "\n"
+                "[after quote](./MISSING-AFTER-QUOTE.md)\n"
+                "\n"
+                "- <pre>\n"
+                "  [listed](./LISTED.md)\n"
+                "\n"
+                "[after list](./MISSING-AFTER-LIST.md)\n",
+            )
+
+            errors = []
+            with patch.object(CHECK_DOCS, "ROOT", root):
+                CHECK_DOCS.check_relative_links(errors, [])
+            report = "\n".join(errors)
+            for example in ("QUOTED", "LISTED"):
+                self.assertNotIn("/%s.md" % example, report)
+            for prose in ("AFTER-QUOTE", "AFTER-LIST"):
+                self.assertIn("MISSING-%s.md" % prose, report)
+
+    def test_one_line_backtick_span_is_not_a_fence(self) -> None:
+        with tempfile.TemporaryDirectory() as directory:
+            root = Path(directory)
+            write(
+                root,
+                "docs/SOURCE.md",
+                "```[span](./SPAN.md)```\n"
+                "\n"
+                "[broken](./MISSING.md)\n"
+                "\n"
+                "```text\n"
+                "[fenced](./FENCED.md)\n"
+                "```\n",
+            )
+
+            errors = []
+            with patch.object(CHECK_DOCS, "ROOT", root):
+                CHECK_DOCS.check_relative_links(errors, [])
+            report = "\n".join(errors)
+            self.assertIn("MISSING.md", report)
+            self.assertNotIn("SPAN.md", report)
+            self.assertNotIn("FENCED.md", report)
+
+    def test_code_block_backticks_do_not_hide_comment_openers(self) -> None:
+        with tempfile.TemporaryDirectory() as directory:
+            root = Path(directory)
+            write(
+                root,
+                "docs/SOURCE.md",
+                "~~~text\n"
+                "`\n"
+                "~~~\n"
+                "<!--\n"
+                "[fenced](./FENCED.md)\n"
+                "-->\n"
+                "`code`\n"
+                "\n"
+                "Intro.\n"
+                "\n"
+                "    `\n"
+                "<!--\n"
+                "[indented](./INDENTED.md)\n"
+                "-->\n"
+                "`code`\n"
+                "\n"
+                "[real](./MISSING-REAL.md)\n",
+            )
+
+            errors = []
+            with patch.object(CHECK_DOCS, "ROOT", root):
+                CHECK_DOCS.check_relative_links(errors, [])
+            report = "\n".join(errors)
+            self.assertIn("MISSING-REAL.md", report)
+            self.assertNotIn("FENCED.md", report)
+            self.assertNotIn("INDENTED.md", report)
+
+    def test_quoted_list_ends_with_its_blockquote(self) -> None:
+        with tempfile.TemporaryDirectory() as directory:
+            root = Path(directory)
+            write(
+                root,
+                "docs/SOURCE.md",
+                "> - item\n"
+                "\n"
+                "    [example](./EXAMPLE.md)\n"
+                "\n"
+                "> - item\n"
+                ">\n"
+                ">       [quoted code](./QUOTED-CODE.md)\n"
+                ">\n"
+                ">   [item prose](./MISSING-ITEM.md)\n",
+            )
+
+            errors = []
+            with patch.object(CHECK_DOCS, "ROOT", root):
+                CHECK_DOCS.check_relative_links(errors, [])
+            report = "\n".join(errors)
+            self.assertNotIn("EXAMPLE.md", report)
+            self.assertNotIn("QUOTED-CODE.md", report)
+            self.assertIn("MISSING-ITEM.md", report)
+
+    def test_thematic_breaks_are_not_list_items(self) -> None:
+        with tempfile.TemporaryDirectory() as directory:
+            root = Path(directory)
+            write(
+                root,
+                "docs/SOURCE.md",
+                "Text.\n"
+                "\n"
+                "- - -\n"
+                "\n"
+                "    [dash](./DASH.md)\n"
+                "\n"
+                "* * *\n"
+                "\n"
+                "    [star](./STAR.md)\n"
+                "\n"
+                "- item\n"
+                "\n"
+                "      [item code](./ITEM-CODE.md)\n"
+                "\n"
+                "  [item prose](./MISSING-ITEM.md)\n",
+            )
+
+            errors = []
+            with patch.object(CHECK_DOCS, "ROOT", root):
+                CHECK_DOCS.check_relative_links(errors, [])
+            report = "\n".join(errors)
+            for example in ("DASH", "STAR", "ITEM-CODE"):
+                self.assertNotIn("/%s.md" % example, report)
+            self.assertIn("MISSING-ITEM.md", report)
+
+    def test_code_span_does_not_cross_block_starts(self) -> None:
+        with tempfile.TemporaryDirectory() as directory:
+            root = Path(directory)
+            write(
+                root,
+                "docs/SOURCE.md",
+                "A literal ` delimiter.\n"
+                "## Next section\n"
+                "[after heading](./MISSING-HEADING.md)\n"
+                "Use `code`.\n"
+                "\n"
+                "## Heading with ` tick\n"
+                "[after tick](./MISSING-TICK.md) and `code`.\n"
+                "\n"
+                "Break ` open\n"
+                "***\n"
+                "[after break](./MISSING-BREAK.md) and `code`.\n"
+                "\n"
+                "Item ` open\n"
+                "- [listed](./MISSING-LISTED.md) and `code`.\n"
+                "\n"
+                "A `multi-line\n"
+                "[code](./CODE.md)` span.\n",
+            )
+
+            errors = []
+            with patch.object(CHECK_DOCS, "ROOT", root):
+                CHECK_DOCS.check_relative_links(errors, [])
+            report = "\n".join(errors)
+            for prose in ("HEADING", "TICK", "BREAK", "LISTED"):
+                self.assertIn("MISSING-%s.md" % prose, report)
+            self.assertNotIn("/CODE.md", report)
+
+    def test_indented_code_may_follow_heading_or_break(self) -> None:
+        with tempfile.TemporaryDirectory() as directory:
+            root = Path(directory)
+            write(
+                root,
+                "docs/SOURCE.md",
+                "## Example\n"
+                "    [example](./EXAMPLE-ONLY.md)\n"
+                "\n"
+                "***\n"
+                "    [after break](./AFTER-BREAK.md)\n"
+                "\n"
+                "Paragraph\n"
+                "    [lazy](./MISSING-LAZY.md)\n",
+            )
+
+            errors = []
+            with patch.object(CHECK_DOCS, "ROOT", root):
+                CHECK_DOCS.check_relative_links(errors, [])
+            report = "\n".join(errors)
+            self.assertNotIn("EXAMPLE-ONLY.md", report)
+            self.assertNotIn("AFTER-BREAK.md", report)
+            self.assertIn("MISSING-LAZY.md", report)
+
+    def test_code_span_stays_in_its_blockquote_paragraph(self) -> None:
+        with tempfile.TemporaryDirectory() as directory:
+            root = Path(directory)
+            write(
+                root,
+                "docs/SOURCE.md",
+                "unmatched `\n"
+                "> [quoted](./MISSING-QUOTED.md) `code`\n"
+                "\n"
+                "> unmatched `\n"
+                ">\n"
+                "> [split](./MISSING-SPLIT.md) `code`\n"
+                "\n"
+                "> A `multi-line\n"
+                "> [code](./CODE.md)` span.\n"
+                "\n"
+                "> A lazy `span\n"
+                "[lazy](./LAZY.md)` ends here.\n",
+            )
+
+            errors = []
+            with patch.object(CHECK_DOCS, "ROOT", root):
+                CHECK_DOCS.check_relative_links(errors, [])
+            report = "\n".join(errors)
+            self.assertIn("MISSING-QUOTED.md", report)
+            self.assertIn("MISSING-SPLIT.md", report)
+            self.assertNotIn("/CODE.md", report)
+            self.assertNotIn("LAZY.md", report)
+
     def test_backticks_inside_comments_do_not_pair_with_code_spans(self) -> None:
         text = (
             "<!-- ` --> <!-- `\n"
````
