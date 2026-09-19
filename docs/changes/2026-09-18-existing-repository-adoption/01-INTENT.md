# 변경 의도: 기존 저장소 적용을 위한 안전한 adoption 계약

## Metadata

- **Change ID:** `2026-09-18-existing-repository-adoption`
- **Status:** Accepted
- **Originator:** Chae Sangwon
- **Source:** 2026-09-18 사용자 대화 — 대부분의 사용자는 기존 저장소에 템플릿을 적용할 가능성이 높으므로 기존 저장소를 주 consumer 시나리오로 검토하고 계약 변경 설계를 요청. 2026-09-19 사용자 대화 — 미해결 질문과 완료 기준을 권고안(A안)으로 결정
- **Parent:** [제품 기준](../../00-PROJECT.md) D-002의 비파괴 installer와 D-004의 GitHub Releases transport
- **Approval:** Chae Sangwon, 2026-09-19 사용자 대화 — D-006 설계의 결정 1~7을 모두 권고안으로 승인하고 설계 PR, 구현 PR 분리와 `v2.1.0` 준비 진행을 승인. 2026-09-18 Draft(`5eefc11`의 `01-CHANGE.md`)는 문제·설계 문서 작성 범위만 승인된 상태였습니다.
- **Spec:** [02-SPEC.md](./02-SPEC.md)

## 1. 문제

현재 `install`은 새 대상에 안전하지만 기존 저장소에서 artifact 경로 하나라도 충돌하면 전체를 중단합니다. 일반 저장소는 대개 `README.md`, `.gitignore`, `LICENSE` 또는 기존 agent 지침을 이미 가지므로 실제 주 사용자는 별도 `export` 후 수동 비교·병합을 해야 합니다. 안전성은 높지만 이 경로가 보조 설명에 머물러 있고, 어떤 파일을 보존·병합·결정해야 하는지 기계적으로 설명하지 않습니다.

`jaff2836/claude-review-e2e`의 임시 clone에 `ko` artifact를 대조한 결과 `README.md`와 `.gitignore`가 충돌했고 나머지 파일을 추가한 혼합 tree에서 문서 검사와 checker 회귀는 통과했습니다. 그러나 일반화된 “없는 파일 전부 복사”는 프로젝트가 선택하지 않은 `LICENSE`를 추가할 수 있어 안전한 공식 계약이 아닙니다.

이후 같은 저장소의 PR #28은 `v2.0.0` `ko` artifact를 export 후 수동 병합했습니다. 문서 지침만으로 `LICENSE` 제외와 기존 README·`.gitignore` 병합은 올바르게 수행됐지만, `docs/10-EXTENSION.md` 제거와 `.cursor/BUGBOT.md`·`.omp/WATCHDOG.md` 유지 여부는 리뷰 finding을 거쳐서야 결정됐습니다.

## 2. 기대 결과

- 기존 저장소 적용을 제품의 주 adoption 시나리오로 설명합니다.
- verified artifact와 대상 tree를 비교해 사용자가 보존·병합·결정할 경로를 명시적인 계획으로 제공합니다.
- 기본 동작은 대상 저장소를 수정하지 않으며, 사람 또는 coding agent가 검토 가능한 staging tree와 report를 사용합니다.
- 새 저장소의 fail-closed `install`과 기존 release 검증 계약은 유지합니다.

## 3. 범위와 비범위

### 범위

- `installer.py adopt` 명령과 검증된 staging tree·adoption report
- artifact 경로별 adoption policy와 그 정본·release materialization
- README·적용 가이드에서 기존 저장소 흐름을 먼저 안내하는 문서 순서
- `v2.1.0` release와 실제 기존 저장소 consumer E2E

### 비범위

- 대상 저장소 자동 overwrite, 누락 파일 자동 복사, `--force`
- semantic Markdown merge, 3-way merge, 이미 적용한 저장소의 자동 upgrade
- 자동 commit·push·PR, locale 자동 전환, 기존 프로젝트의 라이선스 선택
- artifact inventory 밖의 대상 파일(이전 템플릿 판의 파일 포함) 분석

## 4. 제약

- checksum, exact version, repository identity와 installer 자기 검증은 `install`·`export`와 같아야 합니다.
- 대상 파일은 한 byte도 바꾸지 않습니다.
- `LICENSE`, 사용자 README, 기존 agent 정책과 프로젝트 결정은 자동 대체하지 않습니다.
- Python 표준 라이브러리만 사용하며 특정 Git hosting 또는 coding agent에 병합 실행을 의존하지 않습니다.
- v2.0.0의 `install`·`export` CLI는 호환 유지합니다.

## 5. 미해결 질문

2026-09-18 Draft의 세 질문은 2026-09-19 결정으로 해소했습니다. 결정 내용은 SPEC이 소유합니다.

- `adoption-plan.json` 공개 schema 여부 → 첫 판은 실험적 report로 두고 호환을 보장하지 않습니다. [SPEC §3.4](./02-SPEC.md#34-adoption-report)
- coding agent용 병합 prompt 포함 여부 → 포함하지 않고 경로별 이유와 적용 가이드 참조만 제공합니다. [SPEC §2.4](./02-SPEC.md#24-agent용-병합-prompt)
- path policy 위치 → `locales/manifest.json`이 정본이며 packager가 release manifest에 materialize합니다. [SPEC §3.2](./02-SPEC.md#32-adoption-policy)

남은 미해결 질문은 없습니다.

## 6. 변경 기록

- 2026-09-18: 기존 저장소가 실제 주 consumer라는 사용자 판단과 `claude-review-e2e` 임시 clone 관찰을 바탕으로 합본형 `01-CHANGE.md` Draft를 작성했습니다.
- 2026-09-19: 사용자가 해결 범위(`adopt` 구현), policy 위치, report 형식, agent prompt, `decide` 범위, 완료 기준, consumer E2E 방식을 모두 권고안으로 결정했습니다. 구성요소·PR이 여러 개로 늘어 [01-DESIGN.md](../../01-DESIGN.md) §2에 따라 분리형 INTENT·SPEC·PLAN으로 전환하고 `01-CHANGE.md`는 정본으로 남기지 않았습니다. 원래 Draft는 `5eefc11`에서 확인할 수 있습니다.
