import random
from datetime import datetime, timedelta

import streamlit as st

# ──────────────────────────────────────────────
# 기본 설정
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="PRSV | Preservative Recommendation",
    page_icon="🧪",
    layout="centered",
)

FORM_LABELS = {
    "ow": "O/W 유화 (로션·크림)",
    "wo": "W/O 유화 (선크림)",
    "anhydrous": "무수/오일 (밤·오일)",
    "powder": "파우더/무수분말",
    "surfactant": "계면활성제형 (클렌저·샴푸)",
    "gel": "고점도 겔/하이드로겔",
}

PH_LABELS = {
    "lt4": "4 미만",
    "4to5": "4 ~ 5",
    "5to6": "5 ~ 6",
    "gt6": "6 초과",
    "na": "해당없음 (무수 제형)",
}

NAME_POOL = [
    "김민지", "이서연", "박준호", "최유진", "정하늘", "강도윤", "윤소율",
    "임재현", "한지우", "송예은", "조현우", "배수아", "오민석", "신아름",
    "권태양", "문지훈", "백서현", "황준영", "서지안", "고은채",
]

# ──────────────────────────────────────────────
# 추천 로직 (index.html의 getRecommendations를 그대로 이식)
# ──────────────────────────────────────────────
def get_recommendations(form_type, ph_range, nonionic, bioburden, packaging):
    recs = []
    warnings = []

    if form_type in ("anhydrous", "powder") or ph_range == "na":
        recs.append({
            "name": "방부제 불필요 (산화방지제 중심 관리)",
            "reason": "수분활성도(Aw)가 낮아 미생물 증식 조건이 성립하지 않는 무수 제형입니다. 방부보다 산화 안정성 관리가 우선입니다.",
            "limit": "해당없음",
            "source": "초안 · 문헌 검증 예정",
        })
    elif form_type == "ow":
        recs.append({
            "name": "페녹시에탄올 + 에틸헥실글리세린",
            "reason": "O/W 유화에서 광범위 항균 스펙트럼을 갖는 표준 조합입니다.",
            "limit": "페녹시에탄올 ⚠1.0% 이하 (검증 전 잠정치)",
            "source": "초안 · 문헌 검증 예정",
        })
        recs.append({
            "name": "카프릴릴글라이콜 + 1,2-헥산다이올 + 에틸헥실글리세린",
            "reason": "파라벤 프리 대안이 필요한 O/W 제형에 적합한 글리콜계 조합입니다.",
            "limit": "⚠검증 전 잠정치",
            "source": "초안 · 문헌 검증 예정",
        })
        if nonionic == "yes":
            warnings.append("비이온 계면활성제가 포함되어 있어 파라벤류는 미셀화로 효력이 저하될 수 있습니다. 파라벤 단독 사용을 지양하세요.")
    elif form_type == "wo":
        recs.append({
            "name": "페녹시에탄올 (단독 또는 클로르페네신 병용)",
            "reason": "W/O 유화는 수상이 분산상이므로, 양쪽성으로 분배되는 방부제가 수상까지 충분히 도달하도록 선택해야 합니다.",
            "limit": "페녹시에탄올 ⚠1.0% 이하 (검증 전 잠정치)",
            "source": "초안 · 문헌 검증 예정",
        })
    elif form_type == "surfactant":
        recs.append({
            "name": "벤조산나트륨 + 살리실산 (또는 DMDM 하이단토인)",
            "reason": "계면활성제형 제품은 비이온 계면활성제에 의한 파라벤 미셀화 문제가 흔해 파라벤 대신 유기산계/포름알데하이드 방출체를 우선 검토합니다.",
            "limit": "⚠검증 전 잠정치",
            "source": "초안 · 문헌 검증 예정",
        })
        warnings.append("파라벤류는 이 제형에서 효력 저하 가능성이 높아 우선순위에서 제외했습니다.")
    elif form_type == "gel":
        recs.append({
            "name": "벤질알코올 + 살리실산 + 소르빈산 + 데하이드로아세트산 (멀티산 시스템)",
            "reason": "고점도 겔은 방부제 확산이 느려질 수 있어 다중 유기산 조합으로 스펙트럼을 보강합니다.",
            "limit": "⚠검증 전 잠정치",
            "source": "초안 · 문헌 검증 예정",
        })

    if ph_range == "lt4":
        recs.insert(0, {
            "name": "벤조산나트륨 + 소르빈산칼륨 (+ EDTA 병용 권장)",
            "reason": "pH 4 미만에서는 유기산이 비해리 형태로 존재해 항균 효력이 극대화됩니다. EDTA 병용 시 그람음성균(녹농균 등) 대응이 보강됩니다.",
            "limit": "⚠검증 전 잠정치",
            "source": "초안 · 문헌 검증 예정",
        })
    elif ph_range == "gt6" and form_type not in ("anhydrous", "powder"):
        warnings.append("pH 6 초과 구간은 유기산계 방부제의 비해리형 비율이 낮아져 단독 사용 시 효력이 부족할 수 있습니다.")

    if bioburden == "yes":
        warnings.append("점증제/천연추출물/단백질 함유로 오염원(바이오버든) 유입 가능성이 높습니다. 광범위 스펙트럼 조합을 우선 고려하세요.")
    if packaging == "open":
        warnings.append("오픈형 포장은 반복 접촉 오염 위험이 높아 에어리스 대비 방부 시스템을 더 보수적으로 설계하는 것을 권장합니다.")

    return recs[:3], warnings


def format_date(ts: datetime) -> str:
    days = (datetime.now() - ts).days
    if days <= 0:
        return "오늘"
    if days == 1:
        return "어제"
    if days < 30:
        return f"{days}일 전"
    return ts.strftime("%Y.%m.%d")


# ──────────────────────────────────────────────
# session_state 초기화 (기록은 세션 단위 저장 · 사용자 간 공유 안 됨)
# 주의: 실제 브라우저 localStorage와 달리, 브라우저 탭을 새로고침하면
# 세션이 새로 시작되어 기록이 초기화됩니다.
# ──────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ──────────────────────────────────────────────
# 상단
# ──────────────────────────────────────────────
top_col1, top_col2 = st.columns([3, 2])
with top_col1:
    st.markdown("### 🧪 PRSV")
    st.caption("코스맥스 미생물연구팀 · 사내 공유용")

tab_main, tab_history = st.tabs(["🔬 추천받기", "📋 사용 기록"])

# ──────────────────────────────────────────────
# 메인 탭
# ──────────────────────────────────────────────
with tab_main:
    st.title("Preservative Recommendation")
    st.write("제형 특성을 선택하면 근거 기반 방부제 후보를 배합 한도와 함께 추천합니다.")
    st.warning("⚠ 초안 버전 · 문헌 검증 전", icon="⚠️")

    st.subheader("1. 제형 종류")
    form_type = st.radio(
        "제형을 선택하세요",
        options=list(FORM_LABELS.keys()),
        format_func=lambda k: FORM_LABELS[k],
        horizontal=True,
        label_visibility="collapsed",
    )

    st.divider()

    st.subheader("2. 세부 조건 입력")
    name = st.text_input("이름 (기록 페이지에 표시됩니다)", placeholder="예: 김민지 연구원")

    ph_range = st.selectbox(
        "pH 범위",
        options=list(PH_LABELS.keys()),
        index=1,
        format_func=lambda k: PH_LABELS[k],
    )

    nonionic = st.radio(
        "비이온 계면활성제 포함 여부 (폴리소르베이트 등)",
        options=["no", "yes"],
        format_func=lambda v: "포함" if v == "yes" else "미포함",
        horizontal=True,
    )

    with st.expander("선택 항목 더보기"):
        bioburden = st.radio(
            "점증제 / 천연추출물 / 단백질 포함 여부 (바이오버든 증가 요인)",
            options=["no", "yes"],
            format_func=lambda v: "포함" if v == "yes" else "미포함",
            horizontal=True,
        )
        packaging = st.radio(
            "포장 형태",
            options=["airless", "open"],
            format_func=lambda v: "에어리스" if v == "airless" else "오픈형",
            horizontal=True,
        )

    submitted = st.button("방부제 추천받기", type="primary", use_container_width=True)

    if submitted:
        recs, warnings = get_recommendations(form_type, ph_range, nonionic, bioburden, packaging)
        user = name.strip() if name.strip() else "익명"

        st.session_state.history.insert(0, {
            "user": user,
            "form_type": form_type,
            "ph_range": ph_range,
            "result": recs[0]["name"] if recs else "추천 결과 없음",
            "ts": datetime.now(),
        })

        st.success(f"✓ **{user}**님의 기록이 저장되었습니다 · '📋 사용 기록' 탭에서 확인하세요")

        for w in warnings:
            st.warning(w, icon="⚠️")

        for i, r in enumerate(recs, start=1):
            with st.container(border=True):
                st.caption(f"추천 {i}순위")
                st.markdown(f"#### {r['name']}")
                st.markdown(f"**추천 이유**  \n{r['reason']}")
                st.markdown(f"**배합 한도**  \n{r['limit']}")
                st.markdown(f"**출처**  \n{r['source']}")

    st.divider()
    st.caption(
        "본 추천은 화장품과학 표준 문헌 기반 **초안 규칙**이며 개별 논문·규제 인용은 아직 최종 검증되지 않았습니다. "
        "실제 배합 전 반드시 최신 규제(한국 화장품안전기준, EU 1223/2009 Annex V) 원문을 재확인하고, "
        "**방부력시험(Challenge Test)**으로 최종 검증하시기 바랍니다."
    )

# ──────────────────────────────────────────────
# 기록 탭
# ──────────────────────────────────────────────
with tab_history:
    st.title("사용 기록")
    st.caption(f"{len(st.session_state.history)}건의 기록이 누적되어 있습니다.")
    st.info(
        "⚠ 이 기록은 현재 브라우저 세션에만 저장됩니다. 다른 사람의 컴퓨터나 다른 세션과는 공유되지 않아요 — "
        "탭을 닫거나 앱을 새로고침하면 초기화됩니다. 여러 사용자가 함께 보려면 서버/DB 연동이 필요합니다."
    )

    if not st.session_state.history:
        st.write("아직 기록이 없습니다.")
    else:
        for r in st.session_state.history:
            with st.container(border=True):
                c1, c2 = st.columns([3, 2])
                with c1:
                    st.markdown(f"**{r['user']}**")
                    st.caption(
                        f"{format_date(r['ts'])} · {FORM_LABELS[r['form_type']]} · {PH_LABELS[r['ph_range']]}"
                    )
                with c2:
                    st.write(r["result"])

        if st.button("기록 전체 삭제"):
            st.session_state.history = []
            st.rerun()
