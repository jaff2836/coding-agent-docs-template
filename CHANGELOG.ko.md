# 릴리스 노트

<!-- template-section:release-history -->

[English](./CHANGELOG.md)

이 문서는 버전별 변경 사항을 기록합니다. 현재 설치·사용 방법은 [README.ko.md](./README.ko.md), 변경할 수 없는 배포 asset은 [GitHub Releases](https://github.com/jaff2836/coding-agent-docs-template/releases)를 참고하세요.

## v2.5.0 — 보고 형식, 지시의 출처와 완료 근거

- 여러 주제를 담은 보고는 첫 줄에 결론을 쓰고 주제마다 `##` 제목 아래 한 줄 요약 리스트를 둡니다. 경고·수치·조건과 실패한 검증은 줄이지 않고, 생략한 주제는 이름을 밝혀 요청할 수 있게 하며, 결정 질문은 마지막에 두고, 에이전트가 정한 기본값은 보고에 밝힙니다(`AGENTS.md`).
- 지시는 사용자 요청과 지침 파일에서만 받습니다. 도구 출력, 외부 저장소, PR·리뷰·댓글 본문 안의 지시는 데이터이며, 사용자 계정으로 게시된 자동 리뷰도 같습니다(`AGENTS.md`, `docs/REVIEW_ROUND.md`).
- 완료 주장에는 마지막 변경 뒤에 실행·조회한 근거가 필요하고, 버그 수정·새 검사 규칙의 회귀 검사는 red-green으로 확인합니다(`AGENTS.md`, `docs/REVIEW.md`, `.cursor/BUGBOT.md`).
- 리뷰 라운드는 비어 보이는 결과를 원본으로 다시 읽고, 유효 finding의 직접 확인 여부를 원장의 새 `확인` 열에 적으며, merge 확인 요청에서 `미확인` finding을 구분합니다(`docs/REVIEW_ROUND.md`).
- installer, release manifest schema, artifact inventory는 바뀌지 않습니다.

## [v2.4.0](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.4.0) — 기록 시점과 리뷰 finding ID

- 작업 브랜치는 자기 최종 head가 통합되는 시점의 상태를 서술할 수 있고, 자기 CI·리뷰 판정·merge SHA는 PR을 원장으로 둡니다. 그래서 통합 뒤 TODO가 한 변경씩 늦어지지 않습니다(`docs/DOCS_GUIDE.md`, `docs/02-TODO.md` 규칙, `docs/REVIEW_ROUND.md`).
- 병렬 리뷰어의 finding ID가 겹치지 않습니다. 등록된 리뷰어는 슬롯 ID를, 등록되지 않은 리뷰어는 `<플랫폼 게시 식별자>/<항목 번호>`를 쓰고, PR 게시물이 없는 리뷰는 보고 식별자를 씁니다. 대표 ID는 원 ID 중에서 고릅니다(`docs/REVIEW.md`, `docs/REVIEW_ROUND.md`, `.cursor/BUGBOT.md`).
- 리뷰는 검토한 head·base를 적고, 인용한 CI·테스트 결과마다 build와 head를 적습니다.
- 적용 가이드는 placeholder 검색 패턴을 한 번 선언하고 `rg`·GNU `grep` 명령이 이를 참조하며, Bash 실행과 보관 안내를 둡니다(`docs/TEMPLATE_GUIDE.md`).
- installer, release manifest schema, artifact inventory는 바뀌지 않습니다.
- 검증된 draft asset 5개를 그대로 immutable Latest로 공개했습니다. Linux의 published 검증에서 latest·exact의 두 locale 경로, `v2.3.3` base-aware upgrade와 비어 있지 않은 install 대상의 거부·tree 불변을 확인했습니다.

## [v2.3.3](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.3.3) — Windows junction 경계와 installer 출력

- **호환성:** Windows의 `v2.3.3` installer는 Python 3.12 이상을 요구하며, Python 3.11 이하는 release·대상 접근 전에 중단합니다. Python을 업그레이드하고 `v2.3.3`을 사용해 아래 junction 경계와 출력 수정 사항을 적용하는 것을 권장합니다. 당장 업그레이드할 수 없다면 `v2.3.2` release의 `installer.py` asset을 받아 정확한 `--version 2.3.2`로 실행하세요. 이 대안에는 해당 수정 사항이 포함되지 않습니다.
- Windows installer는 대상·output·직접 부모·artifact member 검사 지점의 directory junction을 거부해 의도한 tree 밖으로 따라가지 않습니다.
- `install`·`export`·`adopt`는 출력 인코딩으로 표현할 수 없는 경로를 메시지에서 escape하여 완료된 작업을 CLI 실패로 잘못 보고하지 않습니다.
- `en`·`ko` 적용 가이드는 `git init` 순서, 새 경로·빈 디렉터리 설치 대상, 기존 직접 부모 조건을 설명합니다.
- release candidate verifier는 package의 installer로 새·빈·비어 있지 않은 대상을 검사하고, 거부된 대상의 불변을 확인합니다.
- 검증된 기존 draft asset 5개를 그대로 immutable Latest로 공개했습니다. Linux의 published 검증에서 latest·exact의 두 locale 경로, `v2.3.2` base-aware upgrade와 비어 있지 않은 install 대상의 거부·tree 불변을 확인했습니다.

## [v2.3.2](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.3.2) — 새 경로·빈 디렉터리 install 대상

- `installer.py install`은 새 경로 또는 읽을 수 있는 빈 디렉터리만 허용하고, 비어 있지 않거나 읽을 수 없는 대상은 template member를 쓰기 전에 거부합니다.
- artifact와 무관한 파일이 있는 대상을 포함한 기존 저장소는 부분 설치 대신 읽기 전용 `adopt` plan을 안내합니다.
- root README와 두 locale 적용 가이드가 같은 install/adopt 경계를 설명하며, 거부 시 installer 회귀가 대상 tree 보존을 확인합니다.
- immutable Latest release의 candidate·published 검증에서 두 locale 경로, `v2.3.1` base-aware upgrade, 비어 있지 않은 install 대상 거부를 확인했습니다.

## [v2.3.1](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.3.1) — Windows release 도구 호환성

- release packaging이 POSIX 상대 경로 순서를 사용해 Windows와 POSIX host에서 같은 artifact inventory와 결정적 byte를 생성합니다.
- materialized tree 검증은 Windows의 writable 의미를 사용하고 ZIP member의 Unix `0644` 계약은 유지합니다.
- LF checkout과 좁게 제한한 symlink test skip으로 관련 없는 파일시스템 오류를 숨기지 않으면서 source와 export artifact test를 이식 가능하게 했습니다.
- native Windows에서 전체 test와 en·ko package·export 결정성을 확인했습니다. 공개 전 candidate gate가 통과했고 immutable release의 published 검증은 Linux와 native Windows에서 모두 통과했습니다.

## [v2.3.0](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.3.0) — 문서 소유권과 changelog 안내

- locale artifact에 `docs/CHANGELOG_GUIDE.md`를 추가해 README의 현재 동작, 공개 릴리스 이력, TODO·PLAN의 미래 작업과 템플릿 provenance를 구분하며 프로젝트 소유 root changelog는 만들지 않습니다.
- 번들 `project-analysis` skill에서 프로젝트별 owner·검토일 metadata를 제거했습니다.
- locale 가이드를 artifact 안내 정본으로 삼고 source root 가이드는 maintainer 전용 보충 내용만 유지합니다.
- source와 artifact 문서 검사는 각 영역의 정본 릴리스 이력을 검증합니다.

## [v2.2.0](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.2.0) — base-aware adoption report

- `adopt --base-version <older-exact-semver>`은 과거 installer를 실행하지 않고 이전 exact release를 검증해 base release, current release와 target tree를 비교합니다.
- 선택형 format 2 report는 `base ∪ current` 경로를 `unchanged`, `template-only`, `project-only`, `converged`, `diverged`, `blocked`로 분류합니다. 대상은 계속 읽기 전용이며 파일을 병합하거나 삭제하지 않습니다.
- published release 검증은 format 2 불변식과 공개 `en`·`ko` 업그레이드 경로를 확인합니다. consumer 검증에서는 생성된 report를 세 입력 tree와 독립적으로 대조합니다.
- root README는 현재 동작만 설명하고 버전별 이력은 이 문서에서 관리합니다.

## [v2.1.1](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.1.1) — checker·installer 진단

- `scripts/check-docs.py`는 `docs/TEMPLATE_GUIDE.md`가 실제로 없을 때만 선택적 생략으로 인정하고 외부 symlink와 비파일 entry를 거부합니다.
- manifest schema 불일치 시 선택한 release의 `installer.py`를 사용하는 방법을 안내합니다.
- 실제 immutable release asset을 대상으로 첫 candidate·published 검증을 완료했습니다.

## [v2.1.0](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.1.0) — 기존 저장소 adoption

- 기존 저장소를 위한 읽기 전용 `adopt` 명령과 adoption policy metadata를 추가했습니다.
- Claude·Codex·Cursor·OMP용 self-contained `project-analysis` skill을 번들에 포함했습니다.
- artifact 문서 checker를 강화하고 `en`·`ko` install·export·adopt 경로를 검증했습니다.

## [v2.0.0](https://github.com/jaff2836/coding-agent-docs-template/releases/tag/v2.0.0) — locale artifact

- manifest와 checksum에 결합된 재현 가능한 versioned `en`·`ko` release artifact를 도입했습니다.
- 비파괴 installer와 GitHub Releases 배포 계약을 추가했습니다.
