# 변경 실행 계획: 다국어 템플릿 소스와 배포 구조

> 이 PLAN이 이번 변경의 상세 작업·검증 상태 정본입니다. 설계 승인 전에는 아래 구현 체크박스를 진행하지 않습니다.

## Metadata

- **Change ID:** 2026-09-09-multilingual-template
- **Spec:** [02-SPEC.md](./02-SPEC.md)
- **Global task:** [02-TODO.md](../../02-TODO.md)의 T-001
- **Owner:** Chae Sangwon
- **Baseline:** `fb7017624ec1ac11cbc6d00df9a8e3916ace5262` (`codex/v1.7.1-ci-doc-fixes`)
- **Integration target:** PR #8 merge commit `60638edfbf1e5decb9019b2a3175734b3a5e085c` 이후의 정확한 local `main`; 공개 저장소 target `jaff2836/coding-agent-docs-template`
- **Scope:** locale/common source 분리, `en`·`ko` payload, export·package·installer, manifest/schema, 문서·locale 검사와 migration 문서. GitHub 생성·release 게시 제외

아래 체크 완료는 구현 branch에서 각 작업에 명시한 검증까지 마쳤다는 뜻입니다. W-007 외 작업의 체크는 소비자 지원 검증을 뜻하지 않으며, 어느 체크도 merge·tag·GitHub release 게시를 뜻하지 않습니다.

## 1. 구현 순서와 의존성

1. 사용자가 `v2.0.0` breaking contract와 skill 현지화 S2를 승인했고 공개 repository identity를 `jaff2836/coding-agent-docs-template`로 확정했습니다. release host와 bootstrap URL은 별도 공개 작업에서 확정합니다.
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

- [x] **W-005 비파괴 locale installer 구현**
  - 범위·변경 파일: `scripts/installer.py`, installer tests와 fake release server fixture
  - 대응 요구사항: R-001, R-006, R-007, R-012
  - 선행조건: W-004 release manifest·bundle contract
  - 검증 방법: locale/version 선택, checksum·manifest 불일치, 크기 제한, path traversal, symlink, case-fold 충돌, 기존 파일 충돌, stage/move 실패에서 대상 tree 불변 확인
  - 결과·근거: packager asset으로 게시되는 자기완결 단일 파일 `scripts/installer.py`(표준 라이브러리만 사용)를 구현했습니다. host-neutral 계약으로 모든 원격 명령에 `--release-url`이 필수이며, redirect는 거부합니다. `latest`는 pointer manifest로 버전만 해석한 뒤 immutable `<version>` namespace에서 manifest·SHA256SUMS·locale ZIP을 받습니다. manifest 구조 검증(schema 미러), SUMS 대조, 실행 중 installer 자기 hash 검증, 다운로드·member 크기 상한, ZIP member 전수 검증(정렬·mode 0644·timestamp 1980·stored·Unix metadata), 절대 경로·`..`·backslash·중복·case-fold·부모/자식 path 충돌 거부, 대상 symlink 조상 거부, 전수 충돌 검사 후 `xb` 배타적 쓰기와 실패 시 생성 파일·디렉터리 롤백을 구현했습니다. PR #7 사후 리뷰에서 확인한 중간 디렉터리 `chmod` 실패도 생성 직후 rollback 목록에 등록하도록 보강했습니다. 기존 파일 충돌 시 전체 목록과 export 안내를 출력하고 대상에 아무것도 쓰지 않습니다.

- [x] **W-006 적용·마이그레이션·지원 문서 정렬**
  - 범위·변경 파일: root README 언어 링크를 제외한 Template Guide, Documentation Guide, CI, locale별 README·AGENTS, release/install 안내와 변경 이력
  - 대응 요구사항: R-002, R-006, R-007, R-010, R-011, R-012
  - 선행조건: W-001~W-005의 실제 명령·경로 확정
  - 검증 방법: 문서 명령과 CLI `--help` 일치, v1.7.1 rollback·기존 적용 저장소 수동 diff 절차, 미지원 locale 표현과 지원 상태 검토
  - 결과·근거: root source 저장소와 `en`·`ko` artifact 문서에 release installer의 `list-locales`·`install`·`export` 명령, redirect 없는 최종 asset URL 계약, source checkout exporter 경로를 구분했습니다. 기존 프로젝트와 `v1.7.1` 사용자는 별도 빈 디렉터리 export 후 수동 diff·merge하고 branch/backup으로 rollback하며 자동 update·locale 전환·overwrite를 하지 않도록 정렬했습니다. 미지원 언어는 영어 artifact와 명시적 언어 정책 수정만 fallback으로 안내하고 공식 지원으로 표시하지 않습니다. installer 명령을 locale manifest의 명시 계약으로 추가해 두 locale의 placeholder·command parity를 검사합니다.

- [x] **W-007 exact-head 전체 검증과 소비자 E2E**
  - 범위·변경 파일: 전체 변경, 임시 소비자 저장소 fixture
  - 대응 요구사항: R-001~R-012
  - 선행조건: W-001~W-006 완료
  - 검증 방법: `en`·`ko` export별 G-docs/G-docs-test, locale·packager·installer 전체 테스트, `git diff --check`, clean rebuild, 실제 Claude·Codex·Cursor·OMP loading probe
  - 결과·근거: PR #8 merge commit `60638edfbf1e5decb9019b2a3175734b3a5e085c`의 clean exact head에서 전체 unittest 99개, root docs, stable locale, Python compile, `git diff --check`가 통과했습니다. repository를 `jaff2836/coding-agent-docs-template`로 결합한 `v2.0.0` package를 두 번 clean build해 5개 asset의 byte 동일성을 확인했고, localhost immutable release namespace에서 packaged installer의 `latest`/exact-version locale 조회, `en`·`ko` 각 28-file install/export, source export 동일성, mode와 재설치 충돌 거부를 검증했습니다. 설치 artifact에서 Claude Code 2.1.273, Codex CLI 0.154.0, Cursor Agent 2026.09.10-fd3934a, OMP 18.2.1이 두 locale의 프로젝트 지침과 명시적 `design` skill 계약을 로드했습니다. OMP skill은 실제 사용자 경로인 대화형 `/skill:design`으로 확인했습니다. 공개 release·원격 HTTPS host·bootstrap URL 검증은 별도 단계입니다.

## 3. 검증 기록

| 대상 작업·요구사항 | 확인한 revision 또는 작업 트리 범위 | 실행한 검사 | 결과·남은 한계 |
|---|---|---|---|
| Draft 문서 구조 | `fb70176`에서 분기한 미커밋 설계 문서와 T-001 | `python3 scripts/check-docs.py`; `python3 -m unittest discover -s tests -p 'test_check_docs.py' -v`; `git diff --check` | 통과 — 상대 링크 265개, 절 참조 60건, 문서 검사 6개. 구현 artifact 검증은 미실행 |
| 참조 구현 조사 | `claude-code-pr-review` `origin/main` `a828f26ac0480ae2b6287c475f2c28a9e97cd9ab` | installer, package_release, locale checker와 tests 읽기 | locale bundle 패턴 재사용 가능. 자동 update는 이 템플릿에 부적합 |
| W-001 source boundary | 구현 commit `01240fb0dbd5ac1c1fa61c76a1208c4197ba456f` | manifest/실제/baseline path 집합 대조, 25개 byte 비교, common+ko 임시 materialize 후 G-docs·G-docs-test, root G-docs·G-docs-test, `git diff --check` | 통과 — output 28개, root 검사 7건·ko artifact 검사 6건. release artifact와 소비자 E2E는 후속 단계 |
| W-002 영어 locale | Origin PR #4 final head `3465885cc4a5085d8c897c6fb3528556734c5add`, merge commit `fa01b20ccebb81788241cc41ba5d68610a6663fe` | 24 localized+6 common inventory, placeholder·heading·link·절 참조·명령·marker parity; en/ko materialized G-docs와 G-docs-test; root G-docs; 영어 adoption `rg`·`grep`; JSON·`git diff --check`; 번역 교차·최종 검토 | 통과 — 교차 검토에서 확인한 번역·계약 drift와 lifecycle 정합성 문구를 수정했고 Chae Sangwon의 최종 검수 승인을 받아 `en=complete`로 판정 |
| W-003 locale-aware 검사 | PR #4 merge commit `fa01b20`을 병합한 `codex/multilingual-template-w003` 전체 변경 | `python3 scripts/check-locales.py`; `python3 scripts/check-locales.py --require-stable`; negative fixture를 포함한 locale source test 41개; root G-docs와 root checker test 20개; common checker test 18개; JSON·`git diff --check` | 통과 — strict manifest·inventory·BCP 47 profile·SemVer·placeholder·marker·명령·skill fixture/status 계약과 marker·heading·token·fence/comment/blockquote decoy, example 인접성·indent, artifact 외부 경로·release history 실패 경로를 확인했고 `en`·`ko` stable gate가 통과 |
| W-004 deterministic export/package | Origin `main` `7657d2cd8f4789dab4d64904b30e4ccc2eea169a`에서 분기한 `codex/multilingual-template-w004` 작업 트리 | en/ko 각 28-file export와 artifact test, exporter 7개·packager 7개 회귀 테스트, 두 build byte 비교, ZIP member/order/mode/timestamp/hash, manifest/SHA256SUMS, stable gate, source revision binding, JSON·Python compile·`git diff --check` | 통과 — exporter와 packager core 구현 완료. 실제 `installer.py` 구현과 이를 포함한 repository exact-head CLI package E2E는 W-005 선행조건으로 남음 |
| W-005 installer | PR #7 merge commit `9d4637d`와 후속 수정이 포함된 `codex/multilingual-template-w006` 작업 트리 | installer 회귀 테스트 24개(fake HTTP release server fixture와 redirect·path-prefix·파일 및 중간 디렉터리 rollback negative case 포함), 전체 unittest 99개; PR #7 head `0d8e60d`의 exact-head package-release CLI E2E에서 packager 5 assets, released installer의 list-locales·install en/ko 각 28파일, export-template 동일 inventory, 재설치 전후 hash·mode 불변; `check-docs.py`, `check-locales.py --require-stable`, `git diff --check`, `py_compile` | 통과 — 사후 리뷰의 중간 디렉터리 `chmod` 실패 잔존을 재현·수정했고 tree 불변 회귀 테스트가 통과. 당시 미확정이던 소비자 E2E는 후속 W-007에서 로컬 검증했고 원격 release는 별도 작업으로 분리 |
| W-006 적용·마이그레이션·지원 문서 | Origin `main` `9d4637d`에서 분기한 `codex/multilingual-template-w006` 작업 트리 | installer/exporter/packager CLI `--help` 대조, locale source/stable gate와 회귀 테스트 41개, 전체 unittest 99개, en/ko 각 28-file export 후 G-docs·checker test 18개, root G-docs, `git diff --check` | 통과 — 공식 release 전 로컬 export와 게시 후 installer 경로, 기존 프로젝트 수동 diff·rollback, v1.7.1 보존, 미지원 언어 fallback, `en`·`ko` complete 지원 경계를 한국어·영어 문서와 manifest 명령 계약에 반영. 소비자 loading은 후속 W-007에서 로컬 검증했고 공식 URL·원격 release는 별도 작업으로 분리 |
| W-007 exact-head·소비자 E2E | PR #8 merge commit `60638edfbf1e5decb9019b2a3175734b3a5e085c` clean tree | 전체 unittest 99개; root docs·stable locale·Python compile·`git diff --check`; 동일 입력 package 2회 byte 비교; localhost release에서 packaged installer `list-locales`·install·export; en/ko 각 28-file artifact 검사; Claude Code 2.1.273·Codex CLI 0.154.0·Cursor Agent 2026.09.10-fd3934a·OMP 18.2.1 실제 loading probe | 통과 — manifest repository/source commit 결합, 5 assets 재현성, source/install/export 동일성, 비파괴 충돌 거부, 두 locale의 프로젝트 지침·명시적 design skill 로딩 확인. OMP slash skill은 interactive 경로로 검증. 공개 release·원격 HTTPS·bootstrap은 사용자 요청에 따라 제외 |

## 4. 변경·재검증 기록

- 2026-09-09: root가 배포 payload와 저장소 관리 문서를 겸하는 부트스트랩 문제를 확인했습니다. 한국어 이관 입력을 현재 작업 트리가 아니라 `fb70176` snapshot으로 고정해 이 설계와 maintainer TODO가 locale artifact에 섞이지 않게 했습니다.
- 2026-09-09: `claude-code-pr-review`의 verified locale bundle 패턴은 채택하되 사용자 수정 문서에 대한 자동 update·강제 overwrite는 제외했습니다.
- 2026-09-09: PR #2 병합 후 사용자 승인에 따라 W-001을 구현했습니다. 한국어 checker는 W-003 전까지 locale source가 소유하며 root checker는 source 디렉터리를 materialized artifact로 오인하지 않습니다.
- 2026-09-09: PR #3 병합과 전체 SPEC·S2 승인 후 W-002를 시작했습니다. 영어 payload source와 안정 marker를 구현하고 자동 parity·artifact 검사를 통과했으나, 최종 번역 검수 전에는 `en`을 `complete`로 승격하지 않습니다.
- 2026-09-10: 사용자와 W-003을 W-002 위 stacked branch·PR로 진행하기로 확인했습니다. W-002의 inventory·marker contract가 고정된 exact head에서 구현하되 영어 번역 최종 검수와 merge 순서는 건너뛰지 않습니다.
- 2026-09-10: PR #4 리뷰의 영어 Owner placeholder 검색 누락을 `3701973`에서 수정했습니다. PR #5 리뷰에 따라 예시 불변조건 marker 수명주기, locale source root gate, marker·heading·example 인접성, top-level list와 4-space code의 indentation 경계, exact section token과 fenced/comment/blockquote decoy 방어를 보강하고 W-002 version #2 exact head 위로 restack했습니다.
- 2026-09-16: PR #4 final head `3465885`의 영어 번역을 Chae Sangwon이 최종 승인했고 merge commit `fa01b20`으로 통합했습니다. W-003에 해당 main을 병합한 뒤 `en`을 `complete`로 승격하고 stable locale gate를 재검증했습니다.
- 2026-09-16: PR #5 merge commit `7657d2c`에서 W-003을 통합했습니다. 해당 main에서 W-004를 분기해 원자적 locale exporter, deterministic release packager, release manifest schema와 negative/E2E fixture를 구현했습니다. installer asset의 실제 구현은 W-005에 유지하되 packager 입력은 source commit에 포함되는 고정 경로로 제한했습니다.
- 2026-09-16: W-004 exact head `568f7e8` 위 stacked branch에서 W-005 installer를 구현했습니다. 사용자 확정에 따라 release host는 코드에 내장하지 않고 모든 원격 명령에 host-neutral `--release-url`을 필수로 요구하며, 이는 D-002의 host-neutral installer 결정과 일치합니다. `latest`는 immutable namespace 버전 해석용 pointer만으로 사용합니다.
- 2026-09-17: PR #6을 merge commit `f60ae97`로 통합하고 W-005 branch에 병합했습니다. PR #7 리뷰의 blocking P2 두 건에 따라 manifest member 부모/자식 path 충돌을 쓰기 전에 거부하고 `InstallerError`를 포함한 실패 rollback을 보강했으며, 명시 release URL 밖으로 신뢰 경계가 이동하지 않도록 모든 redirect를 거부했습니다.
- 2026-09-17: PR #7 사후 리뷰에서 중간 parent directory의 `mkdir` 뒤 `chmod`가 실패하면 rollback 등록 전이라 빈 디렉터리가 남는 결함을 재현했습니다. 생성 직후 등록하도록 고치고 회귀 테스트를 추가한 뒤 W-006 문서 정렬과 함께 전체 99개 테스트를 통과했습니다.
- 2026-09-17: W-006에서 release 전 source exporter와 게시 후 installer 사용법, 기존 프로젝트·v1.7.1 수동 migration과 rollback, `en`·`ko` 외 언어 fallback 경계를 root 및 locale별 한국어·영어 문서에 반영했습니다. 실제 release host와 bootstrap URL은 확정하지 않았습니다.
- 2026-09-17: PR #8을 merge commit `60638ed`로 통합했습니다. 사용자가 공개 repository identity를 `jaff2836/coding-agent-docs-template`로 확정하고 공개 release는 제외한 채 최소 실제 consumer probe까지 W-007을 진행하도록 승인했습니다.
- 2026-09-17: `60638ed` clean exact head에서 전체 gate, deterministic package 2회 build, localhost packaged-installer E2E와 Claude·Codex·Cursor·OMP의 `en`·`ko` 프로젝트 지침·design skill loading probe를 통과했습니다. OMP 비대화형 print mode는 slash command를 확장하지 않아 실제 대화형 `/skill:design` 경로로 검증했습니다.

## 5. 인계

- PR #3~#8에서 W-001~W-006이 local·Origin `main` merge commit `60638edfbf1e5decb9019b2a3175734b3a5e085c`까지 통합됐습니다. W-007은 해당 clean exact head의 전체 gate와 최소 실제 consumer probe를 통과했으며, 이 검증 기록은 `codex/multilingual-template-w007` 작업 트리에 반영했습니다.
- 공개 repository identity는 `jaff2836/coding-agent-docs-template`입니다. immutable release host와 installer bootstrap URL은 공개 release 작업에서 확정합니다.
- 구현·통합·release는 각각 별도 완료 조건입니다. W-007 검증 기록은 `codex/multilingual-template-w007` branch의 PR로 통합하며 tag·GitHub release는 별도 위임입니다.
