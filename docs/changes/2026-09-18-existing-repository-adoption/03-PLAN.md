# 변경 실행 계획: 기존 저장소 적용을 위한 안전한 adoption 계약

## Metadata

- **Change ID:** `2026-09-18-existing-repository-adoption`
- **Spec:** [02-SPEC.md](./02-SPEC.md)
- **Global task:** [02-TODO.md](../../02-TODO.md)의 T-004
- **Owner:** Chae Sangwon
- **Baseline:** Origin `main` `5eefc11075652066c90734dd739cc7c650be826c`과 v2.0.0 공개 기록 PR #13
- **Integration target:** Origin `main`, 이후 GitHub `main`과 `v2.1.0` release
- **Scope:** `locales/manifest.json`의 adoption policy, `scripts/check_locales.py`, `scripts/package_release.py`, `schemas/release-manifest.schema.json`, `scripts/installer.py`와 관련 테스트, root·en·ko 적용 문서. `template/common/scripts/check-docs.py`와 그 테스트는 T-005가 소유합니다.

아래 체크 완료는 해당 브랜치에서의 구현·검증 완료이며 병합·릴리스·지원 검증 완료를 뜻하지 않습니다.

## 1. 구현 순서와 의존성

1. 설계 PR: 이 문서들과 PROJECT D-006·전역 TODO·REVIEW §6 불변조건을 통합합니다.
2. W-001·W-002를 한 구현 PR로 올립니다. policy·schema만 먼저 병합하면 소비자 없는 계약 변경이 되므로 `adopt`와 함께 검토합니다.
3. W-003은 W-001·W-002 브랜치 위에 쌓은 별도 문서 PR입니다. CLI 동작이 확정된 뒤 en·ko 문서를 맞춥니다.
4. T-005 checker 강화는 파일 소유 범위가 겹치지 않으므로 W-001~W-003과 병렬로 진행합니다.
5. W-004는 W-001~W-003과 T-005가 Origin `main`에 통합되고 사용자가 tag·release 게시를 위임한 뒤에만 시작합니다.

## 2. 작업 체크리스트

- [x] **W-001 adoption policy와 release manifest schema 2**
  - 범위·변경 파일: `locales/manifest.json`, `scripts/check_locales.py`, `scripts/package_release.py`, `schemas/release-manifest.schema.json`, 관련 테스트
  - 대응 요구사항·상위 완료 조건: R-005, R-008
  - 선행조건: 설계 PR
  - 검증 방법: policy 누락·잉여·잘못된 값 negative 테스트, 두 번 package byte 비교, 생성 manifest의 schema 2와 member `policy` 확인
  - 결과·근거: `artifact.adoption_policy`에 29개 경로(`copy` 16, `merge` 9, `decide` 4)를 SPEC §3.2 표대로 등록했습니다. locale checker는 누락·inventory 밖 경로·알 수 없는 값·비객체를 거부하고, packager는 policy 없는 member를 거부하며 member record에 `policy`를 materialize합니다. release manifest와 schema는 `schema_version` 2입니다.

- [x] **W-002 `installer.py adopt`**
  - 범위·변경 파일: `scripts/installer.py`, `tests/test_install_release.py`
  - 대응 요구사항·상위 완료 조건: R-002, R-003, R-004, R-007, R-009
  - 선행조건: W-001
  - 검증 방법: fake release 성공 경로와 checksum·installer hash·repository 불일치, 대상 symlink·상위 symlink·비정규 파일·대소문자 변형, output 위치 거부, 게시 실패 injection에서 대상 tree snapshot 불변과 output 부재, 같은 입력의 report byte 동일성, `install`·`export` 회귀
  - 결과·근거: `adopt`는 `export`와 같은 release 검증 후 artifact 경로만 list·lstat·read로 분류하고 `artifact/`와 `adoption-plan.json`을 한 번에 게시합니다. export의 staging 게시를 공통 함수로 옮겼고 `install` 충돌 오류는 `adopt`를 안내합니다. 단위 테스트는 다섯 status와 여덟 대상 상태, `latest`·exact report byte 동일성, output 위치·repo root 거부, checksum 실패와 게시 실패에서 대상 snapshot 불변·output 부재를 확인합니다.

- [x] **W-003 기존 저장소 우선 적용 문서**
  - 범위·변경 파일: `README.md`, `README.ko.md`, `locales/en/docs/TEMPLATE_GUIDE.md`, `locales/ko/docs/TEMPLATE_GUIDE.md`, 필요 시 locale `DOCS_GUIDE.md`와 `locales/manifest.json`의 required command
  - 대응 요구사항·상위 완료 조건: R-001, R-006
  - 선행조건: W-002
  - 검증 방법: en/ko 명령 parity, docs·stable locale checker, en·ko export의 `check-docs.py`
  - 결과·근거: root landing README(en·ko)의 설치 순서를 `adopt`(기존 프로젝트) → `install`(새 프로젝트) → `export`로 바꾸고, `v2.0.0`에는 `adopt`가 없다는 안내를 남겼습니다. en·ko 적용 가이드 §2는 `adopt` 명령과 status별 처리 표를 먼저 두고 `install`·`export`를 뒤에 설명합니다. 제목은 "프로젝트에 적용하기"로 바꿨고 절 번호는 그대로입니다. 미릴리스 이력, Template Adoption Checklist, maintainer `AGENTS.md` 명령도 갱신했습니다. `locales/manifest.json`에 `installer-adopt` 필수 명령 계약을 추가해 en·ko 명령 parity를 강제합니다.

- [ ] **W-004 `v2.1.0` 게시와 consumer E2E**
  - 범위·변경 파일: version·release history 정렬 commit, GitHub `v2.1.0` tag·release, 검증 기록
  - 대응 요구사항·상위 완료 조건: SPEC §6 공개 완료·지원 완료
  - 선행조건: W-001~W-003·T-005 통합, 사용자의 commit·push·tag·release 위임
  - 검증 방법: D-004 게시 gate, latest·exact 원격 `adopt`·`install`·`export`, `claude-review-e2e` baseline `4d9c0df` 임시 clone의 대상 불변 plan과 PR #28 결과 대조, 반영 tree의 checker와 Claude·Codex·Cursor·OMP 로딩 probe
  - 결과·근거:

## 3. 검증 기록

| 대상 작업·요구사항 | 확인한 revision 또는 작업 트리 범위 | 실행한 검사 | 결과·남은 한계 |
|---|---|---|---|
| 설계 | PR #13 head `34e2a74` + 설계 문서 변경 | docs·stable locale checker, 전체 unittest | 구현 전. 설계 문서의 계약 정합성만 확인 |
| W-001·W-002 | 설계 PR #14 head `9378fdd` + 이 브랜치 변경 | 전체 unittest 110개, root docs, stable locale, `git diff --check` | 통과 |
| W-003 | W-001·W-002 PR head + 이 브랜치 변경 | 전체 unittest 110개, root docs, stable locale(`installer-adopt` 명령 계약 포함), en·ko export의 `check-docs.py`와 `test_check_docs.py`, `git diff --check` | 통과 |
| W-001·W-002 로컬 consumer | 위 작업 트리를 in-memory package해 localhost release로 제공, `claude-review-e2e` `4d9c0df` clone | `adopt --version latest`·`2.0.0`, 대상 파일 hash 전후 비교, 같은 release의 `export`와 `artifact/` 비교, 대상 안 output 거부 | 통과 — 29개 중 `missing` 23, `merge` 2(`.gitignore`, `README.md`), `decision` 4(`LICENSE`, `docs/10-EXTENSION.md`, `.cursor/BUGBOT.md`, `.omp/WATCHDOG.md`), `blocked` 0. PR #28 수동 병합의 추가·병합·제외 결과와 일치. 원격 release와 병합 후 로딩 probe는 W-004 |

## 4. 변경·재검증 기록

없음.

## 5. 인계

설계 PR 통합 후 W-001·W-002 구현 PR과 W-003 문서 PR을 순서대로 올립니다. W-004의 tag·release 게시는 별도 위임 없이 수행하지 않습니다.
