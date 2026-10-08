# 변경: installer 기본값·Python 하한과 maintainer 정합 검사

## Metadata

- **Change ID:** `2026-10-08-installer-defaults-and-maintainer-checks`
- **Status:** Draft
- **Originator:** Chae Sangwon
- **Source:** 2026-10-08 사용자가 프로젝트 구조·설치 개선안을 물었고, 제안한 다섯 가지 가운데 1(installer `--release-url` 기본값), 2(root 사본 동기화 검사), 3(Python 하한 통일)을 적용하는 구조를 설계하고 4(README locale 표와 manifest 대조)는 check-docs 쪽에 넣으라고 지시했습니다.
- **Parent:** [GitHub Releases 공개 배포 SPEC](../2026-09-18-github-releases-publication/02-SPEC.md) §3.1(D-004), [T-017 경계 설계](../2026-09-23-windows-junction-boundary/01-CHANGE.md)(D-011의 Windows Python 3.12 하한), [문서 소유권 설계](../2026-09-22-documentation-ownership/01-CHANGE.md)(D-009의 root addendum)
- **Decision:** 합의 뒤 PROJECT §8에 등재합니다.
- **Approval:** 미합의. §1.5의 질문에 대한 사용자 선택을 기다립니다.
- **Execution:** [전역 TODO](../../02-TODO.md)의 T-049(maintainer 정합 검사), T-050(installer 기본값과 Python 하한), T-051(`v2.6.0` release)

## 1. Intent

### 1.1 문제와 확인한 근거

**1. installer 명령이 깁니다.**
- `scripts/installer.py`의 `_add_remote_arguments`가 `--release-url`을 모든 원격 명령의 필수 인자로 둡니다. 그래서 README와 guide의 명령마다 `--release-url https://github.com/jaff2836/coding-agent-docs-template/releases`가 붙습니다.
- release root는 D-004 SPEC §3.1에서 이미 하나로 정해져 있습니다. `--version`은 이미 기본값이 `latest`입니다.

**2. root 사본이 ko 원본과 어긋나도 알 수 없습니다.**
- root `docs/REVIEW.md`, `docs/REVIEW_ROUND.md`, `.cursor/BUGBOT.md`는 `locales/ko/`의 같은 파일에 이 저장소의 내용을 채운 사본입니다.
- 지금 차이는 프로젝트가 채우는 절에만 있습니다: REVIEW §6 불변조건과 §9 deferral 행, REVIEW_ROUND §2.1 리뷰어 행, BUGBOT 불변조건과 결정·deferral 목록.
- 이 사본은 T-036~T-038처럼 계약을 고칠 때 손으로 맞춥니다. 둘을 대조하는 검사가 없어서, 한쪽만 고쳐도 문서 검사를 통과합니다. 지금 root `scripts/check-docs.py`가 maintainer 전용으로 대조하는 것은 `project-analysis` 스킬 사본뿐입니다.

**3. Python 하한이 OS마다 다릅니다.**
- installer는 Windows에서만 3.12 미만을 거부합니다(`_require_supported_python`, D-011). Linux·macOS의 하한은 정한 적이 없습니다.
- CI는 Linux 3.13.5, Windows 3.12.10으로 돕니다. 3.12 미만에서 동작하는지는 어떤 OS에서도 검증하지 않습니다.

**4. README locale 표를 손으로 맞춥니다.**
- PR #69에서 root README에 현재 release의 locale 표(`en`·`ko`, `complete`)를 넣었습니다. locale을 추가하거나 상태가 바뀌면 이 표가 `locales/manifest.json`과 어긋날 수 있습니다.

### 1.2 기대 결과

- 공식 release를 쓰는 사용자는 `--release-url` 없이 installer를 실행할 수 있습니다. 다른 저장소의 release를 쓰려면 지금처럼 명시합니다.
- root 사본과 ko 원본이 프로젝트 소유 절 밖에서 다르면 문서 검사가 실패합니다.
- installer가 모든 OS에서 Python 3.12 이상을 요구하고, 그보다 낮으면 release·대상에 접근하기 전에 멈춥니다.
- README locale 표가 manifest의 `complete` locale과 다르면 문서 검사가 실패합니다.

### 1.3 범위와 비범위

**범위:**
- `scripts/installer.py`: `--release-url` 기본값, 모든 OS의 Python 3.12 하한, 관련 테스트
- root `scripts/check-docs.py`: root 사본 동기화 검사, README locale 표 검사, 관련 테스트
- en·ko `docs/TEMPLATE_GUIDE.md`의 Python 하한 문장, PROJECT External Boundaries, release 문서
- release 공개 뒤 root README의 설치 명령

**비범위:**
- payload `template/common/scripts/check-docs.py`. 적용 프로젝트에는 manifest와 root 사본이 없습니다.
- locale guide·`AGENTS.md`·manifest `required_commands`의 installer 명령. 명시적인 `--release-url`은 기본값이 생겨도 유효합니다.
- maintainer 도구(packager, verifier, exporter)의 Python 하한. 이 도구들은 CI에서 3.12·3.13으로 돕니다.
- 기존 release의 installer와 그 지원 범위

### 1.4 제약

- **README 시점:** root [TEMPLATE_GUIDE.md](../../TEMPLATE_GUIDE.md) §6은 README가 현재 공개 동작만 설명한다고 정합니다. `--release-url`을 뺀 명령은 새 installer를 공개한 뒤에만 README에 씁니다.
- **D-004:** release root, exact tag 검증, redirect 경계는 그대로 둡니다. 기본값도 명시한 값과 같은 검증을 거칩니다.
- **공통:** 새 의존성이나 CI 제품을 추가하지 않습니다. en·ko 구조 parity와 기존 검사를 통과해야 합니다.

### 1.5 합의할 질문

1. **Q1 — 기본 release URL을 어디서 정할지:** 권고는 installer source의 상수(A1)입니다(§2.2).
2. **Q2 — 명령 문서를 어디까지 바꿀지:** 권고는 공개 뒤 root README만 바꾸는 것(B1)입니다. locale guide와 `required_commands`는 그대로 둡니다.
3. **Q3 — release version:** 권고는 호환성 안내를 붙인 `v2.6.0`(C1)입니다. Linux·macOS의 Python 3.12 미만 사용자에게는 이전 installer로 정확한 version을 쓰는 대안을 안내합니다.
4. **Q4 — 사본 대조에서 허용할 차이를 어떻게 정할지:** 권고는 root wrapper가 heading으로 프로젝트 소유 절을 찾는 것(D1)입니다. payload에 새 marker를 넣지 않습니다.

## 2. Spec

### 2.1 요구사항과 시나리오

**T-050 installer**

- **R-001 기본 release URL (Q1)**
  - 상황: `python3 installer.py list-locales --version latest`처럼 `--release-url` 없이 원격 명령을 실행
  - 결과: 공식 release root `https://github.com/jaff2836/coding-agent-docs-template/releases`를 씁니다. 명시한 값은 지금처럼 검증한 뒤 기본값보다 우선합니다. 잘못된 명시 값은 지금처럼 거부합니다.
  - 검증: 기존 `test_cli_requires_a_release_url`를 기본값 사용 테스트로 바꾸고, 잘못된 명시 값 거부 테스트를 유지합니다.
- **R-002 Python 3.12 하한**
  - 상황: Windows·Linux·macOS에서 Python 3.11 이하로 installer를 실행
  - 결과: release나 대상에 접근하기 전에 "Python 3.12 or newer is required"로 멈춥니다. 3.12 이상의 동작은 바뀌지 않습니다.
  - 검증: `os.name`과 `sys.version_info`를 바꾼 단위 테스트(POSIX 포함)와 red-green
- **R-003 문서 시점 (Q2)**
  - 결과: en·ko 적용 가이드의 Python 하한 문장과 PROJECT External Boundaries는 구현 PR에서 고칩니다. root README의 설치 명령에서 `--release-url`을 빼는 일은 그 installer를 공개한 뒤의 기록 PR에서 합니다. locale guide의 명령 계약은 그대로 둡니다.
  - 검증: 구현 PR과 기록 PR의 diff 대조

**T-049 maintainer 정합 검사 (root `scripts/check-docs.py`)**

- **R-004 root 사본 동기화 (Q4)**
  - 상황: root `docs/REVIEW.md`, `docs/REVIEW_ROUND.md`, `.cursor/BUGBOT.md` 가운데 하나가 `locales/ko/`의 같은 파일과 프로젝트 소유 절 밖에서 다름
  - 결과: 파일과 처음 다른 줄을 보고하며 실패합니다. 프로젝트 소유 절은 REVIEW §6과 §9 표의 행, REVIEW_ROUND §2.1 리뷰어 표의 행, BUGBOT의 불변조건 절과 결정·deferral 절입니다. 그 안의 차이는 허용합니다.
  - 검증: 소유 절 밖 차이를 넣으면 실패, 안의 차이는 통과하는 회귀 테스트와 red-green. 현재 저장소에서는 통과해야 합니다.
- **R-005 README locale 표**
  - 상황: root `README.md` 또는 `README.ko.md`의 locale 표(첫 열 머리글 `Locale`)가 manifest의 `complete` locale 목록이나 상태와 다름
  - 결과: 파일과 차이를 보고하며 실패합니다. 언어 이름 열은 비교하지 않습니다.
  - 검증: 표에서 locale을 빼거나 상태를 바꾸면 실패하는 회귀 테스트와 red-green

**공통**

- **R-006 계약 보존:** installer의 다른 인자와 동작, release manifest schema, artifact inventory, payload checker는 바뀌지 않습니다. 바뀌는 asset은 `installer.py`, 적용 가이드 문장이 바뀐 en·ko locale ZIP, 그에 따른 `SHA256SUMS`·manifest입니다.

### 2.2 대안과 선택 이유

**Q1 기본 URL의 출처**
- **A1 installer source 상수 (권고):** D-004가 release root를 하나로 정했으므로 상수 하나면 됩니다. fork는 `--release-url`을 쓰거나 상수를 바꿉니다.
- A2 packager가 package할 때 저장소를 installer byte에 넣기: fork에서도 자동으로 맞지만, installer byte가 release마다 달라지고 packager·verifier의 self-binding 검증을 함께 바꿔야 합니다.
- A0 기본값 없음: 문제 1이 남습니다.

**Q2 명령 문서**
- **B1 공개 뒤 root README만 (권고):** 명시적 플래그는 계속 유효하므로 locale guide와 계약은 그대로 둡니다. README만 짧아집니다.
- B2 locale guide·`required_commands`까지: payload 명령 계약이 바뀌어, 적용 프로젝트가 병합할 문서와 검사 변경이 늘어납니다. 이전 installer와 섞여 쓰일 때 혼동될 수 있습니다.

**Q3 release version**
- **C1 `v2.6.0` + 호환성 안내 (권고):** `v2.3.3`이 Windows 하한을 올릴 때도 호환성 안내와 이전 installer 대안을 붙였습니다. 기본 URL은 기존 사용법을 깨지 않는 추가입니다.
- C2 `v3.0.0`: Linux·macOS의 Python 3.11 이하 지원을 끊는 것을 SemVer상 breaking으로 엄격히 보는 선택입니다.

**Q4 사본 대조의 허용 차이**
- **D1 root wrapper가 heading으로 소유 절을 찾기 (권고):** payload를 바꾸지 않습니다. heading이 바뀌면 검사가 실패해 바로 드러납니다.
- D2 payload에 marker 추가: 경계가 더 분명하지만 en·ko payload와 manifest 계약을 바꿉니다.

### 2.3 설계와 계약

**installer (`scripts/installer.py`)**
- `DEFAULT_RELEASE_URL` 상수를 두고 `_add_remote_arguments`의 `--release-url`을 `required=False, default=DEFAULT_RELEASE_URL`로 바꿉니다. 이후 처리(`_validated_release_url` 등)는 같습니다.
- `_require_supported_python`이 OS와 관계없이 3.12 미만을 거부합니다. 오류 문구는 Windows junction 이유와 함께 하한을 알립니다.

**root `scripts/check-docs.py`**
- `check_root_copies()`: 세 파일 쌍을 줄 단위로 비교하기 전에 양쪽에서 프로젝트 소유 절을 지웁니다. 소유 절은 ko heading으로 찾고, heading을 찾지 못하면 실패합니다.
- `check_readme_locale_table()`: 두 README에서 첫 열 머리글이 `Locale`인 표를 읽고, `check_locales.complete_locales()`와 상태를 대조합니다.
- 두 검사는 인자 없는 maintainer 실행에서만 돕니다. `--root`로 artifact를 검사할 때는 실행하지 않습니다.

**문서**
- T-049 PR: root [TEMPLATE_GUIDE.md](../../TEMPLATE_GUIDE.md) §3(무인자 maintainer 검사 설명)과 root `DOCS_GUIDE.md`의 점검 목록
- T-050 PR: [en](../../../locales/en/docs/TEMPLATE_GUIDE.md)·[ko](../../../locales/ko/docs/TEMPLATE_GUIDE.md) 적용 가이드 §2(Python 하한)와 PROJECT External Boundaries
- 기록 PR(공개 뒤): root README 명령에서 `--release-url`을 빼고 Prerequisites를 "Python 3.12 이상"으로 바꿉니다.

### 2.4 상위 설계에 미치는 영향

- **D-004:** release root는 그대로입니다. CLI 인자가 필수에서 기본값이 있는 선택으로 바뀝니다.
- **D-011:** Windows에 한정한 3.12 하한을 모든 OS로 넓힙니다. junction 경계는 그대로입니다.
- **D-009:** root addendum 소유권은 그대로이고, root 사본이 ko 원본과 맞는지를 검사로 강제합니다.

### 2.5 위험·호환성·rollback

- **Linux·macOS의 Python 3.11 이하 사용자:** 새 installer가 거부합니다. release notes에 이전 release의 `installer.py`를 정확한 `--version`으로 쓰는 대안을 적습니다.
- **3.12의 POSIX 검증 공백:** CI는 Linux 3.13, Windows 3.12입니다. POSIX의 3.12는 CI로 검증하지 않습니다(위험 낮음, 기록).
- **fork:** 기본 URL이 공식 저장소를 가리키므로 fork는 `--release-url`을 명시해야 합니다. 안내에 적습니다.
- **heading 의존:** ko heading이 바뀌면 사본 검사가 실패합니다. 이것은 의도된 동작이며 오류 문구에 원인을 적습니다.
- **rollback:** installer는 다음 release에서 되돌리면 됩니다. 검사는 maintainer 도구라 PR 하나로 되돌릴 수 있습니다.

### 2.6 완료 조건과 실행 순서

1. **이 설계 PR:** Q1~Q4를 합의한 뒤 `Accepted`로 바꾸고 PROJECT §8에 결정을 등재합니다.
2. **T-049 구현 PR:** root `scripts/check-docs.py`의 두 검사와 테스트입니다. README 표가 있는 PR #69가 먼저 통합돼야 합니다. release가 필요 없습니다.
3. **T-050 구현 PR:** installer와 테스트, en·ko guide·PROJECT 문서입니다.
4. **T-051 release:** `v2.6.0` 준비 → tag·draft(사용자) → candidate → 공개(사용자) → published(Linux 로컬, Windows Buildkite) → 기록 PR(root README 명령과 Prerequisites)

## 3. 변경 기록

- 2026-10-08: 사용자 지시에 따라 초안을 작성했습니다.
