# 프로젝트 작업 목록

> 프로젝트 전체의 변경·마일스톤·우선순위·의존성을 관리합니다. 제품 기준과 결정은 [00-PROJECT.md](./00-PROJECT.md), 상세 상태의 소유권은 [DOCS_GUIDE.md](./DOCS_GUIDE.md)를 따릅니다.
>
> 이 branch에서는 템플릿 저장소 자체의 다국어 변경을 추적합니다. 기존 사용자용 한국어 TODO 양식은 구현 시 `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`에서 `locales/ko/docs/02-TODO.md`로 이관하며, 이 maintainer 작업은 locale artifact에 포함하지 않습니다.

## Metadata

- **Status:** Active
- **Owner:** Chae Sangwon
- **Last reviewed:** 2026-09-28 (KST)
- **Review cadence:** 작업 범위·우선순위·의존성·통합 결과 변경 시
- **Integration target:** local `main`; 공개 저장소 target `jaff2836/coding-agent-docs-template`; v1.7.1 payload 기준 `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`

## Current Milestone

- **Name:** T-021 install preflight 순서 설계
- **Goal:** 대상 진단·다운로드와 release 오류 우선순위를 비교해 기존 순서 유지 또는 변경을 합의함
- **Target:** `codex/t021-install-preflight-order-design` (Origin·GitHub `main` `4c743f1` 기준)
- **Status:** In Progress — T-022와 C46-001은 PR #46으로 통합됐습니다. 이 브랜치는 사용자 선택 전 Draft 설계이며 상세 실행·검증·통합 조건은 아래 T-021이 소유합니다.
- **다음 마일스톤:** A를 확정하면 T-013 운영 계약 설계가 다음 후보이며, B를 확정하면 preflight 구현을 먼저 별도 PR로 진행합니다.

## 운영 규칙

- 변경별 PLAN이 있으면 이 문서는 링크·우선순위·선행조건과 통합 여부만 관리합니다. 상세 체크박스·검증 로그를 복제하지 않습니다.
- PLAN이 없는 작은 작업은 아래 항목 안에서 범위·구현 순서·완료 조건·검증을 관리합니다.
- `In Progress`는 프로젝트가 선택한 진행 작업입니다. 다른 브랜치나 열린 PR의 실시간 상태를 보장하지 않습니다. 작업 시작 시 실제 Git·PR 상태와 해당 변경의 PLAN을 확인합니다.
- 각 브랜치는 자기 변경의 상세 기록을 갱신합니다. 다른 브랜치 작업을 오래된 사본만 보고 완료·미완료로 되돌리지 않습니다.
- 공통 항목은 범위·의존성·통합 결과가 달라질 때만 수정합니다. 충돌은 최신 기준과 변경-ID를 대조해 해결하고, 영향받은 계약·검증 전제를 재확인합니다.
- `Completed`는 필요한 검증과 지정한 대상에의 반영을 확인한 항목만 담습니다. 브랜치 구현 완료·리뷰 통과·병합·릴리스·지원 검증을 구분하고 해당 작업의 완료 조건으로 판단합니다.
- `T-nnn`은 이 문서의 전역 작업 ID입니다. 변경-ID·PROJECT의 `D-nnn`·변경 폴더의 `R-nnn`/`W-nnn`과 범위가 다릅니다. 발급·충돌 처리는 [DOCS_GUIDE.md](./DOCS_GUIDE.md)의 식별자 범위를 따릅니다. 아래 `T-001` 등은 자리 표시입니다.
- 취소한 변경은 Cancelled에 두고 변경 폴더는 유지합니다. 완료된 SPEC을 현재 제품 기준으로 읽지 않으며, 구현된 계약은 통합 후 PROJECT에 반영합니다.
- 원격 저장소나 PR은 필수가 아닙니다. 로컬 작업은 기준 revision과 대상 브랜치 또는 검토한 작업 트리 범위로 근거를 남깁니다. 미커밋 결과를 commit SHA로 재현된다고 표현하지 않습니다.
- 문서 갱신은 commit·push·merge 권한이 아닙니다. 리뷰 라운드 통과 후 반영은 [REVIEW_ROUND.md](./REVIEW_ROUND.md) §9를 따릅니다.

## In Progress

- [ ] **T-021 install preflight 순서 설계**
  - 정본·범위: [2026-09-28-install-preflight-order](./changes/2026-09-28-install-preflight-order/01-CHANGE.md)가 Intent·대안·요구·호환성·완료 조건을 소유합니다. 상세 실행 상태는 이 항목에서 관리합니다. 현재 선택은 미합의이며 D-010은 Accepted 기준으로 유지합니다.
  - [x] PR #46 version 2 head `e113dd1` / base `9a7764b`의 세 재리뷰와 CI를 확인하고 T-022·C46-001의 실제 통합 결과를 아래 완료 항목에 반영했습니다.
  - [x] 기준 `4c743f149d726c692684f8f626e31fd74db34a73`에서 installer 호출자와 기존 계약을 대조하고, Linux의 기존 합성 release fixture 6개로 오류 우선순위·대상 검사·tree 보존·새/빈 대상 성공을 관찰했습니다. B안은 구현·실측 전입니다.
  - [x] A 현재 순서 유지와 B 대상 검사 선행·쓰기 전 재검사를 비교한 Draft를 준비했습니다. 순서 변경 시 REVIEW §6·BUGBOT의 두 불변조건을 같은 구현 PR에서 갱신한다는 PR #46 인계를 Spec R-005에 반영했습니다.
  - [x] 로컬 root docs·stable locale·docs 회귀 55건·diff 검사가 통과했습니다. 새 설계의 링크·절 참조와 기존 두 불변조건 5개 항목 동등성을 확인했습니다.
  - [ ] 수동 설계 리뷰와 정확한 head의 필수 Windows/Linux CI를 확인합니다.
  - [ ] 사용자 선택을 확인하고 승인 범위를 설계 Metadata와 PROJECT §8에 기록합니다. 승인 전에는 순서·런타임·현재 불변조건을 변경하지 않습니다.
  - [ ] 설계 PR을 Origin·GitHub `main`에 통합합니다. A를 확정하면 구현 없이 종료하고, B를 확정하면 정본의 R-001~R-006에 따른 구현을 별도 PR로 진행합니다.

## Next

T-021에서 A를 확정하면 다음 권고 작업은 Backlog의 T-013 운영 계약 회귀 방지 설계입니다. B를 확정하면 승인된 순서 변경을 먼저 별도 구현 PR로 진행합니다. 선택 전에는 두 경로를 통합 완료로 표시하지 않습니다.

## Blocked

없음.

## Backlog

아래 순서는 위험과 선행조건을 고려한 권고 PR 순서이며, Backlog 항목을 시작하는 권한은 아닙니다.
설계 결과에 따라 필요한 구현은 해당 설계 PR과 분리합니다. `v2.3.3`의 candidate 검증과 공개·published 검증은 D-007 경계에 따라 단계와 기록 PR을 분리합니다.

| 순서 | PR 단위 | 작업 | 선행조건·통합 경계 |
| --- | --- | --- | --- |
| 1 | `codex/t017-windows-junction-design` | T-017: native Windows에서 junction을 재현·설계 | **Integrated** — Origin PR #37 merge `9d53913`과 GitHub `main` fast-forward를 확인했습니다. Windows·Linux 전체 gate와 native 재현을 통과했고, 경계 범위는 D-011로 확정했습니다. |
| 2 | `codex/t017-junction-boundary-implementation` | T-017: 승인된 경계와 native 회귀를 구현 | **Integrated** — Origin PR #38 merge `b5a9c4e`와 GitHub `main` fast-forward를 확인했습니다. 정확한 head의 Windows #27·Linux #12 CI가 통과했습니다. |
| 3 | `codex/t023-release-verifier-contract-regression` | T-023: 실제 installer와 verifier의 설치 거부 계약을 release 전 회귀로 연결 | **Integrated** — Origin PR #39 merge `b40630a`와 GitHub `main` fast-forward를 확인했습니다. Windows #30·Linux #15 CI가 통과했습니다. |
| 4 | `codex/t020-install-onboarding-guidance` | T-020: C34-001과 parent-directory 안내 권고를 진단·문서·회귀로 평가 | **Integrated** — Origin PR #40 merge `f236bf2`와 GitHub `main` 반영 확인; `v2.3.3` asset에 포함 |
| 5 | `codex/t024-installer-stdout-encoding` | T-024: 비-UTF-8 stdout에서 설치 후 거짓 실패 방지 | **Integrated** — Origin PR #41 merge `2901f1a`와 GitHub `main` fast-forward 확인; `v2.3.3` asset에 포함 |
| 6 | `codex/v233-release-prep` | T-025: `v2.3.3` version·이력·package 후보 준비 | **Integrated** — Origin PR #42 merge `989698d`와 GitHub `main` fast-forward 확인 |
| 7 | `codex/v233-candidate-record` | T-027: tag·draft candidate 검증과 인계 기록 | **Integrated** — Origin PR #43 merge `da4d6ae`와 GitHub `main` fast-forward 확인 |
| 8 | `codex/v233-publication-record` | T-028: `v2.3.3` 공개·published 검증 | **Integrated** — Origin PR #44 merge `b423c12`와 GitHub `main` fast-forward 확인; immutable Latest·Linux published 통과 |
| 9 | `codex/t026-document-status-ownership` | T-026: PROJECT §11·설계 Status 중복 정리 | **Integrated** — Origin PR #45 merge `9a7764b`와 GitHub `main` fast-forward 확인; C44-001 해소 |
| 10 | `codex/t022-install-target-invariant` | T-022: 승인된 install 대상 계약을 REVIEW/BUGBOT 불변조건으로 등록 | **Integrated** — Origin PR #46 merge `4c743f1`와 GitHub `main` fast-forward 확인; C46-001 해소 |
| 11 | `codex/t021-install-preflight-order-design` | T-021: preflight 순서 유지·변경을 비교·합의 | **In Progress** — Draft 설계·A 권고; 사용자 선택·리뷰·통합 전. B는 승인 뒤 별도 구현 PR |
| 12 | `codex/t013-operation-contract-design` | T-013: source/artifact checker·LF·placeholder 회귀 방지 범위를 설계 | 승인 뒤 checker·문서 변경을 작은 후속 PR로 분리 |
| 13 | `codex/t014-review-id-policy` | T-014: reviewer-qualified ID와 canonical ID 정책을 합의·반영 | REVIEW/REVIEW_ROUND 영향 검토 후 단일 정책 PR |

- [ ] **T-013 D-009 운영 계약 회귀 방지** — `project-analysis`에 한정한 source root↔`locales/ko` 사본 동등성 검사, source/artifact checker CLI 경계와 source changelog의 공개 전 heading 예외, root `.gitattributes`가 maintainer checkout의 LF를 고정하는 목적, locale별 placeholder 검색 어휘의 단일 출처·검증 방식을 함께 설계합니다. `design`·`review-round` skill 사본은 같은 동등성 계약으로 일반화하지 않습니다.
- [ ] **T-014 병렬 리뷰 finding ID 충돌 방지 방식 검토** — reviewer-qualified ID와 종합 단계 canonical ID 부여를 우선 검토하고, 반복 근거와 사용자 승인 없이 `REVIEW.md`·`REVIEW_ROUND.md` 계약을 바꾸지 않습니다.
- [ ] `en`·`ko` 외 community locale — v2의 locale 추가 계약과 두 공식 locale 지원 검증 후 재검토

## Cancelled

취소한 변경만 둡니다. 변경-ID, 취소 이유, Intent/Spec의 `Rejected` 근거, 유지 중인 변경 폴더 경로를 남깁니다. 완료·진행 항목과 섞지 않으며 폴더는 삭제하지 않습니다.

## Completed

실제 완료 항목만 추가합니다. 변경-ID, 통합 대상, 확인한 revision 또는 작업 트리 범위, 검증 근거의 위치를 남깁니다. 변경 폴더는 유지하고, 구현된 계약이 현재 지원 범위가 되면 PROJECT를 갱신합니다. PR이 있으면 실제 병합 결과를 확인하며, 로컬 작업에 가상의 PR·merge SHA를 만들지 않습니다.

- [x] **T-022 install 대상 불변조건 등록**
  - 출처·범위: 기존 T-022와 2026-09-28 사용자의 리뷰 후 다음 작업 진행 요청에 따라 승인된 D-010을 maintainer 리뷰 불변조건으로 등록합니다. 상위 계약은 [install 대상 설계](./changes/2026-09-22-install-target-contract/01-CHANGE.md) R-001·R-002·§2.3이며 D-011의 기존 symlink·junction 경계도 유지합니다.
  - 평가·선택: REVIEW의 일반 정확성·문서 계약 검사만으로 둘 수도 있지만, BUGBOT은 자신의 단일 파일에서 판단하므로 install 대상 보호를 두 불변조건 목록에 명시하는 안을 채택합니다. 기존 파일과 겹치지 않아도 비어 있지 않으면 거부하고, emptiness를 확인할 수 없으면 fail-closed합니다. 대상 검사 거부 시 tree를 보존하며, 빈 대상·읽기 전용 `adopt` 안내는 비어 있음 검사에서 거부한 경우로 한정합니다.
  - 설계 범위: 이미 승인·구현된 계약의 문서 등록이므로 DESIGN §1의 작은 문서 변경 예외를 적용하고 새 제품 결정·설계를 만들지 않습니다. 대상 preflight의 release·archive 검증 뒤 순서와 오류 우선순위는 D-010 그대로이며, 순서 재설계는 별도 T-021입니다.
  - 변경·검사: `docs/REVIEW.md` §6과 `.cursor/BUGBOT.md`의 `Install 대상 보존` 항목을 같은 문장으로 추가합니다. 기존 checker는 example을 제외한 전체 bullet 목록의 동등성을 검사하므로 코드·규칙 변경 없이 두 목록을 비교합니다. locale payload와 공개 asset은 이 maintainer 정책 변경에 포함되지 않습니다.
  - 최초 등록 검증: PR #46 version 1 head `dc571d9677de44bc72635a8eec7e2a4b6fa08bc4`에서 전체 unittest 184건(Linux의 Windows 전용 2건 skip), root docs의 두 목록 5개 항목 동등성, stable locale·diff 검사가 통과했습니다. 새·빈 대상 성공, 비어 있지 않은 대상과 `.git` 대상 거부·tree 보존, unreadable·uninspectable 대상 fail-closed 회귀를 포함합니다. 정책 문장과 `install` → `_resolve_target_root`·`_require_empty_install_target` → `_write_members`의 실제 순서를 대조했습니다. exact head의 Windows #48·Linux #33 CI도 통과했습니다.
  - C46-001 판정·수정: PR #46 version 1 head `dc571d9` / base `9a7764b`의 자동 리뷰와 Luna가 P3·confidence 0.90·blocking=true로 보고한 안내 범위 모호성을 수용했습니다. `_resolve_target_root`·`_link_kind`의 root·부모·검사 실패 메시지에는 `adopt` 안내가 없으므로, 두 불변조건에서 tree 보존은 대상 검사 거부에 적용하고 안내는 `_require_empty_install_target`의 비어 있음 검사 거부로 한정합니다. version 1은 기본 통과 기준을 충족했지만 같은 PR에서 문구를 수정했고, version 2의 세 재리뷰가 해소와 새 finding 없음을 확인했습니다.
  - 후속 문구 검증: root docs의 두 목록 5개 항목 일치, stable locale·docs 회귀 55건·diff 검사가 통과했습니다. installer 코드·locale payload는 수정하지 않았으며, version 2 exact head의 필수 CI와 두 독립 리뷰에서 전체 unittest 184건을 확인했습니다(Linux의 Windows 전용 2건 skip).
  - PR #45 인계: version 1 head `3281f0b` / base `b423c12`의 세 리뷰가 C44-001 해소와 새 finding 없음을 확인했습니다. T-026의 실제 Origin·GitHub 통합 완료는 아래 완료 항목에 반영합니다. 다음 release 기록에서는 PROJECT Metadata Status와 Current State의 공개 기준을 함께 확인하라는 권고를 유지합니다.
  - 통합 결과: PR #46 version 2 head `e113dd159a986633a87544866b164bbec6b2e7e5`을 Origin merge `4c743f149d726c692684f8f626e31fd74db34a73`에 통합하고 GitHub `main`에도 non-force fast-forward했습니다. exact head의 Windows #49·Linux #34 CI가 통과했습니다. C46-001은 해소됐으며 순서 변경 시 두 불변조건을 함께 갱신한다는 인계는 T-021 설계 범위에 연결합니다.

- [x] **T-026 문서 상태 중복 정리**
  - 출처·범위: PR #41 version 1 head `d86bee8`의 C41-001에서 파생한 기존 T-026과 PR #44 version 1 head `2165887a43aef91455cf7f493edc7d43282c41d3` / base `da4d6aef4b817e396cf1400e912b233a66b58601`의 C44-001을 함께 처리합니다. PROJECT §11과 T-017 설계 Metadata를 기존 [DOCS_GUIDE §2·§4](./DOCS_GUIDE.md)에 맞추는 maintainer 문서 변경입니다.
  - C44-001 판정·이관: T-017 설계 Status의 `다음 release 반영 전`은 공개 후 잘못된 현재 상태입니다. 세 리뷰가 같은 P3를 확인했고 confidence는 0.90~0.95, blocking 판정은 서로 달랐습니다. P0·P1·Blocking P2가 없어 PR #44를 통과시켰으며 T-026에서 해소했습니다. 영구 review deferral은 추가하지 않았습니다.
  - PR #45 정리 결과: 당시 PROJECT §11을 T-021·T-022·T-013·T-014의 미해결 판단과 TODO 링크로 줄였습니다. 완료·통합·CI 상세를 반복하는 방식은 상태 변경 시 동기화 지점을 늘리므로 채택하지 않았으며, 이미 지정된 실행·공개 기록과 확정된 제품 결정은 각 정본에서 보존했습니다.
  - 설계 Metadata: T-017 Status를 승인 상태 `Accepted`만 표시하도록 바꿉니다. D-011의 요구·승인·결정과 날짜별 변경 기록은 유지합니다. 공개 상태는 PROJECT의 현재 기준·CHANGELOG·T-028 기록에서 확인하며, Metadata를 release마다 고치는 사본으로 쓰지 않습니다.
  - 근거 보존: §11의 제품 결정은 PROJECT §1·§5·§8에, PR #37 final head `cc67e31`과 native CI 근거는 T-017 변경 기록·CI 문서에, T-020·T-023 등의 실제 통합은 해당 TODO 완료 항목에 이미 있습니다. 중복 문장을 제거해도 이 근거와 연결은 유지합니다.
  - 통합 결과: PR #45 version 1 head `3281f0b75b30138747e7d350704bf988b61fe056`을 Origin merge `9a7764bca550f828edad757b45150f735cb3d3f7`에 통합하고 GitHub `main`에도 non-force fast-forward했습니다. 세 리뷰 모두 새 finding이 없고 C44-001 해소를 확인했습니다. exact head의 Windows #46·Linux #31 CI가 통과했으며 root docs·stable locale·docs 회귀 55건·diff 검사도 통과했습니다. 전체 unittest 184건은 CI와 두 독립 리뷰에서 확인했습니다(Linux의 Windows 전용 2건 skip).

- [x] **T-028 `v2.3.3` 공개와 published 검증**
  - 범위·위임: 2026-09-28 사용자가 `v2.3.3` 공개부터 다음 기록 PR 게시까지 명시적으로 위임했습니다. D-007의 수동 게시 단계로 기존 draft를 공개하고, tag source의 읽기 전용 verifier로 published gate를 실행했습니다.
  - 공개 결과: [immutable Latest `v2.3.3`](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.3.3)을 2026-09-28 03:01:47 UTC(12:01:47 KST)에 공개했습니다. `isDraft=false`, `isImmutable=true`, `isPrerelease=false`이며 GitHub Latest identity도 일치합니다. 기존 draft asset 5개의 ID·SHA-256은 게시 전후 동일합니다.
  - source·ref: annotated tag의 exact source는 `989698d4070d7a9596117cf410362fea0b7f28bb`입니다. 공개·published 실행 시 Origin·GitHub `main`은 `da4d6aef4b817e396cf1400e912b233a66b58601`로 같았고 source는 그 조상이었습니다. 기록 PR의 source와 release의 source를 구분합니다.
  - published 검증: clean exact tag source에서 `python3 scripts/verify-release.py published --version 2.3.3 --source-commit 989698d4070d7a9596117cf410362fea0b7f28bb --repository jaff2836/coding-agent-docs-template --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --base-version 2.3.2`가 exit 0으로 통과했습니다. Linux에서 tag source 자신의 verifier로 5개 asset byte·immutable Latest, latest·exact의 en·ko list/install/export/adopt, source export와의 동등성, `v2.3.2` base-aware upgrade 및 비어 있지 않은 install 대상의 거부·tree 불변을 확인했습니다.
  - 검증 범위: 이번 원격 published E2E는 Linux에서 실행했습니다. Windows는 tag source와 같은 tree의 PR #42 head에서 Windows #40 CI·native junction 회귀가 통과한 근거를 유지하며, native Windows published E2E를 실행했다고 표시하지 않습니다.
  - PR #43 version 1 인계: head `cb4bd84`의 세 리뷰 모두 새 finding이 없었고 Windows #42·Linux #27 CI가 통과했습니다. PROJECT Status·현재 공개 기준·D-011 공개 범위·§11과 en·ko README·changelog를 갱신합니다. 선택 제안인 draft target 변경은 기존 annotated tag와 exact-source 검증으로 게시 대상을 확인할 수 있어 현 상태를 유지했습니다.
  - 통합 결과: PR #44 head `2165887a43aef91455cf7f493edc7d43282c41d3`을 Origin merge `b423c12db3a4d0771272736a81b5e67789a38293`에 통합하고 GitHub `main`에도 non-force fast-forward했습니다. exact head의 Windows #44·Linux #29 CI가 통과했습니다. 리뷰의 유일한 P3 C44-001은 T-026에서 해소하며 공개·published 성공 근거는 유지합니다.

- [x] **T-027 `v2.3.3` draft candidate 검증과 기록**
  - 범위·위임: 2026-09-28 사용자 대화의 다음 작업 진행 요청에 따라 D-007의 수동 release 준비 단계로 annotated tag·draft asset을 준비하고 candidate gate를 실행했습니다. PR #43은 source changelog·TODO만 변경했고, 공개와 published 검증은 T-028이 소유합니다.
  - 확인한 source·ref: exact clean source `989698d4070d7a9596117cf410362fea0b7f28bb`에 local·GitHub annotated `v2.3.3` tag를 결합했습니다. candidate 실행 시 Origin·GitHub `main`도 같은 commit이었습니다. source tree는 리뷰를 통과한 PR #42 head `cdbe374465f6b676416a4ce73d29631b11ebcaf1`과 같습니다.
  - candidate 검증: `python3 scripts/verify-release.py candidate --version 2.3.3 --source-commit 989698d4070d7a9596117cf410362fea0b7f28bb --repository jaff2836/coding-agent-docs-template`가 exit 0으로 통과했습니다. 전체 unittest·root docs·stable locale·diff 검사, 반복 package byte 동등성, 두 remote·annotated tag와 [당시 GitHub draft](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.3.3)의 5개 asset 동등성을 확인했습니다. candidate 당시 draft는 `isDraft=true`, `isImmutable=false`, `isPrerelease=false`, `publishedAt=null`입니다.
  - version 선택 근거: PR #42가 준비한 `v2.3.3` patch를 유지합니다. 명령 집합·manifest schema 2·locale artifact inventory는 유지하고, D-011 경계 강제와 출력 실패·안내·검증 회귀를 묶습니다. Windows Python 3.12 미만의 실행 중단은 호환성 변화이므로 changelog와 draft notes에 명시합니다. patch 선택을 모든 기존 환경의 호환성 보장으로 해석하지 않습니다.
  - PR #42 version 2 인계: C42-001·C42-002는 해소됐고 새 finding은 없습니다. 별도 비차단 권고였던 version 선택 근거는 이 항목에, Python 업그레이드 우선 안내와 구버전 대안의 수정 누락은 en·ko source changelog 및 draft notes에 반영했습니다. T-026은 release 완료 후의 다음 문서 정리 후보로 우선순위를 올립니다.
  - 통합 결과: PR #43 head `cb4bd842d52f1f62b065793e2d85c2df7ad01020`을 Origin merge `da4d6aef4b817e396cf1400e912b233a66b58601`에 통합하고 GitHub `main`에도 non-force fast-forward했습니다. 세 리뷰에서 새 finding이 없었고 exact head의 Windows #42·Linux #27 CI가 통과했습니다. 공개·published 검증은 T-028이 소유합니다.

- [x] **T-025 `v2.3.3` release 후보 준비**
  - 통합 결과: en·ko artifact version·release history와 source changelog를 정렬한 PR #42 head `cdbe374465f6b676416a4ce73d29631b11ebcaf1`을 Origin merge `989698d4070d7a9596117cf410362fea0b7f28bb`에 통합하고 GitHub `main`에도 non-force fast-forward했습니다. tag·draft candidate 검증은 후속 T-027, 공개·published 검증은 T-028이 소유합니다.
  - 검증 근거: exact PR head의 Buildkite Windows #40·Linux #25가 통과했고, root docs·stable locale·docs test 55건·en/ko export와 artifact docs 검사를 확인했습니다. 같은 source의 package 2회가 5개 asset 모두 byte-identical했고, version 2 리뷰에서 C42-001·C42-002 해소와 새 finding 없음이 확인됐습니다.

- [x] **T-024 installer stdout 인코딩 후속**
  - 통합 결과: 비-UTF-8 stdout에서 `install`·`export`·`adopt` 완료 메시지가 `UnicodeEncodeError`로 거짓 실패를 일으키지 않도록 한 PR #41 head `e06e823dd5d7401c9c6a6853096a788d24afb184`을 Origin merge `2901f1a545d40a14ea95ed243231acb7f3bfab34`에 통합하고 GitHub `main`에도 non-force fast-forward했습니다. 공개 `v2.3.2` asset은 변경하지 않았습니다.
  - 검증 근거: 정확한 PR head의 Buildkite Windows #37·Linux #22가 통과했고, 전체 unittest 184건(Linux에서 Windows 전용 2건 skip), root docs·stable locale·`git diff --check`가 통과했습니다. PR #41 version 3 재리뷰에서 C41-001·C41-002 해소와 새 finding 없음이 확인됐습니다.

- [x] **T-020 install onboarding 진단·안내 평가**
  - 통합 결과: `.git`만 있는 대상의 거부 안내, 새 프로젝트의 `git init` 순서와 직접 부모 조건을 Origin PR #40 merge `f236bf2278fcde83fe0c08ae1d9aa8e422d09a32`에 통합하고 GitHub `main`에도 반영했습니다. D-010의 새·빈 대상 계약과 공개 `v2.3.2` asset은 변경하지 않았습니다.
  - 검증 근거: PR #40 exact head `cd3608f`의 Buildkite Windows #33·Linux #18이 통과했습니다. 전체 unittest 183건, root docs·stable locale, en·ko export와 artifact docs 검사 결과는 PR #40에 기록됐습니다.

- [x] **T-023 release 후보의 verifier·installer 계약 회귀**
  - 통합 결과: 실제 installer와 verifier의 새·빈 대상 허용, 겹치거나 무관한 파일이 있는 대상 거부·tree 불변을 같은 local fixture로 대조하는 회귀를 Origin PR #39 head `930e393`에서 `b40630a`로 병합하고 GitHub `main`에도 non-force fast-forward했습니다. 공개 `v2.3.2` asset은 변경하지 않았습니다.
  - 검증 근거: PR #39 exact head의 Buildkite Windows #30·Linux #15가 통과했습니다. 두 환경에서 전체 unittest 181개와 실제 installer subprocess 회귀를 실행했고, Windows native junction 테스트와 probe도 통과했습니다. 다음 release candidate는 별도 준비·검증 작업입니다.

- [x] **T-017 Windows junction 경계 검증**
  - 통합 결과: 승인된 [D-011 경계](./changes/2026-09-23-windows-junction-boundary/01-CHANGE.md)를 구현한 Origin PR #38 head `42d9923`을 `b5a9c4e`에 병합하고 GitHub `main`에도 non-force fast-forward로 반영했습니다. 공개 `v2.3.2` asset은 변경하지 않았습니다.
  - 검증 근거: PR #38 exact head의 Buildkite Windows #27·Linux #12가 통과했고, Windows native junction probe와 전체 unittest 180개, root docs·stable locale gate를 확인했습니다. 다음 release 후보의 installer·verifier 계약 회귀는 T-023이 소유합니다.

- [x] **T-019 `v2.3.2` 공개 기록과 지원 검증**
  - 통합 결과: T-018 exact source `4c6a798885404fdf5170769e271f7d06f4959234`의 candidate가 통과한 5개 asset을 교체 없이 [immutable Latest `v2.3.2`](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.3.2)로 공개했습니다. verifier의 새 install 거부 문구 대응과 공개 기록은 Origin PR #36 merge `cc791be2370e76930184e473061312518d5fe221`에 통합하고 GitHub `main`에도 non-force fast-forward로 반영했습니다.
  - 검증 근거: clean exact source를 `--root`로 지정한 보완 verifier의 `published --base-version 2.3.1`이 통과했습니다. Latest·immutable metadata와 게시 전과 같은 5개 asset, latest·exact의 en·ko list/install/export/adopt, base-aware upgrade, artifact와 겹치거나 무관한 파일이 있는 install 대상의 거부·tree 불변을 확인했습니다. 두 remote `main`이 merge commit을 가리킵니다.

- [x] **T-001 다국어 템플릿 source와 선택형 배포 도입**
  - 변경-ID: `2026-09-09-multilingual-template`
  - 통합 결과: W-001~W-006이 PR #3~#8로 `main`에 통합됐고 W-007 exact-head consumer probe와 bilingual release README가 `9cea178`에 반영됐습니다.
  - 검증 근거: [PLAN](./changes/2026-09-09-multilingual-template/03-PLAN.md)의 W-001~W-007과 검증 기록. tag·GitHub release는 T-002가 소유합니다.

- [x] **T-002 GitHub Releases 기반 v2.0.0 공개**
  - 변경-ID: `2026-09-18-github-releases-publication`
  - 통합 결과: `v2.0.0` tag commit `8bc8b1b`에서 생성한 기존 5개 draft asset을 재패키징·교체하지 않고 [immutable GitHub Release](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.0.0)로 공개했습니다. 게시 시 Origin·GitHub `main`은 `5eefc11`로 같았고 tag commit은 그 조상이었습니다.
  - 검증 근거: [PLAN](./changes/2026-09-18-github-releases-publication/03-PLAN.md)의 W-003·W-004 및 검증 기록. latest·exact-version의 en·ko install/export와 충돌 tree 불변 검증이 통과했습니다.

- [x] **T-003 프로젝트 전체 분석 skill 이관**
  - 변경-ID: `2026-09-18-project-analysis-skill`
  - 통합 결과: locale별 self-contained `project-analysis` skill과 README·manifest·checker 계약이 Origin PR #12 merge commit `5eefc11`에 통합됐습니다. 고정된 `v2.0.0` artifact는 변경하지 않았고 이 skill은 다음 release inventory에 포함됩니다.
  - 검증 근거: PR #12 exact-head 리뷰와 `main`의 root docs, stable locale, 전체 unittest 및 en·ko artifact 검사.

- [x] **T-004 기존 저장소 adoption 계약**
  - 변경-ID: `2026-09-18-existing-repository-adoption`
  - 통합 결과: 설계는 PR #14, adoption policy·release manifest schema 2·`adopt`는 PR #15, 기존 저장소 우선 문서는 PR #16, release 준비는 PR #18로 Origin `main`에 통합됐습니다. tag commit `36a123ff3bd939a99148e0f804f9e20924f6be0b`의 immutable GitHub Release `v2.1.0`으로 공개했습니다.
  - 검증 근거: [PLAN](./changes/2026-09-18-existing-repository-adoption/03-PLAN.md) W-004와 검증 기록. 원격 latest·exact의 install·export·adopt가 통과했습니다. `claude-review-e2e` baseline에서 대상 불변, PR #28과 같은 분류, report 반영 후 checker 통과를 확인했고, Claude·Codex·Cursor·OMP 로딩 probe가 통과했습니다.

- [x] **T-005 artifact `check-docs.py` 강화 반영**
  - 변경-ID: 없음 — 외부 계약을 바꾸지 않는 checker 결함 수정 묶음
  - 통합 결과: `claude-review-e2e` PR #28 head `719696f`의 강화분을 `template/common/`에 3-way merge로 반영했습니다. 미해결 P2 8건 중 7건을 수정하고 회귀 테스트 7개를 추가했습니다. Setext heading은 지원 범위 밖으로 명시하고 DFR-001로 기록했습니다. Origin PR #17 merge commit `6e664c374f87d26002124fa155c8345a121ba51f`에 통합됐습니다.
  - 검증 근거: 통합 후 `main`에서 전체 unittest 140개와 root docs·stable locale 검사가 통과했습니다. 공개된 `v2.1.0` ko artifact의 `scripts/check-docs.py`·`tests/test_check_docs.py`는 tag commit의 `template/common/` 파일과 byte-identical이고, 설치 tree에서 checker와 테스트 48개가 통과했습니다.

- [x] **T-006 consumer PR #28 마무리 (외부 저장소 `jaff2836/claude-review-e2e`)**
  - 통합 결과: `v2.1.0` `adopt` report를 반영한 PR #28 exact head `4b3987dad933142a192ebee08aea7c525a7681da`를 GitHub `main` merge commit `26c531beb65eaef8f524a00bcf8f06c52445c3d8`에 통합했습니다. 처리된 7개 review thread를 모두 해소했고 template 저장소로 이관한 P3는 T-009에 반영했습니다.
  - 검증 근거: exact head에서 Claude workflow #8과 jaff2836-pr-reviewer가 approve했고 네 job이 통과했습니다. 통합 `main`에서 checker test 48개, docs checker, Python compile과 `git diff --check`가 통과했으며 기존 `.github/`·`src/`는 PR에서 변경되지 않았습니다. 로컬 `.env`는 존재하지 않았고 통합된 `.gitignore`가 `.env`를 제외합니다.

- [x] **T-007 이미 적용한 저장소의 업그레이드를 위한 `adopt` 분류 개선**
  - 변경-ID: `2026-09-20-adopt-upgrade-classification`
  - 통합·공개 결과: base 전용 schema 1·2 검증, 3-way upgrade 분류, format 2 report와 공개 검증은 Origin PR #24, review 후속은 PR #25, release 준비는 PR #26 merge `70a5a7a9e97fa5a89609a120ad69bced7e8ae1ac`에 통합됐습니다. 같은 exact source를 annotated tag와 [immutable `v2.2.0` release](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.2.0)로 공개했습니다.
  - 검증 근거: [PLAN](./changes/2026-09-20-adopt-upgrade-classification/03-PLAN.md) W-001~W-005. candidate·published gate와 en·ko `v2.1.0` base-aware 원격 E2E가 통과했습니다. `claude-review-e2e@26c531beb65eaef8f524a00bcf8f06c52445c3d8`에서 생성 report와 base·current·target byte를 독립 대조했고 format 1 `missing 0`·`identical 10`·`merge 15`·`decision 4`·`blocked 0`이 format 2 `unchanged 11`·`template-only 2`·`project-only 14`·`converged 0`·`diverged 2`·`blocked 0`으로 분해되며 target tree는 불변임을 확인했습니다.

- [x] **T-008 release 검증 절차 스크립트화**
  - 변경-ID: `2026-09-20-release-verification`
  - 통합·운영 결과: Origin PR #20 merge `40306b65fe211402090d7a11b5c3ffafcb3689eb`의 검증 CLI로 `v2.1.1`부터 `v2.3.3`까지 실제 draft candidate·immutable published 경로를 반복 확인했습니다. 각 release에서 검증한 5개 asset을 게시 전후 교체하지 않았으며 exact source는 [변경 기록](./changes/2026-09-20-release-verification/01-CHANGE.md)에 남겼습니다.
  - 검증 근거: 최신 `v2.3.3` published는 Linux에서 tag source 자신의 verifier로 latest·exact의 en·ko `list-locales`·`install`·`export`·`adopt`, `v2.3.2` base-aware upgrade, source export와 비어 있지 않은 target 불변을 확인했습니다. release는 `isDraft=false`, `isImmutable=true`, Latest입니다.

- [x] **T-009 checker·installer 확정 결함 수정**
  - 통합·공개 결과: checker의 선택 파일 경계와 installer schema mismatch 복구 진단을 포함한 exact source `0cfcc896ee92ec018d12c88f3f2638a154b35720`을 annotated tag `v2.1.1`과 immutable GitHub Release로 공개했습니다.
  - 검증 근거: exact source의 전체 unittest 154개, root docs, stable locale, Python compile, `git diff --check`, 두 번 생성한 5개 package byte 동일성과 T-008 candidate·published gate가 통과했습니다.

- [x] **T-010 문서 소유권·skill Metadata·changelog 안내 정리**
  - 변경-ID: `2026-09-22-documentation-ownership`, 결정 D-009
  - 통합·공개 결과: locale artifact 가이드 정본화, root maintainer addendum, source root 두 사본과 locale 네 사본의 `project-analysis` Metadata 제거, en·ko `docs/CHANGELOG_GUIDE.md`와 source/artifact별 release history 검사를 Origin PR #28 merge `5066d821084545554588182f5250cc9dea12e444`에 통합했습니다. 같은 exact source를 annotated tag와 [immutable `v2.3.0` release](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.3.0)로 공개했습니다.
  - 검증 근거: exact source의 전체 unittest 167개, root docs, stable locale, 두 package와 draft 5개 asset byte 동일성, candidate와 `published --base-version 2.2.0`이 통과했습니다. published gate는 latest·exact의 en·ko `list-locales`·`install`·`export`·`adopt`, source export와 target 불변을 확인했습니다.

- [x] **DFR-001 `v2.2.0` 준비 재검토**
  - 결과: 공식 locale source는 적용 가이드 §3의 지원 Markdown 범위만 사용하고 full CommonMark parser가 필요한 새 결함 근거가 없어 현재 범위를 유지합니다. 범위 밖 구문이 공식 source에 들어가거나 적용 consumer에서 검증된 P1/P2 결함으로 재현되면 다시 검토합니다.

- [x] **T-011 release verifier adoption plan 진단 강화**
  - 통합 결과: malformed `adoption-plan.json`을 일관된 `VerificationError`로 진단하고 공개 plan v1의 status 계약을 verifier checkout의 installer와 분리한 구현을 Origin PR #22 merge commit `62d1de45d9eb9c8c0387b3f2c4007fcc17480a21`에 통합했습니다. 리뷰에서 확인한 기존 ancestry 진단 결함은 T-012로 분리했습니다.
  - 검증 근거: PR #22 exact code head `c2bf788288c4ad1b61d69597614b3918e537dae6`에서 verifier test 14개와 전체 unittest 156개, root docs, stable locale, Python compile, `git diff --check`, 공개 `v2.1.0` `published` 검증이 통과했습니다. 최종 문서 증분 `7721962976ac80a276398e2ce993b80dfe411c9b`은 T-012 추적만 추가했습니다. 이 구현 작업의 완료 범위는 Origin·GitHub 통합이며 다음 candidate·published 운영 검증은 T-008이 소유합니다.

- [x] **T-012 release verifier의 remote `main` 객체·history 진단**
  - 통합 결과: remote `main` 객체 부재, shallow history 부족, 충분한 shallow history와 실제 비조상 관계를 구분하는 진단을 Origin PR #25 merge `d821dec23b0e34295b96f9af0690ba15f2d33edb`에 통합했습니다.
  - 검증 근거: PR #25 head의 verifier test 16개와 전체 unittest 166개가 통과했고, 후속 exact source `70a5a7a9e97fa5a89609a120ad69bced7e8ae1ac`의 `v2.2.0` candidate·published 성공 경로에서 동기화된 두 remote `main`과 tag ancestry를 추가 fetch 없이 확인했습니다.

- [x] **T-015 Windows release 도구 호환성 수정**
  - 통합·공개 결과: POSIX 상대 경로 정렬, Windows materialized mode 의미, LF checkout과 제한된 symlink fixture skip을 Origin PR #30 merge `3b4bf674da8f7e8c13b2a69c45b2cf1f8ce54756`에 통합했습니다. release 준비 PR #31 merge `3460e4ccd0065bcd8a24fd64a6cd7135293926a0`의 5개 asset을 교체 없이 [immutable Latest `v2.3.1`](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.3.1)로 공개했습니다.
  - 검증 근거: PR head `a64a8897673924abe1c110baad3b2a6ecc8aa811`의 native Windows·Python 3.14.7에서 전체 unittest 174개(실패·오류 0, symlink 관련 skip 16)와 en·ko package·export artifact 검증이 통과했습니다. `v2.3.1` exact source의 `published --base-version 2.3.0`은 Linux와 native Windows 10.0.28000에서 모두 통과했고, Windows 실행은 synchronized `main` `969d1ed48414cee30e698067417d40122a1b8f59`과 5개 asset을 확인한 뒤 exit code 0으로 끝났습니다.

- [x] **T-016 새 프로젝트 `install` 대상 계약 정합화**
  - 변경-ID: `2026-09-22-install-target-contract`, 결정 D-010. Origin PR #34의 `f4004b727fc6e54ce40e7a05877ce74c20695aa4`은 merge commit `a105740ca16ea3e0b6092a7331bf60b89b06f4a3`으로 Origin `main`에 통합됐습니다.
  - 통합 근거: PR #34는 exact head의 installer 회귀 44개·전체 unittest 176개·root docs·stable locale·en/ko export artifact checker와 각 artifact test 53개·Python compile·`git diff --check`를 통과했습니다. 원격 CI runner는 이 템플릿이 제공하지 않아 `No checks reported`였고, 같은 gate를 로컬에서 실행했습니다.
  - release 경계: 공개 `v2.3.1` asset은 변경하지 않았습니다. D-010 계약을 포함한 `v2.3.2` 공개와 candidate·published 검증은 T-018·T-019가 소유합니다.

- [x] **T-018 `v2.3.2` release 준비**
  - 통합 결과: D-010·T-016이 포함된 source의 version·release history를 Origin PR #35 merge `4c6a798885404fdf5170769e271f7d06f4959234`에 통합하고 GitHub `main`에도 non-force fast-forward로 반영했습니다. 양쪽 `main`과 annotated `v2.3.2` tag가 같은 exact source를 가리킵니다.
  - 검증 근거: clean exact checkout의 root docs·stable locale·전체 unittest 176개, 2회 package byte 동일성, 같은 5개 asset의 GitHub draft와 candidate gate가 통과했습니다. 공개와 published 검증·기록은 T-019가 소유합니다.

완료 이력이 길어지면 기존 CHANGELOG 또는 마일스톤별 보관 문서로 연결하고 본문을 복제하지 않습니다.
