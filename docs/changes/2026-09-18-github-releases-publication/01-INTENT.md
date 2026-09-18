# 변경 의도: GitHub Releases 기반 v2 공개 배포

## Metadata

- **Change ID:** `2026-09-18-github-releases-publication`
- **Status:** Accepted
- **Originator:** Chae Sangwon
- **Source:** 2026-09-18 사용자 대화 — artifact를 GitHub Releases에서만 관리하고 `latest`에서 exact version을 확인하는 구조 선택
- **Parent:** [제품 기준](../../00-PROJECT.md) D-002·D-003과 [다국어 템플릿 SPEC](../2026-09-09-multilingual-template/02-SPEC.md)
- **Approval:** Chae Sangwon, 2026-09-18 사용자 대화 — GitHub Releases 단일 host와 후속 구현 진행 승인
- **Spec:** [02-SPEC.md](./02-SPEC.md)

## 1. 문제

현재 installer는 `<release-url>/<version>/<asset>` 형태의 직접 HTTPS namespace와 redirect 거부를 전제로 합니다. GitHub Releases의 browser download URL은 release asset 저장소로 redirect될 수 있으므로 이 계약으로는 공개 저장소의 release asset을 설치할 수 없습니다. README의 release host와 bootstrap URL도 placeholder 상태입니다.

GitHub Pages나 별도 object storage를 추가하면 redirect 없는 경로를 만들 수 있지만, 같은 artifact를 두 배포면에 동기화하고 운영해야 합니다. 사용자는 이 프로젝트의 첫 공개 v2 배포에서는 GitHub Releases만 관리하기로 결정했습니다.

## 2. 기대 결과

- 사용자는 GitHub의 `latest` release에서 단일 `installer.py`를 내려받아 지원 locale을 확인하고 설치할 수 있습니다.
- `latest`는 version 선택에만 쓰고, 실제 manifest·checksum·archive 검증은 `v<SemVer>` exact tag의 release asset에서 수행합니다.
- release tag, manifest version·repository·source commit과 artifact checksum의 관계를 게시 전후에 재현 가능하게 확인합니다.
- GitHub redirect 지원 때문에 임의 host 또는 HTTP downgrade까지 허용하지 않습니다.

## 3. 범위와 비범위

### 범위

- `jaff2836/coding-agent-docs-template` GitHub Releases 전용 URL 계약
- GitHub release asset에 한정한 HTTPS redirect 처리
- `latest`에서 exact SemVer/tag namespace로 전환하는 installer 동작
- README·locale 안내와 v2.0.0 release metadata 정렬
- exact-head package, tag, draft release, 원격 HTTPS E2E와 최종 release 게시 순서

### 비범위

- GitHub Pages, S3, R2, CDN mirror
- private repository와 인증된 asset 다운로드
- GitHub Enterprise Server나 GitHub 외 release provider
- 기존 프로젝트의 자동 update·overwrite 또는 locale 자동 전환
- 특정 CI runner workflow 추가

## 4. 제약

- production installer는 Python 3 표준 라이브러리만 사용합니다.
- public CLI의 version은 `2.0.0`처럼 `v` 없는 full SemVer를 유지하고, Git tag에서만 `v2.0.0` 형태로 변환합니다.
- branch는 mutable하므로 설치 version의 정본으로 사용하지 않습니다. 게시 gate에서 tag가 manifest의 exact source commit을 가리키는지만 확인합니다.
- redirect는 GitHub release asset 요청에서 시작된 HTTPS chain에만 허용하고 credential·HTTP downgrade를 거부합니다.
- immutable release를 공개한 뒤에는 asset이나 tag를 교체하지 않습니다. 실패하면 새 patch version으로 복구합니다.

## 5. 미해결 질문

- GitHub repository 설정에서 immutable releases를 사용할 수 있는지는 게시 전에 확인합니다. 사용할 수 없더라도 versioned release asset을 교체하지 않는 운영 규칙은 유지합니다.
- 최초 release automation은 범위 밖입니다. v2.0.0은 검증된 수동 절차로 게시하고 반복 비용이 확인된 뒤 별도 변경으로 자동화를 검토합니다.

## 6. 변경 기록

- 2026-09-18: GitHub Pages와 GitHub Releases 병행 권고 대신, 사용자 결정에 따라 GitHub Releases 단일 host를 채택했습니다.
