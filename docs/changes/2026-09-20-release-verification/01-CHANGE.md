# 변경: release 검증 절차 자동화

## Metadata

- **Change ID:** `2026-09-20-release-verification`
- **Status:** Accepted
- **Originator:** Chae Sangwon
- **Source:** 2026-09-20 사용자 대화 — T-008까지 진행하고 T-009의 작업 단위 선택지를 제안하도록 요청
- **Parent:** [제품 기준](../../00-PROJECT.md) D-004와 [GitHub Releases 공개 배포 SPEC](../2026-09-18-github-releases-publication/02-SPEC.md) R-007·R-008
- **Decision:** PROJECT §8 D-007
- **Approval:** Chae Sangwon, 2026-09-20 사용자 대화 — release 게시가 아닌 검증 절차만 자동화
- **Execution:** [전역 TODO](../../02-TODO.md)의 T-008

## 1. Intent

### 1.1 문제

`v2.0.0`과 `v2.1.0`은 같은 release gate와 공개 후 원격 E2E를 수작업으로 반복했습니다. 검사 명령, package 재현성, 두 Git remote의 기준점, draft asset byte, 공개 release의 installer 경로를 사람이 따로 확인하면 누락되거나 서로 다른 source를 검증할 위험이 있습니다.

### 1.2 기대 결과

- maintainer가 clean exact-source checkout에서 게시 후보와 공개 완료 상태를 각각 한 명령으로 검증합니다.
- 후보 검증은 local gate와 package 재현성, Origin·GitHub ref, 이미 만든 draft asset을 결합합니다.
- 공개 후 검증은 immutable Latest release의 asset과 `latest`·exact version의 모든 공식 locale 경로를 결합합니다.
- 도구는 검증 결과만 보고하고 Git ref나 GitHub release를 생성·수정·게시·삭제하지 않습니다.

### 1.3 범위와 비범위

범위는 root maintainer용 `scripts/verify-release.py`, 내부 모듈, 회귀 테스트와 사용 문서입니다. `git push`, tag 생성·삭제, GitHub release 생성·수정·게시·asset upload·삭제, 특정 CI 제품의 workflow, locale artifact inventory와 공개 installer 계약 변경은 포함하지 않습니다.

### 1.4 제약

- Python production dependency를 추가하지 않고 기존 표준 라이브러리 모듈과 maintainer 환경의 `git`·`gh`만 사용합니다.
- candidate는 사람이 annotated tag와 draft release를 준비한 뒤, publish 전에 실행합니다.
- published는 공개 release를 변경하지 않고 GitHub API·asset과 installer의 공개 HTTPS 경로만 읽습니다.
- 검증 중 생성하는 package, install, export와 adoption output은 임시 디렉터리에만 둡니다.

### 1.5 미해결 질문

없습니다. candidate의 실제 draft 성공 경로는 `v2.1.1`·`v2.2.0`·`v2.3.0`·`v2.3.1`·`v2.3.2`에서 운영 검증했습니다.

## 2. Spec

### 2.1 요구사항과 시나리오

| 요구사항 ID | 요구사항 | 상황·입력 | 관찰 가능한 결과 | 검증 방법 |
|---|---|---|---|---|
| R-001 | candidate는 선언한 source commit의 clean checkout에서 정규 source gate를 실행합니다. | `candidate`와 exact commit | 전체 unittest, root docs, stable locale, `git diff --check`가 통과하고 전후 HEAD·tree가 exact clean 상태 | orchestration unit test, 다음 draft 운영 검증 |
| R-002 | candidate package는 두 번 byte-identical해야 합니다. | 같은 version·source·repository로 두 번 package | asset inventory·모든 byte·manifest가 다르면 실패 | package 비교 unit test |
| R-003 | release ref는 두 remote와 exact source에 결합합니다. | Origin·GitHub remote, annotated `v<SemVer>` tag | 두 `main`이 같고 GitHub와 local annotated tag가 exact source를 가리키며 source가 동기화된 `main`의 조상 | ref 성공·drift·lightweight tag unit test |
| R-004 | candidate는 기존 draft의 상태와 asset을 확인합니다. | 사람이 만든 GitHub draft | draft-aware release 조회에서 `draft=true`, `immutable=false`, 정확한 tag이며 local package 5개와 inventory·byte가 같을 때만 통과 | `gh release view` 계약·release shape·download·orchestration unit test, 다음 draft 운영 검증 |
| R-005 | published는 immutable Latest release와 local package를 대조합니다. | 공개된 exact release | `draft=false`, `immutable=true`, `prerelease=false`, GitHub Latest identity 일치, asset inventory·byte 일치 | published unit test, `v2.1.0` 실환경 검증 |
| R-006 | published는 모든 공식 locale과 두 version selector를 공개 경로로 검증합니다. | `latest`·exact version, `en`·`ko` | package의 `installer.py` CLI로 실행한 `list-locales`·`install`·`export`·`adopt`와 tag source export가 같고 artifact checker가 통과하며 install 충돌·adopt 대상은 불변 | packaged-installer materialization unit test, `v2.1.0` 실환경 검증 |
| R-007 | 검증은 fail-closed이고 remote state를 변경하지 않습니다. | 잘못된 identity·ref·metadata·asset·tree 또는 외부 명령 실패 | 즉시 비정상 종료하며 remote mutation 명령을 제공하거나 호출하지 않음 | 입력·CLI·실패 경로 unit test, 코드 검토 |

### 2.2 대안과 선택 이유

- **수동 절차 유지:** 새 코드가 없지만 두 release에서 이미 긴 절차와 근거가 반복됐고 exact source·asset·원격 E2E 사이의 연결을 누락할 수 있어 기각했습니다.
- **특정 CI workflow로 자동 게시:** 중앙 기록은 남지만 runner가 정해지지 않았고 tag·release 쓰기 권한과 되돌리기 어려운 동작까지 범위가 넓어져 선택하지 않았습니다.
- **검증 전용 maintainer CLI:** 기존 packager·installer를 재사용하면서 사람이 소유한 게시 경계를 유지하고 로컬과 원격 근거를 한 실행으로 묶을 수 있어 선택했습니다.

### 2.3 설계와 계약

`scripts/verify-release.py`는 얇은 CLI이고 `scripts/verify_release.py`가 두 subcommand를 구현합니다.

- `candidate`: clean exact-source gate → 두 번 package → remote `main`·annotated tag 확인 → draft-aware metadata 조회와 기존 draft asset byte 확인
- `published`: clean exact-source package → 같은 remote ref 확인 → immutable Latest metadata·asset byte 확인 → package의 `installer.py`를 실행해 `latest`와 exact version의 locale별 공개 `list-locales`·`install`·`export`·`adopt` 확인

두 명령은 version, source commit과 GitHub repository identity를 명시적으로 받고, URL이나 option이 Git remote 위치에 주입되지 않도록 설정된 remote 이름만 허용합니다. `gh`는 읽기 API와 asset download에만 사용합니다. 공개 installer E2E는 byte가 local package와 같다고 확인한 installer를 사용해 검증된 GitHub HTTPS release 경로를 읽습니다.

### 2.4 상위 설계에 미치는 영향

D-004의 transport·source identity·게시 순서는 유지합니다. D-004가 비범위로 둔 release 자동화 중 읽기 전용 검증만 D-007로 좁게 추가하며, tag와 release의 모든 mutation은 계속 사람의 명시적 작업입니다. locale artifact와 installer 공개 계약은 바뀌지 않습니다.

### 2.5 위험·호환성·rollback

| 위험 | 영향 | 완화·rollback |
|---|---|---|
| candidate 통과를 release 게시 권한으로 오해 | 잘못된 공개 작업 | CLI와 문서에 verification-only 경계를 고정하고 게시 명령을 구현하지 않음 |
| GitHub metadata나 `gh` 동작 변경 | 검증 실패 | fail-closed하고 실패 원인을 출력; 원격 상태는 건드리지 않으므로 도구를 수정하거나 기존 수동 gate로 rollback |
| 공개 E2E가 기존 저장소를 변경 | 사용자 데이터 손상 | 임시 fixture만 사용하고 `adopt`·실패한 install의 before/after snapshot을 대조 |
| source와 공개 asset의 우연한 불일치 | 잘못된 release를 정상 판정 | exact tag·remote main·package byte·Latest identity를 독립적으로 모두 확인 |

### 2.6 완료 조건과 미해결 사항

브랜치 구현 완료는 새 unit test, 전체 unittest, root docs, stable locale, Python compile과 `git diff --check` 통과입니다. 공개 경로는 immutable `v2.1.0`의 exact checkout에서 최초 실환경 `published` 검증으로 확인했고, 실제 `candidate`와 `published` 성공 경로는 `v2.1.1`·`v2.2.0`·`v2.3.0`·`v2.3.1`·`v2.3.2`에서 반복 검증했습니다. `v2.2.0`부터는 각각 직전 release를 `--base-version`으로 지정해 모든 공식 locale의 base-aware 공개 E2E를 확인했습니다. Origin 통합과 공개는 각각 실제 remote 상태로 확인합니다.

## 3. 변경 기록

- 2026-09-20: T-008 범위를 게시 전후 검증 전용 maintainer CLI로 확정하고 remote mutation과 특정 CI workflow를 제외했습니다.
- 2026-09-20: unit test와 공개된 immutable `v2.1.0` 기준 실환경 `published` 검증을 수행했습니다.
- 2026-09-20: PR #20 리뷰에 따라 candidate의 draft-aware 조회를 고정하고 published E2E가 package의 installer를 직접 실행하도록 수정했습니다.
- 2026-09-21: `v2.1.1` exact source `0cfcc896ee92ec018d12c88f3f2638a154b35720`과 synchronized `main` `d821dec23b0e34295b96f9af0690ba15f2d33edb`에서 실제 draft candidate와 immutable published 검증이 통과했습니다. 검증된 5개 asset은 게시 전후 교체하지 않았습니다.
- 2026-09-21: synchronized Origin·GitHub `main`과 annotated tag가 가리키는 `v2.2.0` exact source `70a5a7a9e97fa5a89609a120ad69bced7e8ae1ac`에서 candidate와 immutable published `--base-version 2.1.0` 검증이 통과했습니다. 검증된 5개 asset은 게시 전후 교체하지 않았습니다.
- 2026-09-22: synchronized Origin·GitHub `main`과 annotated tag가 가리키는 `v2.3.0` exact source `5066d821084545554588182f5250cc9dea12e444`에서 candidate와 immutable published `--base-version 2.2.0` 검증이 통과했습니다. 검증된 5개 asset은 게시 전후 교체하지 않았습니다.
- 2026-09-22: synchronized Origin·GitHub `main`과 annotated tag가 가리키는 `v2.3.1` exact source `3460e4ccd0065bcd8a24fd64a6cd7135293926a0`에서 candidate와 immutable published `--base-version 2.3.0` 검증이 통과했습니다. 검증된 5개 asset은 게시 전후 교체하지 않았습니다. 후속 native Windows 10.0.28000·PowerShell·Python 3.14.7 실행도 synchronized `main` `969d1ed48414cee30e698067417d40122a1b8f59`과 같은 5개 asset을 확인하고 exit code 0으로 통과했습니다.
- 2026-09-23: synchronized Origin·GitHub `main`과 annotated tag가 가리키는 `v2.3.2` exact source `4c6a798885404fdf5170769e271f7d06f4959234`에서 candidate가 통과한 5개 asset을 교체 없이 immutable Latest로 공개했습니다. 공개 직후 tag source의 verifier는 새 `install` 거부 문구를 구형 문구로만 판정해 실패했고, T-019 verifier 보완 뒤 clean exact source를 `--root`로 지정한 `published --base-version 2.3.1`이 통과했습니다. 이 gate는 en·ko의 latest·exact 경로, artifact와 겹치거나 무관한 파일이 있는 install 대상의 거부·tree 불변을 확인합니다.
