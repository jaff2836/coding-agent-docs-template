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
  - 결과·근거: 공개 완료 조건을 충족했고, 지원 완료 조건은 Codex 로딩 probe만 남았습니다.
    - **release 준비:** Origin PR #18(merge commit `36a123ff3bd939a99148e0f804f9e20924f6be0b`)에서 `Template version`을 2.1.0으로 정렬했습니다.
    - **게시 gate:** 이 commit의 clean clone에서 unittest 140개, docs·stable locale 검사, `git diff --check`가 통과했습니다. 두 번 만든 5개 asset이 byte-identical이었습니다. manifest는 `schema_version` 2, version `2.1.0`, `source_commit`이 tag commit이고, locale별 29개 member(`copy` 16, `merge` 9, `decide` 4)입니다.
    - **게시:** GitHub `main`을 같은 commit으로 fast-forward한 뒤 annotated tag `v2.1.0`을 push했습니다. draft asset은 다시 내려받아 byte 동일성을 확인했습니다. Origin·GitHub `main`과 tag가 같은 SHA임을 재확인한 뒤 2026-09-19T04:41:23Z에 immutable Latest release로 공개했습니다.
    - **원격 E2E:** GitHub latest·exact의 installer와 manifest가 게시 전 package와 byte-identical이었습니다. `list-locales`와 en·ko `install`·`export`(각 29 files)가 tag source export와 일치했고, 설치 tree의 checker와 테스트가 통과했습니다. 기존 `AGENTS.md` 충돌은 대상을 바꾸지 않고 `adopt`를 안내했습니다.
    - **consumer E2E:** `claude-review-e2e` `4d9c0df` clone에 `adopt`를 실행했습니다. 대상 파일은 전후가 같았고, latest와 exact plan이 byte-identical이었습니다. 결과는 PR #28과 같은 `missing` 23, `merge` 2, `decision` 4였습니다.
    - **report 반영:** 23개 추가, README·`.gitignore` 병합, `LICENSE`·`docs/10-EXTENSION.md` 미채택, BUGBOT·WATCHDOG 채택으로 반영했습니다. 적용 가이드 5단계에 따라 확장 문서로 들어오는 링크 4개를 정리하자 checker와 checker 테스트가 통과했습니다.
    - **로딩 probe:** 반영 tree의 `AGENTS.md`에만 둔 probe 값과 한국어 응답 지침을, 도구를 끈 Claude Code 2.1.277과 OMP 18.2.1, 그리고 Cursor Agent 2026.09.15가 답했습니다. 명시적 `design` skill은 Claude(`/design`, 도구 없음), Cursor(도구 호출 0회), OMP(pty 대화형 `/skill:design`)에서 skill 본문의 `docs/01-DESIGN.md §1`을 답했습니다. OMP print mode는 `/skill:design`을 펼치지 않았습니다.
    - **남은 것:** Codex CLI 0.155.0 probe는 사용량 한도로 실행하지 못했습니다.

## 3. 검증 기록

| 대상 작업·요구사항 | 확인한 revision 또는 작업 트리 범위 | 실행한 검사 | 결과·남은 한계 |
|---|---|---|---|
| 설계 | PR #13 head `34e2a74` + 설계 문서 변경 | docs·stable locale checker, 전체 unittest | 구현 전. 설계 문서의 계약 정합성만 확인 |
| W-001·W-002 | 설계 PR #14 head `9378fdd` + 이 브랜치 변경 | 전체 unittest 110개, root docs, stable locale, `git diff --check` | 통과 |
| W-003 | W-001·W-002 PR head + 이 브랜치 변경 | 전체 unittest 110개, root docs, stable locale(`installer-adopt` 명령 계약 포함), en·ko export의 `check-docs.py`와 `test_check_docs.py`, `git diff --check` | 통과 |
| W-004 게시 gate | PR #18 merge commit `36a123f` clean clone | unittest 140개, docs, stable locale, `git diff --check`; package 2회 byte 비교; draft 5개 asset 재다운로드 비교; 게시 직전 Origin·GitHub `main`·tag SHA 대조 | 통과 — immutable Latest `v2.1.0` 공개 |
| W-004 원격 E2E | GitHub `v2.1.0` release | latest·exact installer·manifest byte 비교, `list-locales`, en·ko `install`·`export`와 tag source export 비교, 설치 tree checker·테스트, 충돌 불변, `v2.0.0` installer·version 호환 | 통과 — `v2.0.0` installer는 `2.0.0`만, `v2.1.0` installer는 `2.1.0`만 설치하고 다른 조합은 schema 오류로 fail-closed |
| W-004 consumer | `claude-review-e2e` `4d9c0df` clone, GitHub latest·exact `adopt` | 대상 전후 hash, plan byte 비교, report 반영 후 checker·테스트, Claude·Cursor·OMP 로딩 probe | 통과 — Codex probe는 사용량 한도로 미실행 |
| W-001·W-002 로컬 consumer | 위 작업 트리를 in-memory package해 localhost release로 제공, `claude-review-e2e` `4d9c0df` clone | `adopt --version latest`·`2.0.0`, 대상 파일 hash 전후 비교, 같은 release의 `export`와 `artifact/` 비교, 대상 안 output 거부 | 통과 — 29개 중 `missing` 23, `merge` 2(`.gitignore`, `README.md`), `decision` 4(`LICENSE`, `docs/10-EXTENSION.md`, `.cursor/BUGBOT.md`, `.omp/WATCHDOG.md`), `blocked` 0. PR #28 수동 병합의 추가·병합·제외 결과와 일치. 원격 release와 병합 후 로딩 probe는 W-004 |

## 4. 변경·재검증 기록

- 2026-09-19: Origin의 stacked PR은 부모 PR이 병합된 뒤에도 base가 자동으로 바뀌지 않았습니다. #14·#15·#16·#17의 base를 `main`으로 바꾼 뒤 번호 순서대로 병합했습니다.
- 2026-09-19: release 준비에서 `tests/test_package_release.py`가 version `2.0.0`에 고정돼 있어 버전 정렬 후 실패했습니다. source guide의 `Template version`을 읽도록 고친 뒤 PR #18에 포함했습니다.

## 5. 인계

W-001~W-003은 PR #15·#16, release 준비는 PR #18로 통합됐고 `v2.1.0`이 공개됐습니다. 남은 작업은 반영 tree에서 Codex CLI 로딩 probe 하나입니다. 공개 asset·tag는 교체하지 않으며, 결함이 발견되면 patch release로 복구합니다.
