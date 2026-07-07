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
# 상단 헤더 일러스트 (파스텔 플랫 스타일 화장품 용기)
# ──────────────────────────────────────────────
HEADER_CSS = """
<style>
.prsv-header {
    background: linear-gradient(135deg, #fef6ea 0%, #eaf6f0 55%, #eaf1fb 100%);
    border-radius: 20px;
    padding: 20px 28px 12px 28px;
    margin-bottom: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.prsv-badge {
    display: inline-block;
    background: #ff6f91;
    color: white;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.04em;
    padding: 2px 10px;
    border-radius: 999px;
    margin-bottom: 6px;
}
.prsv-title {
    margin: 0;
    font-size: 28px;
    font-weight: 800;
    color: #2f3b3a;
}
.prsv-caption {
    margin: 2px 0 0 0;
    font-size: 13px;
    color: #6b7573;
}
.prsv-illustration {
    width: 100%;
    margin-top: 14px;
    filter: drop-shadow(0 3px 5px rgba(0,0,0,0.12));
}
.prsv-illustration svg { display: block; width: 100%; height: auto; }
@media (max-width: 640px) {
    .prsv-illustration { margin-top: 8px; }
}
</style>
"""

HEADER_ILLUSTRATION_SVG = """
<svg viewBox="0 0 820 100" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
  <g stroke="#ffffff" stroke-width="5" stroke-linejoin="round" paint-order="stroke">
    <g transform="rotate(-6 40 55)">
      <rect x="18" y="34" width="36" height="46" rx="10" fill="#f4b860"/>
      <rect x="28" y="18" width="14" height="18" rx="4" fill="#4a3728"/>
      <rect x="33" y="10" width="4" height="10" fill="#4a3728"/>
      <rect x="24" y="52" width="22" height="14" rx="3" fill="#fff8ec" opacity="0.85" stroke="none"/>
    </g>
    <g transform="rotate(4 145 60)">
      <rect x="120" y="28" width="46" height="18" rx="7" fill="#3a3a3a"/>
      <rect x="116" y="44" width="54" height="38" rx="14" fill="#fbeee0"/>
      <ellipse cx="143" cy="63" rx="14" ry="8" fill="#f0dcbd" stroke="none"/>
    </g>
    <g transform="rotate(-5 240 55)">
      <rect x="224" y="10" width="30" height="20" rx="4" fill="#e7e1ea"/>
      <path d="M232 30 L246 30 L250 84 Q239 90 230 84 Z" fill="#f2eaf6"/>
      <rect x="220" y="6" width="38" height="8" rx="4" fill="#e79ab8"/>
    </g>
    <g transform="rotate(5 335 55)">
      <rect x="313" y="14" width="26" height="12" rx="5" fill="#2f5c4d"/>
      <rect x="331" y="18" width="12" height="6" rx="2" fill="#2f5c4d"/>
      <rect x="321" y="24" width="10" height="12" fill="#4f8a76"/>
      <rect x="309" y="34" width="34" height="46" rx="9" fill="#8fcab2"/>
    </g>
    <g transform="rotate(-4 430 55)">
      <rect x="410" y="16" width="36" height="52" rx="16" fill="#9bd3ab"/>
      <rect x="420" y="66" width="16" height="12" fill="#4a7a56"/>
      <ellipse cx="422" cy="30" rx="6" ry="3" fill="#ffffff" opacity="0.5" stroke="none"/>
    </g>
    <g transform="rotate(6 525 58)">
      <rect x="500" y="46" width="50" height="34" rx="17" fill="#f7c9a3"/>
      <rect x="514" y="30" width="22" height="18" rx="6" fill="#e08a4f"/>
      <rect x="519" y="20" width="12" height="12" rx="4" fill="#e08a4f"/>
    </g>
    <g transform="rotate(-6 625 55)">
      <rect x="600" y="24" width="20" height="56" rx="10" fill="#e8677e"/>
      <rect x="620" y="24" width="20" height="56" rx="10" fill="#f6a6b6"/>
      <rect x="605" y="14" width="30" height="12" rx="6" fill="#3a3a3a"/>
    </g>
    <g transform="rotate(4 715 60)">
      <ellipse cx="715" cy="76" rx="30" ry="12" fill="#fbeee0"/>
      <rect x="695" y="46" width="40" height="30" rx="14" fill="#fff6ec"/>
    </g>
    <g transform="rotate(-3 800 50)">
      <rect x="784" y="30" width="30" height="42" rx="10" fill="#a9d8e6"/>
      <rect x="792" y="20" width="14" height="12" rx="3" fill="#6fb3c9" stroke="none"/>
    </g>
  </g>
  <circle cx="95" cy="20" r="4" fill="#ff9fb4"/>
  <circle cx="200" cy="86" r="3" fill="#8fd3e8"/>
  <circle cx="285" cy="18" r="3" fill="#ffd76a"/>
  <circle cx="390" cy="88" r="4" fill="#c9a7e0"/>
  <circle cx="470" cy="20" r="3" fill="#8fd3e8"/>
  <circle cx="580" cy="90" r="3" fill="#ff9fb4"/>
  <circle cx="670" cy="22" r="4" fill="#ffd76a"/>
  <circle cx="760" cy="90" r="3" fill="#a9d8e6"/>
</svg>
"""

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
st.markdown(HEADER_CSS, unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="prsv-header">
        <div class="prsv-header-text">
            <div class="prsv-badge">BETA</div>
            <h1 class="prsv-title">🧪 PRSV</h1>
            <p class="prsv-caption">코스맥스 미생물연구팀 · 사내 공유용</p>
        </div>
        <div class="prsv-illustration">{HEADER_ILLUSTRATION_SVG}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

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
