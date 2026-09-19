# 변경 실행 계획: GitHub Releases 기반 v2 공개 배포

## Metadata

- **Change ID:** `2026-09-18-github-releases-publication`
- **Spec:** [02-SPEC.md](./02-SPEC.md)
- **Global task:** [02-TODO.md](../../02-TODO.md) T-002
- **Owner:** Codex 구현, Chae Sangwon 최종 검수
- **Baseline:** `9cea17879d679dd471444b37c0af13610469c813` (`main`)
- **Integration target:** Origin `main`과 GitHub `main`이 같은 commit이고 `v2.0.0` tag commit이 그 `main`의 조상인 상태에서, 검증된 draft asset을 변경 없이 GitHub Release로 게시
- **Scope:** GitHub Releases transport, 공개 사용 문서, v2 metadata, exact package와 원격 release 검증

## 1. 구현 순서와 의존성

1. installer의 GitHub URL·redirect·repository binding을 구현하고 local fixture 회귀 테스트를 통과시킵니다.
2. root·locale 문서의 release URL과 bootstrap 절차를 실제 GitHub Releases 계약으로 바꾸고 v2 source metadata를 정렬합니다.
3. 구현을 Origin `main`에 통합한 exact commit에서 전체 gate와 deterministic package를 수행하고, 그 commit에 annotated `v2.0.0` tag와 검증된 5개 asset의 draft release를 준비합니다.
4. 게시 직전 Origin·GitHub `main`이 같은 commit이고 tag commit이 그 `main`의 조상인지 확인합니다. draft manifest·checksum·asset을 tag commit의 검증 근거와 다시 대조하되, 후속 `main`으로 재패키징하거나 asset을 교체하지 않습니다.
5. 기존 draft를 정식 release로 게시한 즉시 실제 HTTPS 경로에서 latest/exact-version, en/ko install·export와 실패 불변조건을 확인합니다.
6. 검증 근거와 공개 상태를 문서화합니다. immutable release에서 결함이 확인되면 asset이나 tag를 교체하지 않고 patch release 계획으로 전환합니다.

## 2. 작업 체크리스트

- [x] **W-001 GitHub Releases transport**
  - 범위·변경 파일: `scripts/installer.py`, `tests/test_install_release.py`
  - 대응 요구사항·상위 완료 조건: R-001~R-006
  - 선행조건: D-004 승인
  - 검증 방법: URL 생성, repository mismatch, HTTPS redirect chain과 downgrade·credential·비-release redirect negative test, 전체 installer E2E
  - 결과·근거: GitHub Releases root를 `https://github.com/OWNER/NAME/releases`로 제한하고 latest/exact tag asset URL 생성, release URL과 manifest repository 결합, 신뢰한 GitHub asset 요청에서 시작한 HTTPS redirect chain만 허용했습니다. localhost fixture redirect는 계속 거부합니다. GitHub CLI 공개 release의 1,971-byte checksum asset을 `latest/download` 경로에서 실제 redirect handler로 받아 현재 CDN redirect를 확인했습니다.

- [x] **W-002 공개 문서와 v2 metadata 정렬**
  - 범위·변경 파일: `README.md`, `README.ko.md`, root·locale guide, manifest와 제품 문서, `scripts/package_release.py`
  - 대응 요구사항·상위 완료 조건: R-001~R-007
  - 선행조건: W-001의 실제 CLI 계약
  - 검증 방법: docs/locale checker, en/ko command parity, placeholder 부재, version consistency
  - 결과·근거: 실제 release root와 latest bootstrap URL을 영어·한국어 landing과 locale guide에 반영하고 Template version·release history를 `2.0.0`으로 정렬했습니다. packager는 CLI release version과 두 artifact guide의 Template version이 다르면 package 생성을 거부합니다.

- [x] **W-003 exact-head release 후보 검증**
  - 범위·변경 파일: clean exact tag commit에서 생성한 GitHub `v2.0.0` draft의 5개 배포 asset
  - 대응 요구사항·상위 완료 조건: R-006~R-008
  - 선행조건: W-001·W-002 통합, 사용자의 commit·push·tag·release 위임
  - 검증 방법:
    1. `git ls-remote origin main`, `git ls-remote github main`이 같은 SHA인지 확인
    2. `git ls-remote github 'v2.0.0^{}'`로 tag commit을 확정하고 `git merge-base --is-ancestor <tag-commit> <main-commit>`을 확인
    3. tag commit의 clean checkout에서 전체 unittest/docs/locale gate와 2회 package byte equality 근거를 확인
    4. draft manifest `source_commit`과 tag commit을 대조하고 `SHA256SUMS`·asset digest를 생성 시의 검증 근거와 대조
    5. 현재 `main`을 새 package 입력으로 사용하지 않고 tag·draft asset을 재지정·교체하지 않음
  - 결과·근거: 게시 직전 Origin·GitHub `main`은 `5eefc11075652066c90734dd739cc7c650be826c`으로 같았고, `v2.0.0` tag commit `8bc8b1b5049de1f57dead7b2a804e8bee5ce989f`은 그 조상이었습니다. clean tag checkout에서 전체 unittest 102개, docs, stable locale, `git diff --check`가 통과했고 두 번 생성한 5개 asset은 byte-identical이었습니다. 기존 draft의 5개 asset도 재생성본과 byte-identical이며 manifest의 version·repository·`source_commit`이 `2.0.0`·`jaff2836/coding-agent-docs-template`·tag commit으로 일치했습니다. 현재 `main`으로 재패키징하거나 tag·draft asset을 교체하지 않았습니다.

- [x] **W-004 GitHub Release 게시와 원격 HTTPS E2E**
  - 범위·변경 파일: GitHub `v2.0.0` release와 게시 후 검증 기록
  - 대응 요구사항·상위 완료 조건: R-001~R-008
  - 선행조건: W-003, GitHub release 설정 확인, tag·manifest·checksum에 결합된 기존 draft asset
  - 검증 방법: `gh release edit v2.0.0 --draft=false --verify-tag`로 기존 draft를 asset 재업로드 없이 게시하고, latest/exact manifest, en/ko list/install/export, source export와 hash 비교, 충돌 시 tree 불변
  - 결과·근거: 기존 draft를 asset 재업로드 없이 2026-09-18T07:07:35Z에 게시했습니다. release는 `isDraft=false`, `isImmutable=true`이며 `latest`가 `v2.0.0`을 가리킵니다. 실제 latest·exact HTTPS 경로의 installer와 manifest가 서로 및 게시 전 검증본과 byte-identical이었고, 두 version selector의 locale 목록과 en·ko install/export가 모두 성공했습니다. 각 결과의 28개 파일은 tag source export와 일치했고 기존 `AGENTS.md` 충돌은 쓰기 전에 거부되어 target tree가 변하지 않았습니다. 게시 뒤 tag·양쪽 `main`과 5개 asset digest도 게시 전 값과 동일했습니다.

## 3. 검증 기록

| 대상 작업·요구사항 | 확인한 revision 또는 작업 트리 범위 | 실행한 검사 | 결과·남은 한계 |
|---|---|---|---|
| 설계 승인 | `main` `9cea178`에서 추가한 D-004 변경 문서 | 사용자 선택과 기존 installer/release 계약 대조 | GitHub Releases 단일 host 승인; 구현·원격 release 미검증 |
| W-001·W-002 | `9cea178` + `codex/v2-github-releases` 미커밋 변경 | 전체 unittest 102개, root docs, stable locale, Python compile, `git diff --check`; GitHub CLI 공개 release `latest/download` redirect smoke probe | 통과 — 실제 이 저장소의 v2 asset과 latest/exact install은 W-004에서 검증 |
| 게시 전 원격 상태 | `v2.0.0^{}` `8bc8b1b`, Origin·GitHub `main` `d143209`, GitHub draft release | remote ref, ancestry, draft metadata·5개 asset·manifest `source_commit` 확인 | tag commit은 현재 `main`의 조상이고 manifest `source_commit`과 일치. draft asset 게시·원격 E2E는 미수행 |
| W-003 게시 gate | `v2.0.0^{}` `8bc8b1b`, Origin·GitHub `main` `5eefc11`, 기존 GitHub draft | clean tag checkout의 전체 unittest 102개, docs, stable locale, `git diff --check`; 2회 package와 draft 5개 asset의 byte 비교; remote ref·manifest·checksum 재확인 | 통과 — tag는 현재 `main`의 조상이고 package·manifest·draft provenance가 일치; asset 재패키징·교체 없음 |
| W-004 공개 release | GitHub `v2.0.0`, published 2026-09-18T07:07:35Z | latest·exact installer/manifest byte 비교, 두 selector의 locale 목록, en·ko install/export와 tag source tree 비교, 충돌 tree 불변, 게시 후 metadata·digest 재확인 | 통과 — latest `v2.0.0`, immutable release, en·ko 각 28개 파일 일치 |

## 4. 변경·재검증 기록

- 2026-09-18: 기존 계획의 redirect 없는 host 전제를 GitHub Releases 전용 제한 redirect 계약으로 변경했습니다. W-001 이후 기존 redirect 거부 회귀 테스트와 문서 계약을 함께 갱신해야 합니다.
- 2026-09-18: 리뷰 C-001·C-002·C-003 — bootstrap을 curl 7.83 미만에서도 부분 파일 없이 실패하도록 바꾸고, W-003에 Origin/GitHub `main`·tag SHA 결합을 명시했으며 PROJECT §11·§13을 D-004에 맞췄습니다.
- 2026-09-18: 후속 `main` commit을 허용하도록 게시 조건을 tag commit의 `main` 조상 관계로 교정했습니다. `v2.0.0` draft는 tag commit에서 생성한 기존 asset을 재패키징·교체하지 않고 게시합니다.

## 5. 인계

W-001·W-002 구현은 Origin PR #10으로 `main` `8bc8b1b`에 통합됐고, 같은 commit에 고정된 `v2.0.0` tag·asset을 후속 `main` `5eefc11`에서 provenance 재검증한 뒤 공개했습니다. release는 immutable이며 latest·exact 원격 en·ko 검증까지 완료됐습니다. 공개 asset이나 tag에서 결함이 확인되면 교체하지 않고 patch release 계획으로 전환합니다.
