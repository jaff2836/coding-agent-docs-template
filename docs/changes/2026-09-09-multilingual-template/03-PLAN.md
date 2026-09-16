# 변경 실행 계획: 다국어 템플릿 소스와 배포 구조

> 이 PLAN이 이번 변경의 상세 작업·검증 상태 정본입니다. 설계 승인 전에는 아래 구현 체크박스를 진행하지 않습니다.

## Metadata

- **Change ID:** 2026-09-09-multilingual-template
- **Spec:** [02-SPEC.md](./02-SPEC.md)
- **Global task:** [02-TODO.md](../../02-TODO.md)의 T-001
- **Owner:** Chae Sangwon
- **Baseline:** `fb7017624ec1ac11cbc6d00df9a8e3916ace5262` (`codex/v1.7.1-ci-doc-fixes`)
- **Integration target:** Origin PR #2 merge commit `113a6a58f9b03707fe8050b5673d3437b9895d03` 이후의 정확한 `main`
- **Scope:** locale/common source 분리, `en`·`ko` payload, export·package·installer, manifest/schema, 문서·locale 검사와 migration 문서. GitHub 생성·release 게시 제외

아래 체크 완료는 구현 branch에서의 구현·검증 완료이며 merge·tag·GitHub release·도구 지원 검증을 뜻하지 않습니다.

## 1. 구현 순서와 의존성

1. 사용자가 `v2.0.0` breaking contract와 skill 현지화 S2를 승인했습니다. 실제 repository URL은 구현 중 확정할 수 있습니다.
2. `fb70176` tree에서 배포 payload inventory를 고정한 뒤 한국어 locale과 common source를 먼저 이관합니다.
3. root를 저장소 유지관리 영역으로 전환하고 영어 locale을 작성합니다.
4. stable marker와 locale/artifact 검사를 먼저 만든 뒤 export와 release packaging을 연결합니다.
5. 검증된 artifact contract 위에 installer를 구현합니다.
6. 모든 local gate와 소비자 저장소 E2E를 통과한 뒤에만 통합·release 작업을 별도로 요청합니다.

W-001은 뒤 작업의 source boundary입니다. W-002~W-005는 같은 manifest와 output inventory를 바꾸므로 순차 통합합니다. 다만 선행 단계의 inventory·marker 계약이 branch head에서 고정되면 최종 검수·merge를 기다리지 않고 그 exact head에서 stacked branch로 다음 단계를 구현할 수 있습니다. 이 경우 merge 순서는 W-002 → W-003 → W-004 → W-005를 유지하고, 후속 PR의 완료가 선행 PR의 검수·통합 완료를 뜻하지 않습니다. W-006 문서는 실제 구현값을 확인한 뒤 작성하며, W-007은 exact final head에서 전체를 다시 검증합니다.

## 2. 작업 체크리스트

- [x] **W-001 저장소 관리 영역과 payload source 분리**
  - 범위·변경 파일: root `AGENTS.md`, `docs/`, `template/common/`, `locales/manifest.json`, `locales/ko/`
  - 대응 요구사항: R-002, R-003, R-004, R-010
  - 선행조건: 이 단계의 사용자 승인 완료, PR #2가 `113a6a58f9b03707fe8050b5673d3437b9895d03`으로 통합됨
  - 검증 방법: `fb70176` tracked payload inventory와 새 common+ko artifact의 path·byte 비교. 이 변경 폴더와 maintainer TODO가 artifact에 없음을 검사
  - 결과·근거: `locales/manifest.json`의 28개 output path가 common 4개와 ko 24개로 충돌 없이 닫혔습니다. baseline 25개는 byte-identical이고 README 계약 3개만 승인된 변환이며 source landing README만 제외했습니다. root와 materialized ko artifact의 문서 검사·회귀 테스트가 통과했습니다.

- [x] **W-002 영어 locale과 locale별 도구 계약 작성**
  - 범위·변경 파일: `locales/en/`, `locales/ko/`, locale manifest, stable section marker
  - 대응 요구사항: R-001, R-008, R-009, R-011, R-012
  - 선행조건: W-001 inventory 확정, skill 현지화 S2 승인. 최종 번역 검수자는 Chae Sangwon으로 확정
  - 검증 방법: 필수 file/marker/placeholder/명령 parity, 같은 locale의 skill pair와 REVIEW/BUGBOT 대조, 번역 리뷰 기록
  - 결과·근거: Origin PR #4의 최종 head `3465885cc4a5085d8c897c6fb3528556734c5add`에 영어 24개 localized path와 S2 skill·section marker 계약 및 최종 용어 교정을 구현했습니다. en/ko inventory·placeholder·heading·link·절 참조·정본 명령 parity, locale 내부 skill pair와 REVIEW/BUGBOT, 양 locale materialized G-docs·G-docs-test가 통과했습니다. Chae Sangwon이 최종 영어 번역 검수를 승인했고 PR #4가 merge commit `fa01b20ccebb81788241cc41ba5d68610a6663fe`으로 통합되어 `en`을 `complete`로 승격했습니다.

- [x] **W-003 locale-aware 문서·source 검사 구현**
  - 범위·변경 파일: `scripts/check-docs.py`, `scripts/check-locales.py`, 관련 단위·negative fixture
  - 대응 요구사항: R-004, R-008, R-009, R-010
  - 선행조건: W-001~W-002의 inventory·marker 계약
  - 검증 방법: 누락 파일, 중복 output, placeholder 차이, marker 순서, 깨진 링크, 깊은 절 참조, 불변조건·skill drift가 각각 실패하는 테스트
  - 결과·근거: PR #4 merge commit `fa01b20ccebb81788241cc41ba5d68610a6663fe`을 병합한 `codex/multilingual-template-w003`에 manifest 기반 source checker, import 가능한 검사 API, marker 기반 공통 artifact checker와 root wrapper를 구현했습니다. 리뷰 후 fenced code·HTML comment·blockquote fence decoy와 section token 경계, marker-heading·example-bullet 인접성, top-level list와 4-space code의 indentation 경계, 예시 불변조건 marker 수명주기, root locale gate 연결을 보강했습니다. checker·negative fixture, en/ko 28-file materialized artifact의 기본·`--root` 검사와 artifact 단위 테스트가 모두 통과했고, 두 locale의 `complete` 판정과 stable gate도 통과했습니다.

- [x] **W-004 deterministic export와 release packaging 구현**
  - 범위·변경 파일: `scripts/export-template.py`, `scripts/package-release.py`, `schemas/release-manifest.schema.json`, packaging tests
  - 대응 요구사항: R-003, R-004, R-005, R-011
  - 선행조건: W-003 검사 API와 complete locale 판정
  - 검증 방법: 빈 디렉터리 export E2E, 두 번 build한 archive·manifest byte 비교, exact member/mode/timestamp/hash, source commit·version binding과 rebuild 검증
  - 결과·근거: manifest의 닫힌 inventory만 외부 빈 디렉터리에 원자적으로 materialize하고 artifact checker를 실행하는 exporter를 구현했습니다. packager는 `complete` locale과 stable gate를 요구하고, 고정 `stored` ZIP·mode `0644`·1980-01-01 timestamp, member hash·bytes, exact SemVer·source commit·repository를 release manifest와 `SHA256SUMS`에 결합합니다. 실제 installer source는 W-005가 소유하므로 packager는 저장소의 고정 `scripts/installer.py`만 받아 외부 bytes가 source commit에 섞이지 않게 했습니다. en/ko export E2E, 이중 build byte 비교, archive/manifest 검증, clean Git source binding과 실패 경로 테스트가 통과했습니다.

- [ ] **W-005 비파괴 locale installer 구현**
  - 범위·변경 파일: `scripts/installer.py`, installer tests와 fake release server fixture
  - 대응 요구사항: R-001, R-006, R-007, R-012
  - 선행조건: W-004 release manifest·bundle contract
  - 검증 방법: locale/version 선택, checksum·manifest 불일치, 크기 제한, path traversal, symlink, case-fold 충돌, 기존 파일 충돌, stage/move 실패에서 대상 tree 불변 확인
  - 결과·근거: 미실행

- [ ] **W-006 적용·마이그레이션·지원 문서 정렬**
  - 범위·변경 파일: root README 언어 링크를 제외한 Template Guide, Documentation Guide, CI, locale별 README·AGENTS, release/install 안내와 변경 이력
  - 대응 요구사항: R-002, R-006, R-007, R-010, R-011, R-012
  - 선행조건: W-001~W-005의 실제 명령·경로 확정
  - 검증 방법: 문서 명령과 CLI `--help` 일치, v1.7.1 rollback·기존 적용 저장소 수동 diff 절차, 미지원 locale 표현과 지원 상태 검토
  - 결과·근거: 미실행

- [ ] **W-007 exact-head 전체 검증과 소비자 E2E**
  - 범위·변경 파일: 전체 변경, 임시 소비자 저장소 fixture
  - 대응 요구사항: R-001~R-012
  - 선행조건: W-001~W-006 완료
  - 검증 방법: `en`·`ko` export별 G-docs/G-docs-test, locale·packager·installer 전체 테스트, `git diff --check`, clean rebuild, 실제 Claude·Codex·Cursor·OMP loading probe
  - 결과·근거: 미실행. 원격 release·지원 완료는 별도 단계

## 3. 검증 기록

| 대상 작업·요구사항 | 확인한 revision 또는 작업 트리 범위 | 실행한 검사 | 결과·남은 한계 |
|---|---|---|---|
| Draft 문서 구조 | `fb70176`에서 분기한 미커밋 설계 문서와 T-001 | `python3 scripts/check-docs.py`; `python3 -m unittest discover -s tests -p 'test_check_docs.py' -v`; `git diff --check` | 통과 — 상대 링크 265개, 절 참조 60건, 문서 검사 6개. 구현 artifact 검증은 미실행 |
| 참조 구현 조사 | `claude-code-pr-review` `origin/main` `a828f26ac0480ae2b6287c475f2c28a9e97cd9ab` | installer, package_release, locale checker와 tests 읽기 | locale bundle 패턴 재사용 가능. 자동 update는 이 템플릿에 부적합 |
| W-001 source boundary | 구현 commit `01240fb0dbd5ac1c1fa61c76a1208c4197ba456f` | manifest/실제/baseline path 집합 대조, 25개 byte 비교, common+ko 임시 materialize 후 G-docs·G-docs-test, root G-docs·G-docs-test, `git diff --check` | 통과 — output 28개, root 검사 7건·ko artifact 검사 6건. release artifact와 소비자 E2E는 후속 단계 |
| W-002 영어 locale | Origin PR #4 final head `3465885cc4a5085d8c897c6fb3528556734c5add`, merge commit `fa01b20ccebb81788241cc41ba5d68610a6663fe` | 24 localized+6 common inventory, placeholder·heading·link·절 참조·명령·marker parity; en/ko materialized G-docs와 G-docs-test; root G-docs; 영어 adoption `rg`·`grep`; JSON·`git diff --check`; 번역 교차·최종 검토 | 통과 — 교차 검토에서 확인한 번역·계약 drift와 lifecycle 정합성 문구를 수정했고 Chae Sangwon의 최종 검수 승인을 받아 `en=complete`로 판정 |
| W-003 locale-aware 검사 | PR #4 merge commit `fa01b20`을 병합한 `codex/multilingual-template-w003` 전체 변경 | `python3 scripts/check-locales.py`; `python3 scripts/check-locales.py --require-stable`; negative fixture를 포함한 locale source test 41개; root G-docs와 root checker test 20개; common checker test 18개; JSON·`git diff --check` | 통과 — strict manifest·inventory·BCP 47 profile·SemVer·placeholder·marker·명령·skill fixture/status 계약과 marker·heading·token·fence/comment/blockquote decoy, example 인접성·indent, artifact 외부 경로·release history 실패 경로를 확인했고 `en`·`ko` stable gate가 통과 |
| W-004 deterministic export/package | Origin `main` `7657d2cd8f4789dab4d64904b30e4ccc2eea169a`에서 분기한 `codex/multilingual-template-w004` 작업 트리 | en/ko 각 28-file export와 artifact test, exporter 7개·packager 7개 회귀 테스트, 두 build byte 비교, ZIP member/order/mode/timestamp/hash, manifest/SHA256SUMS, stable gate, source revision binding, JSON·Python compile·`git diff --check` | 통과 — exporter와 packager core 구현 완료. 실제 `installer.py` 구현과 이를 포함한 repository exact-head CLI package E2E는 W-005 선행조건으로 남음 |

## 4. 변경·재검증 기록

- 2026-09-09: root가 배포 payload와 저장소 관리 문서를 겸하는 부트스트랩 문제를 확인했습니다. 한국어 이관 입력을 현재 작업 트리가 아니라 `fb70176` snapshot으로 고정해 이 설계와 maintainer TODO가 locale artifact에 섞이지 않게 했습니다.
- 2026-09-09: `claude-code-pr-review`의 verified locale bundle 패턴은 채택하되 사용자 수정 문서에 대한 자동 update·강제 overwrite는 제외했습니다.
- 2026-09-09: PR #2 병합 후 사용자 승인에 따라 W-001을 구현했습니다. 한국어 checker는 W-003 전까지 locale source가 소유하며 root checker는 source 디렉터리를 materialized artifact로 오인하지 않습니다.
- 2026-09-09: PR #3 병합과 전체 SPEC·S2 승인 후 W-002를 시작했습니다. 영어 payload source와 안정 marker를 구현하고 자동 parity·artifact 검사를 통과했으나, 최종 번역 검수 전에는 `en`을 `complete`로 승격하지 않습니다.
- 2026-09-10: 사용자와 W-003을 W-002 위 stacked branch·PR로 진행하기로 확인했습니다. W-002의 inventory·marker contract가 고정된 exact head에서 구현하되 영어 번역 최종 검수와 merge 순서는 건너뛰지 않습니다.
- 2026-09-10: PR #4 리뷰의 영어 Owner placeholder 검색 누락을 `3701973`에서 수정했습니다. PR #5 리뷰에 따라 예시 불변조건 marker 수명주기, locale source root gate, marker·heading·example 인접성, top-level list와 4-space code의 indentation 경계, exact section token과 fenced/comment/blockquote decoy 방어를 보강하고 W-002 version #2 exact head 위로 restack했습니다.
- 2026-09-16: PR #4 final head `3465885`의 영어 번역을 Chae Sangwon이 최종 승인했고 merge commit `fa01b20`으로 통합했습니다. W-003에 해당 main을 병합한 뒤 `en`을 `complete`로 승격하고 stable locale gate를 재검증했습니다.
- 2026-09-16: PR #5 merge commit `7657d2c`에서 W-003을 통합했습니다. 해당 main에서 W-004를 분기해 원자적 locale exporter, deterministic release packager, release manifest schema와 negative/E2E fixture를 구현했습니다. installer asset의 실제 구현은 W-005에 유지하되 packager 입력은 source commit에 포함되는 고정 경로로 제한했습니다.

## 5. 인계

- PR #3 merge commit `2a735eb182662afa69ee2c6d67f4f03d09e56d38`에서 W-001, PR #4 merge commit `fa01b20ccebb81788241cc41ba5d68610a6663fe`에서 W-002, PR #5 merge commit `7657d2cd8f4789dab4d64904b30e4ccc2eea169a`에서 W-003이 통합됐습니다. W-004는 `codex/multilingual-template-w004` 작업 트리에서 구현·검증했으며, W-005는 W-004 통합 후 시작합니다.
- 실제 repository URL은 구현 중 결정합니다.
- 구현·통합·release는 각각 별도 완료 조건이며 tag와 release 게시 권한은 아직 위임되지 않았습니다.
