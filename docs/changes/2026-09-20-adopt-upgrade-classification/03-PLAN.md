# 변경 실행 계획: base-aware `adopt` 분류

> 이 PLAN은 승인된 계약의 후속 구현·검증 순서와 브랜치 검증 상태를 기록합니다. 변경별 완료는 Origin 통합·release 공개·consumer 지원 완료와 구분합니다.

## Metadata

- **Change ID:** `2026-09-20-adopt-upgrade-classification`
- **Spec:** [승인된 합본형 변경 문서](./01-CHANGE.md)
- **Global task:** [02-TODO.md](../../02-TODO.md)의 T-007
- **Owner:** Chae Sangwon
- **Baseline:** Origin·GitHub `main` `1423060d6943d31764729396523222e863de612d`
- **Integration target:** Origin PR #24로 `main` 통합, remote `main` 동기화와 review 후속 뒤 `v2.2.0` release
- **Scope:** 후속 구현은 `scripts/installer.py`, `scripts/verify_release.py`, 관련 테스트, root·en·ko 적용 문서와 release·consumer 검증 기록을 담당합니다. 계약 PR에서는 `01-CHANGE.md`, 이 PLAN, PROJECT·TODO와 D-008을 복제하는 `docs/REVIEW.md`·`.cursor/BUGBOT.md`만 변경합니다.

아래 체크 완료는 해당 구현 브랜치에서의 구현·검증 완료이며 병합·릴리스·지원 검증 완료를 뜻하지 않습니다. 이번 계약 승인은 W-001 시작 권한이 아닙니다.

## 1. 구현 순서와 의존성

1. 이 계약 PR에서 `01-CHANGE.md`, 이 PLAN, PROJECT D-008, 전역 T-007과 두 review invariant 사본만 통합합니다. installer·테스트·사용자 가이드는 변경하지 않습니다.
2. T-011은 Origin PR #22 merge commit `62d1de45d9eb9c8c0387b3f2c4007fcc17480a21`로 `main`에 통합됐습니다. 별도 사용자 시작 요청 뒤 최신 `main`에서 구현을 시작합니다.
3. W-001의 base 전용 verifier와 W-002의 분류·report를 구현하고 함께 검토합니다. legacy parser를 current verifier나 다른 installer 명령에 연결하지 않습니다.
4. W-003으로 release verifier가 format 2와 공개 base-aware E2E를 fail-closed하게 검사하도록 확장한 뒤 W-004 문서를 en·ko로 맞춥니다.
5. 사용자가 기존 순서를 변경해 `v2.1.1` 공개 전 PR #24 통합을 지시했습니다. `v2.1.1`은 T-007 구현 전 exact source commit을 사용하고 동기화된 `main`의 조상인지 T-008로 확인합니다. 별도 release 위임을 받은 뒤에만 W-005의 `v2.2.0` 게시·consumer 검증을 진행합니다.

T-006 consumer 작업은 과거 v2.0→v2.1 회귀 fixture의 근거이며 T-007 구현의 미완료 선행조건이 아닙니다. 자동 merge·삭제·patch·commit·PR 생성은 모든 단계에서 비범위입니다.

## 2. 작업 체크리스트

- [x] **W-001 base 전용 schema 1·2 verifier와 SemVer precedence**
  - 범위·변경 파일: `scripts/installer.py`, `tests/test_install_release.py`
  - 대응 요구사항·상위 완료 조건: R-002, R-003, R-007
  - 선행조건: 계약 PR 통합, 별도 구현 시작 요청, 최신 `main`
  - 검증 방법: schema별 모든 object의 exact-key fixture, checksum 이름 집합 equality와 비선택 archive 미다운로드, identity·installer/archive tamper, redirect·크기 상한, `latest`·leading `v`·불완전 SemVer·base>=current·repository/locale 불일치·미지원 schema failure matrix, prerelease·build metadata truth table, 과거 installer 비실행 감시, `install`·`export`·`list-locales`·base 없는 `adopt`가 legacy parser·importlib·subprocess를 호출하지 않는 격리 회귀, 대상/output snapshot
  - 결과·근거: `scripts/installer.py`의 current verifier와 분리된 base 전용 exact-key parser, opaque installer hash 검증, 닫힌 checksum asset 집합과 SemVer precedence를 구현했습니다. schema 1·2 성공, unknown key·extra checksum·installer tamper·비선택 locale 미다운로드, legacy parser 격리와 대상/output 불변 회귀가 통과했습니다. release asset을 추가할 때는 같은 변경에서 닫힌 집합과 fixture를 함께 갱신합니다.

- [x] **W-002 union 분류와 adoption plan format 2**
  - 범위·변경 파일: `scripts/installer.py`, `tests/test_install_release.py`
  - 대응 요구사항·상위 완료 조건: R-001, R-004~R-008
  - 선행조건: W-001
  - 검증 방법: 다섯 equality partition과 current 추가·제거·unsafe target의 truth table, report cardinality·null·정렬 불변식, base-only reason, format 1 plan·artifact·stdout byte 회귀, base provenance 주의와 고정 status/path 순서의 format 2 stdout, atomic publish와 대상 불변
  - 결과·근거: `base ∪ current`를 정렬해 여섯 equality status로 분류하고 format 2 provenance·두 summary·null·제거 reason을 기록합니다. current artifact만 원자적으로 게시하며 base 없는 format 1 경로와 stdout을 유지합니다. union 9경로 fixture에서 추가·수정·제거·blocked와 고정 stdout 순서를 검증했습니다.

- [x] **W-003 release verifier의 format 2 진단과 원격 E2E**
  - 범위·변경 파일: `scripts/verify_release.py`, `tests/test_verify_release.py`
  - 대응 요구사항·상위 완료 조건: R-007, R-008, R-010
  - 선행조건: W-002
  - 검증 방법: 선택형 `published --base-version` CLI, format 2 top-level·두 summary·path 불변식의 malformed fixture, option 생략 회귀와 candidate에는 새 network 요구 없음 확인, published에서 이전 exact base와 current release의 en·ko base-aware `adopt`, 대상 불변과 source fixture 대조
  - 결과·근거: `published --base-version`을 선택 인자로 추가하고 latest·exact current selector별 모든 locale의 base-aware `adopt`를 실행하도록 연결했습니다. verifier가 format 2 top-level·provenance·두 summary·path 정렬·hash/null·분류 불변식, 알려진 E2E target byte, 대상 불변과 current artifact byte를 독립 검증합니다. base hash는 별도 historical parser를 중복하지 않고 shape·null·분류 일관성만 검사하며 W-005 consumer 대조가 byte ground truth를 담당합니다. 실제 공개 `v2.2.0` 원격 실행은 W-005에 남습니다.

- [x] **W-004 root·en·ko 적용 문서와 locale parity**
  - 범위·변경 파일: `README.md`, `README.ko.md`, `locales/en/docs/TEMPLATE_GUIDE.md`, `locales/ko/docs/TEMPLATE_GUIDE.md`, 필요 시 required command 계약과 release history
  - 대응 요구사항·상위 완료 조건: R-009
  - 선행조건: W-001~W-003 CLI·출력 계약 확정
  - 검증 방법: root docs, stable locale, en·ko export artifact checker·명령 parity, exact base에서 유래한 target 전제와 최초 adoption 구분, 두 summary 분모, 자동 merge·삭제 없음과 base-only 제거 예시 대조
  - 결과·근거: root README와 en·ko 적용 가이드에 exact-base 전제, 최초 adoption 구분, 여섯 status, summary 분모, 제거 예시와 자동 merge·삭제 금지를 반영했습니다. required command manifest와 root `AGENTS.md`·`docs/TEMPLATE_GUIDE.md`의 maintainer 명령을 맞췄고 두 locale export artifact의 checker와 각 49개 테스트가 통과했습니다.

- [ ] **W-005 `v2.2.0` 공개와 consumer 검증**
  - 범위·변경 파일: source version·locale release history, root `README.md`·`README.ko.md`와 별도 bilingual release notes 정렬 commit, GitHub `v2.2.0` tag·release, 이 PLAN의 검증 기록
  - 대응 요구사항·상위 완료 조건: `01-CHANGE.md` §2.6 공개·회귀·지원 완료
  - 선행조건: W-001~W-004와 review 후속 Origin `main` 통합, `v2.1.1` 공개, 사용자 tag·release 위임
  - 검증 방법: T-008 candidate·published gate, v2.0→v2.1 historical fixture의 기존 수동 판정 재현, v2.1 적용 consumer에서 base v2.1→current v2.2 원격 report의 독립 3-way 대조, 대상 tree 불변
  - 결과·근거: `v2.1.1` 공개와 PR #25 통합을 확인하고 `codex/v2.2.0-release-prep`에서 source version·release history와 current-state README·별도 release notes를 정렬했습니다. `claude-review-e2e@719696f`에서 공개 v2.0.0 base·v2.1.0 current byte를 대조해 기존 `merge 13`을 `diverged 6`·`project-only 7`로 재현했고 target snapshot은 동일했습니다. 공개 release와 v2.1→v2.2 consumer 검증은 미수행입니다.

## 3. 검증 기록

| 대상 작업·요구사항 | 확인한 revision 또는 작업 트리 범위 | 실행한 검사 | 결과·남은 한계 |
|---|---|---|---|
| 계약 | Origin `main` `62d1de45d9eb9c8c0387b3f2c4007fcc17480a21` + 계약 문서 변경 | root docs와 REVIEW/BUGBOT invariant 대조, stable locale, docs unittest 51개, `git diff --check` | 통과. Origin PR #23 merge `1423060d6943d31764729396523222e863de612d`와 같은 GitHub `main` 확인 |
| W-001~W-004 | Origin PR #24 head `09c51fe6cb582235955117477b1d2255f45a4da1`, merge `564c1bf5ca36115020fea0b346f95f13931171dd` | installer 42개, verifier 15개, 전체 unittest 165개, root docs, stable locale, Python compile, `git diff --check`, en·ko export artifact checker와 각 49개 test | 통과·Origin 통합. 실제 remote `v2.2.0`·consumer 검증은 미완료 |
| PR #24 C24-001·C24-002와 PR #25 C25-001 | PR #25 head `4366c2a04986aaabb63056db7486ec7ed644998b`, merge `d821dec23b0e34295b96f9af0690ba15f2d33edb` | verifier 16개, 전체 unittest 166개, root docs, stable locale, Python compile, `git diff --check` | 통과·Origin/GitHub 통합. target fixture ground truth와 root maintainer 명령 parity를 보강하고 T-012의 object 부재·shallow history 부족·실제 비조상 진단을 분리했습니다. |
| `v2.1.1` 선행 release | source `0cfcc896ee92ec018d12c88f3f2638a154b35720`, synchronized `main` `d821dec23b0e34295b96f9af0690ba15f2d33edb` | T-008 candidate·published, 5개 asset digest와 latest·exact en·ko 공개 경로 | 통과. immutable Latest로 공개했고 source version을 `2.2.0`으로 정렬할 선행조건 충족 |
| W-005 historical fixture | target `claude-review-e2e@719696fa52be301db314dc276a1c666385540bdf`, base `v2.0.0@8bc8b1b5049de1f57dead7b2a804e8bee5ce989f`, current `v2.1.0@36a123ff3bd939a99148e0f804f9e20924f6be0b` 공개 asset | current format 2 classifier로 공개 asset byte와 target exact tree를 독립 대조하고 전후 target snapshot 비교 | 통과. 기존 format 1 `merge 13`은 `diverged 6`·`project-only 7`로 재현됐고 target은 불변 |
| W-005 release 준비 | `d821dec23b0e34295b96f9af0690ba15f2d33edb` 기준 `codex/v2.2.0-release-prep` 작업 트리 | source version·release history, current-state README와 bilingual release notes, 전체 unittest 166개, root docs, stable locale, Python compile, `git diff --check`, en·ko export artifact checker와 각 49개 test | 통과. 공개 release·v2.1→v2.2 consumer 검증 미수행 |

## 4. 변경·재검증 기록

- 2026-09-20: 사용자 승인 뒤 보안·report·실행 관점의 독립 검토를 반영해 경로 집합, format 2 호환, legacy validator와 release·consumer 검증 경계를 닫았습니다. 구현 작업은 시작하지 않았습니다.
- 2026-09-21: Origin·GitHub `main`을 `1423060d6943d31764729396523222e863de612d`로 동기화한 뒤 사용자 요청에 따라 W-001~W-004를 구현하고 로컬 gate를 통과했습니다. PR #23 C23-005는 strict checksum 집합과 release asset fixture의 동시 갱신 규칙으로 채택했고, Deferred 세 항목은 구현하지 않았습니다.
- 2026-09-21: 사용자 지시에 따라 `v2.1.1` 공개 전 Origin PR #24를 merge commit `564c1bf5ca36115020fea0b346f95f13931171dd`로 통합했습니다. `v2.1.1` exact source는 T-007 구현 전 commit을 사용하고 remote `main`의 조상인지 T-008로 확인합니다. 두 P3는 별도 후속 브랜치로 넘겼습니다.
- 2026-09-21: PR #25 C25-001의 shallow history 오진은 같은 후속 브랜치에서 수정합니다. C25-002의 같은 `2.1.1` version 아래 release source와 현재 artifact 차이는 T-008에 기록하고, `v2.1.1` 공개 직후 W-005의 `2.2.0` source version 정렬로 해소합니다.
- 2026-09-21: PR #25를 merge `d821dec23b0e34295b96f9af0690ba15f2d33edb`으로 통합하고 양쪽 `main`을 동기화한 뒤 `v2.1.1` candidate·published를 통과해 immutable Latest로 공개했습니다. 사용자의 README 요청에 따라 W-005에서 root README는 현재 동작만 유지하고 버전별 설명은 `CHANGELOG.md`·`CHANGELOG.ko.md`로 분리합니다.
- 2026-09-21: historical fixture에서 v2.0.0·v2.1.0 공개 asset과 업그레이드 전 consumer exact tree를 format 2 classifier로 대조했습니다. 기존 format 1의 `merge 13`이 `diverged 6`·`project-only 7`로 재현됐고 target snapshot은 동일했습니다.

## 5. 인계

W-001~W-004와 review 후속은 Origin·GitHub `main`에 통합됐고 `v2.1.1`도 공개됐습니다. W-005는 release-prep 변경의 검토·통합 뒤 별도 release 위임으로 tag·draft·candidate·published와 consumer 검증을 진행합니다.

구현 중 공개 계약을 바꿔야 하는 사실이 발견되면 이 변경의 승인 범위를 임의로 넓히지 않고 설계 변경으로 돌아옵니다. `v2.2.0` tag·release 게시와 GitHub fast-forward는 별도 위임이 필요합니다.

`01-CHANGE.md` §2.5의 Deferred 후보는 W-001~W-005의 미착수 작업이 아닙니다. 지원 검증에서 재검토 조건이 충족돼도 별도 사용자 승인 전에는 PLAN에 추가하지 않습니다.
