# CI 품질 게이트

이 문서는 **무엇을, 어떤 순서로, 성공·실패를 어떻게 판정하는지**를 정합니다. 이 저장소의 Windows·Linux Buildkite pipeline은 각각 `.buildkite/pipeline.yml`·`.buildkite/linux.yml`을 업로드해 실행합니다. 템플릿 적용 프로젝트가 GitHub Actions, Buildkite, 그 외 러너 중 무엇을 쓸지는 각 프로젝트가 고릅니다.

원격 CI는 필수가 아닙니다. CI가 없으면 같은 게이트를 로컬에서 실행하고, 미사용 이유와 대체 검증을 [02-TODO.md](./02-TODO.md)의 통합 완료 조건 또는 프로젝트 README에 남깁니다.

## Metadata

- **Status:** Active
- **Owner:** Repository maintainers
- **Last reviewed:** 2026-09-23
- **Review cadence:** 품질 게이트 구성 또는 로컬 명령이 바뀔 때

명령 문자열의 정본은 루트 [AGENTS.md](../AGENTS.md)와 적용 프로젝트 README입니다. 한쪽만 바꾸지 마세요. 기계적 규칙은 리뷰 finding이 아니라 이 게이트로 강제합니다. 판정 기준은 [REVIEW.md](./REVIEW.md) §12입니다.

## 1. 역할

| 하는 일 | 하지 않는 일 |
| --- | --- |
| 결정적·반복 가능한 검사 (문서 링크, 테스트, 린트, 타입 검사, 빌드) | 설계 합의, 리뷰 판정, 리뷰 라운드 |
| 검사 대상 revision에 대해 통과/실패를 남김 | 비밀값·토큰을 로그에 남김 |
| [AGENTS.md](../AGENTS.md)에 적힌 명령을 그대로 실행 | 문서에 없는 명령을 CI에만 두거나, CI에만 있는 명령을 문서에 성공으로 적음 |
| 실패 시 0이 아닌 종료 코드로 파이프라인을 실패 | 필수 게이트를 무시하고 통과 처리 |

리뷰어 봇·advisor·스킬은 CI 잡을 대체하지 않습니다. 반대로 CI가 잡는 포맷·린트 문제를 리뷰 finding으로 올리지 않습니다.

## 2. 워크플로

적용 프로젝트가 고른 러너에서 아래 순서를 구현합니다. 단계 이름만 바꾸고 순서를 건너뛰지 마세요.

1. **대상 확정.** 통합 대상으로 가는 변경마다 돌립니다. 브랜치 push, 변경 요청(PR·MR)의 열림·갱신, 통합 브랜치로의 merge 직전이 해당합니다. 검사 대상은 그 변경의 **정확한 revision**입니다.
2. **Checkout.** 그 revision만 꺼냅니다. 다른 브랜치나 로컬 미커밋 상태를 섞지 않습니다.
3. **런타임.** 프로젝트 README·AGENTS.md가 요구하는 런타임을 준비합니다. 로컬과 메이저 버전이 같아야 합니다. 문서 게이트만 돌릴 때는 표준 라이브러리 Python이면 충분합니다 (`python`이 없으면 `python3`).
4. **의존성.** 이어지는 게이트가 패키지 설치를 필요로 할 때만 설치합니다. 설치 명령은 AGENTS.md의 Install과 같게 둡니다. 분석·리뷰 **세션**의 “자동 설치 금지”와 CI 러너의 설치는 별개입니다.
5. **게이트 실행.** §3 표를 위에서 아래로 따릅니다. `N/A`이거나 적용 조건에 안 맞는 행은 건너뛰고, 건너뛴 이유를 문서에 남긴 상태여야 합니다.
6. **실패 전달.** 필수 게이트가 0이 아닌 종료 코드로 끝나면 파이프라인을 실패로 표시하고 통합을 막습니다. 실패를 경고만 하고 통과시키지 않습니다.
7. **결과 연결.** 로그와 통과/실패 표시는 검사한 revision에 붙입니다. 이전 커밋의 초록 결과를 현재 head의 통과로 재사용하지 않습니다.

한 잡에서 실패 즉시 중단할지, 모든 게이트를 돌린 뒤 모을지는 프로젝트가 고릅니다. 어느 쪽이든 필수 게이트 실패는 최종 실패여야 합니다.

```text
변경 도착 → revision checkout → 런타임 → (필요 시) 설치
  → 문서 검사 → (원본 템플릿) locale source 검사
  → (조건) 각 검사기의 회귀 테스트
  → 린트 / 타입 검사 / 테스트 / 빌드 중 문서화된 것만
  → 실패 있으면 통합 차단, 없으면 통과 표시
```

## 3. 게이트 목록

| ID | 게이트 | 명령의 정본 | 필수인 때 | 건너뛰는 때 |
| --- | --- | --- | --- | --- |
| G-docs | 문서 검사 | `python3 scripts/check-docs.py` | 이 템플릿의 `scripts/check-docs.py`를 유지하는 저장소 | 스크립트를 적용 저장소에서 제거한 경우. 제거했다면 들어오는 안내 링크도 정리 |
| G-docs-test | 문서 검사 회귀 | `python3 -m unittest discover -s tests -p 'test_check_docs.py' -v` | `scripts/check-docs.py` 또는 `tests/test_check_docs.py`를 바꾼 변경. 템플릿 원본 저장소는 상시 | 적용 저장소에서 검사 스크립트를 바꾸지 않은 일상 변경. 테스트 파일을 제거했다면 G-docs만 유지 |
| G-locale-source | locale source 검사 | `python3 scripts/check-locales.py` | locale source를 관리하는 이 템플릿 원본 저장소 | 적용 artifact와 일반 적용 저장소. 이 gate는 artifact에 포함되지 않음 |
| G-locale-source-test | locale source 검사 회귀 | `python3 -m unittest discover -s tests -p 'test_check_locales.py' -v` | 이 템플릿 원본 저장소는 상시 | 적용 artifact와 일반 적용 저장소 |
| G-lint | 린트 | AGENTS.md / README의 Lint | 해당 명령이 `N/A`가 아니고 검증된 때 | 미설정 placeholder, `N/A`, 또는 미검증으로 기록된 때 |
| G-type | 타입 검사 | AGENTS.md / README의 Typecheck | 위와 같음 | 위와 같음 |
| G-test | 프로젝트 테스트 | AGENTS.md / README의 Test | 위와 같음 | 위와 같음 |
| G-build | 빌드 | AGENTS.md / README의 Build | 산출물이 있고 명령이 `N/A`가 아닌 때 | 위와 같음 |
| G-adopt | placeholder 검색 | [TEMPLATE_GUIDE.md](./TEMPLATE_GUIDE.md) §3의 `rg`/`grep` | 템플릿을 적용한 직후 한 번 | 원본 템플릿 저장소. 이미 값을 채운 뒤의 매 파이프라인. TEMPLATE_GUIDE를 삭제했다면 적용 당시 복사한 검색 명령 또는 [DOCS_GUIDE.md](./DOCS_GUIDE.md) 체크리스트로 대체 |

G-docs는 원본 템플릿의 placeholder 잔존을 실패로 보지 않습니다. G-locale-source는 manifest에 선언한 common·locale source 전체의 placeholder·marker·구조 계약을 검사합니다. 적용 저장소의 placeholder는 G-adopt와 [DOCS_GUIDE.md](./DOCS_GUIDE.md) 체크리스트로 확인합니다.

새 프로젝트 게이트를 추가할 때는 이 표에 행을 넣고 AGENTS.md·README 명령과 같은 문자열을 씁니다. 표에만 있고 문서 명령에 없는 검사를 두지 마세요.

## 4. 연결 체크리스트

러너를 새로 고르거나 기존 파이프라인에 이 템플릿을 붙일 때 사용합니다. 제품 이름은 적지 않아도 됩니다. 기존 파이프라인이 있으면 그 안에 게이트를 넣고, 없을 때만 사용자가 지정한 제품으로 만듭니다.

### 트리거와 revision

- [ ] 통합 대상으로 가는 변경마다 파이프라인이 시작된다.
- [ ] Checkout한 commit이 검사 대상 revision과 같다.
- [ ] 통과 표시가 다른 commit의 결과를 현재 head에 재사용하지 않는다.

### 명령과 문서

- [ ] 각 게이트의 명령 문자열이 AGENTS.md·README와 같다.
- [ ] placeholder가 남은 명령은 실행하지 않으며, `N/A`이면 이유와 함께 이 표에서 건너뛴다.
- [ ] G-docs를 유지하면 러너의 `python`/`python3` 또는 명시적 `python.exe` 경로로 문서의 동일한 스크립트를 실행한다.
- [ ] 의존성 설치가 필요하면 Install 명령을 게이트 앞에만 둔다.

### 실패와 권한

- [ ] 필수 게이트의 0이 아닌 종료 코드가 파이프라인 실패가 된다. 실패를 무시하는 옵션을 필수 게이트에 쓰지 않는다.
- [ ] 실패 로그가 그 변경 요청 또는 commit에서 열린다.
- [ ] 비밀값·토큰이 로그·산출물·캐시에 남지 않는다.
- [ ] 러너 자격 증명은 검사에 필요한 최소 권한이다. 배포·릴리스 권한을 품질 게이트 잡에 넣지 않는다.

### 이 템플릿 원본과 적용 저장소

- [ ] **원본 템플릿 저장소:** G-docs·G-docs-test·G-locale-source·G-locale-source-test와 AGENTS.md의 전체 G-test를 상시 실행한다. release 후보에서는 exact clean source commit으로 package/install E2E도 실행한다. G-adopt(placeholder 검색)는 넣지 않는다.
- [ ] **적용 저장소:** G-docs를 유지한다. G-lint·G-type·G-test·G-build는 채운 명령만 실행한다. 적용 직후 G-adopt를 한 번 확인한다.
- [ ] CI를 쓰지 않으면 같은 게이트를 로컬에서 실행한 기록과, CI를 안 쓰는 이유를 남긴다.
- [ ] 사용자가 러너 제품을 지정하기 전에는 `.github/workflows/`, Buildkite pipeline 파일, 그 외 제품 전용 설정을 새로 만들지 않는다.

## 5. 로컬과의 일치

에이전트와 사람이 로컬에서 돌리는 명령이 CI와 다르면 “로컬은 되는데 CI만 실패”가 됩니다.

- 로컬에서 성공했다고 보고하는 게이트는 CI에서도 같은 명령을 실행할 수 있어야 합니다.
- CI에서만 통과하고 로컬 문서에 없는 검사라면, 명령을 AGENTS.md·README에 올리거나 CI에서 제거합니다.
- `scripts/check-docs.py`를 바꾸면 로컬에서 G-docs-test를 실행한 뒤에만 완료로 보고합니다.

## 6. Buildkite Windows·Linux 검증

두 pipeline은 연결된 Origin installation의 canonical repository URL `https://origin.cursor.com/git/jaff2836/ai-agent-docs-template.git`을 사용합니다. 각 self-hosted agent의 Git URL rewrite가 HTTPS checkout을 SSH로 전환하며 agent key로 정확한 commit을 가져옵니다. Origin branch push에서 두 pipeline이 자동 시작하고 각각 Origin check를 게시합니다. 실제 PR 이벤트의 자동 시작과 GitHub push trigger는 아직 확인하거나 구성하지 않았습니다. agent 인증 비밀값은 저장소와 로그에 기록하지 않습니다.

[`windows-ci`](https://buildkite.com/jaff2836-org/windows-ci)는 [`pipeline.yml`](../.buildkite/pipeline.yml)을 `jaff2836-worker-windows` queue에서 실행합니다. WindowsApps의 실행 불가 `python3` 별칭 대신 공식 Python 3.12.10 NuGet CI 배포본을 `%LOCALAPPDATA%\Programs\Python\Python312-CI\tools\python.exe`에 배치했습니다. root docs·stable locale 검사와 전체 unittest 뒤 T-017 native junction probe를 실행합니다. Probe는 설계 재현용 진단 단계로 현행 installer가 junction 경로를 허용한다고 기록합니다. 경계 회귀 검증으로 승격할 때 허용·거부 결과를 명시적으로 단언해야 합니다.

[`linux-ci`](https://buildkite.com/jaff2836-org/linux-ci)는 [`linux.yml`](../.buildkite/linux.yml)을 `jaff2836-worker-linux` queue에서 실행합니다. agent의 Python 3.13.5로 같은 root docs·stable locale 검사와 전체 unittest를 실행합니다. [Windows build #19](https://buildkite.com/jaff2836-org/windows-ci/builds/19)와 [Linux build #4](https://buildkite.com/jaff2836-org/linux-ci/builds/4)는 같은 commit `ec325e34faa405546f5f4916aa01c47c6f4abe8c`에서 자동 시작해 각각 unittest 176개와 Origin 성공 check를 확인했습니다.

## 7. 제공하지 않는 것

- 템플릿 artifact에 포함할 GitHub Actions 워크플로 파일, Buildkite pipeline 파일, 기타 러너 설정
- 자동 리뷰 실행 잡, 리뷰 프롬프트, 봇 토큰 설정
- 배포·릴리스·tag 잡. 품질 게이트와 배포 권한을 한 잡에 섞지 마세요
- `scripts/check-docs.py`를 다른 언어로 다시 짠 복제 구현
