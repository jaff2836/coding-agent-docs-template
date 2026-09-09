# 변경 명세: 다국어 템플릿 소스와 배포 구조

> 이 명세는 Draft입니다. 사용자 승인 전에는 locale 구조, packager 또는 installer를 구현하지 않습니다.

## Metadata

- **Change ID:** 2026-09-09-multilingual-template
- **Status:** Draft
- **Intent:** [01-INTENT.md](./01-INTENT.md)
- **Parent:** `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`의 [Template Guide](../../TEMPLATE_GUIDE.md) §1·§2·§4·§5
- **Decision:** 미발급 — 승인되면 [PROJECT §8](../../00-PROJECT.md)에 등재
- **Approval:** 미승인 — 2026-09-09 대화에서 locale source, BCP 47, 선택형 installer, 최종 검수자와 첫 안정판의 `en`·`ko` complete 포함까지 부분 합의. skill 현지화 방식과 전체 명세는 미승인
- **Execution:** [03-PLAN.md](./03-PLAN.md), 전역 [T-001](../../02-TODO.md)

## 1. 요구사항과 시나리오

| 요구사항 ID | 요구사항 | 상황·입력 | 관찰 가능한 결과 | 검증 방법 |
|---|---|---|---|---|
| R-001 | 지원 언어는 canonical BCP 47 tag로 식별합니다. | `en`, `ko`, underscore 또는 미지원 tag 입력 | `en`·`ko`는 선택되고 `en_US`·미지원 tag는 쓰기 전에 거부됩니다. region·script subtag는 실제 구분이 필요한 후속 locale에서만 추가합니다. | manifest·CLI 단위 테스트와 BCP 47 형식 negative fixture |
| R-002 | 저장소 관리 영역과 배포 payload를 분리합니다. | maintainer가 root 설계/TODO를 수정하거나 locale source를 편집 | root 관리 문서는 artifact에 없고, artifact에는 공통 payload와 선택 locale source만 있습니다. | artifact member 목록과 root 전용 파일 부재 검사 |
| R-003 | 적용 artifact는 locale 하나를 현재의 고정 경로에 materialize합니다. | `--locale ko`로 build/install | root `AGENTS.md`, `README.md`, `docs/`, `.agents/skills/`, `.claude/skills/`, `.cursor/BUGBOT.md`, `.omp/WATCHDOG.md`가 한국어판 계약으로 배치되고 `locales/`는 없습니다. | 임시 디렉터리 artifact E2E와 정확한 member inventory |
| R-004 | 언어 비의존 파일과 locale별 파일의 소유권이 명시적이어야 합니다. | 같은 output path가 common과 locale에 중복되거나 locale 파일이 누락됨 | build가 모호한 override나 불완전 locale을 거부합니다. | source manifest schema·충돌·누락 fixture |
| R-005 | locale별 artifact는 exact source에 대해 결정적이고 검증 가능해야 합니다. | 같은 commit·version·locale로 두 번 build | archive bytes와 SHA-256이 같고 manifest가 source commit, version, locale, 전체 member hash를 기록합니다. | 이중 build byte 비교, schema 검사, rebuild 검증 |
| R-006 | installer는 명시한 locale artifact만 검증 후 원자적으로 설치합니다. | `--version latest --locale ko --repo-root <path>` | manifest와 archive를 먼저 검증·stage하고 충돌이 없을 때만 씁니다. 실패 전에는 아무 파일도 바뀌지 않습니다. | fake downloader, checksum·경로·symlink·부분 실패·충돌 테스트 |
| R-007 | 사용자가 수정할 문서는 자동 update하거나 덮어쓰지 않습니다. | 대상에 `AGENTS.md`, README 또는 관리 문서가 이미 있음 | installer가 전체 충돌 목록과 별도 export 방법을 안내하고 쓰지 않습니다. locale 전환도 새 디렉터리 export와 수동 merge를 요구합니다. | 기존 파일 보존 E2E와 before/after tree hash |
| R-008 | 모든 공식 locale은 같은 구조·placeholder·정책 marker를 구현합니다. | 영어 source에 필수 파일, placeholder, section marker 또는 명령이 추가됨 | 한국어판이 동등 계약으로 갱신되지 않으면 locale gate가 실패합니다. 번역 문자열 자체의 동일성은 요구하지 않습니다. | locale parity checker와 각 불일치 negative fixture |
| R-009 | 도구별 진입점과 복제 규칙은 locale 안에서 유지됩니다. | 선택 locale을 export | `CLAUDE.md`와 WATCHDOG import가 유효하고, `.agents`/`.claude` 스킬 쌍 및 REVIEW/BUGBOT 불변조건이 그 locale 안에서 일치합니다. | locale별 `check-docs.py --root` 실행과 행동 fixture |
| R-010 | 현재 한국어판의 의미와 검사를 보존합니다. | `v1.7.1`에서 `locales/ko`로 최초 이관 | 저장소 관리 문서를 제외한 기준 payload가 byte-identical하거나 명시적으로 승인된 구조 변경만 보입니다. 기존 문서 검사 6개가 새 root 인자를 사용해 통과합니다. | `fb70176` payload manifest와 이관 결과 비교, 회귀 테스트 |
| R-011 | 지원 상태와 release 정책을 분리해 표시합니다. | 번역이 영어 기준보다 뒤처지거나 실험 locale이 추가됨 | `complete`, `experimental`, `stale` 상태와 기준 version이 보입니다. 첫 안정판은 `en`·`ko`가 모두 `complete`일 때만 만들며 그 밖의 locale은 `complete`인 경우에만 포함합니다. | manifest 상태 전이·필수 locale gate·release inclusion 테스트 |
| R-012 | 미지원 언어에는 안전한 fallback이 있습니다. | 사용자가 `fr` 문서를 원하지만 공식 bundle이 없음 | 영어 bundle 사용과 `AGENTS.md`의 응답·프로젝트 문서 언어 설정 방법을 안내하며 `fr` 지원을 주장하지 않습니다. | CLI 오류/안내 snapshot과 문서 검사 |

## 2. 대안과 선택 이유

| 대안 | 장점 | 비용·위험 | 결정 |
|---|---|---|---|
| A. 영어 root 하나와 응답 언어 설정만 제공 | 정본 하나, 구현·유지 비용 최소 | 템플릿 설명·정책·스킬 자체의 공식 번역을 제공하지 못함 | 미지원 언어 fallback으로 유지 |
| B. 적용 프로젝트의 `docs/<locale>/`에 여러 언어를 함께 설치 | 번역본을 동시에 열람 가능 | 고정 root 진입점은 해결하지 못하고, 정본 중복·링크 drift·에이전트의 잘못된 locale 선택 위험 | 기각 |
| C. locale별 전체 tree를 중복 관리 | build가 단순하고 locale 하나를 그대로 배포 가능 | 언어 비의존 파일까지 복제되어 보안·검사 코드 drift 가능 | locale prose에는 사용하되 common 분리로 보완 |
| D. common payload와 `locales/<tag>` source를 합성해 locale별 artifact 생성 | 고정 경로, 선택 설치, 공통 코드 정본, 완전한 번역을 함께 만족 | packager·manifest·parity 검사 필요 | 선택 |
| E. 사용자가 전체 템플릿을 직접 번역 | 저장소 유지 비용 없음 | 지원이 아니라 책임 전가이며 정책 의미와 검사 계약이 깨질 수 있음 | 공식 미지원 언어의 수동 fallback만 |

선택안 D는 `claude-code-pr-review`의 locale별 immutable bundle·manifest·installer 패턴을 재사용합니다. 다만 이 템플릿의 문서는 적용 후 사용자가 광범위하게 수정하므로 그 프로젝트의 자동 update 의미론은 재사용하지 않습니다.

skill 현지화는 다음 두 안을 별도로 비교합니다.

| 대안 | 장점 | 비용·위험 | 현재 판단 |
|---|---|---|---|
| S1. 영어 `description`·본문을 공통 사용하고 출력 언어만 locale로 지정 | 실행 prompt 정본 하나로 의미 drift가 가장 적음 | 한국어 `complete` artifact에도 사용자가 읽고 수정할 핵심 지침이 영어로 남고, 기존 한국어판에서 사용성이 후퇴함 | 미선택 |
| S2. `description`·본문·출력 정책을 locale별로 작성 | artifact 전체가 해당 locale로 일관되고 사용자가 직접 검토·수정하기 쉬움 | 번역 간 호출 조건·행동 drift를 별도 검증해야 함 | **권고안, 사용자 결정 대기** |

S2를 선택하면 번역 문자열을 정본으로 서로 대조하지 않습니다. `locales/manifest.json`의 안정적인 skill ID·contract marker·fixture ID가 공통 계약을 소유하고, 각 locale의 자연어는 동일한 행동 fixture를 통과해야 합니다. 최종 번역·의미 검수자는 Chae Sangwon입니다.

## 3. 설계와 계약

### 3.1 소스 경계

목표 source layout은 다음과 같습니다. 실제 파일 분류는 PLAN W-001에서 manifest로 고정합니다.

```text
README.md                         # 저장소 영문 소개, artifact 제외
README.ko.md                      # 저장소 한국어 소개, artifact 제외
AGENTS.md                         # 템플릿 저장소 유지관리 지침, artifact 제외
docs/                             # 템플릿 저장소 설계·TODO, artifact 제외

template/common/                  # 언어 비의존 payload
  CLAUDE.md
  LICENSE
  .gitignore
  .agents/skills/review-round/agents/openai.yaml
  scripts/check-docs.py
  tests/test_check_docs.py

locales/manifest.json             # 지원 tag, 상태, source inventory
locales/en/                       # 영어 locale payload source
  AGENTS.md
  README.md
  docs/
  .agents/skills/*/SKILL.md
  .claude/skills/*/SKILL.md
  .cursor/BUGBOT.md
  .omp/WATCHDOG.md
locales/ko/                       # 같은 상대 경로의 한국어 locale payload source
  ...

scripts/export-template.py        # 로컬 source에서 한 locale materialize
scripts/package-release.py        # deterministic ZIP과 release manifest 생성
scripts/installer.py              # release asset 선택·검증·설치
scripts/check-locales.py          # source·artifact parity 검사
schemas/release-manifest.schema.json
tests/                            # packager·installer·locale 계약 검사
```

`template/common`과 한 locale tree는 같은 output path를 소유할 수 없습니다. output inventory는 `locales/manifest.json`의 공통 목록과 locale별 필수 목록으로 닫혀 있으며, 예기치 않은 파일·누락·중복은 build 오류입니다.

W-001 이관 시점의 `scripts/check-docs.py`와 테스트는 한국어 heading을 직접 사용하므로 일단 `locales/ko`가 소유합니다. W-003에서 안정 marker 기반의 locale-aware 구현으로 바꾼 뒤 위 목표 layout의 `template/common`으로 이동합니다. 중간 상태를 언어 비의존이라고 표시하지 않습니다.

### 3.2 locale와 고정 진입점

- locale key는 [BCP 47 / RFC 5646](https://www.rfc-editor.org/info/rfc5646/) tag의 canonical casing을 사용합니다. subtag 구분자는 hyphen(`-`)이며 초기 allowlist는 `en`, `ko`입니다. `_`는 허용하지 않습니다. 첫 구현은 임의 tag를 정규식만으로 "지원"하지 않고 manifest allowlist membership을 판정합니다.
- release artifact에는 locale 하나만 들어가며 tag는 디렉터리명, manifest key, asset 이름, installer 인자에서 동일합니다.
- locale source의 `AGENTS.md`가 적용 artifact의 root `AGENTS.md`가 됩니다. 언어 정책은 이 파일과 같은 locale의 REVIEW/스킬에만 존재합니다.
- locale source의 `README.md`는 기존 `README-PROJECT.md` 내용에서 이관한 적용 프로젝트용 양식이며 artifact root `README.md`가 됩니다. 저장소 소개용 root README와 `README-PROJECT.md`는 artifact에 넣지 않습니다.
- `CLAUDE.md`처럼 내용 전체가 언어 비의존인 import 파일만 common에 둡니다. import 외에 advisor prose가 있는 `.omp/WATCHDOG.md`는 locale source가 소유합니다.
- skill 현지화가 S2로 승인되면 `description`, `argument-hint`, 본문과 출력 언어 정책은 공식 locale별 source가 소유합니다. 같은 locale 안의 `.agents`와 `.claude` `SKILL.md`는 현재처럼 byte-identical이어야 하며, locale 간에는 안정적인 skill ID·contract marker·행동 fixture가 일치해야 합니다. S1이 선택되면 이 항목은 공통 영어 source와 locale별 출력 언어 설정으로 대체합니다.
- `.cursor/BUGBOT.md`는 import를 지원하지 않는 계약 때문에 locale별 source에 두고, 같은 locale의 `docs/REVIEW.md` 불변조건과 대조합니다.

### 3.3 build와 release contract

`export-template.py --locale <tag> --output <empty-dir>`는 common과 선택 locale을 임시 디렉터리에 materialize하고 모든 검사를 통과한 뒤 비어 있는 output에 기록합니다. source tree에서 임의 Markdown을 찾지 않고 manifest inventory만 읽습니다.

`package-release.py`는 exact source commit과 SemVer를 입력받아 다음 asset을 결정적으로 생성합니다.

```text
coding-agent-docs-template-en-v2.0.0.zip
coding-agent-docs-template-ko-v2.0.0.zip
release-manifest.json
SHA256SUMS
installer.py
```

archive entry는 정렬된 regular file, 고정 mode·timestamp, UTF-8/LF 계약을 사용합니다. manifest는 schema version, template version, source commit, repository, locale 상태, archive SHA-256·bytes, 모든 member path·SHA-256·bytes를 포함합니다. 첫 안정 release는 `en`·`ko`가 모두 `complete`여야 만들 수 있고, 추가 locale도 `complete` 상태일 때만 들어갑니다.

### 3.4 installer contract

지원 명령의 초안은 다음과 같습니다.

```text
python3 installer.py install --version latest --locale ko --repo-root /path/to/project
python3 installer.py export --version 2.0.0 --locale en --output /empty/path
python3 installer.py list-locales --version latest
```

- remote 설치는 mutable branch의 raw 파일을 조합하지 않고 같은 immutable release/version namespace의 manifest와 locale ZIP을 받습니다. 실제 배포 host와 bootstrap URL은 구현 중 별도 결정하며 GitHub Releases를 숨은 선행조건으로 두지 않습니다.
- `--locale`는 명시 입력이며 manifest의 `complete` locale이어야 합니다.
- 다운로드 크기와 member 크기를 제한하고 manifest·archive·각 member hash, source commit, version, locale, exact path inventory를 대조합니다.
- 절대 경로, `..`, 중복 member, symlink·비정규 파일과 case-fold 충돌을 거부합니다.
- 모든 bytes를 별도 임시 디렉터리에 stage한 뒤 대상 충돌을 전체 검사합니다. 충돌이 하나라도 있으면 대상에 쓰지 않습니다.
- 첫 버전에는 `--force`와 자동 `update`를 제공하지 않습니다. 기존 프로젝트나 locale 전환은 빈 디렉터리로 export한 뒤 사용자가 diff·merge합니다.
- installer는 commit, push, PR 생성 또는 placeholder 자동 작성을 하지 않습니다.

### 3.5 locale와 문서 검사

현재 `check-docs.py`의 locale별 헤딩 문자열은 안정적인 marker로 바꿉니다. 예시는 `<!-- template-section:release-history -->`, `<!-- template-section:project-invariants -->`처럼 번역하지 않는 HTML comment입니다. 번호가 있는 heading 구조와 내부 상대 링크는 locale 간 동일하게 유지합니다.

검사는 다음 두 층입니다.

1. `check-locales.py`: source inventory, marker 순서, placeholder multiset, 명령 문자열, `.agents`/`.claude` 쌍, locale 상태와 기준 version parity를 검사합니다.
2. `check-docs.py --root <materialized-dir>`: locale artifact 하나의 링크, import, 절 참조, REVIEW/BUGBOT 불변조건, version과 release history를 검사합니다.

root 저장소의 locale source 디렉터리를 활성 프로젝트 문서처럼 재귀 검사하지 않습니다. packager는 모든 `complete` locale을 materialize해 두 검사를 통과해야 artifact를 만듭니다. 진단 메시지 자체의 번역은 첫 버전의 지원 계약에 포함하지 않습니다.

### 3.6 부트스트랩과 데이터 흐름

```text
fb70176의 한국어 payload
  → locale/공통 inventory 분류
  → locales/ko + template/common으로 byte 보존 이관
  → root를 저장소 유지관리 영역으로 전환
  → locales/en 번역·동등성 검사
  → exact commit에서 locale별 ZIP + manifest 생성
  → installer가 version·locale 선택
  → 검증·staging·충돌 검사
  → 표준 root 경로에 한 locale만 설치
```

현재 root의 이 변경 문서와 maintainer TODO는 `fb70176` payload snapshot에 포함되지 않으며 locale artifact에도 들어가지 않습니다. 설계 branch를 그대로 템플릿으로 배포하지 않습니다.

## 4. 상위 설계에 미치는 영향

- [Template Guide](../../TEMPLATE_GUIDE.md) §1의 파일 구조와 §2의 직접 복사 절차를 source·artifact·installer 구조로 대체합니다.
- §4의 root 진입점과 import 관계는 유지하되 source 위치와 materialize 단계를 추가합니다.
- §5의 적용 후 관리는 template version/source revision 비교를 유지하며 자동 update를 금지하는 새 installer 계약을 연결합니다.
- [Documentation Guide](../../DOCS_GUIDE.md)의 단일 언어 운영 원칙은 적용 artifact에 그대로 유지하고, 원본 저장소의 locale source 관리 규칙을 추가합니다.
- 승인되면 PROJECT §8에 새 결정을 추가하고, root 문서는 저장소 유지관리 정본으로 전환합니다. 승인 전에는 현재 제품 기준으로 기록하지 않습니다.

## 5. 위험·호환성·rollback

| 위험 | 영향 | 완화 |
|---|---|---|
| 번역은 존재하지만 의미·호출 조건이 다름 | agent 행동과 리뷰 판정 drift | 안정 marker, placeholder·구조 parity, locale별 행동 fixture, 사람의 번역 승인 |
| common/locale 분류 오류 | 파일 누락 또는 locale 혼합 | 닫힌 manifest inventory, 중복·누락 실패, artifact E2E |
| installer가 기존 프로젝트 문서를 덮어씀 | 사용자 결정·이력 손실 | 충돌 시 전부 중단, 빈 디렉터리 export, 첫 버전 `--force`·`update` 없음 |
| release asset과 source가 다름 | 재현 불가·공급망 위험 | exact full SHA, SHA-256, deterministic rebuild, schema와 checksum |
| root 직접 복사 사용자에게 v2가 깨짐 | 기존 적용 절차 비호환 | v2 major, root README의 명시적 installer 안내, v1.7.1 tag 보존 |
| locale 추가가 모든 release를 영구 차단 | 유지보수 병목 | 상태 분리, 안정판에는 `complete`만 포함, 기존 complete locale의 검사 유지 |

이 변경은 root가 더 이상 직접 복사 가능한 payload가 아니라 source·maintenance repository가 된다는 breaking change이므로 `v2.0.0`을 제안합니다. 기존 사용자는 `v1.7.1` tag를 계속 사용할 수 있고, 이미 적용한 저장소는 자동 migration 대상이 아닙니다. 구현 중 실패하면 source 분리 branch를 폐기하고 `fb70176`/`v1.7.1` 구조로 돌아갑니다.

## 6. 완료 조건과 미해결 사항

### 설계 완료

- 사용자에게 문제·범위, 요구사항, 선택안, installer 차이, migration·rollback을 설명하고 명시적 승인을 받습니다.
- 승인 상태와 PROJECT 결정 ID를 갱신합니다.

### 구현 완료

- PLAN의 모든 작업이 해당 branch에서 검증되고 locale별 deterministic artifact E2E가 통과합니다.
- 기존 한국어 payload 보존 또는 승인된 차이 목록이 확인됩니다.
- 문서 검사, locale parity, packager, installer의 성공·실패 경로가 모두 통과합니다.

### 통합·릴리스·지원 검증

- 구현 commit이 지정한 통합 대상에 반영된 뒤 root 제품 기준과 TODO를 갱신합니다.
- `v2.0.0` tag·GitHub release 게시와 원격 checksum은 별도 명시적 위임이 있을 때만 수행합니다.
- 실제 Claude, Codex, Cursor, OMP가 `en`, `ko` artifact의 고정 진입점과 스킬을 로드하는 소비자 저장소 E2E를 통과해야 두 locale을 지원 완료로 표시합니다.

남은 질문은 [Intent §5](./01-INTENT.md)의 skill 현지화 방식과 실제 공개 repository URL입니다. 번역 최종 승인자와 첫 안정판의 `en`·`ko` complete 포함은 합의되었습니다.

## 7. 명세 변경 기록

- 2026-09-09: locale source, BCP 47, deterministic release bundle과 비파괴 installer를 결합한 최초 Draft를 작성했습니다.
- 2026-09-09: 첫 안정판의 `en`·`ko` 동시 complete gate와 최종 검수자를 확정했습니다. skill 현지화는 S2를 권고하되 미승인 대안으로 구분했습니다.
- 2026-09-09: Origin PR #3 리뷰에 따라 WATCHDOG의 locale 소유권, 적용 README 정본과 installer의 host-neutral asset 계약을 명확히 했습니다.
