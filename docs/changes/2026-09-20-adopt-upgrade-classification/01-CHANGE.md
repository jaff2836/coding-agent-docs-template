# 변경: 기존 적용 저장소의 base-aware `adopt` 분류

## Metadata

- **Change ID:** `2026-09-20-adopt-upgrade-classification`
- **Status:** Accepted
- **Originator:** Chae Sangwon
- **Source:** 2026-09-20 사용자 대화 — T-006·T-011 뒤 T-007 진행 요청
- **Parent:** [제품 기준](../../00-PROJECT.md) D-006과 [기존 저장소 adoption SPEC](../2026-09-18-existing-repository-adoption/02-SPEC.md)
- **Decision:** [PROJECT D-008](../../00-PROJECT.md#8-decisions)
- **Approval:** Chae Sangwon, 2026-09-20 사용자 대화 — 권고 계약 승인, 계약 PR만 진행하고 구현은 별도 시작 요청 전까지 보류. 2026-09-21 사용자 대화 — PR #23 계약 보강 승인, 세 후속 아이디어는 Deferred 후보로만 기록
- **Execution:** [03-PLAN.md](./03-PLAN.md)와 [전역 TODO](../../02-TODO.md)의 T-007

## 1. Intent

### 1.1 문제

현재 `adopt`는 선택한 release artifact와 대상 저장소만 비교합니다. `claude-review-e2e`를 `v2.0.0`에서 `v2.1.0`으로 갱신했을 때 report는 `merge` 13개를 냈지만, 이전 release를 사람이 별도로 export해 비교하자 템플릿도 바뀐 경로는 6개뿐이고 나머지 7개는 프로젝트만 바뀐 경로였습니다. 2-way 결과만으로는 새 템플릿 변경과 기존 프로젝트 수정을 구분할 수 없습니다.

또한 `v2.0.0` release manifest는 schema 1이고 현재 installer는 schema 2와 자기 release의 installer hash만 허용합니다. 따라서 현재 검증 함수를 base version에 그대로 호출하거나 과거 installer를 현재 installer로 가장해서 사용할 수 없습니다.

### 1.2 기대 결과

- 이미 적용한 저장소를 새 release로 갱신할 때 이전 exact release를 base로 지정합니다.
- report가 base·현재 release·대상 파일을 비교해 템플릿 변경과 프로젝트 변경을 구분합니다.
- release 사이에 추가되거나 제거된 artifact 경로도 누락하지 않습니다.
- 대상 저장소는 계속 읽기 전용이며 자동 병합·삭제·commit을 하지 않습니다.
- base를 지정하지 않은 기존 `adopt` 결과와 `install`·`export`·`list-locales` 계약은 유지합니다.

### 1.3 범위와 비범위

범위는 `installer.py adopt --base-version`, 과거 release의 읽기 전용 검증, base와 current release inventory 합집합의 3-way 분류, experimental adoption plan format 2, en·ko 적용 문서와 회귀 테스트입니다.

자동 3-way merge, 파일 추가·수정·삭제, patch 생성, commit·PR 생성, 임의 로컬 directory를 신뢰하는 `--base-path`, release manifest schema 변경은 포함하지 않습니다. base 없는 최초 adoption은 기존 2-way 경로를 그대로 사용합니다.

### 1.4 제약

- production dependency를 추가하지 않고 Python 표준 라이브러리만 사용합니다.
- current release는 지금처럼 실행 중인 installer byte와 manifest가 일치해야 합니다.
- base는 `latest`가 아닌 full SemVer이고, resolved current version보다 SemVer precedence가 낮아야 합니다.
- base artifact를 얻기 위해 과거 `installer.py`를 subprocess로 실행하지 않습니다.
- base release는 exact `v<SemVer>` namespace에서 `SHA256SUMS`·manifest·installer·archive의 내부 일관성을 모두 통과해야 합니다. GitHub release의 immutable 상태는 installer가 증명하지 않으며 공식 release 게시·검증 절차가 확인합니다.
- base asset fetch는 current 경로의 release URL 검증, exact asset URL, HTTPS·GitHub redirect 정책, timeout과 다운로드 크기 상한을 그대로 사용합니다.
- 지원하지 않는 과거 manifest schema는 추정해서 읽지 않고 fail-closed합니다.

### 1.5 미해결 질문

계약의 미해결 질문은 없습니다. 구현 시작은 이번 승인에 포함되지 않으며 별도 사용자 요청 뒤 [03-PLAN.md](./03-PLAN.md)에 따라 진행합니다. 구현 중 새 report 소비자가 발견되면 experimental format 2의 영향을 확인하되 이 계약을 임의로 넓히지 않습니다.

## 2. Spec

### 2.1 요구사항과 시나리오

| 요구사항 ID | 요구사항 | 상황·입력 | 관찰 가능한 결과 | 검증 방법 |
|---|---|---|---|---|
| R-001 | base 없는 기존 `adopt`가 유지됩니다. | `--base-version` 생략 | CLI 인자, format 1 plan, stdout과 artifact byte가 기존 fixture와 같습니다. | 기존 fixture·golden byte 회귀 |
| R-002 | base는 exact release asset으로 검증됩니다. | schema 1 또는 2의 이전 release | exact namespace, checksum, manifest identity, installer byte, locale archive와 member hash가 모두 맞아야 base tree를 읽습니다. 과거 installer는 opaque byte로만 검증하고 실행·import하지 않습니다. | schema별 fake release, tamper negative test |
| R-003 | base 입력과 검증 실패를 fail-closed합니다. | `latest`, leading `v`·불완전 SemVer, base가 current보다 낮지 않음, repository·locale 불일치, 미지원 schema, checksum·redirect·asset tamper | output 없이 원인 범주를 드러내는 `InstallerError`로 실패하고 대상 tree가 같습니다. 개별 오류 문장 전체는 공개 호환 계약으로 고정하지 않습니다. | CLI failure matrix·tree snapshot negative test |
| R-004 | base와 current inventory의 합집합 경로를 분류합니다. | release 사이의 수정·추가·삭제와 프로젝트 수정 | `base ∪ current`의 각 경로에서 target 값을 조회해 `unchanged`·`template-only`·`project-only`·`converged`·`diverged`·`blocked` 중 하나로 분류합니다. target-only 비템플릿 경로는 순회하지 않습니다. | equality truth table·inventory 변화 fixture |
| R-005 | 기존 adoption policy 판단을 보존합니다. | current artifact에 존재하는 경로 | `status`, `policy`, 대상 상태와 기존 `summary`는 현재 release와 대상의 2-way 판단 및 blocked 우선순위를 유지하고, upgrade 분류는 별도 필드입니다. | format 1/2 대조 fixture |
| R-006 | 제거된 template 경로를 숨기지 않습니다. | base에는 있고 current에는 없는 경로 | union `paths`에 `artifact_sha256: null`, `policy: null`, `status: null`로 기록하고 자동 삭제를 제안하지 않습니다. | base-only path fixture |
| R-007 | 대상과 output 안전성을 유지합니다. | 성공·검증 실패·게시 실패·blocked path | 대상 before/after가 같고 output은 전부 원자적으로 게시되거나 남지 않습니다. | failure injection·snapshot 비교 |
| R-008 | report가 결정적이고 provenance를 드러냅니다. | 같은 base/current/target 재실행 | plan byte가 같고 exact `base_release`와 `release`, `upgrade_summary`를 포함합니다. | 두 번 실행 byte 비교 |
| R-009 | 공개 문서가 upgrade와 최초 adoption을 구분합니다. | exact base에서 적용·관리한 저장소와 처음 적용하는 저장소 | en·ko 가이드가 base mode는 target이 exact base에서 유래했다는 전제를 설명하고, 최초 adoption에서는 base를 생략합니다. 여섯 분류, 자동 병합 없음, 제거 예시, `summary`는 current inventory만 세고 `upgrade_summary`는 `base ∪ current`를 세며 base-only 경로는 upgrade 표에만 나타나는 점을 같은 계약으로 설명합니다. | docs·locale parity, export artifact 검사 |
| R-010 | 회귀 fixture와 공개 release에서 upgrade 경로를 확인합니다. | 과거 v2.0→v2.1 fixture 및 다음 minor release와 이전 immutable release | 과거 consumer exact head에서 수동 3-way 판정을 재현하고, 원격 HTTPS에서 `v2.1.0` base→`v2.2.0` current의 base-aware adopt가 대상 불변으로 성공하며 독립 대조와 일치합니다. | historical fixture와 published E2E consumer 검증 |

### 2.2 대안과 선택 이유

- **변경하지 않고 수동 base export 유지:** 코드가 없고 안전하지만 PR #28에서 수동 분류가 필요했고 report의 핵심 정보 격차를 남겨 기각합니다.
- **과거 release의 installer를 자동 다운로드해 실행:** 각 schema를 그 version 코드가 읽는 장점이 있지만, `adopt` 실행 중 검증되기 전의 과거 Python 코드를 자동 실행하는 새 권한 경계를 만들므로 기각합니다.
- **current installer가 모든 과거 schema를 일반 호환:** 편하지만 알 수 없는 미래·과거 schema까지 느슨하게 받아 current release 검증을 약화할 수 있어 기각합니다.
- **base 입력에 한정한 schema 1·2 read-only parser:** 실행 중인 current release 검증은 그대로 두고, 이미 공개된 두 schema의 공통 identity·hash 필드만 엄격히 검증할 수 있어 채택을 권고합니다. 다른 schema는 실패합니다.
- **로컬 `--base-path` 입력:** network 없이 쓸 수 있지만 누가 어떻게 검증한 tree인지 provenance가 사라져 첫 버전에서는 제외합니다.

### 2.3 설계와 계약

#### CLI

```text
python3 installer.py adopt \
  --release-url https://github.com/OWNER/NAME/releases \
  --version <latest-or-current-semver> \
  --base-version <older-exact-semver> \
  --locale <locale> \
  --repo-root <existing-repository> \
  --output <empty-output>
```

`--base-version`은 `adopt`에만 추가되는 선택 인자입니다. 생략하면 D-006 format 1 경로를 그대로 실행합니다. 지정하면 current version을 먼저 exact version으로 resolve하고 SemVer precedence를 비교합니다. base가 current보다 낮지 않거나 같은 repository·locale로 검증되지 않으면 output 생성 전에 실패합니다.

#### Base release 검증

current release는 기존 `_verified_manifest()`와 실행 중인 installer self-binding을 유지합니다. base 전용 검증기는 다음 순서로 읽습니다.

1. exact base version의 `SHA256SUMS`와 `release-manifest.json`을 다운로드하고 manifest byte가 checksum과 맞는지 확인합니다.
2. manifest identity의 repository·version·source commit과 요청한 exact base를 검사합니다. base와 current의 repository·locale는 같아야 합니다.
3. schema 1·2의 모든 object는 아래 exact key 집합을 사용하며 누락·추가 key를 모두 거부합니다. 두 schema의 구조 차이는 `schema_version` 값과 member의 `policy` 유무뿐입니다.
   - top-level: `schema_version`, `version`, `source_commit`, `repository`, `locales`, `installer`
   - installer: `asset`, `sha256`, `bytes`
   - locale record: `status`, `asset`, `sha256`, `bytes`, `compression`, `members`
   - schema 1 member: `path`, `sha256`, `bytes`, `mode`, `timestamp`
   - schema 2 member: schema 1 member key와 `policy`
4. `SHA256SUMS`의 이름 집합은 `{release-manifest.json, installer.py} ∪ {manifest의 모든 locale record가 선언한 asset}`과 정확히 같아야 합니다. 모든 locale archive의 checksum은 manifest record와 대조하지만, 이 단계에서 비선택 locale archive byte를 다운로드하지 않습니다.
5. `installer.py`와 선택 locale archive만 다운로드해 선언된 길이·SHA-256과 대조합니다. base installer byte는 opaque data로만 다루며 import, evaluation, execution 또는 subprocess 호출을 하지 않습니다.
6. 선택 locale archive inventory·mode·timestamp·size·hash를 manifest와 대조해 base member byte를 얻습니다. 정수 위치의 boolean, 범위 밖 크기, 중복·case-fold·부모/자식 충돌 경로도 current verifier와 같은 기준으로 거부합니다.

base asset fetch는 current 경로와 같은 release URL·exact asset URL 구성, HTTPS·GitHub redirect 제한, timeout과 크기 상한을 사용하며 fallback host나 임의 redirect를 허용하지 않습니다. 이 호환 parser는 base 비교에만 쓰며 primary `--version` 검증이나 `install`·`export`에 연결하지 않습니다. GitHub release의 immutable 상태 확인은 installer transport 계약이 아니라 `verify-release.py published`와 release 운영 gate의 책임입니다.

#### 3-way 분류

경로 집합은 base와 current release inventory의 합집합이며 target tree 전체를 순회하지 않습니다. 각 경로의 비교 값은 base artifact `B`, current artifact `C`, target `T`의 file byte이고 부재도 하나의 값으로 취급합니다. symlink·특수 파일·읽기 실패·상위 경로 충돌은 equality 비교 전에 `blocked`입니다.

base mode는 target이 지정한 exact base release에서 적용·관리됐다는 사용자의 선언을 전제로 합니다. byte 비교만으로 “프로젝트가 base 파일을 삭제함”과 “그 파일을 처음부터 적용하지 않음”을 구분할 수 없으므로, 이 provenance를 자동 추론하지 않습니다.

| `upgrade_status` | 조건 | 의미 |
|---|---|---|
| `unchanged` | `B == C == T` | 어느 쪽도 바뀌지 않음 |
| `template-only` | `B == T`, `C != B` | template만 바뀜; 추가·제거 포함 |
| `project-only` | `B == C`, `T != B` | project만 바뀜 |
| `converged` | `C == T`, `B != C` | project가 이미 current template과 같은 결과에 도달 |
| `diverged` | 위 equality 어느 것도 아니고 세 값을 비교 가능 | template과 project가 서로 다른 결과로 바뀜 |
| `blocked` | target을 안전하게 비교할 수 없음 | 수동 경로 판단 필요 |

current 경로의 기존 2-way precedence를 그대로 유지합니다. unsafe target은 policy보다 우선해 current 경로에서는 `status`와 `upgrade_status`가 모두 `blocked`이고, base-only 경로에서는 `status: null`을 유지하며 `upgrade_status`만 `blocked`입니다. 비교 가능한 target에서 policy `decide`는 기존 `status: decision`을 유지하면서 `upgrade_status`를 독립적으로 계산합니다. 분류는 자동 적용 권한이나 권고가 아닙니다.

#### Adoption plan format 2

base를 지정한 실행만 `format_version: 2`를 냅니다.

```json
{
  "format": "coding-agent-docs-template/adoption-plan",
  "format_version": 2,
  "stability": "experimental",
  "base_release": {"repository": "OWNER/NAME", "version": "2.0.0", "source_commit": "<sha>", "locale": "ko"},
  "release": {"repository": "OWNER/NAME", "version": "2.1.0", "source_commit": "<sha>", "locale": "ko"},
  "guide": "artifact/docs/TEMPLATE_GUIDE.md §2",
  "summary": {"missing": 0, "identical": 0, "merge": 0, "decision": 0, "blocked": 0},
  "upgrade_summary": {"unchanged": 0, "template-only": 0, "project-only": 0, "converged": 0, "diverged": 0, "blocked": 0},
  "paths": [
    {
      "path": "README.md",
      "policy": "merge",
      "status": "merge",
      "upgrade_status": "diverged",
      "base_sha256": "<hash-or-null>",
      "artifact_sha256": "<hash-or-null>",
      "target_sha256": "<hash-or-null>",
      "target": "file",
      "reason": "<existing fixed reason or removal review reason>"
    }
  ]
}
```

`paths`는 base와 current inventory의 union이며 POSIX path lexical order로 정렬합니다. current에 있는 경로는 기존 `policy`·`status`·`summary` 계약을 유지합니다. base에만 있는 경로는 `policy`, `status`, `artifact_sha256`이 `null`이고 `summary`에는 포함하지 않으며, `upgrade_summary`에는 포함합니다. 제거는 report에만 드러내고 대상 파일을 삭제하거나 삭제를 안전하다고 판정하지 않습니다. 비교 가능한 base-only 경로의 `reason`은 `This path is absent from the current release; review whether to keep or remove it by hand.`로 고정하고 unsafe target에는 기존 blocked reason이 우선합니다.

다음 report 불변식을 지킵니다.

- `len(paths) == |base ∪ current|`, `sum(summary.values()) == |current|`, `sum(upgrade_summary.values()) == |base ∪ current|`입니다.
- current 경로의 `policy`·`status`는 null이 아니고 base-only 경로에서는 null입니다. `base_sha256`은 base에 없을 때, `artifact_sha256`은 current에 없을 때 null이며 `target_sha256`은 target이 읽을 수 있는 일반 파일일 때만 값을 가집니다.
- JSON key 정렬·UTF-8·LF·마지막 개행과 같은 직렬화 규칙, 기존 `guide`, 절대 경로·실행 시각·사용자 이름을 기록하지 않는 규칙은 format 1과 같습니다.
- output의 `artifact/`는 current release tree만 담습니다. base member byte는 비교에만 쓰며 게시하지 않습니다.
- base 모드 stdout은 먼저 `Upgrade classification assumes the target was derived from base <version>; absence alone cannot prove a project deletion.`을 출력합니다. 기존 `Adoption plan` 줄은 `|current|` 경로와 기존 2-way summary를 세고, non-`identical` current 경로만 기존 status 제목 아래 출력합니다.
- 이어 `Upgrade classification: <|base ∪ current|> paths (...)`를 출력합니다. summary와 경로 section은 `unchanged`, `template-only`, `project-only`, `converged`, `diverged`, `blocked` 순서이고, `upgrade <status>:` section은 `unchanged`를 생략하며 각 section 안의 경로는 POSIX lexical order입니다. base-only 경로는 upgrade 목록에만 나타납니다.

#### Maintainer release verification

`verify-release.py published`에는 선택형 `--base-version <older-exact-semver>`을 추가합니다. 생략하면 D-007의 기존 published E2E와 CLI 동작을 유지합니다. 지정하면 candidate 단계에는 새 network 요구를 만들지 않고, published 단계가 모든 공식 locale에서 `latest`와 exact current selector로 base-aware `adopt`를 실행해 format 2의 두 provenance, cardinality·null 불변식과 target 불변을 확인합니다. 이 임시 fixture 검증은 실제 consumer 검증을 대체하지 않으며 W-005가 별도 consumer에서 결과를 독립 대조합니다.

### 2.4 상위 설계에 미치는 영향

D-006의 대상 무변경, 검증된 staging, 자동 merge·overwrite 제외, experimental report 원칙은 유지합니다. D-006 §3.1 CLI와 §3.3 분류, §3.4 report를 선택형 upgrade 모드로 확장합니다. D-007의 `published`에 선택형 base-aware E2E를 추가하지만 candidate·remote mutation 경계는 유지합니다. release manifest schema 2와 D-004 transport는 바꾸지 않습니다. D-008로 결정하고 PROJECT §11의 T-007 질문을 닫았습니다.

### 2.5 위험·호환성·rollback

| 위험 | 영향 | 완화·rollback |
|---|---|---|
| legacy schema parser가 current 검증을 느슨하게 함 | 잘못된 release 수용 | base 전용 함수로 격리하고 schema 1·2 exact key fixture를 고정 |
| `template-only`를 자동 적용 신호로 오해 | 사용자 문서 손상 | 대상 무변경, 자동 patch 없음, 문서와 plan에 검토 전용 표시 |
| 제거된 경로를 자동 삭제 대상으로 오해 | 프로젝트 파일 손실 | null `status`와 고정 removal reason, 삭제 기능 비범위 |
| inventory union이 report 소비자를 깨뜨림 | 후속 도구 오류 | base 없는 format 1 유지, base 모드만 experimental format 2 |
| SemVer 비교 오류 | 잘못된 base 허용 | prerelease·build metadata truth table과 base >= current negative test |
| 구현 결함 | upgrade 분류 사용 불가 | `--base-version` 생략으로 기존 D-006 경로 사용; target은 항상 불변 |

#### Deferred implementation candidates

아래 항목은 D-008의 승인된 계약과 [03-PLAN.md](./03-PLAN.md) W-001~W-005에 포함되지 않습니다. `v2.2.0` 지원 검증에서 실제 필요가 확인되고 별도 설계 승인을 받은 경우에만 구현 후보로 전환합니다.

- **target metadata의 base version hint:** target의 `docs/DOCS_GUIDE.md` 등에서 기록된 template version을 display-only 참고로 보여 주는 방안입니다. 사용자 편집 값을 base 선택이나 신뢰 판정에 사용하지 않으며, 잘못된 base 선택 사례가 지원 검증에서 확인될 때 재검토합니다.
- **선택형 base source commit pin:** 기계 실행자가 exact base version 외 별도 provenance pin을 요구하는 다중 저장소 자동화가 생길 때 `--base-source-commit`을 재검토합니다. 현재 immutable release·manifest source commit 검증을 중복하는 인자는 추가하지 않습니다.
- **잘못된 upgrade 사용 진단:** `missing` 비율 threshold 경고는 부분 적용 저장소에서 오탐을 만들므로 채택하지 않습니다. target이 base에서 유래했는지 판정할 신뢰 가능한 provenance 신호가 생길 때만 결정적 진단을 다시 설계합니다. 현재는 §2.3의 명시적 전제와 unconditional stdout 주의를 사용합니다.

공개 CLI와 report가 늘어나므로 SemVer는 다음 minor `v2.2.0`을 권고합니다.

### 2.6 완료 조건과 미해결 사항

- **설계 완료:** 이 문서가 승인되고 PROJECT 결정·T-007과 함께 Origin `main`에 통합됩니다.
- **구현 완료:** schema 1·2 base 검증, equality truth table, format 1 호환, format 2 union report, 대상·output 불변 테스트와 전체 gate가 통과하고 Origin `main`에 통합됩니다.
- **공개 완료:** `v2.2.0` immutable release에서 이전 exact release를 base로 한 en·ko 원격 E2E가 통과합니다.
- **회귀 검증:** 업그레이드 전 `claude-review-e2e` exact head와 `v2.0.0` base·`v2.1.0` current byte fixture에서 기존 수동 3-way 판정을 재현합니다.
- **지원 검증:** `v2.1.0`을 적용한 consumer를 target으로 두고 `v2.1.0` base·공개 `v2.2.0` current의 새 report를 사람이 독립적으로 대조합니다.

계약은 승인됐지만 구현은 시작하지 않았습니다. 구현은 별도 사용자 요청 뒤 [03-PLAN.md](./03-PLAN.md)의 미착수 작업부터 진행합니다.

## 3. 변경 기록

- 2026-09-20: T-007 근거와 실제 `v2.0.0` schema 1·`v2.1.0` schema 2 경계를 확인하고 Draft를 작성했습니다. base installer 자동 실행 대신 base 전용 read-only compatibility parser를 권고합니다.
- 2026-09-20: 사용자가 권고 계약을 승인했습니다. 독립적인 보안·report·실행 검토에서 경로 집합, format 2 호환, legacy validator, release·consumer 검증 경계를 보완했고 구현은 별도 시작 요청까지 보류했습니다.
- 2026-09-21: PR #23 리뷰의 checksum 닫힌 집합, schema exact key, base 사용 전제, 두 summary 분모, stdout 순서와 격리 회귀 조건을 보강했습니다. 세 UX·provenance 아이디어는 현재 구현 범위와 분리한 Deferred 후보로 기록했습니다.
