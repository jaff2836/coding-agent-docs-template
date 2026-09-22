# 템플릿 유지관리 보충 안내

> 이 문서는 source 저장소 maintainer가 locale artifact를 구성·검증·배포할
> 때 필요한 보충 규칙만 소유합니다. 적용 프로젝트용 정본은
> [영문](../locales/en/docs/TEMPLATE_GUIDE.md)과
> [한국어](../locales/ko/docs/TEMPLATE_GUIDE.md) locale 가이드입니다.

## Metadata

- **Status:** Active
- **Template version:** 2.3.1
- **Template source:** https://github.com/jaff2836/coding-agent-docs-template
- **Template revision:** release 검증 시 exact source commit으로 확정
- **Owner:** Chae Sangwon
- **Last reviewed:** 2026-09-22
- **Review cadence:** source·artifact 경계 또는 배포 계약 변경 시

## 1. Source와 artifact 구조

- root `docs/`, `README.md`, `README.ko.md`와 maintainer 도구는 저장소 유지관리
  영역이며 artifact에서 제외합니다.
- `template/common/`은 언어 비의존 payload, `locales/<tag>/`는 BCP 47
  locale별 payload source입니다.
- [manifest](../locales/manifest.json)의 닫힌 inventory만 exporter와 packager가
  합성합니다. 생성된 artifact를 직접 고치지 말고 source 또는 manifest를
  수정한 뒤 다시 export합니다.
- locale 안 `.agents`와 `.claude`의 같은 skill은 byte-identical해야 합니다.

구조·inventory·locale 상태를 바꾸면 `scripts/check-locales.py`와 exporter,
artifact 자체의 문서 검사를 함께 실행합니다.

## 2. 적용·배포 경계

새 프로젝트의 `install`, 기존 저장소의 읽기 전용 `adopt`, 빈 디렉터리로의
`export` 계약과 실제 병합 절차는 locale 가이드 §2가 소유합니다.

- [영문 적용 가이드](../locales/en/docs/TEMPLATE_GUIDE.md)
- [한국어 적용 가이드](../locales/ko/docs/TEMPLATE_GUIDE.md)

maintainer 문서에 status 표나 적용 절차를 복제하지 않습니다. 기존 저장소의
README, LICENSE, `.gitignore`, 지침, 결정과 프로젝트 소유 changelog는 자동
덮어쓰기 대상이 아닙니다. `adopt` report는 대상 밖에 만들고 사람이 충돌을
판단합니다.

## 3. Source 검사와 placeholder 확인

source tree의 문서 계약은 다음 명령으로 검사합니다.

```sh
python3 scripts/check-docs.py
python3 -m unittest discover -s tests -p 'test_check_docs.py' -v
python3 scripts/check-locales.py --require-stable
```

템플릿을 적용한 직후 실제 변경 폴더와 프로젝트 소유 문서에 남은
placeholder를 확인합니다. 안내 문서와 `changes/_template/`은 설명·복사용
placeholder를 의도적으로 포함하므로 결과를 문맥에 따라 판정합니다.

```sh
rg --hidden -n --glob '*.md' --glob '!**/.git/**' \
  --glob '!docs/TEMPLATE_GUIDE.md' --glob '!docs/DOCS_GUIDE.md' \
  --glob '!docs/changes/_template/**' \
  '\{\{[^}]+\}\}|YYYY-MM-DD|Customize for the project|프로젝트에 맞게 작성'
```

`rg`가 없으면 같은 exclude 범위를 적용한 `grep -R -n -E`로 대체합니다.
검색 0건은 명령 실행 가능성, 완료 근거나 README 내용까지 검증했다는 뜻이
아닙니다. 적용 프로젝트의 전체 체크리스트는 locale
`docs/DOCS_GUIDE.md`가 소유합니다.

## 4. 문서·도구 소유권

- root [AGENTS.md](../AGENTS.md)는 source 저장소 작업 규칙,
  locale `AGENTS.md`는 export되는 프로젝트 규칙입니다.
- root [문서 운영 보충 안내](./DOCS_GUIDE.md)는 maintainer 상태·ID·release
  기록 방식을, locale `DOCS_GUIDE.md`는 적용 프로젝트 문서 체계를 소유합니다.
- `design`과 `review-round` skill은 locale의 정본 절차를 가리키는 adapter이고,
  `project-analysis`는 독립 로딩 가능한 분석 계약을 본문에 담습니다.
- 외부 방법론 도구를 함께 쓰면 같은 역할의 정본을 하나만 지정합니다.
  PROJECT는 결정·정본 인덱스, TODO는 전역 변경 단위, 외부 산출물은 합의한
  상세 설계 또는 실행 상태만 소유하도록 경계를 기록합니다.
- 도구별 지침은 공통 규칙을 복제하지 않습니다. OMP 등 실제 consumer가
  요구하는 우선순위와 import 동작은 사용하는 version에서 확인합니다.

## 5. Release와 consumer 검증

release candidate는 clean exact source commit에서 package하고 tag·manifest·draft
asset provenance를 대조합니다. 공개 후에는 published verifier로 immutable
asset, latest·exact 설치, export와 지원 locale 경로를 확인합니다.

source 변경을 적용 프로젝트에 이관할 때는 기록된 이전 revision과 새 revision을
원본 저장소에서 비교하고 프로젝트가 의도적으로 바꾼 내용을 보존합니다.
locale 가이드의 `Template source`, `Template version`, `Template revision`은
실제 복사 기준을 기록하며 미커밋 또는 일부 반영을 exact release처럼 표시하지
않습니다.

## 6. 릴리스 노트 소유권

- source 저장소의 공개 이력 정본은 [CHANGELOG.md](../CHANGELOG.md)와
  [CHANGELOG.ko.md](../CHANGELOG.ko.md)입니다.
- README는 현재 공개 동작만 설명하고 미래 작업은 [02-TODO.md](./02-TODO.md)
  또는 변경별 PLAN에 둡니다.
- 적용 프로젝트의 changelog 규칙은 locale
  `docs/CHANGELOG_GUIDE.md`가 소유합니다. artifact는 안내를 제공하지만 실제
  root `CHANGELOG.md`를 만들거나 기존 형식을 덮어쓰지 않습니다.
- 버전별 적용 변화는 locale `TEMPLATE_GUIDE.md` §6에 유지합니다. source
  changelog와 같은 이력을 이 문서에 다시 복제하지 않습니다.
