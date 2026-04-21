def build_documents(answers: dict) -> list:
    docs = [
        {
            "title": "Паспорт або ID-карта",
            "details": "Копії всіх сторінок паспорта з записами або копія ID-картки + витяг про місце реєстрації.",
            "format": "Копія",
            "instruction_key": None,
            "important": True,
            "hr_note": None,
        },
        {
            "title": "ІПН",
            "details": "Копія ІПН.",
            "format": "Копія",
            "instruction_key": None,
            "important": True,
            "hr_note": None,
        },
    ]

    labor = answers.get("labor_book")
    if labor == "Є трудова книжка":
        docs.append({
            "title": "Витяг з ЕТК",
            "details": "Надати витяг з електронної трудової книжки у форматі PDF. Якщо паперова трудова книжка є на руках — надати також її.",
            "format": "PDF (+ паперова за наявності)",
            "instruction_key": "etk",
            "important": True,
            "hr_note": None,
        })
    elif labor == "Це моє перше офіційне працевлаштування":
        docs.append({
            "title": "Довідка з ПФУ",
            "details": "Надати довідку про відсутність індивідуальних відомостей про особу за формою ПФУ. Замовити можна на вебпорталі ПФУ.",
            "format": "PDF / Копія",
            "instruction_key": None,
            "important": True,
            "hr_note": None,
        })

    education = answers.get("education", "")
    edu_map = {
        "Шкільний атестат": "Атестат про повну загальну середню освіту",
        "Диплом училища або коледжу (ПТУ, фахова передвища)": "Диплом училища або коледжу",
        "Диплом університету або інституту (вища освіта)": "Диплом університету або інституту",
    }
    edu_label = edu_map.get(education, education)
    docs.append({
        "title": "Документ про освіту",
        "details": f"Надати: {edu_label}. Без додатків.",
        "format": "Копія",
        "instruction_key": None,
        "important": True,
        "hr_note": None,
    })

    docs.append({
        "title": "Фото 3×4",
        "details": "2 екземпляри, надати в оригіналі при заповненні документів на оформлення.",
        "format": "Оригінал",
        "instruction_key": None,
        "important": True,
        "hr_note": None,
    })

    if answers.get("military_liable") == "Так":
        docs.append({
            "title": "Військово-обліковий документ (Резерв ID)",
            "details": (
                "Роздруківка або PDF з застосунку Резерв+ на поточну дату. "
                "З грудня 2025 року електронний ВОД у Резерв+ є основним та єдиним "
                "офіційним військово-обліковим документом (постанова КМУ № 559)."
            ),
            "format": "PDF / Роздруківка",
            "instruction_key": None,
            "important": True,
            "hr_note": "Завантажити Резерв+: https://reserveplus.mod.gov.ua",
        })

    if answers.get("children_u18") == "Так":
        docs.append({
            "title": "Свідоцтво про народження дітей",
            "details": "Копії свідоцтв про народження дітей до 18 років.",
            "format": "Копія",
            "instruction_key": None,
            "important": False,
            "hr_note": None,
        })

    disability = answers.get("disability_status")
    if disability == "Так, інвалідність встановлено до 2025 року":
        docs += [
            {
                "title": "Довідка МСЕК",
                "details": "Документ, що підтверджує групу інвалідності.",
                "format": "Копія",
                "instruction_key": None,
                "important": False,
                "hr_note": None,
            },
            {
                "title": "Індивідуальна програма реабілітації (ІПР)",
                "details": "Надати ІПР для врахування умов та облаштування робочого місця.",
                "format": "Копія",
                "instruction_key": None,
                "important": False,
                "hr_note": None,
            },
        ]
    elif disability == "Так, інвалідність встановлено з 2025 року":
        docs += [
            {
                "title": "Витяг з рішення експертної команди",
                "details": "Витяг з рішення експертної команди з оцінювання повсякденного функціонування особи.",
                "format": "PDF / Копія",
                "instruction_key": None,
                "important": False,
                "hr_note": None,
            },
            {
                "title": "Рекомендації",
                "details": "Рекомендації як частина індивідуальної програми реабілітації особи з інвалідністю.",
                "format": "PDF / Копія",
                "instruction_key": None,
                "important": False,
                "hr_note": None,
            },
        ]

    statuses = set(answers.get("extra_statuses", []))
    STATUS_DOCS = {
        "Пенсіонер": {
            "title": "Пенсійне посвідчення",
            "details": "Копія пенсійного посвідчення.",
            "format": "Копія",
            "instruction_key": None,
            "important": False,
            "hr_note": None,
        },
        "Постраждалий від ЧАЕС": {
            "title": "Посвідчення постраждалого від ЧАЕС",
            "details": "Копія відповідного посвідчення.",
            "format": "Копія",
            "instruction_key": None,
            "important": False,
            "hr_note": None,
        },
        "ВПО (внутрішньо переміщена особа)": {
            "title": "Довідка ВПО",
            "details": "Копія довідки про взяття на облік внутрішньо переміщеної особи.",
            "format": "Копія",
            "instruction_key": None,
            "important": False,
            "hr_note": None,
        },
        "Змінювали прізвище": {
            "title": "Свідоцтво про шлюб або документ про зміну прізвища",
            "details": "Копія свідоцтва про шлюб або іншого документа, що підтверджує зміну прізвища.",
            "format": "Копія",
            "instruction_key": None,
            "important": False,
            "hr_note": None,
        },
        "Одинока мати або батько": {
            "title": "Документи для статусу одинокої матері / батька",
            "details": "Підготуйте підтвердні документи. HR уточнить точний перелік.",
            "format": "Копія",
            "instruction_key": None,
            "important": False,
            "hr_note": "HR може додатково запросити витяг з РАЦСу або інші підтвердні документи.",
        },
        "Маю дитину з інвалідністю": {
            "title": "Документи щодо дитини з інвалідністю",
            "details": "Підготуйте підтвердні документи для кадрового та податкового обліку. HR уточнить деталі.",
            "format": "Копія",
            "instruction_key": None,
            "important": False,
            "hr_note": "HR може окремо уточнити довідку МСЕК або аналогічний актуальний документ.",
        },
    }
    for status, doc in STATUS_DOCS.items():
        if status in statuses:
            docs.append(doc)

    return docs
