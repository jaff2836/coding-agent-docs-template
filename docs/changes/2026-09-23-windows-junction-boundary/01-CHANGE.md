# 변경: Windows junction 대상 경계

## Metadata

- **Change ID:** `2026-09-23-windows-junction-boundary`
- **Status:** Draft — Windows 최소 Python 3.12 선택은 합의됐고, native 재현·전체 설계는 미확정
- **Originator:** Chae Sangwon
- **Source:** Origin PR #30 C30-002에서 이월된 T-017과 2026-09-23 사용자 요청("T-017 이후 바로 T-023")
- **Parent:** [제품 기준](../../00-PROJECT.md) D-002·D-006·D-010 및 [install 대상 계약](../2026-09-22-install-target-contract/01-CHANGE.md)
- **Decision:** 미발급 — 전체 설계 합의 후 PROJECT §8에 등록
- **Approval:** Windows installer 최소 Python 3.12 이상과 Windows CI runner로 Buildkite를 선택했습니다. 아래 경계·구현 설계 전체는 아직 승인되지 않음
- **Execution:** [전역 TODO](../../02-TODO.md)의 T-017. 이 문서는 설계 PR 범위이며 구현은 별도 PR

## 1. Intent

### 1.1 문제와 근거

`scripts/installer.py`는 `install` 대상 root·부모·member 경로, `adopt` 대상과
분류 대상, `export`/`adopt` output을 `Path.is_symlink()` 또는 `lstat().st_mode`의
symlink 판정으로 보호합니다. [Python 문서](https://docs.python.org/3.12/library/pathlib.html#pathlib.Path.is_junction)는
Windows directory junction을 별도 경로 종류로 정의하고 `is_junction()`을
Python 3.12부터 제공합니다. 따라서 junction에서 현재 symlink 검사만으로는
보호되지 않을 수 있습니다. **이 마지막 동작과 실제 외부 경로 접근은 현재 Linux
환경에서 코드·문서로 추론한 것이며 native Windows에서 아직 재현하지 못했습니다.**

### 1.2 기대 결과와 범위

- Windows의 `install`·`adopt`·`export`가 symlink와 junction을 경계 경로에서
  일관되게 거부하고, 거부 시 기존 target·외부 tree를 변경하지 않습니다.
- `adopt`가 junction을 통해 target 바깥 파일을 읽거나 report에 반영하지 않습니다.
- Windows에서 새 installer의 최소 지원 Python은 3.12로 명시합니다. 이전
  Python에서는 명확하게 중단해 junction 검사를 우회하지 않습니다.
- 이번 변경은 installer의 대상 경계·검증·사용법에 한정합니다. 공개된 `v2.3.2`
  asset, release transport, 자동 병합, 별도 maintainer exporter·packager는
  변경하지 않습니다.

### 1.3 제약과 미해결 사항

- 기존 D-010의 새 경로·빈 디렉터리 `install`, D-006의 읽기 전용 `adopt`,
  `export`의 빈 output과 rollback을 유지합니다.
- production dependency를 추가하지 않습니다. 사용자가 선택한 Buildkite 설정은 native 재현·품질 게이트에만 사용하며 installer runtime 계약을 바꾸지 않습니다.
- native Windows에서 Python 3.12 이상의 junction fixture로 현재 동작을 먼저
  재현해야 합니다. 이 환경에는 Windows 실행기가 없어 재현 근거가 없습니다.
- 사용자가 Buildkite 조직 `jaff2836-org`에 self-hosted Windows machine이 있고
  Origin의 Buildkite 앱을 설치했다고 확인했습니다. 로컬 `.env`에는 Windows
  queue key `jaff2836-worker-windows`와 agent token 설정이 있습니다. token 값은
  이 문서에 기록하지 않습니다.
  2026-09-23 읽기 전용 Buildkite Agent API 지표에서 조직 slug 일치와 이
  queue의 idle agent 1대를 확인했습니다.
  [Origin 연동](https://buildkite.com/docs/pipelines/source-control/origin)은
  Origin-hosted repository의 PR trigger와 check 게시를 지원하고, 현재 저장소는
  `origin repo mirror status`에서 `no-mirror`로 확인됐습니다. `.buildkite/pipeline.yml`과
  임시 진단 probe를 추가하고 Buildkite pipeline `windows-ci`를 연결했습니다.
  2026-09-23 build #1은 정확한 commit `63cfef85ed3f6a1e779ef45ca869f0dadd7f5b68`로
  Windows queue의 agent까지 도달했지만, HTTPS checkout에서 대화형 자격 증명을
  요구해 exit 128로 실패했습니다. 따라서 native probe와 테스트는 실행되지 않았고
  Origin check 게시도 검증되지 않았습니다. 개인 API token의 pipeline·build·cluster
  읽기를 확인했습니다.
  `jaff2836-worker-windows` queue가 `Default cluster`에 속합니다. 앞서 권한
  권고에서 cluster 조회용 `read_clusters`를 빠뜨렸으나 사용자가 추가해 현재는
  조회됩니다. `write_pipelines`와 `write_builds` scope로 pipeline 생성과 build
  실행이 성공했습니다. cluster나 queue 쓰기 권한은 필요하지 않습니다. 사용자가 준비했다고 한 SSH key는
  Origin checkout에 적용되지 않았습니다. Origin이 문서화한 clone URL은 HTTPS이며,
  이 self-hosted agent에서 SSH 주소를 확인하지 못했습니다. private checkout을
  재시도하려면 Windows agent의 checkout 전에 Origin HTTPS 자격 증명을 제공해야
  합니다. 비대화형 CI의 최소 권한 권고 경로는 Origin App의 App ID, 설치 ID, 해당
  저장소의 `repository:contents:read` 승인 및 Ed25519 private signing key로 짧은
  수명의 installation token을 발급하는 것입니다. private key는 Buildkite/agent
  비밀 저장소에만 둡니다. 대안으로 Origin CLI 사용자 인증을 agent service 계정에
  구성할 수도 있지만, checkout 전 인증 설정이 필요하다는 점은 같습니다.
- Buildkite가 선정됐으므로 T-017 Origin PR은 정확한 head SHA에서 이 Windows
  queue를 실행해야 합니다. GitHub의 후속 fast-forward 검증은 별도 trigger로
  구분합니다. Buildkite의 Origin provider는 Origin 저장소 PR trigger와 check
  게시를 지원하지만, self-hosted agent의 private checkout credential은 별도
  설정해야 합니다. 현재 checkout 실패는 그 별도 인증 설정이 없음을 확인한 결과입니다.
- 기존 코드가 직접 검사하는 경로만 고칠지, 선택된 root/output의 모든 기존
  상위 component도 검사할지 전체 설계 합의가 필요합니다. 후자를 권고합니다.

## 2. Spec (제안)

### 2.1 요구사항과 시나리오

| ID | 요구사항 | 상황·입력 | 관찰 가능한 결과 | 검증 |
|---|---|---|---|---|
| R-001 | Windows installer의 Python 하한은 3.12입니다. | Windows Python 3.11 이하에서 installer 명령 실행 | 네트워크 조회나 target 접근 전에 명확한 오류로 중단합니다. 3.12 이상과 비-Windows 동작은 유지합니다. | 지원 버전 경계 단위 검사와 native 3.12 이상 실행 |
| R-002 | `install` root·부모·member 디렉터리 경로의 symlink/junction을 거부합니다. | root 자체 또는 새 root의 부모가 junction; `_write_members`의 방어적 member 검사에 junction이 있는 경우 | 쓰기 전에 거부하고 연결된 tree와 원래 target을 보존합니다. 새·빈 실제 디렉터리는 성공합니다. | native junction fixture, target·외부 snapshot |
| R-003 | `adopt` root와 분류 대상의 symlink/junction을 따라가지 않습니다. | root junction, member의 부모 junction, 최종 member junction | root는 거부하고 member는 blocked 상태로 분류하며 바깥 파일은 읽지 않습니다. target 불변을 유지합니다. | native fixture, report 및 바깥 tree 검사 |
| R-004 | `export`와 `adopt` output의 symlink/junction을 거부합니다. | output 또는 그 상위 경로가 junction | staging·게시 전에 중단하고 연결된 tree에 파일을 만들지 않습니다. | native fixture, 두 tree snapshot |
| R-005 | 문서와 release 검증이 변경된 지원 범위와 경계를 반영합니다. | Windows 설치 안내 및 다음 release candidate | Python 하한과 새 installer의 경계가 일치하고, candidate 전 테스트에서 회귀가 드러납니다. | README en·ko, installer 테스트, candidate gate |

### 2.2 조사할 현재 경계

- `install`: `_resolve_target_root`, `_checked_member_target`, `_ensure_parent_dirs`.
  `install`의 빈 대상 preflight는 이미 존재하는 member 경로를 막지만, root
  junction이나 빈 디렉터리의 junction 부모는 통과할 여지가 있습니다.
- `adopt`: `_validated_adoption_root`, `_adoption_target`. 후자는 member마다
  `lstat().st_mode`의 symlink만 blocked 처리합니다. output 격리의 `resolve()`는
  경로 중첩을 확인하지만 root·output의 junction 거부를 대신하지 않습니다.
- `export`와 `adopt` output: `_validated_export_output`은 output과 직접 부모의
  symlink만 확인합니다. 다른 상위 component를 검사하지 않습니다.
- 현재 경계의 검사 후 쓰기 사이에 경로가 바뀌는 경쟁 조건은 남아 있습니다.
  새 설계도 stdlib의 경로 기반 검사만으로 적대적 동시 변경을 완전히 차단한다고
  주장하지 않으며, 기존 exclusive 파일 생성·rollback은 유지합니다.

### 2.3 대안과 권고

| 대안 | 장점 | 비용·위험 | 판정 |
|---|---|---|---|
| A. Windows Python 3.12+에서 `Path.is_junction()`을 symlink 검사와 결합 | 표준 라이브러리의 명시적 junction 판정, 작은 구현 | 이전 Windows Python 지원 중단; 검사 위치를 빠뜨리면 우회 | **권고** — 사용자 선택한 하한과 일치 |
| B. 기존 Python 범위에서 `lstat().st_file_attributes`의 reparse bit 검사 | 구형 Windows Python에 적용 가능, 알려지지 않은 reparse point도 거부 | 플랫폼 속성·지원 하한을 별도로 설명해야 하고 더 넓은 종류를 거부 | Python 3.12 선택에 따라 보류 |
| C. 기존 검사 유지 또는 `resolve()`의 경로 중첩 검사에 의존 | 코드 변경 적음 | junction 종류 자체를 거부하지 못하고 `adopt` member 분류에 적용되지 않음 | 기각 제안 |

권고 구현은 Windows Python 하한을 명확히 검사한 뒤, `Path.is_symlink()`과
`Path.is_junction()`을 한 경계 판정 함수에서 사용하고 root·output의 **모든
기존 상위 component** 및 member 검사·쓰기·adoption 분류에 적용합니다. 없는
component는 기존 새 경로 규칙에 따라 허용합니다. 경로 확인 실패는 허용으로
취급하지 않습니다. POSIX 경로의 기존 검사는 유지합니다. 검사 대상과 오류
메시지는 native 재현 뒤 최종 확정합니다.

### 2.4 호환성·배포·rollback

- 새 installer가 포함된 다음 release부터 Windows의 Python 3.11 이하 호출은
  중단됩니다. `v2.3.2`와 그 이전 immutable installer는 바꾸지 않습니다.
- junction 또는 junction 상위 경로를 통과하던 호출은 실패합니다. 사용자는 실제
  디렉터리를 대상으로 재실행할 수 있습니다.
- Linux/macOS 지원 범위를 의도적으로 바꾸지 않습니다. runtime 하한을
  Windows에서만 적용하므로 OS 분기를 단위·native 검사로 확인합니다.
- 설계가 잘못되면 새 release의 후속 patch에서 보완하며 공개 asset은 교체하지
  않습니다. 이전 버전으로 `latest`를 되돌려 안전하다고 주장하지 않습니다.

### 2.5 실행·검증 계획

1. native Windows에서 임시 실제 디렉터리와 junction을 만들고
   `is_symlink()`·`is_junction()` 및 현행 installer의 root·output·adoption
   경계 결과를 기록합니다. 연결 대상과 기존 target의 before/after를 대조합니다.
   Buildkite Origin pipeline의 정확한 PR head SHA를 Windows queue에서
   실행해야 하며, GitHub의 후속 fast-forward 검증은 별도 trigger로 구분합니다.
2. 재현과 전체 설계에 사용자 합의를 받은 뒤 별도 구현 PR에서 경계 판정을
   공유 지점에 추가하고 `install`·`adopt`·`export`의 모든 호출자를 갱신합니다.
3. 실제 junction fixture의 허용·거부·불변 회귀를 native Windows에서 실행하고,
   기존 symlink 회귀와 Linux 전체 unittest, root docs, stable locale 검사,
   en·ko artifact 검사, `git diff --check`를 수행합니다.
4. 다음 release candidate 전에 T-023 verifier·installer 계약 회귀 PR을
   통합하고, 그 뒤 exact source의 candidate gate를 실행합니다.

native 재현 probe는 [`.buildkite/t017-junction-probe.py`](../../../.buildkite/t017-junction-probe.py)입니다.
임시 디렉터리에만 junction을 만들고 대상의 before/after 불변을 확인한 뒤
junction을 제거합니다. 현재는 관찰 결과를 출력하는 진단 단계라 취약 동작도
통과할 수 있으며, 경계 구현 뒤 허용·거부를 assert하는 회귀 테스트로 바꿔야
합니다. 저장소 checkout에서 Linux로는 실행하지 않습니다.

## 3. 변경 기록

- 2026-09-23: Origin PR #36 merge `cc791be2370e76930184e473061312518d5fe221`
  뒤 T-017 설계를 시작했습니다. 사용자 응답으로 Windows Python 3.12 이상을
  선택했으며 native 재현과 전체 경계 설계는 Draft로 남습니다.
- 2026-09-23: 사용자가 Buildkite Windows CI를 선택해 queue 전용 pipeline과
  junction 진단 probe를 준비했습니다. pipeline `windows-ci`와 build #1을 만들고
  정확한 branch revision을 실행했습니다. Windows agent 연결은 성공했지만 Origin
  HTTPS checkout은 credentials 부재로 실패해 native 재현은 시작되지 않았습니다.
  SSH key는 이 HTTPS checkout에 적용되지 않으며, Origin App installation token을
  checkout hook에 안전하게 제공하는 구성이 필요합니다.
