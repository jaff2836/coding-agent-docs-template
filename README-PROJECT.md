<!-- 적용 시 이 파일을 루트 README.md로 바꿔 넣고, 이 주석을 삭제한 뒤 placeholder를 채우세요. 이 저장소 자체 소개는 README.md입니다. -->

# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

## Requirements

- 프로젝트에 필요한 런타임과 도구를 작성하세요.

## Setup

프로젝트 설치 및 초기 구성 절차를 작성하세요.

## Run

```text
{{RUN_COMMAND}}
```

## Build

```text
{{BUILD_COMMAND}}
```

## Test

```text
{{TEST_COMMAND}}
```

## Quality Checks

```text
{{LINT_COMMAND}}
{{TYPECHECK_COMMAND}}
```

## Project Documentation

- [Template Guide](./docs/TEMPLATE_GUIDE.md): 이 템플릿을 프로젝트에 처음 적용하는 방법
- [AGENTS.md](./AGENTS.md): AI 개발 도구의 공통 프로젝트 지침
- [Documentation Guide](./docs/DOCS_GUIDE.md): 문서 체계, source of truth 및 템플릿 완료 체크리스트
- [00-PROJECT.md](./docs/00-PROJECT.md): 제품 개요·기본 설계·현재/목표 구조·결정·설계 인덱스
- [01-DESIGN.md](./docs/01-DESIGN.md): 구조·계약을 바꾸는 변경의 구현 전 설계 절차
- [02-TODO.md](./docs/02-TODO.md): 프로젝트 전체의 변경·우선순위·의존성과 통합 결과
- [10-EXTENSION.md](./docs/10-EXTENSION.md): 선택형 장기 확장 설계와 단계별 완료 조건
- 변경별 양식 묶음: 합본형 [01-CHANGE.md](./docs/changes/_template/01-CHANGE.md), 분리형 [01-INTENT.md](./docs/changes/_template/01-INTENT.md)·[02-SPEC.md](./docs/changes/_template/02-SPEC.md), 선택형 [03-PLAN.md](./docs/changes/_template/03-PLAN.md). 템플릿 적용 시 `_template/` 묶음은 모두 복사하고, 실제 변경에서는 필요한 형식만 별도 변경-ID 폴더에 복사해 사용합니다.
- [REVIEW.md](./docs/REVIEW.md): PR 리뷰 정책
- [REVIEW_ROUND.md](./docs/REVIEW_ROUND.md): 리뷰 라운드 절차와 권한 위임 범위
- [PROJECT_ANALYSIS.md](./docs/PROJECT_ANALYSIS.md): 명시적으로 요청된 전체 프로젝트 분석 절차

## Security

취약점 신고 방식과 공개하면 안 되는 정보를 작성하세요.

## License

프로젝트 라이선스를 작성하세요.

이 템플릿 자체는 MIT 라이선스([LICENSE](./LICENSE))로 제공됩니다. 템플릿을 적용한 프로젝트는 자기 라이선스를 정해 `LICENSE` 파일과 이 절을 교체하세요. 템플릿의 MIT 고지를 프로젝트 라이선스로 그대로 두지 마세요.
