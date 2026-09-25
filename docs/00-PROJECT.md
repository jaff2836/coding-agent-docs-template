# 프로젝트 기준과 설계

> 제품 개요·현재 구조·기본 설계·결정과 상세 설계의 인덱스입니다. 기존 제품 설계를 통합할 때는 결정·계약·근거를 보존하고 중복 설명과 작업 상태를 정리합니다. 실행 계획은 [02-TODO.md](./02-TODO.md) 또는 변경별 PLAN에서 관리합니다.
>
> §1~§5, §8, §11은 필수입니다. 나머지 절은 해당 사항이 있을 때만 유지합니다. 기존 상세 설계를 유지한다면 본문을 복제하지 않고 §13에서 정본을 연결합니다. 절을 제거하거나 번호를 바꾸면 들어오는 절 참조도 갱신하세요.

## Metadata

- **Project:** coding-agent-docs-template
- **Status:** Active — immutable Latest `v2.3.2` 공개·지원 검증과 T-019 기록 통합 완료
- **Owner:** Chae Sangwon
- **Last reviewed:** 2026-09-25
- **Review cadence:** 아키텍처·범위 변경 시 또는 마일스톤 종료 시

## 1. Context

### Problem

Claude, Codex, Cursor와 OMP가 같은 문서·설계·리뷰 계약을 사용하도록 하는 공개 템플릿입니다. v1.7.1까지는 저장소 root가 한국어 복사형 payload와 저장소 관리 문서를 겸했기 때문에 locale 확장 시 maintainer 작업이 사용자 템플릿에 섞이는 문제가 있습니다.

### Target Users

- 템플릿을 관리·번역·릴리스하는 maintainer
- AI 코딩 에이전트 협업 규칙을 기존 또는 새 프로젝트에 적용하는 개발자

### Current State

- 공개 release 기준은 [immutable GitHub Release `v2.3.2`](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.3.2)(2026-09-23 공개, Latest)이며 annotated tag와 당시 Origin·GitHub `main`의 commit은 `4c6a798885404fdf5170769e271f7d06f4959234`입니다. candidate·보완한 published gate에서 교체하지 않은 5개 asset, latest·exact의 en·ko install/export/adopt, `v2.3.1` base-aware upgrade 및 비어 있지 않은 install 대상 불변을 확인했습니다. 이전 release는 그대로 유지되며 exact version에 맞는 자기 installer로만 설치할 수 있습니다.
- W-001의 root 유지관리 영역과 `template/common/`·`locales/ko/` payload source 분리는 Origin PR #3 merge commit `2a735eb182662afa69ee2c6d67f4f03d09e56d38`에 통합됐습니다.
- W-002의 `locales/en`·locale별 skill S2 계약과 W-003 locale/artifact 검사는 각각 Origin PR #4·#5에 통합됐습니다. `en`·`ko` source는 모두 `complete`입니다.
- W-004 exporter·packager는 Origin PR #6 merge commit `f60ae97`, W-005 비파괴 installer는 PR #7 merge commit `9d4637d`, W-006 적용 문서는 PR #8 merge commit `60638ed`에 통합됐습니다.
- W-007은 `60638ed` exact head에서 `en`·`ko` package/install/export와 Claude·Codex·Cursor·OMP의 실제 로딩 probe를 통과했습니다. D-004 공개 gate에서는 tag commit의 102개 테스트·docs·stable locale, deterministic package와 기존 draft asset byte 동일성, 실제 GitHub HTTPS latest·exact 설치를 추가로 확인했습니다.
- `project-analysis` locale별 skill(D-005, PR #12), 기존 저장소용 읽기 전용 `adopt`와 adoption policy·release manifest schema 2(D-006, PR #14~#16), 강화된 artifact `check-docs.py`(T-005, PR #17)가 `v2.1.0` asset에 포함됐습니다.
- D-008의 base-aware `adopt`와 release verifier 후속은 Origin PR #24·#25, release 준비는 PR #26 merge `70a5a7a9e97fa5a89609a120ad69bced7e8ae1ac`로 통합됐습니다. 공개 en·ko upgrade E2E와 `claude-review-e2e@26c531beb65eaef8f524a00bcf8f06c52445c3d8`의 v2.1→v2.2 report 독립 대조를 통과했고 consumer tree는 바뀌지 않았습니다.
- D-009의 locale artifact guide 정본화, root maintainer addendum, 선택형 프로젝트 changelog 안내와 skill Metadata 제거는 Origin PR #28 merge `5066d821084545554588182f5250cc9dea12e444`와 `v2.3.0` artifact에 통합됐습니다.
- T-015의 Windows artifact 정렬·materialized mode·LF checkout·symlink fixture 보완은 Origin PR #30 merge `3b4bf674da8f7e8c13b2a69c45b2cf1f8ce54756`에 통합됐습니다. PR head `a64a8897673924abe1c110baad3b2a6ecc8aa811`의 native Windows·Python 3.14.7에서 전체 unittest 174개(16개 skip)와 en·ko package·export artifact 검증이 통과했습니다. exact `v2.3.1` source `3460e4ccd0065bcd8a24fd64a6cd7135293926a0`의 published E2E도 Linux와 native Windows에서 모두 통과해 T-015를 완료했습니다.
- D-010의 새 경로·빈 디렉터리 `install` 계약(T-016)은 Origin PR #34 merge commit `a105740ca16ea3e0b6092a7331bf60b89b06f4a3`에 통합됐고, PR #35 merge `4c6a798885404fdf5170769e271f7d06f4959234`의 `v2.3.2` asset으로 공개됐습니다. 두 remote `main`, annotated tag, draft candidate와 immutable published 검증이 통과했습니다. 공개 검증기의 새 거부 문구 대응과 지원 검증 기록은 Origin PR #36 merge `cc791be2370e76930184e473061312518d5fe221`에 통합하고 GitHub `main`에도 fast-forward로 반영했습니다.
- 기존 적용 저장소의 사용자 수정 문서는 자동 덮어쓰기나 locale 자동 전환 대상이 아닙니다.

현재 구현·검증된 지원 범위와 그 근거를 기록합니다. 설계 승인·코드 구현·통합·릴리스·지원 검증을 구분합니다. 열린 PR이나 브랜치별 상세 상태를 여기에 복제하지 않습니다.

## 2. Goals

- `en`·`ko` complete source에서 고정 경로의 단일-locale artifact를 재현 가능하게 생성합니다.
- artifact와 exact source commit·version·member hash를 결합하고 비파괴 installer로 검증 후 설치합니다.
- Claude, Codex, Cursor와 OMP에서 locale별 진입점·스킬·리뷰 계약이 동일하게 동작하는지 검증합니다.

## 3. Non-goals

- `en`·`ko` 외 locale의 공식 번역과 품질 보증
- 특정 CI runner pipeline 또는 자동 리뷰 실행 구성
- 기존 프로젝트 문서의 자동 update·overwrite
- GitHub Releases 외 별도 host·mirror와 release 자동화

## 4. Constraints

- Python 표준 라이브러리만 사용하고 새 production dependency를 추가하지 않습니다.
- locale은 BCP 47 tag를 사용하며 manifest allowlist에 등록된 값만 지원합니다.
- 적용 artifact의 `AGENTS.md`, `CLAUDE.md`, `docs/`, tool별 고정 경로는 v1 계약을 유지합니다.
- path traversal, symlink, 부분 설치, checksum 불일치와 기존 파일 충돌은 쓰기 전에 거부합니다.

## 5. Current Architecture

현재 코드와 실제 배포 구성에 존재하는 구조를 기록합니다. 아직 구현되지 않은 목표 상태를 현재 구조처럼 작성하지 않습니다.

### Components

| Component | Responsibility | Dependencies | Owner |
| --------- | -------------- | ------------ | ----- |
| root maintenance plane | 저장소 소개, 제품 결정, 변경 설계·TODO와 maintainer 도구 지침 | artifact source와 분리 | Chae Sangwon |
| `template/common/` | 현재 언어 비의존으로 확인된 payload source | `locales/manifest.json` inventory | Chae Sangwon |
| `locales/en/`, `locales/ko/` | complete locale별 prose·도구 계약 source | common source와 합성 | Chae Sangwon |
| `locales/manifest.json` | baseline, locale 상태, common/localized output inventory | checker·exporter·packager가 사용 | Chae Sangwon |
| 번들 skill | `design`, `project-analysis`, `review-round`의 조건부 절차를 tool별 고정 경로에 제공 | locale별 `.agents`·`.claude` byte-identical 사본과 skill fixture | Chae Sangwon |
| locale exporter·packager | 단일-locale tree와 deterministic ZIP·manifest·checksum 생성 | complete locale source, 고정 installer source | Chae Sangwon |
| 비파괴 installer | 명시한 GitHub Releases root의 manifest·checksum·locale ZIP을 검증하고 새 경로 또는 빈 디렉터리에만 install하거나 빈 디렉터리로 export하며, 기존 저장소에는 `adopt`로 대상 밖 output에 artifact와 경로별 plan을 게시합니다. 선택형 exact base가 있으면 과거 코드를 실행하지 않고 base·current·target의 3-way upgrade 상태를 함께 분류합니다. | GitHub asset HTTPS redirect만 제한 허용, 비어 있지 않거나 읽을 수 없는 install 대상은 쓰기 전 전체 중단, `adopt`는 대상에 쓰거나 자동 병합·삭제하지 않음 | Chae Sangwon |
| release 검증 도구 | 게시 후보의 local gate·재현 package·draft asset과 공개된 immutable Latest release의 모든 locale 경로를 읽기 전용으로 검증하며, 선택형 base-aware 공개 upgrade E2E도 검사 | clean exact-source checkout, `git`, `gh`, GitHub Releases | Chae Sangwon |

### Data Flow

exporter는 manifest의 common과 선택 locale inventory만 외부 빈 디렉터리에 합성하고 artifact checker를 통과한 뒤 원자적으로 게시합니다. packager는 `complete` locale을 고정 ZIP metadata로 묶고 source commit·version·repository·member hash를 release manifest에 결합합니다. packager는 `locales/manifest.json`의 adoption policy도 각 member에 materialize합니다(`schema_version` 2). installer는 GitHub의 `latest` release에서 version을 선택한 뒤 같은 repository의 exact `v<SemVer>` release asset을 검증하고, `install` 대상이 새 경로 또는 읽을 수 있는 빈 디렉터리인지 확인한 뒤 경로 충돌·부분 실패를 거부하거나 rollback합니다. 기존 저장소에는 `adopt`가 같은 검증 후 artifact 경로만 list·lstat·read로 분류하고, 대상 밖의 빈 output에 `artifact/`와 실험적 `adoption-plan.json`을 원자적으로 게시합니다. 선택형 base-aware 경로는 더 낮은 exact SemVer의 schema 1·2 release를 과거 코드 실행 없이 별도 검증하고 `base ∪ current` 경로를 target과 비교한 format 2 report를 만듭니다. release 검증 도구는 사람이 만든 draft와 공개된 immutable release를 package byte·ref·공개 installer 경로와 대조할 뿐 tag나 release를 변경하지 않습니다. source root 자체는 배포하지 않습니다. `v2.0.0`·`v2.1.0`·`v2.1.1`·`v2.2.0`·`v2.3.0`·`v2.3.1`·`v2.3.2`는 실제 immutable GitHub Release에서 각 계약에 맞는 원격 E2E를 검증했습니다.

### External Boundaries

- 공개 저장소 identity와 release host는 `jaff2836/coding-agent-docs-template`의 GitHub Releases로 확정했습니다. bootstrap URL과 version URL 계약은 [D-004 SPEC](./changes/2026-09-18-github-releases-publication/02-SPEC.md)이 소유합니다.
- 파일시스템과 release asset 다운로드가 신뢰 경계입니다. manifest·archive·member hash를 모두 확인해야 합니다.

### Contracts and Core Design

상세 요구사항·오류 처리·마이그레이션 계약은 [다국어 템플릿 SPEC](./changes/2026-09-09-multilingual-template/02-SPEC.md), 실행 상태는 [PLAN](./changes/2026-09-09-multilingual-template/03-PLAN.md)이 정본입니다.

## 6. Target Architecture

합의되었지만 아직 완전히 구현되지 않은 목표 구조를 기록합니다. **제안만 있고 합의되지 않은 항목은 여기 두지 않습니다.** 미합의 항목은 §11 Open Questions 또는 §12 Rejected or Deferred Ideas에 두고, 결정이 내려진 뒤에만 이 표로 옮깁니다. 이 표만 읽는 사람은 여기 있는 것을 이미 결정된 것으로 읽습니다.

### Target Components

승인된 목표 구성은 `template/common/`과 BCP 47 tag별 `locales/<tag>/` source, 닫힌 manifest inventory, locale 검사, deterministic exporter·packager와 비파괴 installer입니다. 첫 안정판은 `en`·`ko`가 모두 `complete`일 때만 만들며 skill prose와 출력 정책은 locale별 source가 소유합니다.

D-006의 `adopt`·adoption policy·release manifest schema 2는 `v2.1.0`으로 구현·공개되어 §5 현재 구조로 옮겼습니다. 상세 계약은 [adoption SPEC](./changes/2026-09-18-existing-repository-adoption/02-SPEC.md)을 따릅니다.

D-008의 선택형 `adopt --base-version <older-exact-semver>`과 format 2 report는 `v2.2.0`으로 구현·공개되어 §5 현재 구조로 옮겼습니다. 상세 계약과 완료 근거는 [base-aware adoption 변경](./changes/2026-09-20-adopt-upgrade-classification/01-CHANGE.md)과 [PLAN](./changes/2026-09-20-adopt-upgrade-classification/03-PLAN.md)을 따릅니다.

D-011은 Windows Python 3.12 이상에서 installer의 기존 root·output·직접 부모·member 검사 지점에 junction 거부를 추가하고 D-006 adoption SPEC §3.3의 대상 상태를 확장합니다. 선택 경로보다 위의 기존 상위 component는 확대 검사하지 않습니다. 상세 계약은 [T-017 경계 설계](./changes/2026-09-23-windows-junction-boundary/01-CHANGE.md)를 따릅니다. 구현·native 회귀는 Origin PR #38 merge `b5a9c4e`와 GitHub `main`에 반영됐고 다음 release에는 아직 포함되지 않았습니다.

### Target Data Flow

common과 선택 locale 하나를 manifest inventory에 따라 표준 root 경로로 합성하고 검사합니다. exact source commit과 version에 결합된 locale별 archive·manifest를 만든 뒤 installer가 검증·stage·전체 충돌 검사를 거쳐 대상에 기록합니다. 상세 계약은 [SPEC §3](./changes/2026-09-09-multilingual-template/02-SPEC.md)을 따릅니다.

### Compatibility Requirements

- v1.7.1 한국어 payload는 `fb70176` 기준으로 보존합니다.
- source root를 직접 복사하지 않으며 locale artifact만 적용합니다.
- 이미 적용한 저장소는 자동 migration하지 않습니다.

## 7. Transition Plan

현재 구조에서 목표 구조로 이동하는 순서와 안전 조건을 작성합니다. 단계 정의·완료 조건을 다루며, 상세 실행 체크박스는 TODO 또는 변경별 PLAN에서 관리합니다. 확장 문서가 같은 전환을 정의하면 그 절을 참조합니다.

| Phase | Change | Preconditions | Compatibility/Rollback | Completion Evidence |
|---|---|---|---|---|
| W-001 | root maintainer 영역과 common/ko source 분리 | 사용자 승인, PR #2 병합 | `fb70176` payload 보존; 실패 시 source 분리 폐기 | PR #3 merge commit `2a735eb`, closed inventory와 path·byte 비교 |
| W-002 | en locale과 locale별 skill S2 | W-001 | v1.7.1 유지 | PR #4 merge commit `fa01b20`, 최종 번역 승인 |
| W-003 | locale/artifact 검사 | W-002 | marker·inventory 계약 유지 | PR #5 merge commit `7657d2c`, source/stable gate |
| W-004 | deterministic export/package | W-003, complete locale | v1.7.1 유지 | PR #6 merge commit `f60ae97`, deterministic package gate |
| W-005 | 비파괴 installer | W-004 manifest·bundle 계약 | v1.7.1 유지; 공식 v2 release 전 | PR #7 merge commit `9d4637d`, exact-head package/install E2E |
| W-006 | 적용·마이그레이션·지원 문서 정렬 | W-001~W-005 | 실제 release 전에는 원격 설치를 완료로 표시하지 않음 | PR #8 merge commit `60638ed` |
| W-007 | exact-head 전체 검증과 소비자 E2E | W-006 | 공개 release 없이 로컬 immutable release namespace로 검증 | `60638ed` exact-head gate와 Claude·Codex·Cursor·OMP probe |
| 공개 배포 | GitHub Releases transport와 v2.0.0 게시 | W-007, D-004 | 공개된 tag·asset은 교체하지 않고 결함 시 patch release | `v2.0.0` tag `8bc8b1b`, immutable release와 [W-003·W-004 검증](./changes/2026-09-18-github-releases-publication/03-PLAN.md) |
| 기존 저장소 adoption | adoption policy, release manifest schema 2, `adopt`, 기존 저장소 우선 문서와 `v2.1.0` 게시 | D-006, T-005 checker 강화 | `install`·`export` CLI 유지; 결함 시 `adopt`·policy를 제거한 patch release | PR #14~#18, `v2.1.0` tag `36a123f` immutable release와 [adoption PLAN](./changes/2026-09-18-existing-repository-adoption/03-PLAN.md) W-004 원격 E2E |
| base-aware adoption 분류 | exact base 검증, 3-way 분류, format 2 report와 `v2.2.0` 지원 검증 | D-008, T-011 뒤 구현·review 후속 통합 | base 없는 format 1 유지; 과거 installer 비실행; 자동 merge·삭제 없음; `--base-version` 생략으로 rollback | Origin PR #24~#26, `v2.2.0` tag `70a5a7a`, [base-aware adoption PLAN](./changes/2026-09-20-adopt-upgrade-classification/03-PLAN.md) W-001~W-005 |
| 문서 소유권과 changelog 안내 | locale guide 정본화, root maintainer addendum, skill Metadata 제거, 선택형 changelog 안내 | D-009 승인, T-010 구현·검증 | 기존 프로젝트 changelog 보존; 새 안내 경로 제거와 checker 기본값 복원으로 rollback | Origin PR #28 merge `5066d82`, `v2.3.0` immutable release와 [문서 소유권 변경](./changes/2026-09-22-documentation-ownership/01-CHANGE.md) R-001~R-006 |

## 8. Decisions

결정 상태는 `Proposed`, `Accepted`, `Superseded`, `Rejected` 중 하나를 사용합니다.

| ID | Date | Status | Decision | Rationale / Canonical source | Alternatives / Consequences | Approval |
|---|---|---|---|---|---|---|
| D-001 | 2026-09-09 | Accepted | 저장소 root 유지관리 영역과 배포 payload source를 분리하고 W-001을 PR #3에서 구현 | [SPEC §3.1](./changes/2026-09-09-multilingual-template/02-SPEC.md), Origin PR #3 리뷰 F-001 | source root 직접 복사 중단; v1.7.1 snapshot 보존 | Chae Sangwon, 2026-09-09 대화 |
| D-002 | 2026-09-09 | Accepted | common+locale 합성 artifact, locale별 skill S2 계약과 host-neutral installer를 포함한 v2 전체 구조 | [다국어 템플릿 SPEC](./changes/2026-09-09-multilingual-template/02-SPEC.md) | v2 breaking change; release host는 구현 중 확정 | Chae Sangwon, 2026-09-09 대화 |
| D-003 | 2026-09-17 | Accepted | 공개 저장소 identity를 `jaff2836/coding-agent-docs-template`로 사용하고 W-007은 공개 release 없이 local exact-head·소비자 probe까지 검증 | [PLAN W-007](./changes/2026-09-09-multilingual-template/03-PLAN.md) | GitHub 게시, immutable release host와 bootstrap URL 검증은 별도 작업 | Chae Sangwon, 2026-09-17 대화 |
| D-004 | 2026-09-18 | Accepted | v2 artifact를 GitHub Releases에서만 관리하고 `latest`에서 선택한 version을 exact `v<SemVer>` tag asset으로 검증 | [GitHub Releases 공개 배포 SPEC](./changes/2026-09-18-github-releases-publication/02-SPEC.md) | D-002의 host-neutral·redirect 전면 거부 transport를 대체; GitHub HTTPS asset redirect만 제한 허용 | Chae Sangwon, 2026-09-18 대화 |
| D-005 | 2026-09-18 | Accepted | 전체 프로젝트 분석 절차를 locale별 self-contained `project-analysis` skill로 이관하고 세 번들 skill의 목적을 README에 공개 | [project-analysis skill 변경](./changes/2026-09-18-project-analysis-skill/01-CHANGE.md) | 별도 분석 문서와 skill adapter 병행 대신 단일 skill 정본; 다음 release에서 artifact inventory 변경 | Chae Sangwon, 2026-09-18 대화 |
| D-006 | 2026-09-19 | Accepted | 기존 저장소를 주 adoption 시나리오로 두고 `installer.py adopt`로 검증된 staging tree와 읽기 전용 실험적 adoption report를 제공. 경로별 policy는 `locales/manifest.json`이 소유하고 release manifest `schema_version` 2에 materialize | [기존 저장소 adoption SPEC](./changes/2026-09-18-existing-repository-adoption/02-SPEC.md) | 문서만 보강, 자동 추가·overwrite, installer 내장 policy, 공개 report schema, agent prompt를 기각. D-002의 수동 merge 계약을 확장하고 D-004 transport는 유지; `v2.1.0` minor release | Chae Sangwon, 2026-09-19 대화 — 결정 1~7 권고안 승인 |
| D-007 | 2026-09-20 | Accepted | release 준비를 candidate와 published의 두 읽기 전용 검증 단계로 자동화하고 tag·release mutation은 사람이 수행 | [release 검증 변경](./changes/2026-09-20-release-verification/01-CHANGE.md) | 수동 반복과 특정 CI 자동 게시를 기각; D-004의 transport·게시 경계를 유지하고 검증만 확장 | Chae Sangwon, 2026-09-20 대화 — T-008 진행 요청 |
| D-008 | 2026-09-20 | Accepted | `adopt --base-version <older-exact-semver>`으로 검증된 base·current release inventory 합집합을 target과 3-way 분류하고 base 모드에만 experimental format 2 report를 제공 | [base-aware adoption 변경](./changes/2026-09-20-adopt-upgrade-classification/01-CHANGE.md) | 과거 installer 자동 실행, 모든 schema 일반 호환과 로컬 base path를 기각. base 전용 schema 1·2 검증, base 없는 format 1, 대상 무변경과 자동 merge·삭제 없음 유지; `v2.2.0` minor release | Chae Sangwon, 2026-09-20 대화 — 권고 계약 승인, 이후 별도 요청으로 구현 시작 |
| D-009 | 2026-09-22 | Accepted | locale guide를 artifact 정본으로 두고 root guide는 maintainer addendum으로 축약하며, `project-analysis` Metadata를 제거하고 선택형 changelog 안내를 `v2.3.0` artifact에 추가 | [문서 소유권 변경](./changes/2026-09-22-documentation-ownership/01-CHANGE.md) | 수동 복제·생성 계층·root-only 안내·실제 changelog 자동 생성을 기각. 기존 프로젝트 문서 보존과 source/artifact별 release history 검증 유지 | Chae Sangwon, 2026-09-22 대화 — T-010 권고안과 `docs/` changelog 안내 승인 |
| D-010 | 2026-09-23 | Accepted | 새 프로젝트용 `install`은 존재하지 않는 경로나 빈 디렉터리만 허용하고 비어 있지 않거나 emptiness를 확인할 수 없는 대상은 쓰기 전에 거부하며 기존 저장소에는 `adopt`를 안내 | [install 대상 계약 변경](./changes/2026-09-22-install-target-contract/01-CHANGE.md) | artifact 경로 충돌만 거부하는 기존 구현과 문서 완화를 기각. 겹치지 않는 파일이 있는 대상도 실패하지만 D-006의 `install`·`adopt` 역할과 사용자 tree 보존을 강제 | Chae Sangwon, 2026-09-23 대화 — A안 권고 뒤 계속 진행 승인 |
| D-011 | 2026-09-25 | Accepted | Windows installer는 Python 3.12 이상에서 현재 검사하는 root·output 자체, 직접 부모와 member 경로의 symlink·junction을 거부하고, 더 위의 상위 경로 검사는 확대하지 않음 | [T-017 경계 설계](./changes/2026-09-23-windows-junction-boundary/01-CHANGE.md) R-001~R-005 | 기존 POSIX symlink 경로와 Windows 사용자 프로필 junction의 호환성을 보존; 더 넓은 상위 경로 차단은 이번 범위에서 제외. 구현·native 회귀는 별도 PR | Chae Sangwon, 2026-09-25 대화 — 1번 안 선택 |

중요한 결정이 많아지면 개별 ADR 문서로 분리하고 여기에는 링크와 요약만 남깁니다.

결정 상태와 정본 위치는 이 표가 기준입니다. `D-nnn`은 이 표에 등재할 때 전역으로 발급합니다. 표의 `D-001` 행은 자리 표시이므로 적용 시 삭제하거나 실제 결정으로 교체하세요. 변경 폴더의 `R-001` 등과 같은 번호대가 아닙니다. 상세 설계에 이유·대안·영향이 있으면 여기에는 링크와 요약만 남깁니다. 승인한 사람·범위·확인 가능한 근거를 연결하고, 기존 결정을 대체하면 삭제하지 않고 `Superseded`로 남깁니다. 기존 결정 ID를 파일 번호에 맞춰 재번호하지 않습니다.

## 9. Delivery Strategy

### Phase 1 — source boundary

- root maintainer plane과 `template/common`·`locales/ko`를 분리합니다.
- baseline inventory 보존과 root 직접 복사 금지를 검증합니다.

### Phase 2 — multilingual delivery

- 승인된 순서에 따라 `en`, locale parity 검사, deterministic packaging과 installer를 구현합니다.
- exact-head consumer E2E와 공개 release를 분리해 판정합니다. 로컬 consumer E2E 통과가 원격 release 게시·검증을 뜻하지 않습니다.

### Phase 3 — public release

- GitHub Releases 전용 transport를 검증하고 exact source commit에 `v2.0.0` tag와 동일 byte asset을 게시합니다.
- 게시 시점의 Origin·GitHub `main`은 같은 commit이어야 하며 tag commit은 그 `main`의 조상이어야 합니다. `main`이 tag 이후 전진했더라도 검증된 draft asset은 재패키징·교체하지 않습니다.
- `latest`와 exact version의 원격 en/ko install·export를 확인하고 공개 완료 근거를 별도 기록합니다.
- 다음 release부터 `verify-release.py candidate`로 기존 draft를 게시 전에, `published`로 immutable Latest와 공개 installer 경로를 게시 후에 검증합니다. 이 도구는 tag·release를 만들거나 변경하지 않습니다.

### Phase 4 — base-aware existing-repository upgrade report

- 더 낮은 exact SemVer의 base release를 과거 코드 실행 없이 검증하고 `base ∪ current` 경로의 3-way 분류를 추가했습니다.
- base 없는 format 1과 target 불변을 회귀로 고정하고, 공개 `v2.2.0`과 v2.1 적용 consumer에서 base-aware report를 독립 대조했습니다.

### Phase 5 — documentation ownership

- locale guide를 artifact 정본으로 유지하고 root maintainer guide와 책임을 분리합니다.
- 선택형 changelog 안내를 배포하되 적용 프로젝트의 실제 release notes는 만들거나 덮어쓰지 않습니다.
- source·artifact의 각 정본 이력을 검사하고 `v2.3.0` release gate에서 새 inventory를 검증했습니다.

## 10. Risks

| Risk | Likelihood | Impact | Mitigation | Trigger/Signal |
| ---- | ---------- | ------ | ---------- | -------------- |
| maintainer 문서가 artifact에 포함됨 | Medium | High | manifest의 닫힌 inventory와 artifact 부재 검사 | root 전용 path가 archive member에 등장 |
| locale 번역의 행동 계약 drift | Medium | High | stable marker·fixture·사람의 최종 검수 | locale parity 또는 소비자 E2E 실패 |
| installer가 기존 문서를 덮어씀 | Low | High | 충돌 시 전체 중단, `--force` 미제공 | before/after tree hash 차이 |
| release asset redirect가 신뢰 경계를 넓힘 | Low | High | 검증된 GitHub asset URL에서 시작한 HTTPS chain만 허용하고 exact tag checksum 검증 | HTTP downgrade, 비-release 시작점 또는 checksum 불일치 |
| `adopt` report를 자동 병합 승인으로 오해하거나 대상에 기록 | Medium | High | 대상 밖 output 강제, `decision` 분류, 실험적 report 표시와 대상 tree 불변 테스트 | 대상 before/after snapshot 차이 또는 `LICENSE` 무단 추가 |
| base 비교를 위해 검증되지 않은 과거 installer를 실행하거나 legacy parser가 current 검증을 느슨하게 함 | Low | High | base installer는 opaque byte로만 검증, schema 1·2 exact-key parser를 base 경로에 격리, 나머지 schema fail-closed | subprocess/import 감시 실패, current 명령에서 legacy schema 수용 |
| 수동 release gate에서 source·asset·remote 근거가 어긋남 | Medium | High | candidate는 exact source·두 remote·draft asset byte를, published는 immutable Latest asset과 package의 installer를 통한 공개 E2E를 각각 한 실행에 결합 | 단계별 검증 대상 SHA·version 불일치 또는 일부 locale 누락 |
| 비어 있지 않은 기존 저장소에 `install`이 파일을 추가 | Medium | High | 새 경로·빈 디렉터리 preflight와 불변 snapshot 회귀, 기존 저장소에는 읽기 전용 `adopt` 안내 | 겹치지 않는 `existing.txt`가 있는 대상에서 install 성공 또는 tree 변경 |

## 11. Open Questions

`v2.3.0` 범위는 D-009와 T-010, `v2.3.1` 범위는 T-015로 완료했습니다. D-010·T-016의 `install` 대상 계약은 `v2.3.2`에 포함됐고 T-018 candidate와 T-019 공개·published 검증 및 기록 통합을 마쳤습니다. install 안내·preflight 순서·리뷰 불변조건 권고는 Backlog의 독립 PR 단위로 둡니다. Windows Python 3.12 하한과 junction 경계는 [D-011](./changes/2026-09-23-windows-junction-boundary/01-CHANGE.md)로 확정하고 Origin PR #38 merge `b5a9c4e` 및 GitHub `main`에 구현을 반영했습니다. Origin의 Buildkite Windows·Linux pipeline은 정확한 head에서 전체 gate를 통과했고, Windows Python 3.12.10의 PR #37 native probe로 구현 전 installer의 junction 허용을 재현했습니다. PR #37을 연 직후에는 기존 head check가 표시됐고 새 build는 관찰되지 않았지만, 이후 PR head push는 PR 정보가 연결된 두 build와 성공 check를 자동 생성했습니다. 최종 head `cc67e31`의 두 check 통과 후 Origin PR #37을 `9d53913`에 병합하고 GitHub `main`에도 fast-forward로 반영했습니다. 두 check는 Origin `main` 병합 필수 조건입니다. T-017 구현 head `42d9923`에서 Windows Buildkite #27·Linux #12가 통과했고, T-023 release 후보 회귀가 다음 candidate의 선행조건입니다. 운영 회귀 방지와 `.gitattributes` 목적 문서화는 T-013, 병렬 리뷰 ID 정리는 T-014의 후속 후보입니다. `en`·`ko` 외 community locale은 구현 범위가 아니라 §12의 별도 재검토 후보입니다.

## 12. Rejected or Deferred Ideas

- `en`·`ko` 외 공식 locale은 v2 계약과 두 필수 locale 지원 검증 후 재검토합니다.
- 기존 적용 저장소의 자동 update·overwrite는 사용자 문서 손실 위험 때문에 첫 버전에서 제외합니다.

## 13. 설계 문서 인덱스

| 범위 | 정본 | 상위 설계와의 관계 | 적용 조건 |
|---|---|---|---|
| 기본 제품 설계 | 이 문서 | 저장소 현재 상태와 승인된 결정 | root 유지관리 작업 |
| 다국어 배포 변경 | [2026-09-09-multilingual-template SPEC](./changes/2026-09-09-multilingual-template/02-SPEC.md) | D-001을 구현하고 D-002를 제안 | 연결된 PLAN의 승인 범위 |
| GitHub Releases 공개 배포 | [2026-09-18-github-releases-publication SPEC](./changes/2026-09-18-github-releases-publication/02-SPEC.md) | D-004가 D-002의 host-neutral transport를 대체 | v2 공개 배포와 installer transport |
| 프로젝트 전체 분석 skill | [2026-09-18-project-analysis-skill](./changes/2026-09-18-project-analysis-skill/01-CHANGE.md) | D-005가 D-002의 locale skill bundle을 확장 | 전체 분석 명시 요청과 다음 artifact release |
| 기존 저장소 adoption | [2026-09-18-existing-repository-adoption SPEC](./changes/2026-09-18-existing-repository-adoption/02-SPEC.md) | D-006이 D-002의 수동 export/merge 계약을 확장하고 release manifest를 schema 2로 갱신 | 기존 저장소 적용, installer·packager·locale manifest 변경 |
| release 검증 자동화 | [2026-09-20-release-verification](./changes/2026-09-20-release-verification/01-CHANGE.md) | D-007이 D-004의 사람이 소유한 게시 경계를 유지하며 게시 전후 검증을 자동화 | maintainer release candidate와 공개 완료 검증 |
| base-aware adoption 분류 | [2026-09-20-adopt-upgrade-classification](./changes/2026-09-20-adopt-upgrade-classification/01-CHANGE.md) | D-008이 D-006의 읽기 전용 report를 선택형 3-way upgrade 분류로 확장 | 기존 적용 저장소를 다음 exact release와 비교할 때 |
| 문서 소유권과 changelog 안내 | [2026-09-22-documentation-ownership](./changes/2026-09-22-documentation-ownership/01-CHANGE.md) | D-009가 locale artifact 안내와 root maintainer 보충 문서의 소유권을 분리 | `v2.3.0` 문서 inventory·skill·checker 변경 |
| 새 프로젝트 install 대상 계약 | [2026-09-22-install-target-contract](./changes/2026-09-22-install-target-contract/01-CHANGE.md) | D-010이 D-002·D-006의 `install`·`adopt` 역할 경계를 새 경로·빈 디렉터리 preflight로 명확화 | installer·root README·locale 적용 가이드 변경 |

선택형 문서를 사용하지 않으면 해당 행과 링크를 제거합니다. 개별 변경 SPEC은 §8의 결정에서 연결합니다. 문서 번호나 작성일만으로 다른 설계 전체를 대체하지 않습니다.
