# 템플릿 유지관리 보충 안내

> 이 문서는 source 저장소 maintainer가 locale artifact를 구성·검증·배포할
> 때 필요한 보충 규칙만 소유합니다. 적용 프로젝트용 정본은
> [영문](../locales/en/docs/TEMPLATE_GUIDE.md)과
> [한국어](../locales/ko/docs/TEMPLATE_GUIDE.md) locale 가이드입니다.

## Metadata

- **Status:** Active
- **Template version:** 2.4.0
- **Template source:** https://github.com/jaff2836/coding-agent-docs-template
- **Template revision:** release 검증 시 exact source commit으로 확정
- **Owner:** Chae Sangwon
- **Last reviewed:** 2026-09-28
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

`scripts/check-docs.py`의 **무인자 실행**이 maintainer source 검사입니다.
root `CHANGELOG.md`에서 현재 version 이력을 확인하고, top-level `locales/`와
`template/`은 재귀 문서 탐색에서 제외합니다. `docs/locales/` 같은 중첩 경로는
제외하지 않습니다. 별도로 root와 `locales/ko`의 `.agents`·`.claude`
`project-analysis/SKILL.md` 네 사본이 byte-identical한지 확인하며, 파일 누락·
읽기 실패·저장소 밖 경로·사본 차이는 실패로 진단합니다. `design`과
`review-round`의 root↔ko 본문 차이는 이 동등성 검사 대상이 아닙니다.

CLI 인자를 하나라도 주면 canonical artifact checker에 위임합니다.
`--root <export된 artifact 경로>`는 artifact의 `docs/TEMPLATE_GUIDE.md` 이력을
검사하고 source 제외 범위나 root↔ko 의존성을 사용하지 않습니다.
`--root .`도 artifact 의미이므로 source 검사를 대신하지 않습니다.

root [`.gitattributes`](../.gitattributes)의 `* text=auto eol=lf`는 Windows를
포함한 maintainer checkout에서 텍스트를 LF로 유지합니다. payload source의
UTF-8·LF·최종 newline은 locale 검사로도 확인합니다. 이 attribute 파일은
artifact inventory에 포함되지 않으며 적용 프로젝트의 Git 설정을 바꾸지 않습니다.

템플릿을 적용한 직후 실제 변경 폴더와 프로젝트 소유 문서에 남은
placeholder를 확인합니다. 검색 선언·rg/grep 명령의 정본은
[영문 가이드](../locales/en/docs/TEMPLATE_GUIDE.md) §3과
[한국어 가이드](../locales/ko/docs/TEMPLATE_GUIDE.md) §3입니다.
해당 locale의 Bash·동일 shell 실행 순서와 §5의 선언·명령 보관 절차를 따릅니다.
source locale 검사는 이 선언·참조·sentinel과 root 안내의 정본 위임을 확인합니다.
이 절의 코드 블록에는 위 세 source 검사 명령과 `#` 주석만 둘 수 있고, 코드 블록
밖에도 locale 검색식에 걸리는 어휘를 옮겨 적지 않습니다. 검색 도구와 관계없이
적용됩니다.
안내 문서와 `changes/_template/`의 설명·복사용 placeholder는 문맥에 따라
판정하며, 검색 0건을 적용 완료로 해석하지 않습니다. 전체 체크리스트는 locale
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

### 원격 저장소와 통합

개발 PR·리뷰·필수 CI는 private Origin([CI.md](./CI.md) §6)에서, 공개 `main`·
release tag·GitHub Release는 `jaff2836/coding-agent-docs-template`에서
관리합니다. 두 저장소는 mirror가 아니며 release verifier의 기본 remote 이름은
각각 `origin`과 `github`입니다.

- PR은 Origin에서 merge한 뒤 같은 merge commit을 GitHub `main`에 non-force
  fast-forward로 push합니다(`git push github <merge-commit>:refs/heads/main`).
  push 전에 GitHub `main`이 그 commit의 조상인지 확인하고, push 뒤 두 remote의
  `main`을 `git ls-remote`로 대조합니다.
- GitHub에는 두 ruleset을 active로 유지합니다. `refs/heads/main` 대상은
  `non_fast_forward`·`deletion`으로 force push와 삭제를 막고 fast-forward push는
  허용합니다. `refs/tags/v*` 대상은 `update`·`deletion`으로 tag 갱신과 삭제를
  막으며 게시 전 candidate tag도 이 ruleset이 보호합니다. 설정을 바꾼 뒤와
  release candidate 전에 두 ruleset을 확인합니다. 목록 API
  `gh api repos/jaff2836/coding-agent-docs-template/rulesets`는 id와
  `enforcement`만 주므로, 각 id를
  `gh api repos/jaff2836/coding-agent-docs-template/rulesets/<id>`로 조회해
  `enforcement`·`conditions.ref_name`·`rules`·`bypass_actors`를 확인합니다.
- release tag의 정본은 GitHub의 annotated `v<SemVer>` tag입니다. candidate
  verifier는 원격에서 두 `main`의 일치와 GitHub annotated tag를 확인하고,
  실행하는 checkout의 로컬 annotated tag도 같은 source commit을 가리키며
  source가 동기화된 `main`의 조상이어야 합니다. Origin 원격 tag는 verifier
  입력이 아니므로 Origin에는 release tag를 동기화하지 않고, Origin에 남은 과거
  tag를 release 근거로 쓰지 않습니다.
- stack된 PR은 부모가 merge돼도 base가 자동으로 바뀌지 않습니다. 부모를
  통합한 뒤 base를 `main`으로 옮기고, 새 base에 부모 외의 변경이 있으면 head를
  갱신해 필수 CI를 다시 받습니다.

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

**Maintainer source의 공개 준비 예외:** version을 올리는 준비 commit에서는
현재 version의 plain heading에 `미공개 후보` 또는 `unpublished candidate`를
명시해 entry를 만들 수 있습니다. 공개 전에는 실제 release 링크나 공개 완료로
표시하지 않습니다. 공개 후 실제 release 링크와 검증 결과를 반영합니다.
빈 `Unreleased` 절을 기본으로 만들지 않습니다. 이 예외는 source 공개 준비에만
적용하며, 적용 프로젝트의 locale `CHANGELOG_GUIDE.md`가 정한 공개 후 기록
원칙은 유지합니다. 문서 checker의 heading 통과는 구조 확인이며 게시 완료
근거는 candidate·published release gate에서 확인합니다.
