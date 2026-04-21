from fpdf import FPDF
import os

FONTS_DIR = os.path.join(os.path.dirname(__file__), "assets", "fonts")


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
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", os.path.join(FONTS_DIR, "DejaVuSans.ttf"), uni=True)
    pdf.add_font("DejaVu", "B", os.path.join(FONTS_DIR, "DejaVuSans-Bold.ttf"), uni=True)

    pdf.set_font("DejaVu", "B", 14)
    pdf.multi_cell(0, 10, "Перелік документів для працевлаштування")
    pdf.ln(4)

    for i, doc in enumerate(docs, start=1):
        pdf.set_font("DejaVu", "B", 11)
        pdf.multi_cell(0, 8, f"{i}. {doc['title']}")
        pdf.set_font("DejaVu", "", 10)
        pdf.multi_cell(0, 7, f"Що надати: {doc['details']}")
        pdf.multi_cell(0, 7, f"Формат: {doc['format']}")
        if doc.get("hr_note"):
            pdf.set_text_color(100, 100, 100)
            pdf.multi_cell(0, 7, f"Примітка: {doc['hr_note']}")
            pdf.set_text_color(0, 0, 0)
        pdf.ln(3)

    return bytes(pdf.output())
