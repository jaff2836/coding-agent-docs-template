# 프로젝트 작업 목록

> 프로젝트 전체의 변경·마일스톤·우선순위·의존성을 관리합니다. 제품 기준과 결정은 [00-PROJECT.md](./00-PROJECT.md), 상세 상태의 소유권은 [DOCS_GUIDE.md](./DOCS_GUIDE.md)를 따릅니다.
>
> 템플릿 저장소 자체의 maintainer 작업을 추적하며 locale artifact에 포함하지 않습니다. 사용자용 TODO 양식의 source는 `locales/<tag>/docs/02-TODO.md`입니다. 한국어 양식은 W-001(Origin PR #3)에서 `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`의 root 양식을 옮긴 것입니다.

## Metadata

- **Status:** Active
- **Owner:** Chae Sangwon
- **Last reviewed:** 2026-10-12 (KST)
- **Review cadence:** 작업 범위·우선순위·의존성·통합 결과 변경 시
- **Integration target:** Origin `main`(PR merge)과 공개 저장소 `jaff2836/coding-agent-docs-template`의 `main`(같은 merge commit의 non-force fast-forward, [TEMPLATE_GUIDE §5](./TEMPLATE_GUIDE.md)); v1.7.1 payload 기준 `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`

## Current Milestone

- **Name:** `v3.0.1` — 외부 분석 후속
- **Goal:** 2026-10-12 사용자가 전달한 외부 project-analysis 결과의 1~7번을 반영하고 `v3.0.1`로 공개함
- **Target:** 아래 Backlog 36~40행
- **Status:** In Progress — 2026-10-12 사용자가 1~6번 수정과 7번의 `v3.0.1` 전 진행을 정했습니다. 같은 결과의 `SECURITY.md` 제안은 읽는 agent가 있을 때만 추가하기로 했고, 네 도구의 지침 로딩 경로에 없어 보류했습니다. T-043은 보류(Blocked)입니다.

## 운영 규칙

- 변경별 PLAN이 있으면 이 문서는 링크·우선순위·선행조건과 통합 여부만 관리합니다. 상세 체크박스·검증 로그를 복제하지 않습니다.
- PLAN이 없는 작은 작업은 아래 항목 안에서 범위·구현 순서·완료 조건·검증을 관리합니다.
- `In Progress`는 프로젝트가 선택한 진행 작업입니다. 다른 브랜치나 열린 PR의 실시간 상태를 보장하지 않습니다. 작업 시작 시 실제 Git·PR 상태와 해당 변경의 PLAN을 확인합니다.
- 각 브랜치는 자기 변경의 상세 기록을 갱신합니다. 다른 브랜치 작업을 오래된 사본만 보고 완료·미완료로 되돌리지 않습니다.
- 공통 항목은 범위·의존성·통합 결과가 달라질 때만 수정합니다. 충돌은 최신 기준과 변경-ID를 대조해 해결하고, 영향받은 계약·검증 전제를 재확인합니다.
- `Completed`는 필요한 검증과 지정한 대상에의 반영을 확인한 항목, 또는 작업 브랜치에서 자기 최종 head의 통합과 동시에 완료되는 항목(결합 서술)을 담습니다. 릴리스·지원 검증처럼 통합 뒤에 일어나는 완료는 그 일이 끝난 뒤에만 기록합니다. 브랜치 구현 완료·리뷰 통과·병합·릴리스·지원 검증을 구분하고 해당 작업의 완료 조건으로 판단합니다.
- 자기 PR의 CI build·리뷰 판정·merge SHA는 PR을 원장으로 두고 이 문서에는 PR 참조만 둡니다. 상세 규칙과 사용자 요청 예외는 [DOCS_GUIDE.md](./DOCS_GUIDE.md)의 로컬 Git과 병렬 브랜치 절을 따릅니다.
- `T-nnn`은 이 문서의 전역 작업 ID입니다. 변경-ID·PROJECT의 `D-nnn`·변경 폴더의 `R-nnn`/`W-nnn`과 범위가 다릅니다. 발급·충돌 처리는 [DOCS_GUIDE.md](./DOCS_GUIDE.md)의 식별자 범위를 따릅니다.
- 취소한 변경은 Cancelled에 두고 변경 폴더는 유지합니다. 완료된 SPEC을 현재 제품 기준으로 읽지 않으며, 구현된 계약은 통합 후 PROJECT에 반영합니다.
- 원격 저장소나 PR은 필수가 아닙니다. 로컬 작업은 기준 revision과 대상 브랜치 또는 검토한 작업 트리 범위로 근거를 남깁니다. 미커밋 결과를 commit SHA로 재현된다고 표현하지 않습니다.
- 문서 갱신은 commit·push·merge 권한이 아닙니다. 리뷰 라운드 통과 후 반영은 [REVIEW_ROUND.md](./REVIEW_ROUND.md) §9를 따릅니다.

## In Progress

없음. 다음 작업은 Current Milestone과 Backlog 순서를 따릅니다.

## Next

Backlog 37·38행을 진행합니다. T-058(39행)은 36행 위에 쌓은 PR로 진행합니다. 새 작업은 사용자와 정한 뒤 PR 단위로 수동 리뷰·필수 CI·통합을 거칩니다.

## Blocked

- [ ] **T-043 community locale 설계 (보류)** — 2026-10-08 사용자 결정으로 보류합니다.
  - 보류 이유: 지금 계약에서는 manifest의 모든 locale이 `en`과 구조 parity를 유지해야 합니다(`check_locales.py`의 `_check_structural_parity`, `experimental` 포함). locale을 하나 추가하면 이후 payload PR마다 그 locale에도 구조 변경을 반영해야 합니다. 또 `stale`·`baseline_version`은 manifest 기준 판 `1.7.1`(v1 이관 시점)에 묶여 있어 현재 release와 번역 사이의 차이를 표현하지 못합니다.
  - 재개 조건: 실제 수요가 생기거나 사용자가 다시 정하는 경우입니다. 후보 locale은 중국어(`zh-Hans`)와 일본어(`ja`)이고, 번역 검수는 사용자 본인이 할 수 있습니다. 다시 시작하면 먼저 상태 장치를 고칠지(뒤처진 locale을 parity에서 빼고 현재 release 기준으로 `stale`을 표시) 정한 뒤 locale을 추가합니다.
  - 등록 당시 설명은 [완료 작업 보관](./TODO_ARCHIVE.md)에 있습니다.

## Backlog

아래 순서는 위험과 선행조건을 고려한 권고 PR 순서이며, Backlog 항목을 시작하는 권한은 아닙니다.
설계 결과에 따라 필요한 구현은 해당 설계 PR과 분리합니다.

통합된 순서 1~35의 기록은 [완료 작업 보관](./TODO_ARCHIVE.md)에 있습니다.

| 순서 | PR 단위 | 작업 | 선행조건·통합 경계 |
| --- | --- | --- | --- |
| 36 | `claude/installer-hardening` | T-055 installer 경로·복구·manifest 검사 보강 | **In Progress** — PR #77. 공개는 40행 |
| 37 | `claude/maintainer-check-hardening` | T-056 package source 대조와 locale 주석 해석 | 36과 독립. release 불필요 |
| 38 | `claude/readme-attestation-order` | T-057 root README attestation 순서와 CI 문구 | 독립. release 불필요 |
| 39 | `claude/t058-candidate-e2e` | T-058 candidate 실제 package E2E | **In Progress** — 이 변경의 PR(36 위에 쌓음). 40행 candidate부터 적용 |
| 40 | `claude/v3.0.1-release-prep` 등 | T-059 `v3.0.1` release | 36~39 통합 뒤 |

- [ ] **T-056 maintainer 검사 보강** — 외부 분석 1·4번입니다. `package_release.verify_source_revision()`이 `assume-unchanged`·`skip-worktree`로 숨긴 작업 트리 변경을 통과시키지 않게 하고, `check_locales._mask_html_comments()`가 inline code·fenced code 안의 `<!--`를 주석 시작으로 읽지 않게 합니다. exporter·packager가 게시에 실패하면 먼저 지운 빈 output을 되살리는지도 installer와 맞춥니다. 각각 red-green 회귀를 둡니다.
- [ ] **T-057 root README 설치 안내** — 외부 분석 5번과 CI 문구입니다. root `README.md`·`README.ko.md`에서 `gh release verify-asset` 확인을 첫 installer 실행보다 앞에 두고, "특정 CI 제품의 pipeline이 없다"는 문장을 artifact 기준으로 고칩니다. root 문서라 release가 필요 없습니다.
- [ ] **T-059 `v3.0.1` release** — T-055의 installer 변경을 D-007 단계에 따라 patch release로 공개합니다. candidate는 T-058을 포함해 실행합니다.

## Cancelled

취소한 변경만 둡니다. 변경-ID, 취소 이유, Intent/Spec의 `Rejected` 근거, 유지 중인 변경 폴더 경로를 남깁니다. 완료·진행 항목과 섞지 않으며 폴더는 삭제하지 않습니다.

- **T-044 문서 필터 payload 이관** — 2026-10-08 취소. T-040 평가에서 문체 필터를 중단해 옮길 대상이 없습니다. 변경 폴더는 만들지 않았습니다.
- **T-046 `v2.6.0` release** — 2026-10-08 취소. T-044·T-045가 취소돼 공개할 payload 변경이 없습니다. 이후 payload를 바꾸는 작업이 생기면 그 작업에서 release 항목을 새로 등록합니다.
- **T-045 community locale 구현** — 2026-10-08 취소. 선행 설계 T-043을 보류해 구현할 계약이 없습니다. 변경 폴더는 만들지 않았습니다. T-043을 다시 시작하면 그 설계에서 구현 항목을 새로 등록합니다.

## Completed

실제 완료 항목만 추가합니다. 변경-ID, 통합 대상, 확인한 revision 또는 작업 트리 범위, 검증 근거의 위치를 남깁니다. 변경 폴더는 유지하고, 구현된 계약이 현재 지원 범위가 되면 PROJECT를 갱신합니다. PR이 있으면 실제 병합 결과를 확인합니다. 운영 규칙이 허용하는 결합 서술은 통합 전에 적을 수 있습니다. 로컬 작업에 가상의 PR·merge SHA를 만들지 않습니다.

상세 기록은 [완료 작업 보관](./TODO_ARCHIVE.md)에 있습니다. 새 완료 항목은 한 줄로 적고 상세 근거는 PR과 변경 문서에 둡니다.

- [x] **T-058 candidate 실제 package E2E** — 외부 분석 7번입니다. 2026-10-12 사용자가 승인한 방식대로 `verify-release.py candidate`가 draft byte 대조 뒤 그 byte를 loopback(`127.0.0.1`) release root로 제공하고, published와 같은 `_verify_published_e2e()`를 실행합니다(en·ko × `latest`·exact × `list-locales`·`install`·`export`·`adopt`, install 충돌·adopt 대상 불변, artifact checker). 선택형 `--base-version`을 주면 공개된 base release asset도 같은 root로 제공해 base-aware `adopt`까지 확인합니다(같은 날 사용자 결정). 설계: [release 검증 변경](./changes/2026-09-20-release-verification/01-CHANGE.md) R-008. 회귀 테스트는 `tests/test_verify_release.py`에 있고 red-green 결과는 PR 본문에 있습니다. 첫 운영 적용은 T-059 candidate입니다. 통합: 이 변경의 PR.
- [x] **T-055 installer 경로·복구·manifest 검사 보강** — 외부 분석 2·3·6번(2026-10-12 사용자 결정)입니다. source `scripts/installer.py`의 member 경로가 source 검사와 같은 규칙으로 드라이브·colon·제어문자·끝의 점과 공백·Windows 예약 이름을 거부합니다. install rollback은 취소(`KeyboardInterrupt`)에도 실행되고, 지우지 못한 경로가 있으면 대상 불변 대신 그 경로를 보고합니다. export·adopt 게시가 실패하면 먼저 지운 빈 output 디렉터리를 되살립니다. 현재 release manifest는 문자열 필드 타입, installer 크기, `SHA256SUMS`의 asset 목록과 locale ZIP digest까지 대조합니다. 회귀 테스트는 `tests/test_install_release.py`에 있고 red-green 결과는 PR 본문에 있습니다. 공개는 T-059(`v3.0.1`)입니다. 통합: 이 변경의 PR.
- [x] **T-054 root 관리 문서 정리** — 2026-10-12 사용자 요청으로 root `docs/00-PROJECT.md`·`docs/02-TODO.md`의 오래된 문장과 템플릿 안내를 고쳤습니다. PROJECT §6은 남은 목표 구조가 없다고 적고 다른 절과 겹치던 설명을 뺐으며, root에서는 실제 항목인 `D-001`·`T-001`을 자리 표시라고 한 문장을 지웠습니다. TODO의 머리말·Integration target·Backlog 안내를 현재 운영에 맞추고 두 문서의 `Last reviewed`를 갱신했습니다. root 문서만 바뀌어 release가 필요 없습니다. 통합: 이 변경의 PR.
- [x] **T-051 `v3.0.0` release** — 준비는 PR #74로 통합됐습니다. 2026-10-12(KST) 사용자가 exact source `2c27a4d`에 annotated tag와 draft를 만들어 immutable Latest로 공개했고, candidate 검증과 Linux·native Windows(Buildkite `windows-ci`)의 published(`--base-version 2.5.0`) 검증이 통과했습니다. root README 명령·Prerequisites와 공개 기록은 이 변경의 PR에서 고쳤습니다. 상세는 [완료 작업 보관](./TODO_ARCHIVE.md)에 있습니다.
- [x] **T-053 자기 점검 규칙 payload 반영** — T-047 평가 뒤 사용자 결정(2026-10-09)으로 root `AGENTS.md` Communication의 자기 점검 규칙과 같은 뜻의 한 줄을 en·ko payload `AGENTS.md` Communication에 넣었습니다. ko는 root와 같은 문장이고 en은 번역입니다. 공개는 T-051(`v3.0.0`)입니다. 통합: PR #73.
- [x] **T-047 자기 점검 규칙 root 시범** — 평가 완료(4 PR, 사용자 결정으로 단축). 시범 PR #69~#72에서 작성자가 고친 것은 2·1·3·0건이었습니다. 2026-10-09 사용자가 다섯 번째 PR 없이 평가를 마치고 규칙을 payload에 넣기로 정해 T-053으로 반영했습니다. 상세는 [완료 작업 보관](./TODO_ARCHIVE.md)에 있습니다. 통합: PR #73.
- [x] **T-050 installer 기본값과 Python 하한** — source `scripts/installer.py`의 `--release-url` 기본값을 `DEFAULT_RELEASE_URL`(공식 release root)로 두고, 모든 OS에서 Python 3.12 미만이면 release·대상 접근 전에 멈춥니다(D-018). en·ko 적용 가이드 §2의 Python 하한·기본 URL 문장과 installer 명령, manifest `required_commands`, root `AGENTS.md` Commands에서 `--release-url`을 뺐고 PROJECT External Boundaries를 고쳤습니다. 회귀 테스트는 `tests/test_install_release.py`에 있고 red-green 결과는 PR 본문에 있습니다. 공개는 T-051(`v3.0.0`)이며 root README 명령은 공개 뒤 기록 PR에서 바꿉니다. 설계: [installer·검사 설계](./changes/2026-10-08-installer-defaults-and-maintainer-checks/01-CHANGE.md) R-001~R-003. 통합: PR #72.
- [x] **T-052 Completed 안내문을 D-013에 맞춤** — root·en·ko `docs/02-TODO.md`의 Completed 안내문에 운영 규칙이 허용하는 결합 서술을 통합 전에 적을 수 있다는 예외를 넣었습니다. PR #69 리뷰의 무효 finding(C69-B-001)이 근거로 든 문장입니다. payload 변경은 T-051(`v3.0.0`)로 공개합니다. 통합: PR #72.
- [x] **T-049 maintainer 정합 검사** — root `scripts/check-docs.py`의 무인자 실행이 root `REVIEW.md`·`REVIEW_ROUND.md`·`.cursor/BUGBOT.md`를 ko heading으로 찾은 프로젝트 소유 절 밖에서 ko 원본과 대조하고, root README locale 표의 tag가 manifest의 `complete` locale이며 상태가 `complete`인지 확인합니다(D-019). `check_locales.read_validated_manifest()`를 추가해 `check_locales()`와 함께 씁니다. 회귀 테스트는 `tests/test_check_docs.py`에 있고 red-green 결과는 PR 본문에 있습니다. root `TEMPLATE_GUIDE.md` §3·§5, `DOCS_GUIDE.md` 점검 목록, PROJECT 기능 표를 고쳤습니다. 통합: PR #71.
- [x] **T-048 root README 설치 절 정리** — 2026-10-08 사용자 요청으로 root `README.md`·`README.ko.md`를 더 형식적이고 짧게 고쳤습니다. 설치 절은 사전 요구사항, 다운로드, 선택 확인(지원 locale 표, `list-locales`, attestation), 적용(선택 A `adopt`, B `install`, C `export`) 순서이고, installer 명령의 Windows 블록은 `python`·Windows 경로 안내 한 줄로 합쳤습니다. root README는 artifact가 아니어서 release가 필요 없습니다. 통합: PR #69.
- [x] **T-040 문서·주석 필터 root 시범** — 2026-10-08 평가: 시범 PR 5개(#64~#68)에서 채택은 대부분 문장 다듬기였고, 정확도를 높인 것은 D1 한 건과 규칙 밖의 사실·일관성 확인이었습니다. 사용자 결정으로 문체 필터를 중단하고 `docs/DOC_FILTER.md`를 지웠습니다. 대신 root `AGENTS.md` Communication에 바뀐 줄을 다시 읽어 수치·상태·위치·참조와 문체를 점검하는 규칙 한 줄을 넣었습니다. payload는 바꾸지 않고, 규칙은 root에서 T-047로 더 시범합니다. 상세는 [완료 작업 보관](./TODO_ARCHIVE.md)에 있습니다. 통합: PR #68.
- [x] **T-042 Origin 원격 branch 정리** — 2026-10-08 사용자 승인으로, `main`을 뺀 Origin 원격 branch 66개(`claude/*`·`codex/*`·`cursor/*`)를 지웠습니다. 삭제 직전에 모든 head가 `origin/main`의 조상인지 다시 확인했고, 삭제 뒤 `git ls-remote origin`에는 `refs/heads/main`만 남았습니다. 열린 PR은 없었습니다. PR 없는 원격 작업이라 이 기록은 다음 PR(이 변경)에 담았습니다.
- [x] **T-041 native Windows published 검증** — `v2.5.0`을 사용자가 Windows 10에서 직접 검증했고(PR #66 기록), Buildkite `windows-ci`의 수동 published 검증 step(PR #66)이 실환경에서 통과했습니다. Build #112(`main` `e105412`, `v2.5.0` 변수)는 Origin check에서 success로 조회됩니다. 상세는 [완료 작업 보관](./TODO_ARCHIVE.md)과 [CI.md](./CI.md) §6에 있습니다.
- [x] **T-035 release 신뢰 루트 검토** — 2026-10-08 검토: 재검토 조건(게시 권한 구조 변경, 외부 배포 요구, 표준 라이브러리만으로 검증할 경로)은 모두 충족되지 않았습니다. `v2.0.0`~`v2.5.0`의 모든 release에 GitHub release attestation이 있어 `gh release verify`로 검증했습니다. 이 서명은 GitHub가 공개 시점에 기록한 digest를 증명할 뿐 게시 계정 탈취는 막지 못합니다. 사용자 선택에 따라 root README(영·한)에 `gh release verify-asset` 선택 검증 안내와 그 한계를 추가했습니다. maintainer 독립 서명은 게시 권한 구조가 바뀌거나 외부 배포 요구가 생기면 새 항목으로 제안합니다. 통합: PR #63.
- [x] **T-039 `v2.5.0` locale release** — 준비는 PR #61로 통합됐습니다. 2026-10-07 사용자가 exact source `6d04b97`에 annotated tag와 draft를 만들어 immutable Latest로 공개했고, candidate와 published(`--base-version 2.4.0`) 검증이 통과했습니다. 상세는 [완료 작업 보관](./TODO_ARCHIVE.md)에 있습니다.
- [x] **T-036·T-037·T-038 보고·검증 규범 구현** — D-015~D-017을 en·ko locale과 root 사본의 `AGENTS.md`(보고 형식, 기본값 명시, 지시의 출처, 완료 근거, red-green), `docs/REVIEW.md` §5, `docs/REVIEW_ROUND.md` §1·§4~§7(위임 경계, 원본 재조회, 원장 `확인` 열), `.cursor/BUGBOT.md`에 반영했습니다. PR #59의 인계 C59-B-001(Codex, P3)도 [완료 작업 보관](./TODO_ARCHIVE.md)에서 해소했습니다. 통합: PR #60. R-002의 요청 안내는 T-039 준비에서 보완했습니다(C60-B-001). 공개는 T-039입니다.
- [x] **T-036·T-037·T-038 보고·검증 규범 설계** — Accepted D-015~D-017([설계](./changes/2026-10-07-agent-reporting-and-verification/01-CHANGE.md)). 통합: PR #59. 공개는 T-039입니다.
- [x] **T-034 `v2.4.0` locale release** — 준비는 PR #58로 통합됐습니다. 2026-10-07 사용자가 exact source `4fe3f76`에 annotated tag와 draft를 만들어 immutable Latest로 공개했고, candidate와 published(`--base-version 2.3.3`) 검증이 통과했습니다. 상세는 [완료 작업 보관](./TODO_ARCHIVE.md)에 있습니다.
- [x] **T-033 TODO 완료 이력 보관** — Completed 상세와 통합된 Backlog 행을 [완료 작업 보관](./TODO_ARCHIVE.md)으로 옮기고 이 문서에는 한 줄 목록만 남겼습니다. PR #56의 인계 C56-005(P3: sticky 게시물의 짧은 인용이 head를 버림)를 en·ko·root `REVIEW.md` §7과 설계 R-006에서 해소했습니다. 통합 근거: 이 변경의 PR(D-013 결합 서술).
- [x] **T-030·T-014 기록 시점·리뷰 finding ID 계약 구현** — 통합: PR #56(D-013·D-014). 공개는 T-034.
- [x] **T-030·T-014 기록 시점·리뷰 finding ID 계약 설계**
- [x] **T-032 원격 운영: GitHub `main` 보호·동기화 절차·tag 정책**
- [x] **T-031 CI 검색 도구 gate**
- [x] **T-029 root 검색식 gate 보강 (C50-002·C51-001·C51-002)**
- [x] **T-013 D-009 운영 계약 회귀 방지**
- [x] **T-021 install preflight 순서 설계**
- [x] **T-022 install 대상 불변조건 등록**
- [x] **T-026 문서 상태 중복 정리**
- [x] **T-028 `v2.3.3` 공개와 published 검증**
- [x] **T-027 `v2.3.3` draft candidate 검증과 기록**
- [x] **T-025 `v2.3.3` release 후보 준비**
- [x] **T-024 installer stdout 인코딩 후속**
- [x] **T-020 install onboarding 진단·안내 평가**
- [x] **T-023 release 후보의 verifier·installer 계약 회귀**
- [x] **T-017 Windows junction 경계 검증**
- [x] **T-019 `v2.3.2` 공개 기록과 지원 검증**
- [x] **T-001 다국어 템플릿 source와 선택형 배포 도입**
- [x] **T-002 GitHub Releases 기반 v2.0.0 공개**
- [x] **T-003 프로젝트 전체 분석 skill 이관**
- [x] **T-004 기존 저장소 adoption 계약**
- [x] **T-005 artifact `check-docs.py` 강화 반영**
- [x] **T-006 consumer PR #28 마무리 (외부 저장소 `jaff2836/claude-review-e2e`)**
- [x] **T-007 이미 적용한 저장소의 업그레이드를 위한 `adopt` 분류 개선**
- [x] **T-008 release 검증 절차 스크립트화**
- [x] **T-009 checker·installer 확정 결함 수정**
- [x] **T-010 문서 소유권·skill Metadata·changelog 안내 정리**
- [x] **DFR-001 `v2.2.0` 준비 재검토**
- [x] **T-011 release verifier adoption plan 진단 강화**
- [x] **T-012 release verifier의 remote `main` 객체·history 진단**
- [x] **T-015 Windows release 도구 호환성 수정**
- [x] **T-016 새 프로젝트 `install` 대상 계약 정합화**
- [x] **T-018 `v2.3.2` release 준비**

완료 이력이 길어지면 기존 CHANGELOG 또는 마일스톤별 보관 문서로 연결하고 본문을 복제하지 않습니다.
