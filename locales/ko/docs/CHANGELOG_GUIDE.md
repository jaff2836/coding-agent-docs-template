# 변경 이력 안내

> 프로젝트가 릴리스 노트를 도입하거나 관리할 때 이 문서를 사용합니다.
> root `CHANGELOG.md`는 프로젝트가 소유하는 선택 문서이며, 이 템플릿을
> 적용해도 자동으로 만들거나 덮어쓰지 않습니다.

## Metadata

- **Status:** Active
- **Owner:** 프로젝트에 맞게 작성
- **Last reviewed:** 적용 시 실제 검토일로 교체
- **Review cadence:** 릴리스 절차 또는 문서 소유권 변경 시

## 1. 문서 경계

각 정보는 하나의 정본에서 관리합니다.

| 정보 | 정본 문서 |
| ---- | --------- |
| 현재 설치·사용법과 지원 동작 | `README.md` |
| 공개가 끝난 릴리스의 사용자 가시적 변경 | 프로젝트가 선택해 관리하는 root `CHANGELOG.md` |
| 계획 또는 미완료 작업 | `docs/02-TODO.md` 또는 변경별 PLAN |
| 템플릿 적용 source·version·revision | `docs/DOCS_GUIDE.md`와 `docs/TEMPLATE_GUIDE.md` |

계획한 동작을 README의 현재 동작이나 공개 릴리스 이력처럼 서술하지
마세요. 제품 changelog를 상세 작업 추적기로 사용하지도 마세요.

## 2. Changelog 시작과 보존

- 먼저 저장소에 기존 릴리스 노트가 있는지 확인하고, 프로젝트가
  migration을 명시적으로 결정하지 않았다면 기존 파일명과 형식을
  보존합니다.
- 새 changelog는 프로젝트에 다른 규칙이 없다면 저장소 root의
  `CHANGELOG.md`를 사용합니다.
- 비어 있는 `Unreleased` 절을 기본으로 추가하지 않습니다. 미래 작업은
  TODO 또는 PLAN이 소유합니다. 프로젝트가 `Unreleased` 절을 의도적으로
  사용할 수는 있지만, 공개 완료 릴리스와 명확히 구분해야 합니다.
- 템플릿 upgrade는 사용자에게 보이는 동작이 바뀔 때만 제품 changelog에
  기록합니다. 템플릿 provenance는 안내 문서에 별도로 기록합니다.

## 3. 공개 릴리스 항목

릴리스가 실제로 존재한 뒤 항목을 추가합니다. 정확한 version과 공개일을
기록하고 공개 immutable release 페이지가 있으면 연결합니다. 최신 version을
위에 둡니다.

내용이 있는 분류만 사용합니다. 일반적인 분류는 `Added`, `Changed`,
`Fixed`, `Removed`, `Security`이며, 작은 릴리스는 분류 없는 목록으로
작성해도 됩니다.

포함할 내용:

- 사용자에게 보이는 동작과 지원 workflow
- 호환성 또는 migration 요구 사항
- 사용자가 대응해야 하는 보안·운영 변경
- deprecation과 제거 사항

raw commit 목록, review 이력, 사용자에게 영향이 없는 내부 refactor는
제외합니다.

예시:

```markdown
## [v1.4.0](https://example.com/releases/tag/v1.4.0) — 2026-06-15

### Added

- 기존 저장소용 읽기 전용 report를 추가했습니다.

### Changed

- 과거 설정에 필요한 migration 단계를 명시했습니다.
```

## 4. 릴리스 체크리스트

- [ ] README 서술이 공개된 현재 동작을 설명합니다.
- [ ] 릴리스 항목의 version·날짜·asset이 실제 공개 상태와 일치합니다.
- [ ] 호환성·migration·보안·제거 영향을 명시했습니다.
- [ ] 계획 작업은 공개 항목이 아니라 TODO 또는 PLAN에 남아 있습니다.
- [ ] 기존 changelog 구조와 프로젝트 소유 내용을 보존했습니다.
- [ ] 안내 문서의 템플릿 provenance가 정확합니다.
