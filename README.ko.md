# AI Agent Docs Template

AI 코딩 에이전트와 사람이 **같은 문서 체계, 설계 절차, 리뷰 기준**으로 협업하기 위한 템플릿입니다. 앱 프레임워크가 아니라 프로젝트 문서와 에이전트 지침을 제공합니다.

Claude, Codex, Cursor와 [Oh My Pi](https://github.com/can1357/oh-my-pi)를 지원합니다.

[English](./README.md)

## 설치하기

### 사전 요구사항

- Python 3 (Windows는 3.12 이상)
- `curl` (Windows는 `curl.exe`)
- GitHub 네트워크 접근
- 선택: 2단계의 attestation 확인에 쓰는 GitHub CLI(`gh`)

### 1. installer 다운로드

Linux 또는 macOS:

```sh
curl -fL --proto-redir '=https' -o installer.py.part \
  https://github.com/jaff2836/coding-agent-docs-template/releases/latest/download/installer.py &&
mv installer.py.part installer.py
```

Windows PowerShell:

```powershell
curl.exe -fL --proto-redir "=https" -o installer.py.part `
  https://github.com/jaff2836/coding-agent-docs-template/releases/latest/download/installer.py
if ($LASTEXITCODE -ne 0) { throw "installer.py 다운로드 실패" }
Move-Item -Force -ErrorAction Stop installer.py.part installer.py
```

다운로드가 성공한 경우에만 다음 단계로 진행하세요. Windows에서는 아래 명령의 `python3` 대신 `python`과 Windows 경로를 사용합니다.

### 2. 확인 (선택)

현재 release의 locale:

| Locale | 언어 | 상태 |
| --- | --- | --- |
| `en` | 영어 | complete |
| `ko` | 한국어 | complete |

```sh
python3 installer.py list-locales --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest
gh release verify-asset installer.py --repo jaff2836/coding-agent-docs-template
```

`list-locales`는 release의 locale을 보여 줍니다. `gh release verify-asset`은 installer를 GitHub가 latest release에 서명한 attestation과 대조합니다. 특정 release와 대조하려면 파일 이름 앞에 `v2.5.0` 같은 tag를 넣으세요. attestation은 게시 계정이 탈취된 경우를 막지 못합니다.

### 3. 템플릿 적용

다음 중 하나를 고르고 `--locale`에 지원 locale을 지정합니다.

#### 선택 A: 기존 프로젝트 (`adopt`)

```sh
python3 installer.py adopt --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale ko --repo-root /path/to/existing-project --output /path/to/empty-directory
```

`adopt`는 프로젝트에 아무것도 쓰지 않습니다. 프로젝트 밖의 output 디렉터리에 검증된 파일을 담은 `artifact/`와, 각 경로를 `missing`, `identical`, `merge`, `decision`, `blocked`로 분류한 `adoption-plan.json`을 만듭니다. 병합은 `artifact/docs/TEMPLATE_GUIDE.md`의 절차를 따릅니다. 이전 exact release에서 적용한 프로젝트를 올릴 때는 `--base-version <older-exact-semver>`를 더하면, report가 경로를 `unchanged`, `template-only`, `project-only`, `converged`, `diverged`, `blocked`로 분류합니다. plan 형식은 실험적입니다.

#### 선택 B: 새 프로젝트 (`install`)

```sh
python3 installer.py install --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale ko --repo-root /path/to/new-project
```

설치 대상은 존재하지 않는 경로이거나 빈 디렉터리여야 합니다. 대상이 아직 없다면 바로 위 부모가 이미 존재하는 디렉터리이고 symlink나 junction이 아니어야 합니다. `git init`은 설치한 뒤에 실행합니다. `.git`이 있는 디렉터리는 비어 있지 않으므로 선택 A를 사용합니다.

#### 선택 C: 파일만 (`export`)

```sh
python3 installer.py export --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale ko --output /path/to/empty-directory
```

`export`는 계획 없이 검증된 파일만 빈 디렉터리에 씁니다.

installer는 쓰기 전에 release manifest, checksum과 자기 자신의 byte를 검증하며 기존 파일을 덮어쓰지 않습니다. `--force`, 자동 update, locale 전환은 제공하지 않습니다. 다른 언어가 필요하면 영어 artifact를 현지화할 수 있지만 공식 검증 대상은 아닙니다.

## 설치 후 사용하기

1. `README.md`와 `AGENTS.md`의 placeholder, 프로젝트 정보와 명령을 실제 값으로 바꿉니다.
2. 제품 기준은 `docs/00-PROJECT.md`, 진행 상태는 `docs/02-TODO.md`에 기록합니다.
3. 구조·공개 계약을 바꾸는 작업은 `design` 절차를 사용합니다.
4. PR 리뷰는 `docs/REVIEW.md`를 따르고, 반복 수정·재리뷰가 필요할 때만 `review-round`를 명시적으로 호출합니다.

각 도구는 `AGENTS.md`, `CLAUDE.md`, `.agents/skills/`, `.claude/skills/`, `.cursor/`, `.omp/`의 고정 경로를 통해 같은 계약을 읽습니다.

## 템플릿 검사하기

저장소 개발과 release 도구는 Python 3 표준 라이브러리만 사용합니다.

```text
python3 scripts/check-docs.py
python3 scripts/check-locales.py --require-stable
python3 -m unittest discover -s tests -v
python3 scripts/export-template.py --locale ko --output /path/to/empty-directory
```

- `check-docs.py`: 링크, import, 스킬 사본, 불변조건과 문서 판 번호
- `check-locales.py`: locale inventory, placeholder, marker와 skill 계약
- `export-template.py`: source checkout에서 locale artifact를 빈 디렉터리에 씀
- 테스트: exporter, deterministic packager, installer의 `install`·`export`·읽기 전용 `adopt`의 성공·실패 경로

maintainer는 clean exact-source checkout에서 사람이 준비한 draft를 게시 전에, immutable Latest를 게시 후에 검사합니다. 두 명령 모두 remote를 바꾸지 않으며 `git`과 `gh`가 필요합니다.

```text
python3 scripts/verify-release.py candidate --version {{VERSION}} --source-commit {{EXACT_COMMIT}} --repository {{OWNER/NAME}}
python3 scripts/verify-release.py published --version {{VERSION}} --source-commit {{EXACT_COMMIT}} --repository {{OWNER/NAME}} --release-url https://github.com/{{OWNER/NAME}}/releases
```

## 포함된 것

- **공통 지침:** `AGENTS.md`, `CLAUDE.md`와 도구별 연결 파일
- **문서 체계:** 프로젝트 기준, 설계, TODO, 리뷰 및 CI 가이드
- **스킬:** `design`, `project-analysis`, `review-round`
- **다국어 배포:** `template/common/`, `locales/en/`, `locales/ko/`, manifest와 schema
- **도구:** 문서·locale 검사, export, release package·검증, installer

구조와 적용 체크리스트: [한국어 Template Guide](./locales/ko/docs/TEMPLATE_GUIDE.md)·[Documentation Guide](./locales/ko/docs/DOCS_GUIDE.md), [영문 Template Guide](./locales/en/docs/TEMPLATE_GUIDE.md)·[Documentation Guide](./locales/en/docs/DOCS_GUIDE.md). root [Template Guide](./docs/TEMPLATE_GUIDE.md)와 [Documentation Guide](./docs/DOCS_GUIDE.md)는 maintainer 보충 안내입니다. 이 저장소에는 애플리케이션 코드나 특정 CI 제품의 pipeline이 없습니다.

## 번들 스킬

- **`design`:** 구조나 공개 계약을 바꾸기 전에 필요한 최소 Intent·Spec·실행 계획과 사용자 합의를 정리합니다.
- **`project-analysis`:** 명시적으로 요청된 프로젝트 전체를 기본 읽기 전용으로 근거 중심 분석하고 GO·조건부 GO·NO-GO·근거 부족 중 하나로 판단합니다.
- **`review-round`:** 명시적으로 시작한 PR 리뷰·수정 라운드를 exact head 기준으로 진행하고, 설정한 gate 통과와 사용자 확인 후에만 merge합니다.

Codex·Cursor·OMP는 `.agents/skills/`, Claude Code는 byte-identical한 `.claude/skills/` 복제본을 읽습니다.

## 릴리스 노트

버전별 변경 사항은 [릴리스 노트](./CHANGELOG.ko.md)([영문](./CHANGELOG.md))에 있습니다.

## License

이 템플릿은 [MIT License](./LICENSE)로 배포됩니다. 적용 프로젝트에서는 해당 프로젝트의 라이선스와 보안 신고 방법을 별도로 정하세요.
