# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

> 이 파일은 선택한 locale artifact가 프로젝트 루트에 배치한 README 양식입니다. 템플릿 source 저장소 소개문으로 교체하지 말고, 아래 placeholder와 안내를 실제 프로젝트 값으로 바꾸세요. 적용한 Template source·version·revision은 [Template Guide](./docs/TEMPLATE_GUIDE.md)와 [Documentation Guide](./docs/DOCS_GUIDE.md)에 기록합니다.

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
python scripts/check-docs.py
python -m unittest discover -s tests -p 'test_check_docs.py' -v
```

문서 검사 회귀 테스트는 `scripts/check-docs.py` 또는 `tests/test_check_docs.py`를 바꿀 때 실행합니다. 문서 검사와 CI 연결은 [CI.md](./docs/CI.md)를 따릅니다. 특정 러너의 YAML은 템플릿에 없습니다. 명령 문자열은 [AGENTS.md](./AGENTS.md)와 같게 유지하세요.

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
- [CI.md](./docs/CI.md): 러너 불문의 품질 게이트 워크플로와 연결 체크리스트

## Security

취약점 신고 방식과 공개하면 안 되는 정보를 작성하세요.

## License

프로젝트 라이선스를 작성하세요.

이 템플릿 자체는 MIT 라이선스([LICENSE](./LICENSE))로 제공됩니다. 템플릿을 적용한 프로젝트는 자기 라이선스를 정해 `LICENSE` 파일과 이 절을 교체하세요. 템플릿의 MIT 고지를 프로젝트 라이선스로 그대로 두지 마세요.
