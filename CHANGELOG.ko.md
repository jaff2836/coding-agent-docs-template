# 릴리스 노트

[English](./CHANGELOG.md)

이 문서는 버전별 변경 사항을 기록합니다. 현재 설치·사용 방법은 [README.ko.md](./README.ko.md), 변경할 수 없는 배포 asset은 [GitHub Releases](https://github.com/jaff2836/coding-agent-docs-template/releases)를 참고하세요.

## v2.2.0 — base-aware adoption report

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
