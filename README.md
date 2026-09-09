# AI Agent Docs Template

AI 코딩 에이전트와 사람이 **같은 문서 체계, 설계 절차, 리뷰 기준**을 쓰도록 만든 템플릿의 source 저장소입니다. 앱 런타임이나 프레임워크가 아니라, 프로젝트 문서와 에이전트 지침의 출발점입니다.

> **v2 전환 중:** 현재 root는 저장소 유지관리 영역이므로 새 프로젝트에 직접 복사하지 마세요. 한국어 `v1.7.1` payload는 `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`에서 보존되며, 새 locale artifact와 installer는 아직 구현 중입니다.

Origin 같은 Git 호스트에는 source와 변경 이력을 보관합니다. 특정 CI 제품의 pipeline 파일은 포함하지 않습니다. 품질 게이트 절차는 [CI.md](./docs/CI.md)에 있습니다.

현재 판은 [Template Guide](./docs/TEMPLATE_GUIDE.md) Metadata의 `Template version`을 따릅니다.

## 무엇을 풀려고 하는가

에이전트에게 저장소만 주면 다음이 자주 갈립니다.

- 제품 기준, 이번 변경의 설계, 실행 상태를 한 문서에 섞어 쓰거나 서로 덮어씀
- 작은 버그 수정을 큰 설계 절차로 부풀리거나, 구조 변경을 합의 없이 구현
- 리뷰 기준이 도구마다 달라져 같은 결함을 다르게 판정
- 적용 저장소가 어느 템플릿 판을 복사했는지 재현할 수 없음

이 템플릿은 그 경계를 파일과 절차로 고정합니다. 공통 규칙은 `AGENTS.md`, 조건부 절차는 `docs/`, 도구별 스킬은 그 절차를 가리키는 어댑터만 둡니다.

## 포함되는 것

| 구분 | 역할 |
| --- | --- |
| [AGENTS.md](./AGENTS.md) | Cursor·Codex·OMP 등이 읽는 공통 지침. Claude Code는 [CLAUDE.md](./CLAUDE.md)의 `@AGENTS.md` import로 연결 |
| [locales/ko/README.md](./locales/ko/README.md) | 한국어 적용 프로젝트 README 양식. locale artifact의 루트 `README.md`로 배치 |
| [docs/TEMPLATE_GUIDE.md](./docs/TEMPLATE_GUIDE.md) | 최초 적용, 기존 저장소 이관, 도구 연결, 판 이력 |
| [docs/DOCS_GUIDE.md](./docs/DOCS_GUIDE.md) | 문서 소유권, 식별자 범위, 적용 완료 체크리스트 |
| [docs/00-PROJECT.md](./docs/00-PROJECT.md) | 제품 기준·현재/목표 구조·결정 인덱스 |
| [docs/01-DESIGN.md](./docs/01-DESIGN.md) | 구조·계약을 바꾸는 변경의 구현 전 설계 절차 |
| [docs/02-TODO.md](./docs/02-TODO.md) | 전역 변경 목록·우선순위·통합 결과 |
| [docs/10-EXTENSION.md](./docs/10-EXTENSION.md) | 선택형 장기 확장 설계 |
| `docs/changes/_template/` | 합본형·분리형 Intent/Spec과 선택형 Plan 양식 |
| [docs/REVIEW.md](./docs/REVIEW.md) | PR 리뷰 판정 기준 |
| [docs/REVIEW_ROUND.md](./docs/REVIEW_ROUND.md) | 명시 호출된 리뷰 라운드와 권한 위임 |
| [docs/PROJECT_ANALYSIS.md](./docs/PROJECT_ANALYSIS.md) | 명시 요청 시의 전체 분석 절차 |
| [docs/CI.md](./docs/CI.md) | 러너 불문의 품질 게이트 워크플로와 연결 체크리스트 |
| `scripts/check-docs.py` | 의존성 없는 문서 검사 (상대 링크, 스킬 사본, import, 불변조건, 절 번호, 판 번호) |
| `.agents/skills/`, `.claude/skills/` | `design`·`review-round` 스킬 어댑터 |
| `.cursor/BUGBOT.md`, `.omp/WATCHDOG.md` | 선택형 도구 전용 리뷰 연결 |

전체 트리와 도구별 주의사항은 [Template Guide §1·§4](./docs/TEMPLATE_GUIDE.md)에 있습니다.

## 포함되지 않는 것

- 애플리케이션 코드, 패키지 매니저, 컨테이너, IaC
- 저장소 초기화 스크립트나 대화형 생성기
- GitHub Actions·Buildkite 등 특정 CI 제품의 pipeline 파일, 자동 리뷰 실행 잡, 리뷰 프롬프트. 품질 게이트 절차는 [CI.md](./docs/CI.md)에 있습니다.
- CODEOWNERS 파일 자체 (안내만 있음)
- 적용 프로젝트의 라이선스·보안 신고 채널 (템플릿 `LICENSE`는 이 템플릿 자체의 MIT)

## 새 프로젝트에 적용하기

현재 v2 source tree는 직접 복사 대상이 아닙니다. `template/common/`과 선택한 `locales/<tag>/`를 합성하는 exporter·installer가 완성되기 전에는 한국어 `v1.7.1` 기준 commit `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`을 사용하세요. 새 구조의 계약과 진행 상태는 [다국어 템플릿 SPEC](./docs/changes/2026-09-09-multilingual-template/02-SPEC.md)과 [PLAN](./docs/changes/2026-09-09-multilingual-template/03-PLAN.md)에 있습니다.

기존 프로젝트에 넣을 때는 같은 이름 파일을 덮어쓰지 말고 기존 지침·문서와 비교해 병합하세요. v2 installer도 기존 파일 충돌 시 쓰지 않는 방향으로 설계되어 있습니다.

## 이 템플릿 저장소에서 검사하기

문서 검사와 검사 스크립트의 회귀 테스트는 표준 라이브러리만 사용합니다. `python`이 없으면 `python3`을 쓰세요.

```text
python scripts/check-docs.py
python -m unittest discover -s tests -p 'test_check_docs.py' -v
```

적용을 마친 저장소에서도 `scripts/check-docs.py`는 동작합니다. 원본 템플릿의 placeholder 잔존은 이 검사가 실패로 보지 않습니다. 같은 게이트를 원격 CI에 붙이는 순서와 체크리스트는 [CI.md](./docs/CI.md)를 따릅니다.

## 문서와 도구

- 일상 운영과 문서별 정본은 [DOCS_GUIDE.md](./docs/DOCS_GUIDE.md)가 기준입니다. `docs/` 안에 `README.md`를 두지 않습니다.
- `review-round`는 사용자가 명시적으로 호출한 경우에만 실행합니다. `design`은 적용 조건에 맞는 변경에서 절차를 시작할 수 있습니다.
- Cursor Bugbot 또는 OMP advisor를 쓰지 않으면 해당 전용 파일을 삭제하고 안내 문서의 링크도 정리합니다.

## License

이 템플릿 자체는 MIT 라이선스([LICENSE](./LICENSE))입니다. 적용한 프로젝트는 자기 라이선스를 정해 `LICENSE`와 프로젝트 README의 License 절을 교체하세요. 템플릿의 MIT 고지를 프로젝트 라이선스로 그대로 두지 마세요.
