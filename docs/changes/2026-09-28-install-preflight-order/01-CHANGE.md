# 변경: install preflight 순서 평가

## Metadata

- **Change ID:** `2026-09-28-install-preflight-order`
- **Status:** Accepted
- **Originator:** Chae Sangwon
- **Source:** 기존 T-021과 2026-09-28 사용자의 PR #46 새 head 리뷰 후 다음 작업 진행 요청. PR #46 version 2 head `e113dd159a986633a87544866b164bbec6b2e7e5`의 세 리뷰 인계를 반영합니다.
- **Parent:** [제품 기준](../../00-PROJECT.md) D-004·D-006·D-010·D-011, [install 대상 계약](../2026-09-22-install-target-contract/01-CHANGE.md) §2.3
- **Decision:** A — 현재 순서 유지. PROJECT §8의 Accepted D-010 §2.3을 재확인하며 기존 결정을 대체하거나 새 결정 ID를 발급하지 않습니다.
- **Approval:** Chae Sangwon, 2026-09-28 대화 “A안으로 할게.” — PR #47 version 1 head `978be1788fd3e2fc15c72ac823b8c04815e5fc0e`에서 제시한 A안과 §2.3의 현재 검증·대상 검사·쓰기 순서 유지를 승인했습니다. B안은 선택하지 않았으며 별도 구현·release가 필요하지 않습니다.
- **Execution:** [전역 TODO](../../02-TODO.md)의 T-021이 상세 실행 상태·검증·통합 조건을 소유합니다.

## 1. Intent

### 1.1 문제와 확인한 근거

현재 `install`은 release manifest·installer self-binding·locale archive 검증을 마친 뒤
대상 root와 emptiness를 검사합니다. 비어 있지 않은 대상도 다운로드 뒤에 거부되며,
release 오류가 함께 있으면 대상 안내보다 release 오류가 먼저 나옵니다.
이는 D-010 §2.3과 일치하는 현재 동작이며, 확인된 안전 결함으로 분류하지 않습니다.

분석 기준은 PR #46 merge `4c743f149d726c692684f8f626e31fd74db34a73`입니다.
`scripts/installer.py`의 `install`과 대상 검사·쓰기 helper의 production 호출자를
확인했습니다. `_resolve_target_root`·`_require_empty_install_target`·`_write_members`의
production 호출자는 `install` 하나입니다.

Linux에서 기존 `tests/test_install_release.py`의 `FakeReleaseServer`와
`build_release_payloads`로 exact `2.0.0`의 합성 release를 만든 임시 probe를 실행했습니다.
현재 installer를 호출하고 HTTP 요청 수·대상 검사 호출·거부 전후 tree snapshot을 대조했습니다.

| 입력 | 현재 결과 | fixture HTTP 요청 | 대상 검사 | 대상에 쓴 파일 |
|---|---|---|---|---|
| 정상 release + `existing.txt`가 있는 대상 | 비어 있지 않음 거부·빈 대상/`adopt` 안내 | 3 | root·emptiness 각 1회 | 0, tree 동일 |
| `SHA256SUMS` 404 + 같은 대상 | release 요청 오류 | 1 | 없음 | 0, tree 동일 |
| checksum·manifest는 맞지만 ZIP 형식이 잘못된 archive + 같은 대상 | archive 오류 | 3 | 없음 | 0, tree 동일 |
| 미지원 locale + 같은 대상 | locale 선택 오류 | 2 | 없음 | 0, tree 동일 |
| 정상 release + 빈 대상 | 성공 | 3 | root·emptiness 각 1회 | fixture member 4개 |
| 정상 release + 새 대상 | 성공 | 3 | root·emptiness 각 1회 | fixture member 4개 |

이 수치는 exact-version localhost fixture의 호출 관찰이며 원격 GitHub의 지연·속도
측정이 아닙니다. Windows에서 이 probe를 실행하지 않았습니다. 현재 코드의 Windows
회귀는 PR #46 exact head의 Windows #49 CI로 확인됐고, 제안하는 B안은 구현·검증 전입니다.

### 1.2 기대 결과

대상 진단·불필요한 다운로드와 release 오류 우선순위 중 무엇을 우선할지 결정합니다.
선택과 무관하게 새·빈 대상 계약, 검증된 artifact만 쓰는 경계와 대상 보존을 유지합니다.

### 1.3 범위와 비범위

범위는 `install`의 대상 preflight 시점, 함께 실패하는 입력의 오류 우선순위,
선택에 따른 회귀·문서·리뷰 불변조건 갱신 계획입니다. 이 PR은 설계 문서만 다룹니다.
`adopt`·`export`·`list-locales`, 새 CLI 옵션, 검사 범위의 상위 경로 확대,
dependency·CI runner·공개 asset 변경은 포함하지 않습니다.

### 1.4 제약

- D-010의 새·빈 실제 디렉터리만 허용하는 경계와 D-006의 읽기 전용 `adopt`를 유지합니다.
- D-011의 Windows Python 3.12 하한·현재 symlink/junction 검사 지점을 유지합니다.
- release·archive·member 검증 전에 artifact를 대상에 쓰지 않습니다.
- root·부모 검사 거부의 tree 보존과 비어 있음 검사 거부의 안내 범위를 구분합니다(C46-001).
- 기존 immutable `v2.3.3` tag·asset은 변경하지 않습니다.

### 1.5 선택과 미해결 질문

**사용자가 A안(현재 순서 유지)을 선택했습니다.** 코드 변경 없이 설계 판단을 기록합니다.
선택에 관한 미해결 질문은 없습니다. B안은 비교 근거로 보존하며 승인 범위에 포함하지
않습니다. 향후 순서 변경을 다시 제안하려면 사용자 근거와 재검사·오류 우선순위를
재평가하고 별도로 합의해야 합니다.

## 2. Spec

### 2.1 공통 요구사항과 시나리오

| 요구사항 ID | 요구사항 | 상황·입력 | 관찰 가능한 결과 | 검증 방법 |
|---|---|---|---|---|
| R-001 | 현재 install 허용·보존 계약 유지 | 새·빈 대상, `.git` 또는 무관한 파일이 있는 대상, 검사 불가 | 새·빈 대상만 성공; 거부 시 기존 tree에 artifact 추가 없음 | CLI 회귀·before/after snapshot |
| R-002 | 검증된 release만 기록 | checksum·manifest·installer binding·archive·member 오류 | 검증 실패 시 artifact 기록 없음 | 기존 installer·verifier 회귀 |
| R-003 | 오류 우선순위를 선택한 안과 일치시킴 | 비어 있지 않은 대상과 release·locale 오류가 함께 있음 | A는 release·locale 검증 오류 우선; B는 유효한 로컬 인자 확인 뒤 대상 오류 우선 | 두 오류를 결합한 fixture·HTTP 호출 관찰 |
| R-004 | B의 선행 검사를 마지막 검사로 오해하지 않음 | 초기에는 빈 대상, 다운로드 중 파일 생성 또는 root link로 교체 | 검증 뒤 첫 쓰기 전 root·emptiness를 재검사하고 새 상태를 거부 | 다운로드 callback으로 상태 변경, 대상 snapshot·native Windows 회귀 |
| R-005 | 문서·리뷰 불변조건과 구현을 함께 갱신 | B로 순서 변경 | REVIEW §6·BUGBOT 두 사본의 순서 문구와 실제 호출이 일치 | 기존 docs checker·계약 회귀 |
| R-006 | 다른 명령·플랫폼 경계 유지 | `adopt`·`export`·`list-locales`, Windows Python 하한·junction | 기존 지원 범위와 실패 경계 유지 | 전체 unittest·필수 Windows/Linux CI |

### 2.2 대안과 선택 이유

| 대안 | 순서 | 장점 | 비용·오류 의미 |
|---|---|---|---|
| **A — 현재 순서 유지(선택)** | 로컬 인자 검증 → release·locale·archive 검증 → 대상 root·emptiness → 쓰기 | 승인된 D-010·현재 공개 installer·리뷰 불변조건과 일치; 별도 구현 없음 | 비어 있지 않은 대상에서도 다운로드하며 release 오류가 대상 안내를 가림 |
| **B — 대상 검사 선행 + 쓰기 전 재검사(미선택)** | 로컬 인자 검증 → 대상 root·emptiness → release·locale·archive 검증 → 대상 root·emptiness 재검사 → 쓰기 | 거부할 대상은 release 다운로드 전에 진단 가능 | 대상 오류가 release·locale 오류보다 우선; 검사 2회와 추가 회귀·문서·release 작업 필요 |

A를 권고하는 이유는 현재 순서가 대상 보존을 강제하고, T-020의 새·빈 대상 안내도 이미
공개되어 있기 때문입니다. 현재 인계에는 순서 때문에 발생한 데이터 손실이나 release
검증 우회가 없으며, 다운로드·진단 이득만으로 공개된 오류 순서를 바꾸는 근거는 아직
부족합니다. 사용자는 이 비교안에서 A를 선택했습니다. B의 비용과 동작은 향후 재평가를
위한 비교 근거이며 이번 승인·실행 범위에 포함하지 않습니다.

**대상 검사를 앞으로 옮기기만 하는 방식은 B에 포함하지 않습니다.** 다운로드 중
무관한 파일이 생기면 member 충돌 검사만으로 비어 있지 않은 상태를 거부할 수 없습니다.
따라서 B를 선택한다면 기존 helper를 쓰기 전에도 다시 호출해야 합니다. 이 재검사도
마지막 검사 이후의 모든 동시 변경을 원자적으로 막는 보장은 아니며, D-010의 기존
member 충돌·`xb`·rollback 경계를 유지합니다.

### 2.3 선택별 설계와 오류 계약

**A:** 현재 `install`의 `_verified_manifest` → `_selected_locale_record` →
`_verified_members` → `_resolve_target_root` → `_require_empty_install_target` →
`_write_members` 순서를 유지합니다. release 오류와 대상 오류가 겹치면 앞 단계의 오류를
보고합니다. 새 코드·중복 검사·release를 요구하지 않습니다.

**B를 승인하는 경우:** CLI의 Python 하한 확인과 `install`의 URL·version 로컬 검증을
유지한 뒤 `_resolve_target_root`·`_require_empty_install_target`를 먼저 호출합니다.
유효하지 않은 대상은 HTTP 요청 없이 거부합니다. 통과하면 현재 release·locale·archive
검증을 수행하고, 첫 쓰기 전에 두 대상 helper를 다시 호출합니다. 기존 helper·오류 메시지와
쓰기·rollback을 사용하며 검사 생략 플래그나 별도 설정 계층을 추가하지 않습니다.

B에서는 유효한 URL·version 문자열이라도 원격 release 실패·미지원 locale과 대상 거부가
겹치면 대상 오류가 먼저 나옵니다. 대상이 처음에는 유효하고 release 검증이 실패하면
release 오류를 보고합니다. 대상이 검증 도중 바뀌고 release 검증이 성공하면 마지막
대상 검사 오류를 보고합니다. 마지막 검사도 C46-001의 기존 안내 범위를 유지합니다.

### 2.4 상위 계약·문서의 영향

A는 D-010·D-011·D-004·D-006을 유지합니다. B를 승인하면 D-010 §2.3의 **검사 순서**를
변경하는 결정과 연결하고, 새·빈 대상·안내·보존 요구는 유지함을 명시해야 합니다.
기존 D-010의 승인 기록은 유지합니다. 이번 승인은 A에만 적용되며 B의 비교 설명을
현재 계약으로 읽지 않습니다.

B의 구현 PR 범위는 `scripts/installer.py`, `tests/test_install_release.py`, 필요한
verifier 계약 회귀, PROJECT의 현재 흐름과 결정 연결, REVIEW §6·BUGBOT의 두 불변조건입니다.
root README·en/ko 적용 가이드·release notes에서 오류 우선순위 안내가 필요한지도 함께
대조합니다. 승인 설계 자체를 유지하며 상세 실행 상태는 TODO에서 추적합니다.

### 2.5 위험·호환성·배포와 rollback

| 위험 | 영향 | 완화·rollback |
|---|---|---|
| A의 다운로드·진단 비용을 남김 | 비어 있지 않은 대상에서도 release 오류·네트워크 대기가 먼저 발생 | 현재 onboarding의 새·빈 대상 조건과 기존 저장소 `adopt` 안내를 유지; 실제 사용자 근거가 생기면 재평가 |
| B의 오류 우선순위 변경 | 같은 잘못된 입력 조합에서 다른 오류가 먼저 보임 | 결합 오류 fixture로 고정하고 다음 release notes에 호환성 변화 명시 |
| B의 초기 검사 이후 대상 변경 | 재검사 없이 쓰면 새 외부 파일 옆에 artifact 추가 | 첫 쓰기 전 root·emptiness 재검사와 기존 member 충돌·rollback 유지 |
| 순서만 바꾸고 불변조건 방치 | 승인된 구현을 Bugbot이 규칙 위반으로 보고 | 같은 구현 PR에서 REVIEW·BUGBOT 문구 갱신, 기존 checker 동등성 통과 |
| B 구현·문서·공개 경로가 어긋남 | 현재 공개 installer와 새 문서의 동작 차이 | 구현 통합 뒤 별도 release 후보·published gate, 공개 asset 교체 금지 |

A에는 새 artifact release가 필요하지 않습니다. 향후 B를 별도로 승인하면 구현·native Windows/Linux
회귀·두 목록 검사·Origin/GitHub 통합을 거쳐 후속 release에서 배포합니다. version 선택과
release 작업은 별도 요청·작업에서 정하며, 이 설계가 게시 권한을 추가하지 않습니다.
B를 되돌릴 때는 순서와 관련 문서·불변조건을 함께 되돌리고 새 release로 배포합니다.

### 2.6 완료 조건

설계 완료는 사용자 선택과 승인 범위가 문서·PROJECT 결정 인덱스에 기록되고,
설계 PR의 문서·locale 검사와 수동 리뷰·필수 CI가 통과해 Origin/GitHub에 통합되는 것입니다.
사용자가 A를 선택했으므로 별도 구현·release 없이, 설계 PR의 검증·리뷰와 통합을 확인한
뒤 T-021을 종료합니다. B의 R-004·R-005와 구현·배포 계획은 미선택 대안의 조건이며
현재 작업으로 실행하지 않습니다. 승인 상태 `Accepted`와 fixture 관찰만으로 PR 통합
완료를 표시하지 않습니다. 상세 검증·통합 상태는 TODO가 소유합니다.

## 3. 변경 기록

- 2026-09-28: PR #46 version 2의 C46-001 해소와 두 불변조건 동시 갱신 인계를 확인하고
  T-021을 시작했습니다. `4c743f1`의 현재 순서를 Linux fixture 6개로 확인했습니다.
  A 유지와 B 선행·재검사를 비교한 Draft를 준비했으며, 권고안 A의 사용자 선택은 대기 중입니다.
- 2026-09-28: 사용자가 PR #47 version 1 head `978be17`의 비교안에 “A안으로 할게.”라고
  답해 현재 순서 유지를 승인했습니다. Status를 `Accepted`로 바꾸고 D-010 §2.3 유지와
  별도 구현·release 없음, B안 미선택 범위를 기록했습니다. PR 통합 상태는 TODO에서 관리합니다.
- 2026-09-28: PR #47 version 2 리뷰의 선택 권고에 따라 HTTP 1회 관찰의 실패 asset을
  `SHA256SUMS`로 명시했습니다. A안 판단·승인과 installer 동작은 유지하며 T-013의
  다음 문서 변경에 함께 반영합니다.
