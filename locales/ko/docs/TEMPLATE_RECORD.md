# 템플릿 적용 기록

> 이 프로젝트가 적용한 템플릿 원본과 적용 내역을 기록하는 프로젝트 소유 문서입니다. 업그레이드 때는 기존 내용을 보존하고 템플릿 절만 병합합니다. 템플릿이 소유하는 문서와 양식은 `docs/template/`에 있고, 그 소유 규칙은 [DOCS_GUIDE.md](./template/DOCS_GUIDE.md)의 「템플릿 소유 폴더」를 따릅니다.

## Metadata

- **Status:** Active
- **Owner:** 프로젝트에 맞게 작성
- **Last reviewed:** YYYY-MM-DD
- **Review cadence:** 템플릿을 처음 적용하거나 새 판으로 업그레이드할 때

## 적용 기준

`docs/template/`의 `Template version`은 그 폴더 내용의 판이므로 여기에 다시 적지 않습니다. 값을 확인하는 방법은 TEMPLATE_GUIDE §5의 「Git으로 복사 기준 기록하기」를 따릅니다.

- **Template source:** 템플릿 원본 저장소의 URL 또는 다시 접근할 수 있는 보관 위치를 프로젝트에 맞게 작성
- **Template revision:** 복사 기준인 원본 commit의 전체 SHA를 프로젝트에 맞게 작성 (미커밋 변경을 포함했다면 `미확정 (기준 commit: <전체 SHA>, 미커밋 변경 포함)`)
- **Template release:** 원본이 release tag와 정확히 일치하면 `release`, 아니면 `미릴리스 (최근 tag: v1.2)` 또는 `미릴리스 (tag 없음)`을 프로젝트에 맞게 작성

## 템플릿 적용 기록

처음 적용할 때와 새 판으로 업그레이드할 때 채웁니다. 해당 없는 항목은 `없음`으로 둡니다.

- **이전 기준:** 업그레이드라면 이전 판과 그때의 source·revision. `adopt --base-version`에는 이 판을 씁니다
- **적용 시작 revision:** 병합을 시작한 이 프로젝트의 commit
- **경로 적응:** 기존 이름을 유지했거나 다른 경로로 옮긴 템플릿 문서와 그 대응
- **보존·제외:** 템플릿 판 대신 프로젝트 판을 유지했거나 적용하지 않은 경로와 이유. `docs/template/TEMPLATE_GUIDE.md`를 지웠다면 여기에 적습니다
- **템플릿 소유 파일의 수정:** `copy` 정책 파일(`docs/template/`, 검사 스크립트·테스트 포함)을 고쳤다면 그 내용과 이유. 다음 업그레이드에서 artifact 판에서 시작해 다시 적용할 대상입니다
- **미검증:** 확인하지 못한 도구 로딩·명령·CI 항목
