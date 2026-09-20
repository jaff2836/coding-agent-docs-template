# 변경 실행 계획: base-aware `adopt` 분류

> 이 PLAN은 승인된 계약의 후속 구현·검증 순서를 기록합니다. 계약 PR에서는 모든 작업을 미착수로 유지하며, 별도 사용자 요청 전에는 구현 파일을 변경하지 않습니다.

## Metadata

- **Change ID:** `2026-09-20-adopt-upgrade-classification`
- **Spec:** [승인된 합본형 변경 문서](./01-CHANGE.md)
- **Global task:** [02-TODO.md](../../02-TODO.md)의 T-007
- **Owner:** Chae Sangwon
- **Baseline:** Origin `main` `0cfcc896ee92ec018d12c88f3f2638a154b35720`; 구현 시작 시 T-011 통합 뒤 최신 `main`으로 갱신
- **Integration target:** Origin `main`, 이후 GitHub `main`과 `v2.2.0` release
- **Scope:** 후속 구현은 `scripts/installer.py`, `scripts/verify_release.py`, 관련 테스트, root·en·ko 적용 문서와 release·consumer 검증 기록을 담당합니다. 계약 PR에서는 `01-CHANGE.md`, 이 PLAN, PROJECT·TODO와 D-008을 복제하는 `docs/REVIEW.md`·`.cursor/BUGBOT.md`만 변경합니다.

아래 체크 완료는 해당 구현 브랜치에서의 구현·검증 완료이며 병합·릴리스·지원 검증 완료를 뜻하지 않습니다. 이번 계약 승인은 W-001 시작 권한이 아닙니다.

## 1. 구현 순서와 의존성

1. 이 계약 PR에서 `01-CHANGE.md`, 이 PLAN, PROJECT D-008, 전역 T-007과 두 review invariant 사본만 통합합니다. installer·테스트·사용자 가이드는 변경하지 않습니다.
2. T-011 Origin PR #22가 `main`에 통합된 뒤 최신 `main`에서 구현을 시작합니다. T-011은 기능 선행조건은 아니지만 `verify_release.py`·테스트·TODO 소유 범위가 겹칩니다.
3. W-001의 base 전용 verifier와 W-002의 분류·report를 구현하고 함께 검토합니다. legacy parser를 current verifier나 다른 installer 명령에 연결하지 않습니다.
4. W-003으로 release verifier가 format 2와 공개 base-aware E2E를 fail-closed하게 검사하도록 확장한 뒤 W-004 문서를 en·ko로 맞춥니다.
5. W-001~W-004가 Origin `main`에 통합되고 별도 release 위임을 받은 뒤에만 W-005의 `v2.2.0` 게시·consumer 검증을 진행합니다.

T-006 consumer 작업은 과거 v2.0→v2.1 회귀 fixture의 근거이며 T-007 구현의 미완료 선행조건이 아닙니다. 자동 merge·삭제·patch·commit·PR 생성은 모든 단계에서 비범위입니다.

## 2. 작업 체크리스트

- [ ] **W-001 base 전용 schema 1·2 verifier와 SemVer precedence**
  - 범위·변경 파일: `scripts/installer.py`, `tests/test_install_release.py`
  - 대응 요구사항·상위 완료 조건: R-002, R-003, R-007
  - 선행조건: 계약 PR 통합, 별도 구현 시작 요청, T-011 통합 뒤 최신 `main`
  - 검증 방법: schema별 모든 object의 exact-key fixture, checksum 이름 집합 equality와 비선택 archive 미다운로드, identity·installer/archive tamper, redirect·크기 상한, `latest`·leading `v`·불완전 SemVer·base>=current·repository/locale 불일치·미지원 schema failure matrix, prerelease·build metadata truth table, 과거 installer 비실행 감시, `install`·`export`·`list-locales`·base 없는 `adopt`가 legacy parser·importlib·subprocess를 호출하지 않는 격리 회귀, 대상/output snapshot
  - 결과·근거: 미착수

- [ ] **W-002 union 분류와 adoption plan format 2**
  - 범위·변경 파일: `scripts/installer.py`, `tests/test_install_release.py`
  - 대응 요구사항·상위 완료 조건: R-001, R-004~R-008
  - 선행조건: W-001
  - 검증 방법: 다섯 equality partition과 current 추가·제거·unsafe target의 truth table, report cardinality·null·정렬 불변식, base-only reason, format 1 plan·artifact·stdout byte 회귀, base provenance 주의와 고정 status/path 순서의 format 2 stdout, atomic publish와 대상 불변
  - 결과·근거: 미착수

- [ ] **W-003 release verifier의 format 2 진단과 원격 E2E**
  - 범위·변경 파일: `scripts/verify_release.py`, `tests/test_verify_release.py`
  - 대응 요구사항·상위 완료 조건: R-007, R-008, R-010
  - 선행조건: W-002와 T-011 통합
  - 검증 방법: 선택형 `published --base-version` CLI, format 2 top-level·두 summary·path 불변식의 malformed fixture, option 생략 회귀와 candidate에는 새 network 요구 없음 확인, published에서 이전 exact base와 current release의 en·ko base-aware `adopt`, 대상 불변과 source fixture 대조
  - 결과·근거: 미착수

- [ ] **W-004 root·en·ko 적용 문서와 locale parity**
  - 범위·변경 파일: `README.md`, `README.ko.md`, `locales/en/docs/TEMPLATE_GUIDE.md`, `locales/ko/docs/TEMPLATE_GUIDE.md`, 필요 시 required command 계약과 release history
  - 대응 요구사항·상위 완료 조건: R-009
  - 선행조건: W-001~W-003 CLI·출력 계약 확정
  - 검증 방법: root docs, stable locale, en·ko export artifact checker·명령 parity, exact base에서 유래한 target 전제와 최초 adoption 구분, 두 summary 분모, 자동 merge·삭제 없음과 base-only 제거 예시 대조
  - 결과·근거: 미착수

- [ ] **W-005 `v2.2.0` 공개와 consumer 검증**
  - 범위·변경 파일: version·release history 정렬 commit, GitHub `v2.2.0` tag·release, 이 PLAN의 검증 기록
  - 대응 요구사항·상위 완료 조건: `01-CHANGE.md` §2.6 공개·회귀·지원 완료
  - 선행조건: W-001~W-004 Origin `main` 통합, 사용자 tag·release 위임
  - 검증 방법: T-008 candidate·published gate, v2.0→v2.1 historical fixture의 기존 수동 판정 재현, v2.1 적용 consumer에서 base v2.1→current v2.2 원격 report의 독립 3-way 대조, 대상 tree 불변
  - 결과·근거: 미착수

## 3. 검증 기록

| 대상 작업·요구사항 | 확인한 revision 또는 작업 트리 범위 | 실행한 검사 | 결과·남은 한계 |
|---|---|---|---|
| 계약 | Origin `main` `0cfcc896ee92ec018d12c88f3f2638a154b35720` + 계약 문서 변경 | root docs와 REVIEW/BUGBOT invariant 대조, stable locale, docs unittest 51개, `git diff --check` | 통과. 구현·release·consumer 검증은 미착수 |
| W-001~W-005 | 미착수 | 미실행 | 별도 구현 시작 요청 필요 |

## 4. 변경·재검증 기록

- 2026-09-20: 사용자 승인 뒤 보안·report·실행 관점의 독립 검토를 반영해 경로 집합, format 2 호환, legacy validator와 release·consumer 검증 경계를 닫았습니다. 구현 작업은 시작하지 않았습니다.

## 5. 인계

계약 PR의 완료 범위는 승인된 문서와 실행 계획을 Origin에 올리는 것까지입니다. PR 통합 뒤에도 T-007은 `계약 승인, 구현 미착수` 상태이며, 다음 세션은 사용자에게서 구현 시작 요청을 받은 뒤 T-011 통합 상태와 최신 `main`을 먼저 확인합니다.

구현 중 공개 계약을 바꿔야 하는 사실이 발견되면 이 변경의 승인 범위를 임의로 넓히지 않고 설계 변경으로 돌아옵니다. `v2.2.0` tag·release 게시와 GitHub fast-forward는 별도 위임이 필요합니다.

`01-CHANGE.md` §2.5의 Deferred 후보는 W-001~W-005의 미착수 작업이 아닙니다. 지원 검증에서 재검토 조건이 충족돼도 별도 사용자 승인 전에는 PLAN에 추가하지 않습니다.
