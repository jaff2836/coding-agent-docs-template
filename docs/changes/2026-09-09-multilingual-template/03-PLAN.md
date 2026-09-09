# 변경 실행 계획: 다국어 템플릿 소스와 배포 구조

> 이 PLAN이 이번 변경의 상세 작업·검증 상태 정본입니다. 설계 승인 전에는 아래 구현 체크박스를 진행하지 않습니다.

## Metadata

- **Change ID:** 2026-09-09-multilingual-template
- **Spec:** [02-SPEC.md](./02-SPEC.md)
- **Global task:** [02-TODO.md](../../02-TODO.md)의 T-001
- **Owner:** Chae Sangwon
- **Baseline:** `fb7017624ec1ac11cbc6d00df9a8e3916ace5262` (`codex/v1.7.1-ci-doc-fixes`)
- **Integration target:** Origin PR #2의 `v1.7.1` 변경이 `main`에 반영된 뒤 그 정확한 head
- **Scope:** locale/common source 분리, `en`·`ko` payload, export·package·installer, manifest/schema, 문서·locale 검사와 migration 문서. GitHub 생성·release 게시 제외

아래 체크 완료는 구현 branch에서의 구현·검증 완료이며 merge·tag·GitHub release·도구 지원 검증을 뜻하지 않습니다.

## 1. 구현 순서와 의존성

1. 사용자에게 Draft SPEC의 skill 현지화 방식과 `v2.0.0` breaking contract를 승인받습니다. 실제 repository URL은 구현 중 확정할 수 있습니다.
2. `fb70176` tree에서 배포 payload inventory를 고정한 뒤 한국어 locale과 common source를 먼저 이관합니다.
3. root를 저장소 유지관리 영역으로 전환하고 영어 locale을 작성합니다.
4. stable marker와 locale/artifact 검사를 먼저 만든 뒤 export와 release packaging을 연결합니다.
5. 검증된 artifact contract 위에 installer를 구현합니다.
6. 모든 local gate와 소비자 저장소 E2E를 통과한 뒤에만 통합·release 작업을 별도로 요청합니다.

W-001은 뒤 작업의 source boundary입니다. W-002~W-005는 같은 manifest와 output inventory를 바꾸므로 순차 통합합니다. W-006 문서는 실제 구현값을 확인한 뒤 작성하며, W-007은 exact final head에서 전체를 다시 검증합니다.

## 2. 작업 체크리스트

- [ ] **W-001 저장소 관리 영역과 payload source 분리**
  - 범위·변경 파일: root `AGENTS.md`, `docs/`, `template/common/`, `locales/manifest.json`, `locales/ko/`
  - 대응 요구사항: R-002, R-003, R-004, R-010
  - 선행조건: SPEC 승인, PR #2의 통합 기준 확정
  - 검증 방법: `fb70176` tracked payload inventory와 새 common+ko artifact의 path·byte 비교. 이 변경 폴더와 maintainer TODO가 artifact에 없음을 검사
  - 결과·근거: 미실행

- [ ] **W-002 영어 locale과 locale별 도구 계약 작성**
  - 범위·변경 파일: `locales/en/`, `locales/ko/`, locale manifest, stable section marker
  - 대응 요구사항: R-001, R-008, R-009, R-011, R-012
  - 선행조건: W-001 inventory 확정, skill 현지화 방식 결정. 최종 번역 검수자는 Chae Sangwon으로 확정
  - 검증 방법: 필수 file/marker/placeholder/명령 parity, 같은 locale의 skill pair와 REVIEW/BUGBOT 대조, 번역 리뷰 기록
  - 결과·근거: 미실행

- [ ] **W-003 locale-aware 문서·source 검사 구현**
  - 범위·변경 파일: `scripts/check-docs.py`, `scripts/check-locales.py`, 관련 단위·negative fixture
  - 대응 요구사항: R-004, R-008, R-009, R-010
  - 선행조건: W-001~W-002의 inventory·marker 계약
  - 검증 방법: 누락 파일, 중복 output, placeholder 차이, marker 순서, 깨진 링크, 깊은 절 참조, 불변조건·skill drift가 각각 실패하는 테스트
  - 결과·근거: 미실행

- [ ] **W-004 deterministic export와 release packaging 구현**
  - 범위·변경 파일: `scripts/export-template.py`, `scripts/package-release.py`, `schemas/release-manifest.schema.json`, packaging tests
  - 대응 요구사항: R-003, R-004, R-005, R-011
  - 선행조건: W-003 검사 API와 complete locale 판정
  - 검증 방법: 빈 디렉터리 export E2E, 두 번 build한 archive·manifest byte 비교, exact member/mode/timestamp/hash, source commit·version binding과 rebuild 검증
  - 결과·근거: 미실행

- [ ] **W-005 비파괴 locale installer 구현**
  - 범위·변경 파일: `scripts/installer.py`, installer tests와 fake release server fixture
  - 대응 요구사항: R-001, R-006, R-007, R-012
  - 선행조건: W-004 release manifest·bundle contract
  - 검증 방법: locale/version 선택, checksum·manifest 불일치, 크기 제한, path traversal, symlink, case-fold 충돌, 기존 파일 충돌, stage/move 실패에서 대상 tree 불변 확인
  - 결과·근거: 미실행

- [ ] **W-006 적용·마이그레이션·지원 문서 정렬**
  - 범위·변경 파일: root README 언어 링크를 제외한 Template Guide, Documentation Guide, CI, locale별 README·AGENTS, release/install 안내와 변경 이력
  - 대응 요구사항: R-002, R-006, R-007, R-010, R-011, R-012
  - 선행조건: W-001~W-005의 실제 명령·경로 확정
  - 검증 방법: 문서 명령과 CLI `--help` 일치, v1.7.1 rollback·기존 적용 저장소 수동 diff 절차, 미지원 locale 표현과 지원 상태 검토
  - 결과·근거: 미실행

- [ ] **W-007 exact-head 전체 검증과 소비자 E2E**
  - 범위·변경 파일: 전체 변경, 임시 소비자 저장소 fixture
  - 대응 요구사항: R-001~R-012
  - 선행조건: W-001~W-006 완료
  - 검증 방법: `en`·`ko` export별 G-docs/G-docs-test, locale·packager·installer 전체 테스트, `git diff --check`, clean rebuild, 실제 Claude·Codex·Cursor·OMP loading probe
  - 결과·근거: 미실행. 원격 release·지원 완료는 별도 단계

## 3. 검증 기록

| 대상 작업·요구사항 | 확인한 revision 또는 작업 트리 범위 | 실행한 검사 | 결과·남은 한계 |
|---|---|---|---|
| Draft 문서 구조 | `fb70176`에서 분기한 미커밋 설계 문서와 T-001 | `python3 scripts/check-docs.py`; `python3 -m unittest discover -s tests -p 'test_check_docs.py' -v`; `git diff --check` | 통과 — 상대 링크 265개, 절 참조 60건, 문서 검사 6개. 구현 artifact 검증은 미실행 |
| 참조 구현 조사 | `claude-code-pr-review` `origin/main` `a828f26ac0480ae2b6287c475f2c28a9e97cd9ab` | installer, package_release, locale checker와 tests 읽기 | locale bundle 패턴 재사용 가능. 자동 update는 이 템플릿에 부적합 |

## 4. 변경·재검증 기록

- 2026-09-09: root가 배포 payload와 저장소 관리 문서를 겸하는 부트스트랩 문제를 확인했습니다. 한국어 이관 입력을 현재 작업 트리가 아니라 `fb70176` snapshot으로 고정해 이 설계와 maintainer TODO가 locale artifact에 섞이지 않게 했습니다.
- 2026-09-09: `claude-code-pr-review`의 verified locale bundle 패턴은 채택하되 사용자 수정 문서에 대한 자동 update·강제 overwrite는 제외했습니다.

## 5. 인계

- 다음 단계는 Draft SPEC의 skill 현지화 방식과 전체 범위 승인입니다. 실제 repository URL은 구현 중 결정합니다.
- 승인 전에는 W-001 이후 구현을 시작하지 않습니다.
- 기존 Origin PR #2에는 이 설계 branch의 변경을 push하거나 섞지 않습니다.
- 구현·통합·release는 각각 별도 완료 조건이며 commit, push, tag, GitHub release 권한은 아직 위임되지 않았습니다.
