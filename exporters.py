from fpdf import FPDF
import os
import urllib.request

FONTS_DIR = os.path.join(os.path.dirname(__file__), "assets", "fonts")

FONT_URLS = {
    "DejaVuSans.ttf":      "https://cdn.jsdelivr.net/npm/dejavu-fonts-ttf@2.37.3/ttf/DejaVuSans.ttf",
    "DejaVuSans-Bold.ttf": "https://cdn.jsdelivr.net/npm/dejavu-fonts-ttf@2.37.3/ttf/DejaVuSans-Bold.ttf",
}

CYRILLIC_TRANSLIT = {
    'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ж':'Zh','З':'Z',
    'И':'I','Й':'Y','К':'K','Л':'L','М':'M','Н':'N','О':'O','П':'P',
    'Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'Kh','Ц':'Ts','Ч':'Ch',
    'Ш':'Sh','Щ':'Shch','Ъ':'','Ы':'Y','Ь':'','Э':'E','Ю':'Yu','Я':'Ya',
    'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ж':'zh','з':'z',
    'и':'i','й':'y','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p',
    'р':'r','с':'s','т':'t','у':'u','ф':'f','х':'kh','ц':'ts','ч':'ch',
    'ш':'sh','щ':'shch','ъ':'','ы':'y','ь':'','э':'e','ю':'yu','я':'ya',
    'І':'I','і':'i','Ї':'Yi','ї':'yi','Є':'Ye','є':'ye','Ґ':'G','ґ':'g',
}


def _translit(text: str) -> str:
    return "".join(CYRILLIC_TRANSLIT.get(c, c) for c in text)


def _ensure_fonts() -> bool:
    os.makedirs(FONTS_DIR, exist_ok=True)
    for filename, url in FONT_URLS.items():
        path = os.path.join(FONTS_DIR, filename)
        if not os.path.exists(path):
            try:
                urllib.request.urlretrieve(url, path)
            except Exception:
                return False
    return True


def build_txt(docs: list) -> str:
    lines = ["Перелік документів для працевлаштування", "=" * 44, ""]
    for i, doc in enumerate(docs, start=1):
        lines.append(f"{i}. {doc['title']}")
        lines.append(f"   Що надати: {doc['details']}")
        lines.append(f"   Формат: {doc['format']}")
        if doc.get("hr_note"):
            lines.append(f"   Примітка: {doc['hr_note']}")
        lines.append("")
    return "\n".join(lines)


def build_pdf(docs: list) -> bytes:
    fonts_ok = _ensure_fonts()

    pdf = FPDF()
    # Set margins BEFORE add_page — критично для fpdf2 2.7+
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)
    pdf.set_top_margin(15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    regular_path = os.path.join(FONTS_DIR, "DejaVuSans.ttf")
    bold_path    = os.path.join(FONTS_DIR, "DejaVuSans-Bold.ttf")
    use_dejavu   = fonts_ok and os.path.exists(regular_path) and os.path.exists(bold_path)

    if use_dejavu:
        pdf.add_font("DejaVu", "",  regular_path)
        pdf.add_font("DejaVu", "B", bold_path)
        font_name = "DejaVu"
        def t(text): return text
    else:
        font_name = "Helvetica"
        def t(text): return _translit(text)

    # Явна ширина — обов'язково, 0 може дати помилку в деяких версіях fpdf2
    W = pdf.w - pdf.l_margin - pdf.r_margin

    pdf.set_font(font_name, "B", 14)
    pdf.multi_cell(W, 10, t("Перелік документів для працевлаштування"))
    pdf.ln(4)

    for i, doc in enumerate(docs, start=1):
        pdf.set_font(font_name, "B", 11)
        pdf.multi_cell(W, 8, t(f"{i}. {doc['title']}"))
        pdf.set_font(font_name, "", 10)
        pdf.multi_cell(W, 7, t(f"Що надати: {doc['details']}"))
        pdf.multi_cell(W, 7, t(f"Формат: {doc['format']}"))
        if doc.get("hr_note"):
            pdf.set_text_color(100, 100, 100)
            pdf.multi_cell(W, 7, t(f"Примітка: {doc['hr_note']}"))
            pdf.set_text_color(0, 0, 0)
        pdf.ln(3)

    return bytes(pdf.output())
