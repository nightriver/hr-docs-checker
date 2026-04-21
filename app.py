import streamlit as st
import base64, os
from documents import build_documents
from instructions import INSTRUCTIONS
from exporters import build_txt, build_pdf
from styles import CARD_CSS

st.set_page_config(
    page_title="HR-опитувальник документів | Smart Solutions",
    page_icon="📋",
    layout="centered",
)

TOTAL_STEPS = 6

DEFAULT_ANSWERS = {
    "military_liable": None,
    "labor_book": None,
    "education": None,
    "children_u18": None,
    "disability_status": None,
    "extra_statuses": [],
}

if "step" not in st.session_state:
    st.session_state.step = 1
if "answers" not in st.session_state:
    st.session_state.answers = DEFAULT_ANSWERS.copy()

st.markdown(CARD_CSS, unsafe_allow_html=True)


# ─── Callbacks ────────────────────────────────────────────────
def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

def reset_app():
    st.session_state.clear()


# ─── Логотип ──────────────────────────────────────────────────
_logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.svg")
try:
    with open(_logo_path, "rb") as _f:
        _logo_b64 = base64.b64encode(_f.read()).decode("utf-8")
    _logo_html = f'<img src="data:image/svg+xml;base64,{_logo_b64}" style="height:48px;">'
except Exception:
    _logo_html = '<span style="font-weight:800;font-size:22px;color:#1A1A1A;">Smart<span style="color:#E8312A;">Solutions</span></span>'

st.markdown(f"""
<div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;">
    {_logo_html}
    <div style="font-size:15px;color:#555;margin-left:4px;">HR-опитувальник документів</div>
</div>
<hr style="border:none;border-top:2px solid #FFD100;margin-bottom:20px;">
""", unsafe_allow_html=True)


# ─── Рендер картки документа ──────────────────────────────────
def render_doc_card(doc: dict):
    icon = "🟢" if doc["important"] else "🔵"
    st.markdown(f"""
        <div class="doc-card">
            <div class="doc-title">{icon} {doc["title"]}</div>
            <div class="doc-details">{doc["details"]}</div>
            <div class="doc-format">📄 Формат: {doc["format"]}</div>
        </div>
    """, unsafe_allow_html=True)

    if doc.get("hr_note"):
        st.caption(f"ℹ️ {doc['hr_note']}")

    key = doc.get("instruction_key")
    if key and key in INSTRUCTIONS:
        with st.expander("📋 Як отримати цей документ", expanded=False):
            for i, step_text in enumerate(INSTRUCTIONS[key], start=1):
                st.markdown(f"{i}. {step_text}")


# ─── Кроки опитувальника ──────────────────────────────────────
step = st.session_state.step

if step <= TOTAL_STEPS:
    st.progress(step / TOTAL_STEPS)
    st.caption(f"Крок {step} з {TOTAL_STEPS}")
    st.markdown("---")

# ── Крок 1 ──
if step == 1:
    st.subheader("Чи є ви військовозобов'язаною особою?")
    st.caption(
        "Чоловіки 18–60 років підлягають обов'язковому військовому обліку. "
        "Жінки — якщо мають медичну або фармацевтичну освіту, або добровільно проходять / проходили службу."
    )
    val = st.radio(
        "Оберіть варіант:",
        ["Так", "Ні"],
        index=["Так", "Ні"].index(st.session_state.answers["military_liable"])
        if st.session_state.answers["military_liable"] in ["Так", "Ні"] else 0,
        key="r_military",
        label_visibility="collapsed",
    )
    st.session_state.answers["military_liable"] = val

# ── Крок 2 ──
elif step == 2:
    st.subheader("Яка у вас ситуація з трудовою книжкою?")
    options2 = ["Є трудова книжка", "Це моє перше офіційне працевлаштування"]
    val = st.radio(
        "Оберіть варіант:",
        options2,
        index=options2.index(st.session_state.answers["labor_book"])
        if st.session_state.answers["labor_book"] in options2 else 0,
        key="r_labor",
        label_visibility="collapsed",
    )
    st.session_state.answers["labor_book"] = val

# ── Крок 3 ──
elif step == 3:
    st.subheader("Який у вас документ про освіту?")
    options3 = [
        "Шкільний атестат",
        "Диплом училища або коледжу (ПТУ, фахова передвища)",
        "Диплом університету або інституту (вища освіта)",
    ]
    val = st.radio(
        "Оберіть варіант:",
        options3,
        index=options3.index(st.session_state.answers["education"])
        if st.session_state.answers["education"] in options3 else 0,
        key="r_edu",
        label_visibility="collapsed",
    )
    st.session_state.answers["education"] = val

# ── Крок 4 ──
elif step == 4:
    st.subheader("Чи є у вас діти до 18 років?")
    val = st.radio(
        "Оберіть варіант:",
        ["Так", "Ні"],
        index=["Так", "Ні"].index(st.session_state.answers["children_u18"])
        if st.session_state.answers["children_u18"] in ["Так", "Ні"] else 0,
        key="r_children",
        label_visibility="collapsed",
    )
    st.session_state.answers["children_u18"] = val

# ── Крок 5 ──
elif step == 5:
    st.subheader("Чи маєте ви інвалідність або відстрочку у зв'язку з інвалідністю?")
    st.info(
        "З 2025 року замість довідки МСЕК та індивідуальної програми реабілітації (ІПР) "
        "використовується Витяг з рішення експертної команди та Рекомендації."
    )
    options5 = [
        "Ні",
        "Так, інвалідність встановлено до 2025 року",
        "Так, інвалідність встановлено з 2025 року",
    ]
    val = st.radio(
        "Оберіть варіант:",
        options5,
        index=options5.index(st.session_state.answers["disability_status"])
        if st.session_state.answers["disability_status"] in options5 else 0,
        key="r_disability",
        label_visibility="collapsed",
    )
    st.session_state.answers["disability_status"] = val

# ── Крок 6 ──
elif step == 6:
    st.subheader("Чи маєте ви додаткові статуси?")
    st.caption("Позначте все, що стосується вас. Якщо жодне не підходить — просто натисніть «Сформувати перелік».")

    OPTIONS_6 = [
        "Пенсіонер",
        "Постраждалий від ЧАЕС",
        "ВПО (внутрішньо переміщена особа)",
        "Змінювали прізвище",
        "Одинока мати або батько",
        "Маю дитину з інвалідністю",
    ]

    current = set(st.session_state.answers.get("extra_statuses", []))
    selected = []
    for opt in OPTIONS_6:
        checked = st.checkbox(opt, value=(opt in current), key=f"cb_{opt}")
        if checked:
            selected.append(opt)
    st.session_state.answers["extra_statuses"] = selected


# ── Фінальний екран ──
elif step > TOTAL_STEPS:
    st.success("✅ Ваш персональний перелік документів сформовано!")
    docs = build_documents(st.session_state.answers)

    mandatory = [d for d in docs if d["important"]]
    conditional = [d for d in docs if not d["important"]]

    if mandatory:
        st.markdown("### 🟢 Обов'язкові документи (для всіх)")
        for doc in mandatory:
            render_doc_card(doc)

    if conditional:
        st.markdown("### 🔵 Додаткові документи (за вашою ситуацією)")
        for doc in conditional:
            render_doc_card(doc)

    st.markdown("---")
    st.markdown("**Завантажити перелік:**")

    col_pdf, col_txt = st.columns(2)

    with col_pdf:
        try:
            pdf_bytes = build_pdf(docs)
            st.download_button(
                label="📥 Завантажити PDF",
                data=pdf_bytes,
                file_name="perelik_dokumentiv.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as e:
            st.warning(f"PDF недоступний: {e}")

    with col_txt:
        txt_data = build_txt(docs)
        st.download_button(
            label="📄 Завантажити TXT",
            data=txt_data.encode("utf-8"),
            file_name="perelik_dokumentiv.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.markdown("")
    st.button("🔄 Почати спочатку", on_click=reset_app, use_container_width=True)

    st.markdown("---")
    st.caption("🟢 — обов'язковий для всіх &nbsp;&nbsp; 🔵 — потрібен за вашою ситуацією")
    st.stop()


# ─── Навігація ────────────────────────────────────────────────
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.session_state.step > 1:
        st.button("← Назад", on_click=prev_step, use_container_width=True)
with col2:
    if st.session_state.step < TOTAL_STEPS:
        st.button("Далі →", on_click=next_step, type="primary", use_container_width=True)
    elif st.session_state.step == TOTAL_STEPS:
        st.button("✅ Сформувати перелік", on_click=next_step, type="primary", use_container_width=True)
