# 변경 의도: 다국어 템플릿 소스와 배포 구조

> 이 변경은 템플릿 저장소 자체에 [변경 설계 절차](../../01-DESIGN.md)를 적용한 기록입니다. 구현 전까지 현재 `v1.7.1` 한국어 템플릿 계약은 유지하며, 이 폴더는 locale artifact에 포함하지 않습니다.

## Metadata

- **Change ID:** 2026-09-09-multilingual-template
- **Status:** Draft
- **Originator:** Chae Sangwon
- **Source:** 2026-09-09 사용자 대화 — locale별 소스 관리, BCP 47, 언어 선택형 다운로드·변환 방식 검토 요청
- **Parent:** [Template Guide](../../TEMPLATE_GUIDE.md) §1·§2·§4·§5의 배포 구조와 고정 도구 진입점
- **Approval:** 부분 합의 — locale별 소스 관리, BCP 47 tag, 언어 선택형 installer, 최종 검수자 Chae Sangwon, 첫 안정판의 `en`·`ko` complete 포함, W-001의 payload/maintainer 영역 분리 구현. skill 현지화 방식과 나머지 구현 범위는 미승인
- **Spec:** [02-SPEC.md](./02-SPEC.md)

## 1. 문제

현재 `v1.7.1` 템플릿의 안내·정책·스킬 prose와 기본 응답 언어는 한국어입니다. 다른 언어 사용자는 파일을 직접 번역하거나 영어 지침과 자국어 프로젝트 문서를 혼용해야 합니다. 직접 번역하면 다음 계약이 조용히 어긋날 수 있습니다.

- `AGENTS.md`, `CLAUDE.md`, `.agents/skills/`, `.claude/skills/`의 고정 탐색 경로와 import
- `docs/REVIEW.md`와 `.cursor/BUGBOT.md`의 불변조건 복제
- 문서 링크, 번호가 있는 절 참조, placeholder와 명령 문자열
- `scripts/check-docs.py`가 현재 사용하는 한국어 헤딩과 예시 문구

원본 저장소의 root 파일은 동시에 배포할 한국어 payload와 템플릿 자체의 개발 문서 역할을 합니다. locale source를 추가하면서 이 두 역할을 분리하지 않으면 실제 변경 설계와 TODO가 사용자용 템플릿에 섞이는 부트스트랩 문제가 생깁니다.

## 2. 기대 결과

- 영어와 한국어를 독립적으로 검증되는 공식 locale로 제공합니다.
- 저장소에서는 locale별 source와 언어 비의존 공통 파일을 관리하고, 사용자는 선택한 locale 하나가 표준 root 경로에 배치된 artifact를 받습니다.
- 사용자는 BCP 47 language tag와 템플릿 버전을 지정해 검증된 release bundle을 설치하거나 빈 디렉터리로 export할 수 있습니다.
- 원본 저장소의 관리 문서와 사용자에게 배포하는 템플릿 payload가 분리됩니다.
- 기존 `v1.7.1` 한국어판과 이미 적용한 저장소는 자동 변경하거나 덮어쓰지 않습니다.

## 3. 범위와 비범위

### 범위

- root 저장소 관리 영역, locale source, 공통 payload의 책임과 경로
- 초기 공식 locale `en`, `ko`
- BCP 47 기반 locale 식별과 지원 상태
- locale별 deterministic artifact, release manifest와 안전한 installer/exporter 계약
- 고정 진입점·스킬·리뷰 정책의 locale별 배치
- locale 간 파일·placeholder·절·링크·복제 계약과 artifact 회귀 검사
- `v1.7.1`에서 새 구조로의 마이그레이션과 rollback

### 비범위

- `en`, `ko` 외 번역 작성과 품질 보증
- 기계 번역을 공식 지원 locale로 자동 승격하는 기능
- 날짜·통화·정렬 등 일반적인 애플리케이션 locale 기능
- GitHub 저장소 생성, release 게시, Origin/GitHub mirror 설정
- 이미 적용되어 사용자가 수정한 문서를 자동 update·덮어쓰기
- 공개 저장소 root `README.md`·`README.ko.md`의 최종 소개문 작성

## 4. 제약

- language tag는 [BCP 47 / RFC 5646](https://www.rfc-editor.org/info/rfc5646/) 형식을 사용하고 underscore 기반 자체 규칙을 만들지 않습니다. 처음에는 `en`, `ko`만 allowlist로 지원합니다.
- 적용 artifact에는 locale 디렉터리를 남기지 않고 `AGENTS.md`, `CLAUDE.md`, `docs/`, `.agents/skills/` 등 현재의 표준 경로를 유지합니다.
- 한 적용 저장소에서 활성 정책 언어의 정본은 하나여야 합니다. 여러 locale의 실행용 prompt·정책을 동시에 설치하지 않습니다.
- `CLAUDE.md`의 `@AGENTS.md`, `.omp/WATCHDOG.md`의 `@../docs/REVIEW.md`, Codex의 명시 호출 정책 등 현재 도구 계약을 보존합니다.
- installer와 packager는 Python 표준 라이브러리만 사용하고, symlink·경로 탈출·부분 설치·무검증 overwrite를 허용하지 않습니다.
- release artifact는 전체 source commit, template version, locale, member 목록과 SHA-256에 결합되어야 합니다.
- 기존 한국어 payload의 이관 기준은 이 변경 문서가 추가되기 전 commit `fb7017624ec1ac11cbc6d00df9a8e3916ace5262`입니다. 저장소 관리용 설계와 TODO를 locale payload로 복사하지 않습니다.

## 5. 미해결 질문

- [x] 영어판 전체 번역과 한국어판 재검수의 최종 승인자는 Chae Sangwon입니다.
- [x] 첫 안정판은 `en`, `ko`를 모두 `complete` 상태로 포함합니다. 어느 하나라도 완료 조건을 충족하지 못하면 안정판을 게시하지 않습니다.
- [ ] skill 자연어를 영어로 공통화하고 출력 언어만 locale로 제어할지, `description`·본문·출력을 모두 locale별로 작성할지 결정합니다. 권고안은 후자이며, 번역하지 않는 contract ID·marker와 locale 공통 행동 fixture로 의미 동등성을 검증합니다.
- [ ] installer bootstrap URL과 release asset 이름의 실제 owner/repository는 이 Draft PR에서 고정하지 않고 구현 중 공개 저장소 구성이 확정되면 결정합니다.

## 6. 변경 기록

- 2026-09-09: 사용자와 locale별 source, BCP 47, 언어 선택형 다운로드·변환 방향을 합의하고 전체 계약 검토를 위한 Draft를 작성했습니다.
- 2026-09-09: 최종 번역 검수자를 Chae Sangwon으로 정하고 첫 안정판에 `en`·`ko` complete locale을 함께 포함하기로 합의했습니다. skill 현지화 방식과 실제 repository URL은 미결정으로 유지했습니다.
- 2026-09-09: Origin PR #3 리뷰 F-001의 수정 방법으로 W-001 payload/maintainer 영역 분리 구현을 승인했습니다. F-002~F-004의 언어 소유권·README·호스트 중립 계약도 리뷰에서 확인된 모순을 제거하는 범위로 교정합니다.
