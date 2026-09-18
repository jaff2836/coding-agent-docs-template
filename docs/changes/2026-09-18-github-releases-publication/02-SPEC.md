# 변경 명세: GitHub Releases 기반 v2 공개 배포

## Metadata

- **Change ID:** `2026-09-18-github-releases-publication`
- **Status:** Accepted
- **Intent:** [01-INTENT.md](./01-INTENT.md)
- **Parent:** [제품 기준](../../00-PROJECT.md) D-004
- **Decision:** D-004
- **Approval:** Chae Sangwon, 2026-09-18 사용자 대화 — GitHub Releases 단일 host와 후속 구현 진행 승인
- **Execution:** [03-PLAN.md](./03-PLAN.md)

## 1. 요구사항과 시나리오

| 요구사항 ID | 요구사항 | 상황·입력 | 관찰 가능한 결과 | 검증 방법 |
|---|---|---|---|---|
| R-001 | 공개 release root는 GitHub repository의 Releases URL 하나입니다. | `--release-url https://github.com/jaff2836/coding-agent-docs-template/releases` | 다른 public host나 mirror 없이 asset을 조회합니다. | URL 단위 테스트, 원격 E2E |
| R-002 | `latest`는 exact version 선택에만 사용합니다. | `--version latest` | `/releases/latest/download/release-manifest.json`에서 full SemVer를 읽고 이후 요청은 `/releases/download/v<version>/...`를 사용합니다. | fake release와 원격 요청 기록 |
| R-003 | exact version과 tag naming을 결합합니다. | `--version 2.0.0` | `v2.0.0` release asset만 조회하며 manifest version은 `2.0.0`이어야 합니다. | URL·manifest mismatch 회귀 테스트 |
| R-004 | GitHub asset redirect만 제한적으로 따릅니다. | GitHub가 browser download URL에 3xx를 반환 | GitHub HTTPS release asset URL에서 시작된 HTTPS chain만 따르고 downgrade, credential URL, 비-release 시작점은 거부합니다. | redirect handler 단위·negative 테스트와 원격 E2E |
| R-005 | release URL과 manifest repository를 결합합니다. | manifest의 `repository`가 URL의 `OWNER/NAME`과 다름 | checksum이 맞더라도 설치 전에 실패합니다. | manifest mismatch 테스트 |
| R-006 | bootstrap과 선택 version을 일치시킵니다. | latest installer로 latest 설치 또는 versioned installer로 exact version 설치 | 실행 중 installer hash가 exact manifest와 일치합니다. 서로 다른 release installer 조합은 실패합니다. | installer hash 회귀 테스트 |
| R-007 | 게시 전 exact source와 artifact를 확인합니다. | `v2.0.0` 후보 | tag commit, manifest `source_commit`, package 입력 commit이 같고 clean deterministic package가 통과합니다. 게시 시점의 Origin·GitHub `main`은 같은 SHA이고 tag commit을 조상으로 포함합니다. | local gate, `merge-base --is-ancestor`, GitHub release metadata 확인 |
| R-008 | 공개 전 local gate와 공개 직후 remote gate를 분리합니다. | draft asset과 아직 공개하지 않은 release | 공개 E2E에 필요한 GitHub 다운로드 경로가 draft asset을 제공하지 않으므로 게시 전 deterministic local gate를 통과하고, 검증된 draft asset을 재패키징·교체하지 않은 채 exact release를 게시한 직후 원격 gate를 실행합니다. 실패 시 release를 변조하지 않고 patch release로 복구합니다. | local exact-head gate, draft asset hash 대조, 실제 HTTPS E2E와 release 정책 기록 |

## 2. 대안과 선택 이유

- **GitHub Pages + Releases:** installer의 redirect 거부를 유지할 수 있지만 동일 byte를 두 곳에 게시하고 동기화해야 하므로 기각했습니다.
- **S3/R2/custom CDN:** 직접 asset host와 lifecycle을 통제할 수 있지만 첫 release에 별도 자격 증명·비용·운영면을 추가하므로 보류했습니다.
- **GitHub REST API로 모든 asset 탐색:** `tag_name`과 `browser_download_url`을 명시적으로 얻을 수 있지만 unauthenticated rate limit과 더 큰 응답 검증면을 runtime에 추가합니다. 첫 버전은 GitHub의 stable browser download URL과 release manifest를 사용합니다.
- **GitHub Releases browser download URL:** 저장소와 artifact를 한곳에서 관리하고 `latest`와 exact tag URL을 구분할 수 있어 채택했습니다. redirect 범위를 제한하는 대신 기존의 전면 거부 계약을 대체합니다.

## 3. 설계와 계약

### 3.1 공개 URL

```text
release root:
https://github.com/jaff2836/coding-agent-docs-template/releases

latest bootstrap:
https://github.com/jaff2836/coding-agent-docs-template/releases/latest/download/installer.py

latest pointer:
https://github.com/jaff2836/coding-agent-docs-template/releases/latest/download/release-manifest.json

exact asset:
https://github.com/jaff2836/coding-agent-docs-template/releases/download/v2.0.0/<asset>
```

CLI의 `--release-url`은 release root를 받습니다. GitHub public URL은 정확히 `https://github.com/<OWNER>/<NAME>/releases` 형태여야 합니다. localhost는 테스트 fixture에서만 기존 `<root>/<version>/<asset>` 구조를 허용합니다.

### 3.2 Version resolution

1. `latest` 요청은 latest release의 `release-manifest.json`을 받습니다.
2. pointer manifest를 schema 검증하고 `version`을 얻습니다.
3. 이후 `SHA256SUMS`, exact manifest, installer와 locale archive는 모두 `v<version>` tag의 release URL에서 받습니다.
4. exact manifest의 version, repository, checksum과 실행 중 installer hash를 확인합니다.

latest pointer는 신뢰할 최종 manifest가 아니라 exact namespace를 선택하는 입력입니다. 최종 설치 판단에는 exact tag namespace에서 다시 받은 checksum과 manifest만 사용합니다.

### 3.3 Redirect boundary

- redirect를 시작할 수 있는 URL은 검증된 GitHub release root에서 만든 `latest/download/<asset>` 또는 `download/v<SemVer>/<asset>`뿐입니다.
- 모든 hop은 HTTPS이고 hostname이 존재하며 credential과 fragment가 없어야 합니다.
- 첫 GitHub 응답에서 이어진 redirect chain만 허용하고 별개의 임의 URL은 허용하지 않습니다.
- redirect 수와 반복은 표준 library handler의 제한보다 더 좁게 제한합니다.
- localhost fixture는 redirect를 계속 거부합니다.

GitHub가 사용하는 CDN hostname은 공개 영구 계약이 아니므로 특정 S3/CDN hostname 목록을 코드에 고정하지 않습니다. 대신 신뢰한 GitHub asset endpoint가 직접 지시한 HTTPS chain과 최종 byte checksum을 함께 검증합니다.

### 3.4 Release provenance

- public SemVer `2.0.0`은 annotated tag `v2.0.0`에 대응합니다.
- tag가 가리키는 commit, packager의 `--source-commit`, manifest `source_commit`은 같아야 합니다.
- 게시 시점의 Origin `main`과 GitHub `main`은 같은 commit을 가리키고, tag commit은 그 commit의 조상이어야 합니다. tag 이후 `main`의 정상적인 전진은 release provenance를 깨뜨리지 않습니다.
- draft에 올린 검증된 asset은 게시 직전의 더 최신 `main`으로 다시 package하거나 교체하지 않습니다.
- manifest `repository`는 release root에서 추출한 `jaff2836/coding-agent-docs-template`와 같아야 합니다.
- mutable branch의 현재 head는 설치 시점의 version 증거로 사용하지 않습니다.

## 4. 상위 설계에 미치는 영향

D-004는 D-002의 locale artifact·checksum·비파괴 설치 구조를 유지하지만, host-neutral URL과 redirect 전면 거부 부분을 GitHub Releases 전용 transport로 대체합니다. 2026-09-09 SPEC은 당시 구현·검증 이력으로 유지하며 현재 공개 배포 계약은 이 문서가 소유합니다.

## 5. 위험·호환성·rollback

- v2.0.0은 아직 공개되지 않았으므로 `--release-url` 의미와 redirect 정책 변경은 공개 설치 호환성을 깨지 않습니다.
- GitHub latest release 선택 규칙이나 browser URL이 바뀌면 원격 E2E가 실패합니다. API 기반 탐색 또는 별도 host 전환은 새 설계로 처리합니다.
- immutable release 게시 뒤 잘못된 asset은 교체하지 않습니다. 문제 release를 latest에서 제외하고 수정한 patch version을 새 tag·release로 게시합니다.
- tag를 push한 뒤 release 게시 전 실패하면 tag가 외부에 소비되지 않았는지 확인하고 중단합니다. 공개된 tag는 재지정하지 않습니다.

## 6. 완료 조건과 미해결 사항

구현 완료는 installer·문서·회귀 테스트가 현재 branch에서 통과하는 상태입니다. 공개 완료는 deterministic package를 생성한 exact tag commit이 현재 Origin·GitHub `main`의 조상이고 tag·manifest·draft asset provenance가 일치하며, draft asset을 재패키징·교체하지 않고 게시한 GitHub release의 remote HTTPS en/ko install·export와 checksum 검증까지 통과하고 그 근거가 PROJECT와 PLAN에 기록된 상태입니다.

GitHub immutable releases 설정의 실제 사용 가능 여부는 release 게시 전에 확인하며, 결과와 무관하게 asset 비변조 운영 규칙을 적용합니다.

## 7. 명세 변경 기록

- 2026-09-18: 사용자 승인에 따라 GitHub Releases 단일 host, tag 기반 exact namespace와 제한된 HTTPS redirect 계약을 Accepted로 기록했습니다.
- 2026-09-18: 후속 `main` 통합으로 tag SHA와 branch head가 달라진 상태를 반영해, tag commit의 `main` 조상 관계를 요구하고 검증된 draft asset을 재패키징 없이 게시하는 조건으로 교정했습니다.
