# AI Agent Docs Template

AI 코딩 에이전트와 사람이 **같은 문서 체계, 설계 절차, 리뷰 기준**으로 협업하기 위한 템플릿입니다. 앱 프레임워크가 아니라 프로젝트 문서와 에이전트 지침을 제공합니다.

Claude, Codex, Cursor와 [Oh My Pi](https://github.com/can1357/oh-my-pi)를 지원하며, v2는 영어(`en`)와 한국어(`ko`)를 제공합니다.

[English](./README.md)

## 설치하기

최신 GitHub release에서 `installer.py`를 내려받은 뒤 지원 locale을 확인하고 새 프로젝트에 설치합니다.

### 1. installer 다운로드

Linux 또는 macOS에서는 다음 명령을 사용합니다.

```sh
curl -fL --proto-redir '=https' -o installer.py.part \
  https://github.com/jaff2836/coding-agent-docs-template/releases/latest/download/installer.py &&
mv installer.py.part installer.py
```

Windows PowerShell에서는 다음 명령을 사용합니다.

```powershell
curl.exe -fL --proto-redir "=https" -o installer.py.part `
  https://github.com/jaff2836/coding-agent-docs-template/releases/latest/download/installer.py
if ($LASTEXITCODE -ne 0) { throw "installer.py 다운로드 실패" }
Move-Item -Force -ErrorAction Stop installer.py.part installer.py
```

다운로드 블록이 성공한 경우에만 다음 단계로 진행하세요.

### 2. 지원 locale 확인

```sh
python3 installer.py list-locales --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest
```

Windows PowerShell에서는 다음과 같이 실행합니다.

```powershell
python installer.py list-locales --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest
```

### 3. locale 설치

```sh
python3 installer.py install --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale ko --repo-root /path/to/new-project
```

Windows PowerShell에서는 다음과 같이 실행합니다.

```powershell
python installer.py install --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale ko --repo-root C:\path\to\new-project
```

`--locale`에는 `en` 또는 `ko`를 지정합니다. 설치 대상은 존재하지 않거나 비어 있어야 하며, 기존 파일이 하나라도 있으면 아무것도 쓰지 않습니다.

### 기존 프로젝트에 적용하기

v1을 사용 중이거나 자체 문서를 이미 운영하는 프로젝트에는 바로 설치하지 마세요. v2를 빈 디렉터리로 export한 뒤 기존 파일과 비교하여 필요한 변경만 수동으로 반영합니다.

```sh
python3 installer.py export --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale ko --output /path/to/empty-directory
```

Windows PowerShell에서는 다음과 같이 실행합니다.

```powershell
python installer.py export --release-url https://github.com/jaff2836/coding-agent-docs-template/releases --version latest --locale ko --output C:\path\to\empty-directory
```

installer는 기존 파일을 덮어쓰지 않으며 자동 update, locale 전환, `--force`를 제공하지 않습니다. 검증된 GitHub release asset URL에서 시작한 HTTPS redirect chain만 따른 뒤 exact tag release의 manifest, checksum과 실행 중인 installer 자체를 검증합니다. 다른 언어가 필요하면 영어 artifact를 기반으로 프로젝트 지침과 문서를 직접 현지화할 수 있지만 공식 검증 대상은 아닙니다.

## 설치 후 사용하기

1. `README.md`와 `AGENTS.md`의 placeholder, 프로젝트 정보와 명령을 실제 값으로 바꿉니다.
2. 제품 기준은 `docs/00-PROJECT.md`, 진행 상태는 `docs/02-TODO.md`에 기록합니다.
3. 구조·공개 계약을 바꾸는 작업은 `design` 절차를 사용합니다.
4. PR 리뷰는 `docs/REVIEW.md`를 따르고, 반복 수정·재리뷰가 필요할 때만 `review-round`를 명시적으로 호출합니다.

각 도구는 `AGENTS.md`, `CLAUDE.md`, `.agents/skills/`, `.claude/skills/`, `.cursor/`, `.omp/`의 고정 경로를 통해 같은 계약을 읽습니다.

## 템플릿 검사하기

저장소 개발과 release 준비에는 production dependency 없이 Python 3 표준 라이브러리만 사용합니다.

```text
python3 scripts/check-docs.py
python3 scripts/check-locales.py --require-stable
python3 -m unittest discover -s tests -v
```

source checkout에서 locale artifact를 직접 확인하려면 빈 디렉터리로 export합니다.

```text
python3 scripts/export-template.py --locale ko --output /path/to/empty-directory
```

- `check-docs.py`: 링크, import, 스킬 사본, 불변조건과 문서 판 번호 검사
- `check-locales.py`: locale inventory, placeholder, marker와 skill 계약 검사
- 전체 테스트: exporter, deterministic package와 비파괴 installer의 성공·실패 경로 검사

## 포함된 것

- **공통 지침:** `AGENTS.md`, `CLAUDE.md`와 도구별 연결 파일
- **문서 체계:** 프로젝트 기준, 설계, TODO, 리뷰 및 CI 가이드
- **스킬:** `design`, `project-analysis`, `review-round`
- **다국어 배포:** `template/common/`, `locales/en/`, `locales/ko/`, manifest와 schema
- **도구:** 문서·locale 검사, export, release package, installer

전체 구조와 적용 체크리스트는 [Template Guide](./docs/TEMPLATE_GUIDE.md), 문서별 역할과 운영 규칙은 [Documentation Guide](./docs/DOCS_GUIDE.md)를 참고하세요. 이 저장소에는 애플리케이션 코드나 특정 CI 제품의 pipeline이 포함되지 않습니다.

## 번들 스킬

- **`design`:** 구조나 공개 계약을 바꾸기 전에 필요한 최소 Intent·Spec·실행 계획과 사용자 합의를 정리합니다.
- **`project-analysis`:** 명시적으로 요청된 프로젝트 전체를 기본 읽기 전용으로 근거 중심 분석하고 GO·조건부 GO·NO-GO·근거 부족 중 하나로 판단합니다.
- **`review-round`:** 명시적으로 시작한 PR 리뷰·수정 라운드를 exact head 기준으로 진행하고, 설정한 gate 통과와 사용자 확인 후에만 merge합니다.

`project-analysis`는 `v2.0.0` 다음 release부터 번들 skill로 포함됩니다. `v2.0.0` artifact는 동일한 절차를 `docs/PROJECT_ANALYSIS.md` 문서로 제공합니다.

Codex·Cursor·OMP는 `.agents/skills/`, Claude Code는 byte-identical한 `.claude/skills/` 복제본을 읽습니다.

## License

이 템플릿은 [MIT License](./LICENSE)로 배포됩니다. 적용 프로젝트에서는 해당 프로젝트의 라이선스와 보안 신고 방법을 별도로 정하세요.
