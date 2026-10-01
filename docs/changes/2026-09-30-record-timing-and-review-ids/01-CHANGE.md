# 변경: 기록 시점과 리뷰 finding ID·근거 계약

## Metadata

- **Change ID:** `2026-09-30-record-timing-and-review-ids`
- **Status:** Accepted
- **Originator:** Chae Sangwon
- **Source:** 2026-09-29 전체 분석 뒤 사용자 논의에서 TODO 지연을 구조 문제로 보고 해결 방안을 요청했습니다. 같은 날 사용자가 merge 결합 서술 범위를 결정했습니다(§1.4). T-014는 PR #28 version 2 권고 `cmt_01m33dxsvpenytt4nndy29hwz9`에서 출발했습니다. 2026-09-30 사용자의 다음 작업 진행 요청으로 T-030과 함께 설계합니다.
- **Parent:** [제품 기준](../../00-PROJECT.md) §11, [문서 소유권 설계](../2026-09-22-documentation-ownership/01-CHANGE.md)(D-009), locale `DOCS_GUIDE.md`·`02-TODO.md`·`REVIEW.md`·`REVIEW_ROUND.md`의 현재 계약
- **Decision:** PROJECT §8의 D-013(T-030 기록 시점: A2·E1)과 D-014(T-014 리뷰 finding ID·근거: B1·C1)
- **Approval:** Chae Sangwon, 2026-09-30 선택 응답 — PR #55 version 1 head `150ebc94ba4d4518b75464d299cdd7887f305668`의 Q1 “채택”, Q2 “PR 본문”, Q3 “슬롯 ID+대표 ID”, Q4 “채택”. 요구사항 R-001~R-009, §2.3 설계, §2.6 순서를 함께 승인했습니다. §1.4는 2026-09-29 사용자 결정입니다.
- **Execution:** [전역 TODO](../../02-TODO.md)의 T-030·T-014가 실행 상태를 소유합니다. 정리 작업 T-033과 release 작업 T-034는 §2.6의 PR 순서를 따릅니다.

## 1. Intent

### 1.1 문제와 확인한 근거

**통합 대상의 TODO가 한 PR씩 늦습니다.** 원인은 다음 세 규칙이 겹친 데 있습니다.

- `Completed`는 통합을 확인한 뒤에만 기록합니다(locale `02-TODO.md` 운영 규칙).
- 통과한 head는 동결하고 기록용 commit을 금지합니다(locale `DOCS_GUIDE.md` 88행, [REVIEW_ROUND.md](../../REVIEW_ROUND.md) §6).
- 통과 뒤 기록은 다음 작업이 받습니다([REVIEW_ROUND.md](../../REVIEW_ROUND.md) §9, `DOCS_GUIDE.md` 109행 `문서 반영 대기`).

실제로 이 지연이 반복됐습니다.

| merge한 PR | merge 뒤 `main`에 남은 상태 | 고친 PR |
|---|---|---|
| #50 | T-013 구현 2가 In Progress | #51 |
| #51 | T-029가 In Progress | #52 |
| #53 | T-031 미완료 | #54 |

**기록 전용 commit이 끝나지 않는 고리를 만듭니다.** PR 안에 자기 head의 CI 번호나 리뷰 결과를 적으면, 그 commit이 새 head가 되어 CI와 재리뷰가 다시 필요합니다.

- PR #50·#51은 fix commit마다 이전 version의 CI 번호를 TODO에 적었습니다.
- PR #54 version 3(`a6f51e8`)은 외부 설정(ruleset) 복원만 기록한 commit이었는데도 CI #72·#57과 재리뷰를 새로 요구했습니다.

**병렬 리뷰어가 같은 finding ID를 씁니다.**

- PR #28에서는 한 리뷰어의 `C28-00x`가 먼저 게시된 리뷰와 겹쳐 정정 댓글이 필요했습니다.
- PR #29에서는 `C29-001`이 두 리뷰에서 서로 다른 항목에 붙었습니다.
- 그 뒤로는 리뷰어들이 앞 리뷰를 읽고 "새 ID를 만들지 않는다"는 식으로 비공식 조율만 하고 있습니다. #46·#50·#51·#54에서 확인됩니다.
- 이 설계 PR #55 version 3에서도 사용자 review `rev_01m3rcyqd7fh99b3f86sgtp9db`(05:35:16Z)와 Codex review `rev_01m3rd1vm9exsa8ha5qvfpgd2f`(05:36:59Z)가 서로 다른 finding에 같은 `C55-002`를 붙였습니다.
- 구현 PR #56 version 1에서도 사용자 review `rev_01m3rm714afajs2y14gqnewvdp`와 Codex review `rev_01m3rmcrpgebtsdrpph29rrkz3`가 서로 다른 finding에 같은 `C56-001`을 붙였습니다.
- locale 계약에는 게시되는 finding ID의 형식이 없고, 세션 원장의 `F-nnn`만 있습니다([REVIEW_ROUND.md](../../REVIEW_ROUND.md) §7).

**리뷰 근거가 exact head와 어긋납니다.**

- PR #53 리뷰 가운데 하나는 exact head(212건)와 다른 unittest 수(210건)를 근거로 적었습니다.
- 다른 리뷰는 Windows 로그를 읽지 못한 채(HTTP 403) check 성공만 근거로 삼았습니다.
- 사용자는 일부 리뷰가 CI 재실행 전 결과를 본 것으로 판단했습니다.
- [REVIEW_ROUND.md](../../REVIEW_ROUND.md) §4의 head 정렬은 finding에만 적용되고, 리뷰 본문의 CI·검증 주장에는 적용되지 않습니다.

### 1.2 기대 결과

- 변경을 merge한 commit의 TODO·PLAN이 그 변경의 완료 상태를 바로 보여 줍니다. 완료만 기록하는 후속 PR이 필요 없습니다.
- PR 안에 자기 head의 CI·리뷰 결과만 적는 commit이 생기지 않습니다.
- 병렬 리뷰어가 서로 조율하지 않아도 게시된 finding ID가 겹치지 않고, 다른 PR·TODO에서 인용해도 모호하지 않습니다.
- 리뷰가 인용한 CI·검증 결과가 어느 head에서 나온 것인지 추적할 수 있습니다.

### 1.3 범위와 비범위

**범위:**
- en·ko locale의 `docs/DOCS_GUIDE.md`, `docs/02-TODO.md` 운영 규칙, `docs/REVIEW.md` §5·§7·§10, `docs/REVIEW_ROUND.md` §2.1·§4·§6·§7·§9
- `.cursor/BUGBOT.md`의 해당 복제 규칙과 review-round skill 사본(문구가 바뀌는 경우)
- 같은 내용을 쓰는 root maintainer 문서

**비범위:**
- CI 설정과 코드
- 기록 자동화 봇
- 중요도·임계값·blocking 정의
- 저장소 밖 리뷰 도구의 내부 prompt
- 과거 기록의 소급 수정

### 1.4 제약

- **사용자 결정(2026-09-29):**
  - branch 문서는 그 branch의 최종 head가 merge되는 시점까지의 상태를 결합 서술할 수 있습니다.
  - merge 이후의 사건(release 공개, 다른 원격 동기화, 다른 PR, 외부 검증)을 서술하는 것은 기본적으로 위반입니다.
  - 사용자가 명시적으로 요청한 경우에만 허용합니다. 사용자는 README 같은 문서를 직접 고칠 때 이 예외가 가끔 필요하다고 했습니다.
- **리뷰어 구성:** 바뀔 수 있습니다. 2026-09-29부터 Claude가 개발을, Codex가 리뷰를 맡습니다. 그래서 식별자에는 모델명이 아니라 고정된 리뷰어 슬롯 라벨을 씁니다.
- **기존 규칙 유지:** [REVIEW_ROUND.md](../../REVIEW_ROUND.md) §1의 위임 범위(재리뷰 요청 외 PR 댓글 금지)와 통과 head 동결은 그대로 둡니다.
- **구현 조건:** en·ko 구조 parity와 기존 문서 검사를 통과해야 하며, 새 의존성이나 CI 제품을 추가하지 않습니다.

### 1.5 합의한 선택

2026-09-30 사용자가 네 질문 모두 권고안을 선택했습니다. 비교한 대안은 §2.2에 근거로 남깁니다.


1. **Q1 — PR 원장:** 자기 head의 사후 사실(CI build, 리뷰 판정, merge SHA)을 TODO·PLAN에 쓰지 않고 PR을 근거로 삼을지 정해야 합니다. 권고는 채택입니다(§2.2 A2).
2. **Q2 — 예외 기록:** 사용자가 요청한 merge 이후 서술의 근거를 어디에 남길지 정해야 합니다. 권고는 PR 본문(PR이 없으면 작업 보고)입니다.
3. **Q3 — finding ID 형식:** 리뷰어 슬롯이 붙은 ID와 대표 ID를 쓸지 정해야 합니다. 권고는 채택입니다(§2.2 B1).
4. **Q4 — 리뷰 근거:** 리뷰 본문에 검토한 head와 인용한 CI build·head를 적도록 요구할지 정해야 합니다. 권고는 채택입니다(§2.2 C1).

## 2. Spec

### 2.1 요구사항과 시나리오

| ID | 요구사항 | 상황·입력 | 관찰 가능한 결과 | 검증 |
|---|---|---|---|---|
| R-001 | merge 결합 서술 | 작업 branch가 자기 T 항목을 `Completed`로 옮기고 근거를 "이 변경의 PR"로 적음 | merge 직후 통합 대상의 TODO가 완료를 보여 줌. PR이 닫혀 merge되지 않거나 revert되면 서술도 함께 사라짐 | locale 두 guide·TODO 규칙 문구, 구현 PR 다음 PR에서의 적용 |
| R-002 | merge 이후 사건의 서술 금지와 예외 | 사용자 요청 없이 release 공개나 다른 원격 동기화를 완료로 적음 | 리뷰에서 위반 finding이 됨. 사용자 요청이 있으면 요청 근거(요청자·시점·범위)가 PR 본문에 있어야 허용됨 | REVIEW §5 점검 항목, 시나리오 대조 |
| R-003 | PR 원장 (Q1) | fix commit 뒤 CI·재리뷰가 끝남 | 그 결과를 기록하려고 commit하지 않음. TODO에는 "근거: PR"만 두고, 실제 수정이 있는 commit에서만 이전 version의 판정을 기록할 수 있음 | DOCS_GUIDE·TODO 규칙, PR 사례 대조 |
| R-004 | 최종 head finding 인계 | 통과한 최종 head의 리뷰에서 새 비차단 finding이 나옴 | 기존 §9처럼 `문서 반영 대기`로 다음 관련 작업이 받음. 통과 head를 바꾸지 않음 | REVIEW_ROUND §6·§9 |
| R-005 | PR 없는 작업 | 로컬 통합 대상에 직접 반영 | 결합 서술의 조건은 그 통합 commit이고, 근거는 기준 revision과 변경 범위. 가상의 PR·SHA를 만들지 않음 | DOCS_GUIDE 로컬 Git 절 |
| R-006 | 리뷰어 슬롯이 붙은 finding ID (Q3) | 병렬 리뷰어가 같은 PR에 finding을 게시함. 등록되지 않은 두 리뷰어가 같은 라벨을 고르는 경우도 포함 | 슬롯 ID는 리뷰어 목록(§2.1 표 또는 프로젝트가 정한 목록)에 한 번씩만 등록된 역할 라벨을 가진 리뷰어만 발급하므로 대상 안에서 겹치지 않음. 등록되지 않은 리뷰어는 슬롯 ID를 발급하지 않음. 대신 게시물 안의 finding마다 항목 번호(1, 2, …)를 붙이고 `<플랫폼 게시 식별자>/<항목 번호>`로 가리킴. finding이 하나뿐이어도 원 ID는 `/1`이며, 게시 식별자만 쓴 인용은 `/1`과 같음. 같은 게시물을 head마다 덮어쓰는(sticky) 리뷰어는 `<게시 식별자>@<head 12자리>/<항목 번호>`를 쓰며, 짧은 인용도 `@<head 12자리>/1`과 같고 head 없는 인용은 원 ID로 쓰지 않음. PR 게시물이 없는 리뷰는 세션 종료 보고를 게시물로 보고 `<branch>@<마지막 리뷰 head 12자리>@<보고 UTC 시각>-<보고별 무작위 16진수 8자리>/<항목 번호>`를 씀. 같은 head 재리뷰, 미커밋 변경, 같은 초의 다른 세션도 무작위 값으로 구별됨 | REVIEW §7, REVIEW_ROUND §2.1 열, BUGBOT 복제, 미등록 리뷰어 두 명이 같은 라벨을 고르는 시나리오, 한 리뷰 본문에 finding 두 건이 있는 시나리오, PR 없는 `reviewers = self` 리뷰의 인계 시나리오, 같은 branch·head를 다른 세션이나 미커밋 변경으로 다시 리뷰하는 시나리오, 두 세션이 같은 UTC 초에 보고를 만드는 시나리오, sticky 게시물이 head마다 다른 finding을 싣는 시나리오 |
| R-007 | 대표 ID | 두 리뷰어가 같은 원인을 보고하거나, 인계할 finding에 슬롯 ID가 없음 | 대표 ID는 원 ID 중 가장 먼저 게시된 슬롯 ID이고, 슬롯 ID가 없으면 가장 먼저 게시된 원 ID임. 게시 순서가 같으면 원 ID 문자열의 사전순으로 가장 앞선 것을 고름. 대표 ID를 따로 발급하지 않으므로 슬롯이 하나도 없는 `reviewers = self` 인계에서도 항상 존재함. 원장과 인계 목록이 원 ID(슬롯 ID 또는 `<플랫폼 게시 식별자>/<항목 번호>`)를 모두 남김. 세션 원장의 `F-nnn`은 세션 안에서만 씀 | REVIEW_ROUND §4 중복 통합·§7 표 |
| R-008 | 리뷰 근거의 head 결합 (Q4) | 리뷰 본문이 CI 성공·테스트 수를 인용함 | 검토한 head·base와 인용한 CI build의 head를 밝힘. head가 다르거나 밝히지 않은 주장은 판정 근거로 쓰지 않고 미확인으로 다룸 | REVIEW §10, REVIEW_ROUND §4 |
| R-009 | 기존 계약 보존 | 리뷰 라운드 위임·통과 head 동결·임계값 | 바뀌지 않음. 추가 PR 댓글이나 ID 예약 댓글을 요구하지 않음 | 해당 절 diff 대조 |

### 2.2 대안과 선택 이유

**T-030 기록 시점**

| 안 | 내용 | 효과 | 판단 |
|---|---|---|---|
| A0 | 현행 유지 | 상태 지연과 기록 전용 commit이 남음 | 기각 |
| A1 | merge 결합 서술만 도입(§1.4) | 상태 지연은 없어지지만, 자기 CI·리뷰 결과를 적는 commit과 재검증 고리는 남음 | 부분 |
| **A2** | **A1 + PR 원장(R-003)** | 상태 지연과 기록 전용 commit이 모두 없어짐. 최종 head finding의 인계만 한 번 남음(R-004) | **권고** |
| A3 | merge 뒤 봇·사람이 기록 commit | 리뷰·필수 CI를 우회하고 §9와 `main` 보호 방향에 반하며 CI 제품에 종속됨 | 기각 |

예외 기록 위치는 두 안을 비교했습니다. PR 본문에 요청 근거를 남기는 안(E1)을 권고합니다. 근거 없이 허용하는 안(E2)은 리뷰어가 정당한 예외와 위반을 구분할 수 없어 기각했습니다.

**T-014 finding ID**

| 안 | 내용 | 판단 |
|---|---|---|
| B0 | 현행: 리뷰어가 기존 리뷰를 읽고 조율 | 동시에 도는 리뷰어는 서로를 볼 수 없어 #28·#29가 재발할 수 있음. 기각 |
| **B1** | **등록 슬롯 ID + 미등록 리뷰어의 `<게시 식별자>/<항목 번호>` + 대표 ID(R-006·R-007)** | 등록 목록, 플랫폼 게시 식별자, 게시물 안 항목 번호가 유일성을 보장하므로 조율이 필요 없고, 추가 댓글도 필요 없음. **권고** |
| B2 | ID 예약 댓글 | 경쟁 상태가 남고, 라운드 위임에서 금지한 추가 댓글이 필요함. 기각 |
| B3 | 실행 주체만 ID를 부여 | 리뷰어끼리 인용하거나 스레드를 맞출 기준이 사라짐. 기각 |

**리뷰 근거**

현행(C0)은 finding의 head만 정렬합니다. C1은 리뷰 본문의 CI·검증 주장에도 head를 결합하도록 요구합니다(R-008). 적은 문서 변경으로 PR #53 같은 혼동을 막을 수 있어 **C1을 권고**합니다.

### 2.3 설계와 계약

**기록 시점 (locale `DOCS_GUIDE.md` "로컬 Git과 병렬 브랜치", `02-TODO.md` 운영 규칙)**

- 통합 대상의 TODO·PLAN은 그 revision에 통합된 계획과 결과라는 기존 정의를 유지합니다. 여기에 "작업 branch의 문서는 그 branch가 통합되는 시점의 상태를 적을 수 있다"는 해석을 더합니다(R-001).
- 결합 서술이 가정할 수 있는 조건은 자기 최종 head의 통합 하나뿐입니다. merge 이후 사건은 R-002의 예외로만 적습니다.
- `Completed` 규칙은 다음과 같이 바꿉니다. "통합 확인 뒤"라는 조건을 "통합과 동시에 참이 되는 결합 서술 또는 통합 확인 뒤"로 넓힙니다. release·지원 검증처럼 merge 이후에 일어나는 완료는 해당 작업이 확인한 뒤에만 적습니다.
- PR 원장(R-003): 자기 head의 CI build, 리뷰 판정·댓글 ID, merge SHA는 PR에 두고 문서에는 PR 참조만 둡니다. 이전 version의 판정이나 인계를 기록하는 것은 실제 수정이 있는 commit에서만 합니다.

**리뷰 라운드 (`REVIEW_ROUND.md`)**

- **§6:** 통과 head 동결과 기록 commit 금지는 그대로 둡니다. 완료 서술은 통과 전 최종 수정에 결합 서술로 포함할 수 있다고 적고, 포함하지 못한 경우에만 §9로 인계합니다.
- **§9:** 인계 대상을 "최종 head 리뷰에서 새로 나온 finding과 결합 서술로 담지 못한 기록"으로 좁힙니다.
- **§2.1:** 리뷰어 표에 `슬롯` 열을 추가합니다. 라벨은 모델·도구가 바뀌어도 유지되는 역할 라벨이며, 예시로 `A`·`B`·`owner`를 둡니다. 한 라벨은 표에 한 번만 둡니다. 모델이 바뀌면 라벨이 아니라 표의 리뷰어 칸을 고칩니다.
- **§4:** "중복 통합"에 대표 ID 규칙(R-007)을, "head 정렬"에 CI·검증 주장의 head 결합(R-008)을 추가합니다.
- **§7:** 판정 표에 `원 ID` 열을 추가합니다. 원 ID는 슬롯 ID이고, 슬롯 ID가 없으면 `<플랫폼 게시 식별자>/<항목 번호>`입니다. 인계 목록에는 대표 ID와 원 ID를 모두 적습니다.

**리뷰 정책 (`REVIEW.md`, `.cursor/BUGBOT.md`)**

- **§7 Finding Requirements:** 게시하는 finding에 ID를 붙일 때는 대상 식별자와 자기 슬롯을 포함해 같은 대상의 다른 리뷰어와 겹치지 않게 합니다. 대상 식별자의 형식은 프로젝트가 정하며, 이 저장소의 root 문서는 `C<PR>-<슬롯>-<nnn>`를 예로 둡니다. 슬롯은 리뷰어 목록에 등록된 것만 씁니다. 등록되지 않은 리뷰어는 ID를 발급하지 않고, 게시물 안의 finding마다 항목 번호를 붙여 `<플랫폼 게시 식별자>/<항목 번호>`로 가리키게 합니다. 변경 폴더 ID를 `<변경-ID>/R-001`로 가리키는 기존 규칙과 같은 방식입니다.
- **§10 Review Conclusion:** 결론에 검토한 head·base를 적고, 인용한 CI·검증 결과마다 build와 그 head를 적습니다. 읽지 못했거나 아직 끝나지 않은 결과는 그렇다고 적습니다.
- **§5 Tests and Documentation:** 문서 변경 리뷰에서 R-002 위반(요청 근거 없는 merge 이후 서술)을 점검합니다.
- Bugbot은 BUGBOT.md만 읽으므로 ID·근거 규칙을 같은 문장으로 복제합니다. WATCHDOG은 REVIEW.md를 import하므로 바꾸지 않습니다.

### 2.4 상위 설계에 미치는 영향

- **D-009:** locale guide를 정본으로 두고 root를 addendum으로 두는 소유권은 유지합니다. 이 변경은 그 정본 문서의 기록·리뷰 계약을 확장합니다.
- **REVIEW_ROUND:** 위임 범위와 임계값은 대체하지 않습니다.
- **T-033:** TODO 완료 이력 보관은 새 규칙을 적용한 TODO 구조에서 진행합니다.

### 2.5 위험·호환성·rollback

- **적용 프로젝트:** locale 문서는 `adopt` report의 merge·decide 대상이므로 자동으로 덮어쓰이지 않습니다. 기존 TODO 기록은 소급해서 바꾸지 않습니다.
- **규칙 변화의 성격:** 제약을 완화하는 부분(R-001)과 강화하는 부분(R-003·R-006·R-008)이 함께 있습니다. release notes에 두 가지를 구분해 적습니다.
- **위험 1:** 결합 서술을 merge 이후 사건으로 확대 해석할 수 있습니다. 완화책은 R-002 점검 항목과 리뷰 finding입니다.
- **위험 2:** 등록되지 않은 리뷰어가 있을 수 있습니다. 이들은 슬롯 ID를 발급하지 않고 `<플랫폼 게시 식별자>/<항목 번호>`로 finding을 가리키므로, 한 게시물에 finding이 여럿이어도 겹치지 않습니다. 대표 ID는 원 ID 중에서 고르므로 슬롯이 없어도 인계할 수 있습니다(C55-001, Codex의 C55-002, #56 version 4 리뷰).
- **rollback:** 다음 release에서 문서를 되돌리면 됩니다. 데이터나 코드 migration은 없습니다.

### 2.6 완료 조건과 실행 순서

1. **이 설계 PR:** Q1~Q4를 합의한 뒤 Status를 `Accepted`로 바꾸고, PROJECT §8에 두 결정을 등재합니다.
2. **구현 PR:**
   - en·ko locale 문서, BUGBOT, root maintainer 사본을 같은 문장으로 고칩니다.
   - 문서 검사, stable locale, 문서·locale 회귀, en·ko export와 artifact 검사를 통과해야 합니다.
   - 새 규칙은 base 정책으로 리뷰하므로 구현 PR 자신에게는 적용하지 않습니다. 첫 적용은 그 다음 PR입니다.
   - T-033(TODO 완료 이력 보관)은 같은 PR에 포함하거나, diff가 커지면 바로 다음 PR로 나눕니다.
3. **release(T-034):** T-013의 guide 변경과 함께 한 release로 공개합니다. D-007의 candidate·published 단계를 따릅니다.
4. **완료 기준:** 구현 통합과 release 공개를 구분합니다. 이 설계의 완료는 구현 PR 통합이고, 공개는 T-034가 소유합니다.

## 3. 변경 기록

- 2026-09-30: 초안 작성. §1.4는 2026-09-29 사용자 결정이고, Q1~Q4는 합의 전입니다.
- 2026-09-30: Chae Sangwon, 2026-09-30 선택 응답 — PR #55 version 1 head `150ebc94ba4d4518b75464d299cdd7887f305668`의 Q1 “채택”, Q2 “PR 본문”, Q3 “슬롯 ID+대표 ID”, Q4 “채택”. Status를 `Accepted`로 바꾸고 D-013·D-014를 PROJECT §8에 등재했습니다. 요구사항·설계 본문은 바꾸지 않았습니다.
- 2026-09-30: PR #55 version 2 리뷰의 **C55-001**(Codex review `rev_01m3r4c4fqegmvmv22trdc8pw9`, P2·confidence 0.94·blocking=true; 사용자 review `rev_01m3r4bzxxez4aq8cfmvtdmye1`의 후속 댓글 `cmt_01m3r4dfysfeh9e8kvew23s507`가 같은 조건을 재현하고 그 approve의 누락을 정정)을 수용했습니다. 미등록 리뷰어가 스스로 라벨을 밝히는 fallback은 두 리뷰어가 같은 라벨을 고르면 ID가 겹칩니다. 그래서 R-006·R-007·§2.2 B1·§2.3·§2.5를 다음과 같이 고쳤습니다: 등록 슬롯만 ID를 발급하고, 미등록 리뷰어는 플랫폼 식별자로 가리키며, 필요하면 종합하는 쪽이 대표 ID를 발급합니다. Q3의 선택(B1: 슬롯 ID와 대표 ID)과 다른 결정은 유지하며, 사용자의 2026-09-30 "리뷰 확인하고 결정해 봐" 위임에 따라 보완했습니다.
- 2026-09-30: PR #55 version 3 리뷰를 반영했습니다. 두 리뷰가 서로 다른 finding에 같은 `C55-002`를 붙였으므로 게시 식별자로 구분합니다.
  - Codex review `rev_01m3rd1vm9exsa8ha5qvfpgd2f`의 C55-002(P2·confidence 0.96·blocking=true): 한 리뷰 본문의 여러 finding이 플랫폼 식별자만으로 구별되지 않습니다. 미등록 리뷰어의 원 ID를 `<플랫폼 게시 식별자>/<항목 번호>`로 정의하고, R-006 검증에 한 본문 두 finding 시나리오를 추가했습니다.
  - 사용자 review `rev_01m3rcyqd7fh99b3f86sgtp9db`의 C55-002(P3): 재현 댓글의 작성자 표기를 정정했습니다.
  - 같은 review의 C55-003(P3): §2.3의 `REVIEW_ROUND` §7 목록에 원 ID 형식과 인계를 반영했습니다.
  - Q3 선택(B1)과 다른 결정은 유지하며, 사용자의 "리뷰 확인하고 결정해 봐" 위임에 따라 보완했습니다.
- 2026-09-30: 구현하면서 두 가지 위치를 정정했습니다. 요구사항 내용은 같습니다.
  - R-002 점검 항목은 [REVIEW.md](../../REVIEW.md) §7이 아니라 §5 Tests and Documentation에 둡니다. §7은 finding의 필수 항목 목록이고, 리뷰 점검 항목은 §5가 소유합니다.
  - 대표 ID를 발급하는 실행 주체·PR 작성자의 슬롯은 §2.1 표의 리뷰어 행이 아니라 표 아래 한 줄로 적습니다. 리뷰어 정족수 집계에 섞이지 않게 하기 위해서입니다.
- 2026-09-30: 구현 PR #56 version 1 리뷰를 반영했습니다. 두 리뷰가 서로 다른 finding에 같은 `C56-001`을 붙였으므로 게시 식별자로 구분하고, 이 사례를 §1.1 근거에 추가했습니다.
  - 사용자 review `rev_01m3rm714afajs2y14gqnewvdp`의 C56-001(P2): #55 version 4 사용자 계정 review `rev_01m3rh5yptfmrt3v5ncg5bzf11`를 본문 없음으로 잘못 기록했습니다. 그 review에는 C55-004(P3, §1.1 근거 순서)와 C55-005(P3, 한 건짜리 게시물의 원 ID 두 형식)가 있습니다. TODO 기록을 정정하고, C55-004는 §1.1 순서를 바로잡아 해소했습니다.
  - 같은 review의 C56-002(P3)와 C55-005: 한 건짜리 게시물도 원 ID를 `/1`로 두고, 식별자만 쓴 인용은 `/1`과 같다고 R-006·`REVIEW.md`·BUGBOT에 맞췄습니다.
  - Codex review `rev_01m3rmcrpgebtsdrpph29rrkz3`의 C56-001(P2): PR 없는 `reviewers = self` 리뷰에는 원 ID를 만들 게시물이 없습니다. 세션 종료 보고를 게시물로 보고 `<branch>@<마지막 리뷰 head 12자리>/<항목 번호>`를 원 ID로 쓰도록 R-006·[REVIEW_ROUND.md](../../REVIEW_ROUND.md) §7·[REVIEW.md](../../REVIEW.md) §7에 정의했습니다.
  - Q3 선택(B1)과 다른 결정은 유지하며, 사용자의 위임에 따른 보완입니다.
- 2026-10-01: 구현 PR #56 version 2 리뷰를 반영했습니다. 사용자 review `rev_01m3tmj3nyf7ct24jt2rarmx4g`의 C56-003(P3·confidence 0.82·blocking=true)과 Codex review `rev_01m3tn29k9fpdt4875a2xz1799`의 Finding 1(새 규칙으로는 `rev_01m3tn29k9fpdt4875a2xz1799/1`, P2·confidence 0.97·blocking=true)은 같은 원인입니다. 로컬 보고 식별자 `<branch>@<head>`는 같은 head를 다시 리뷰하거나 미커밋 변경을 리뷰할 때, 또는 다른 세션이 같은 head를 리뷰할 때 보고마다 유일하지 않습니다. 보고 식별자에 보고를 만든 UTC 시각(초 단위)을 넣어 보고마다 유일하게 하고, 인계받은 원 ID는 유지하도록 R-006과 en·ko·root [REVIEW_ROUND.md](../../REVIEW_ROUND.md) §7을 고쳤습니다. 번호를 이어 쓰는 대안은 이전 보고를 알아야 해서 택하지 않았습니다. 다른 결정은 유지하며, 사용자의 위임에 따른 보완입니다.
- 2026-10-01: 구현 PR #56 version 3 리뷰를 반영했습니다. 사용자 review `rev_01m3ttw7zxfgktgpr7p7g8f7xs`는 finding이 없었습니다. Codex review `rev_01m3tv6t2pfk4s6v7e5mxn1sc8`의 Finding 1(새 규칙으로는 `rev_01m3tv6t2pfk4s6v7e5mxn1sc8/1`, P2·confidence 0.98·blocking=true)은 두 로컬 세션이 같은 초에 보고를 만들면 시각만으로는 보고를 구별하지 못한다는 지적입니다. 시각을 더 잘게 나누는 대신 보고마다 새로 만드는 무작위 16진수 8자리를 보고 식별자에 붙여 R-006과 en·ko·root [REVIEW_ROUND.md](../../REVIEW_ROUND.md) §7을 고쳤습니다. 다른 결정은 유지하며, 사용자의 위임에 따른 보완입니다.
- 2026-10-01: 구현 PR #56 version 4 리뷰를 반영했습니다. 사용자 review `rev_01m3tzb8ndfmva74y4r1209kbc`는 finding이 없었습니다. Codex review `rev_01m3tzqb7re6yv8r62artz61wp`의 Finding 1(새 규칙으로는 `rev_01m3tzqb7re6yv8r62artz61wp/1`, P2·confidence 0.96·blocking=true)은 다음 경우를 지적했습니다: 슬롯이 하나도 없는 `reviewers = self` 인계는 대표 ID를 요구받지만, 대표 ID를 발급할 실행 주체 슬롯이 없습니다. fallback 단계를 더 붙이는 대신 발급 단계를 없앴습니다. 대표 ID는 원 ID 중 가장 먼저 게시된 슬롯 ID, 없으면 가장 먼저 게시된 원 ID이며, 실행 주체·작성자 슬롯 개념을 삭제했습니다(앞의 표 아래 한 줄 정정은 대체됨). R-007, §2.3, §2.5, D-014, en·ko·root [REVIEW_ROUND.md](../../REVIEW_ROUND.md) §2.1·§4·§7을 맞췄습니다. Q3에서 고른 "가장 먼저 게시된 ID를 대표 ID로"에 더 가깝습니다.
- 2026-10-01: 구현 PR #56 version 5 리뷰를 반영했습니다.
  - 사용자 review `rev_01m3v5sjwrfkrvtnyvk26sk2v9`의 C56-004(P3·confidence 0.8·blocking=true): 같은 시각의 원 ID 사이에서 대표 ID를 정할 기준이 없습니다. 원 ID 문자열의 사전순으로 정하도록 R-007과 §4를 고쳤습니다.
  - Codex review `rev_01m3v6kv4dfmm9jphxn12kmzmk`의 Finding 1(새 규칙으로는 `…/1`, P2·confidence 0.96·blocking=true): 같은 게시물을 head마다 덮어쓰는 sticky 리뷰어는 head가 달라도 원 ID가 재사용됩니다. sticky 게시물의 원 ID에 그 내용이 다룬 head 앞 12자리를 붙이도록 R-006, [REVIEW.md](../../REVIEW.md) §7, BUGBOT, en·ko·root [REVIEW_ROUND.md](../../REVIEW_ROUND.md) §7을 고쳤습니다.
  - 다른 결정은 유지하며, 사용자의 위임에 따른 보완입니다.
- 2026-10-01: PR #56은 version 7 head `e4a9b58`로 통합됐습니다(merge `379c0f0`). 그 Cursor(A) 리뷰 `rev_01m3v7hw4ze7vsj60j3f1dhngg`의 C56-005(P3·confidence 0.86·blocking=true)를 T-033 PR에서 해소했습니다. sticky 게시물의 짧은 인용도 `@<head 12자리>/1`과 같고, head 없는 인용은 원 ID로 쓰지 않습니다. R-006과 en·ko·root [REVIEW.md](../../REVIEW.md) §7을 고쳤습니다.
