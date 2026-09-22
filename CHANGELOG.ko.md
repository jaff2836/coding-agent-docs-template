# 릴리스 노트

<!-- template-section:release-history -->

[English](./CHANGELOG.md)

이 문서는 버전별 변경 사항을 기록합니다. 현재 설치·사용 방법은 [README.ko.md](./README.ko.md), 변경할 수 없는 배포 asset은 [GitHub Releases](https://github.com/jaff2836/coding-agent-docs-template/releases)를 참고하세요.

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
