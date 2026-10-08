# 변경: installer 기본값·Python 하한과 maintainer 정합 검사

## Metadata

- **Change ID:** `2026-10-08-installer-defaults-and-maintainer-checks`
- **Status:** Accepted
- **Originator:** Chae Sangwon
- **Source:** 2026-10-08 사용자가 프로젝트 구조·설치 개선안을 물었고, 제안한 다섯 가지 가운데 1(installer `--release-url` 기본값), 2(root 사본 동기화 검사), 3(Python 하한 통일)을 적용하는 구조를 설계하고 4(README locale 표와 manifest 대조)는 check-docs 쪽에 넣으라고 지시했습니다.
- **Parent:** [GitHub Releases 공개 배포 SPEC](../2026-09-18-github-releases-publication/02-SPEC.md) §3.1(D-004), [T-017 경계 설계](../2026-09-23-windows-junction-boundary/01-CHANGE.md)(D-011의 Windows Python 3.12 하한), [문서 소유권 설계](../2026-09-22-documentation-ownership/01-CHANGE.md)(D-009의 root addendum)
- **Decision:** PROJECT §8의 D-018(T-050 installer: A1·B2·C2)과 D-019(T-049 maintainer 검사: D1)
- **Approval:** Chae Sangwon, 2026-10-08 선택 응답 — PR #70 version 1 head `3355cb5bbc797461236a28c45fc39e1512f00341`의 Q1 "installer source 상수", Q2 "locale guide와 계약까지", Q3 "v3.0.0", Q4 "heading으로 찾기". 나머지 요구사항과 설계는 같은 version에 권고안으로 함께 제시됐고, Q2·Q3 선택에 맞춰 R-003, §1.3, §2.3, §2.5, §2.6을 고쳤습니다. 리뷰 C70-B-001(=C70-A-001)에 따라 R-005를 부분집합 검사와 공개 기록 절차로 바꿨고, 사용자가 2026-10-08 "70은 1안으로"로 승인했습니다.
- **Execution:** [전역 TODO](../../02-TODO.md)의 T-049(maintainer 정합 검사), T-050(installer 기본값과 Python 하한), T-051(`v3.0.0` release)

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
- README locale 표에 manifest의 `complete` locale이 아닌 tag나 다른 상태가 있으면 문서 검사가 실패합니다.

### 1.3 범위와 비범위

**범위:**
- `scripts/installer.py`: `--release-url` 기본값, 모든 OS의 Python 3.12 하한, 관련 테스트
- en·ko 적용 가이드와 manifest `required_commands`, root `AGENTS.md` Commands의 installer 명령에서 `--release-url` 제거
- root `scripts/check-docs.py`: root 사본 동기화 검사, README locale 표 검사, 관련 테스트
- en·ko `docs/TEMPLATE_GUIDE.md`의 Python 하한 문장, PROJECT External Boundaries, release 문서
- release 공개 뒤 root README의 설치 명령

**비범위:**
- payload `template/common/scripts/check-docs.py`. 적용 프로젝트에는 manifest와 root 사본이 없습니다.
- maintainer 도구(packager, verifier, exporter)의 Python 하한. 이 도구들은 CI에서 3.12·3.13으로 돕니다.
- 기존 release의 installer와 그 지원 범위

### 1.4 제약

- **README 시점:** root [TEMPLATE_GUIDE.md](../../TEMPLATE_GUIDE.md) §6은 README가 현재 공개 동작만 설명한다고 정합니다. `--release-url`을 뺀 명령은 새 installer를 공개한 뒤에만 README에 씁니다.
- **D-004:** release root, exact tag 검증, redirect 경계는 그대로 둡니다. 기본값도 명시한 값과 같은 검증을 거칩니다.
- **공통:** 새 의존성이나 CI 제품을 추가하지 않습니다. en·ko 구조 parity와 기존 검사를 통과해야 합니다.

### 1.5 합의한 선택

2026-10-08 사용자가 Q1·Q4는 권고안을, Q2는 B2, Q3는 C2를 골랐습니다. 비교한 대안은 §2.2에 근거로 남깁니다.


1. **Q1 — 기본 release URL을 어디서 정할지:** 권고는 installer source의 상수(A1)입니다(§2.2).
2. **Q2 — 명령 문서를 어디까지 바꿀지:** 권고는 공개 뒤 root README만 바꾸는 B1이었고, 사용자는 locale guide와 명령 계약까지 바꾸는 B2를 골랐습니다.
3. **Q3 — release version:** 권고는 호환성 안내를 붙인 `v2.6.0`(C1)이었고, 사용자는 `v3.0.0`(C2)을 골랐습니다. Linux·macOS의 Python 3.12 미만 사용자에게는 이전 installer로 정확한 version을 쓰는 대안을 안내합니다.
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
  - 결과: en·ko 적용 가이드의 Python 하한 문장과 installer 명령, manifest `required_commands`, root `AGENTS.md` Commands, PROJECT External Boundaries는 T-050 구현 PR에서 고칩니다. installer 명령에서는 `--release-url`을 뺍니다. payload 문서와 installer가 같은 release로 함께 배포되므로 문서가 설명하는 동작과 배포되는 동작이 일치합니다. root README의 설치 명령은 README가 공개 동작만 설명하므로 `v3.0.0` 공개 뒤의 기록 PR에서 고칩니다.
  - 검증: 구현 PR과 기록 PR의 diff 대조

**T-049 maintainer 정합 검사 (root `scripts/check-docs.py`)**

- **R-004 root 사본 동기화 (Q4)**
  - 상황: root `docs/REVIEW.md`, `docs/REVIEW_ROUND.md`, `.cursor/BUGBOT.md` 가운데 하나가 `locales/ko/`의 같은 파일과 프로젝트 소유 절 밖에서 다름
  - 결과: 파일과 처음 다른 줄을 보고하며 실패합니다. 프로젝트 소유 절은 REVIEW §6과 §9 표의 행, REVIEW_ROUND §2.1 리뷰어 표의 행, BUGBOT의 불변조건 절과 결정·deferral 절입니다. 그 안의 차이는 허용합니다.
  - 검증: 소유 절 밖 차이를 넣으면 실패, 안의 차이는 통과하는 회귀 테스트와 red-green. 현재 저장소에서는 통과해야 합니다.
- **R-005 README locale 표 (리뷰 C70-B-001로 변경)**
  - 상황: root `README.md` 또는 `README.ko.md`의 locale 표(첫 열 머리글 `Locale`)에 manifest의 `complete` locale이 아닌 tag가 있거나, 상태 열이 `complete`가 아님
  - 결과: 파일과 차이를 보고하며 실패합니다. 표는 공개된 release를 설명하므로, source manifest에만 있고 아직 공개되지 않은 `complete` locale이 표에 없어도 실패하지 않습니다(부분집합 검사). 새 locale은 그 release의 공개 기록 PR에서 표에 추가하며, 이 단계를 root [TEMPLATE_GUIDE.md](../../TEMPLATE_GUIDE.md) §5의 release 절차에 적습니다. 언어 이름 열은 비교하지 않습니다.
  - 한계: 공개 뒤 표 갱신을 잊으면 검사가 잡지 못하고 release 절차에 맡깁니다.
  - 검증: 표에 manifest에 없는 tag를 넣거나 상태를 바꾸면 실패하고, manifest에만 있는 `complete` locale은 통과하는 회귀 테스트와 red-green

**공통**

- **R-006 계약 보존:** installer의 다른 인자와 동작, release manifest schema, artifact inventory, payload checker는 바뀌지 않습니다. 바뀌는 asset은 `installer.py`, 적용 가이드 문장이 바뀐 en·ko locale ZIP, 그에 따른 `SHA256SUMS`·manifest입니다.

### 2.2 대안과 선택 이유

**Q1 기본 URL의 출처**
- **A1 installer source 상수 (권고):** D-004가 release root를 하나로 정했으므로 상수 하나면 됩니다. fork는 `--release-url`을 쓰거나 상수를 바꿉니다.
- A2 packager가 package할 때 저장소를 installer byte에 넣기: fork에서도 자동으로 맞지만, installer byte가 release마다 달라지고 packager·verifier의 self-binding 검증을 함께 바꿔야 합니다.
- A0 기본값 없음: 문제 1이 남습니다.

**Q2 명령 문서**
- B1 공개 뒤 root README만 (권고였음): 명시적 플래그는 계속 유효하므로 locale guide와 계약은 그대로 둡니다. README만 짧아집니다.
- **B2 locale guide·`required_commands`까지 (사용자 선택):** payload 명령 계약이 바뀌어, 적용 프로젝트가 병합할 문서와 검사 변경이 늘어납니다. 이전 installer와 섞여 쓰일 때 혼동될 수 있습니다.

**Q3 release version**
- C1 `v2.6.0` + 호환성 안내 (권고였음): `v2.3.3`이 Windows 하한을 올릴 때도 호환성 안내와 이전 installer 대안을 붙였습니다. 기본 URL은 기존 사용법을 깨지 않는 추가입니다.
- **C2 `v3.0.0` (사용자 선택):** Linux·macOS의 Python 3.11 이하 지원을 끊고 payload 명령 계약을 바꾸므로 SemVer상 breaking으로 봅니다.

**Q4 사본 대조의 허용 차이**
- **D1 root wrapper가 heading으로 소유 절을 찾기 (권고):** payload를 바꾸지 않습니다. heading이 바뀌면 검사가 실패해 바로 드러납니다.
- D2 payload에 marker 추가: 경계가 더 분명하지만 en·ko payload와 manifest 계약을 바꿉니다.

### 2.3 설계와 계약

**installer (`scripts/installer.py`)**
- `DEFAULT_RELEASE_URL` 상수를 두고 `_add_remote_arguments`의 `--release-url`을 `required=False, default=DEFAULT_RELEASE_URL`로 바꿉니다. 이후 처리(`_validated_release_url` 등)는 같습니다.
- `_require_supported_python`이 OS와 관계없이 3.12 미만을 거부합니다. 오류 문구는 Windows junction 이유와 함께 하한을 알립니다.

**root `scripts/check-docs.py`**
- `check_root_copies()`: 세 파일 쌍을 줄 단위로 비교하기 전에 양쪽에서 프로젝트 소유 절을 지웁니다. 소유 절은 ko heading으로 찾고, heading을 찾지 못하면 실패합니다.
- `check_readme_locale_table()`: `scripts/check_locales.py`에 검증된 manifest를 돌려주는 공개 함수(기존 `_read_manifest`와 `_validate_manifest_schema`를 사용)를 두고, 그 결과를 `complete_locales(manifest)`에 넘깁니다. manifest를 읽거나 검증하지 못하면 그 오류를 보고하고 표는 대조하지 않습니다. 두 README에서 첫 열 머리글이 `Locale`인 표를 읽어, 각 tag가 반환된 목록에 있고 상태 열이 `complete`인지 확인합니다(R-005, 부분집합).
- 두 검사는 인자 없는 maintainer 실행에서만 돕니다. `--root`로 artifact를 검사할 때는 실행하지 않습니다.

**문서**
- T-049 PR: root [TEMPLATE_GUIDE.md](../../TEMPLATE_GUIDE.md) §3(무인자 maintainer 검사 설명)과 §5(공개 기록 PR에서 README locale 표 갱신), root `DOCS_GUIDE.md`의 점검 목록
- T-050 PR: [en](../../../locales/en/docs/TEMPLATE_GUIDE.md)·[ko](../../../locales/ko/docs/TEMPLATE_GUIDE.md) 적용 가이드 §2(Python 하한)와 PROJECT External Boundaries
- T-050 PR: en·ko 적용 가이드의 installer 명령과 manifest `required_commands`, root `AGENTS.md` Commands에서 `--release-url` 제거
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
- **명령 계약 변경:** payload 문서의 installer 명령에서 `--release-url`이 빠지므로, 이 문서를 보고 `v2.x` installer를 쓰면 명령이 실패합니다. 문서와 installer가 같은 release로 배포되고 README가 최신 installer를 받게 하므로 위험은 낮습니다. release notes에 적습니다.
- **rollback:** installer는 다음 release에서 되돌리면 됩니다. 검사는 maintainer 도구라 PR 하나로 되돌릴 수 있습니다.

### 2.6 완료 조건과 실행 순서

1. **이 설계 PR:** Q1~Q4를 합의한 뒤 `Accepted`로 바꾸고 PROJECT §8에 결정을 등재합니다.
2. **T-049 구현 PR:** root `scripts/check-docs.py`의 두 검사와 테스트입니다. README 표가 있는 PR #69가 먼저 통합돼야 합니다. release가 필요 없습니다.
3. **T-050 구현 PR:** installer와 테스트, en·ko guide·PROJECT 문서입니다.
4. **T-051 release:** `v3.0.0` 준비 → tag·draft(사용자) → candidate → 공개(사용자) → published(Linux 로컬, Windows Buildkite) → 기록 PR(root README 명령과 Prerequisites)

## 3. 변경 기록

- 2026-10-08: 사용자 지시에 따라 초안을 작성했습니다.
- 2026-10-08: PR #70 version 1(`3355cb5`)에 대한 Q1~Q4 선택을 반영해 `Accepted`로 바꿨습니다. Q2는 B2, Q3는 C2를 골라 R-003, §1.3, §2.3, §2.5, §2.6을 고쳤습니다.
- 2026-10-08: PR #70 version 2 리뷰의 C70-B-001(=C70-A-001, P2)에 따라 R-005를 공개 release 기준에 맞춰 부분집합 검사로 바꾸고 새 locale의 표 갱신을 공개 기록 절차에 넣었습니다(사용자 승인 "70은 1안으로"). C70-B-002(=C70-A-002, P2)에 따라 §2.3에 검증된 manifest를 `complete_locales(manifest)`에 넘기는 흐름을 적었습니다.
