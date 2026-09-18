# 변경 실행 계획: GitHub Releases 기반 v2 공개 배포

## Metadata

- **Change ID:** `2026-09-18-github-releases-publication`
- **Spec:** [02-SPEC.md](./02-SPEC.md)
- **Global task:** [02-TODO.md](../../02-TODO.md) T-002
- **Owner:** Codex 구현, Chae Sangwon 최종 검수
- **Baseline:** `9cea17827877e4567d372a5e73ed3e1513953055` (`main`)
- **Integration target:** `main` 후 `v2.0.0` GitHub Release
- **Scope:** GitHub Releases transport, 공개 사용 문서, v2 metadata, exact package와 원격 release 검증

## 1. 구현 순서와 의존성

1. installer의 GitHub URL·redirect·repository binding을 구현하고 local fixture 회귀 테스트를 통과시킵니다.
2. root·locale 문서의 release URL과 bootstrap 절차를 실제 GitHub Releases 계약으로 바꾸고 v2 source metadata를 정렬합니다.
3. 구현을 검토 가능한 branch/PR로 통합한 뒤 exact `main`에서 전체 gate와 deterministic package를 수행합니다.
4. exact commit에 annotated `v2.0.0` tag를 만들고 GitHub Release asset을 게시합니다.
5. 실제 HTTPS 경로에서 latest/exact-version, en/ko install·export와 실패 불변조건을 확인합니다.
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

- [ ] **W-003 exact-head release 후보 검증**
  - 범위·변경 파일: clean exact main에서 생성한 5개 배포 asset
  - 대응 요구사항·상위 완료 조건: R-006~R-008
  - 선행조건: W-001·W-002 통합, 사용자의 commit·push·tag·release 위임
  - 검증 방법: 전체 unittest/docs/locale gate, 2회 package byte equality, tag/source/manifest SHA 일치
  - 결과·근거:

- [ ] **W-004 GitHub Release 게시와 원격 HTTPS E2E**
  - 범위·변경 파일: GitHub `v2.0.0` release와 게시 후 검증 기록
  - 대응 요구사항·상위 완료 조건: R-001~R-008
  - 선행조건: W-003, GitHub release 설정 확인
  - 검증 방법: latest/exact manifest, en/ko list/install/export, source export와 hash 비교, 충돌 시 tree 불변
  - 결과·근거:

## 3. 검증 기록

| 대상 작업·요구사항 | 확인한 revision 또는 작업 트리 범위 | 실행한 검사 | 결과·남은 한계 |
|---|---|---|---|
| 설계 승인 | `main` `9cea178`에서 추가한 D-004 변경 문서 | 사용자 선택과 기존 installer/release 계약 대조 | GitHub Releases 단일 host 승인; 구현·원격 release 미검증 |
| W-001·W-002 | `9cea178` + `codex/v2-github-releases` 미커밋 변경 | 전체 unittest 102개, root docs, stable locale, Python compile, `git diff --check`; GitHub CLI 공개 release `latest/download` redirect smoke probe | 통과 — 실제 이 저장소의 v2 asset과 latest/exact install은 W-004에서 검증 |

## 4. 변경·재검증 기록

- 2026-09-18: 기존 계획의 redirect 없는 host 전제를 GitHub Releases 전용 제한 redirect 계약으로 변경했습니다. W-001 이후 기존 redirect 거부 회귀 테스트와 문서 계약을 함께 갱신해야 합니다.

## 5. 인계

현재 구현 branch는 `codex/v2-github-releases`입니다. commit·push·PR·tag·release는 각각 프로젝트 위임 규칙과 W-003 선행조건을 확인한 뒤 수행합니다.
