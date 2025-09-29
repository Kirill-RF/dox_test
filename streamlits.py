import os
import tempfile
from pathlib import Path
from docx import Document
from docxcompose.composer import Composer
import streamlit as st

# Укажите путь к локальной структуре (в облаке вы можете включить файлы в репозиторий)
BASE_DIR = Path(__file__).parent / "Angle grinder"

def collect_instruction(tool_type: str):
    if tool_type == "corded":
        tool_dir = BASE_DIR / "Corded tools"
        order = [
            "1 Cover",
            "2 General safety",
            "3 Icon",
            "4 Additional safety and Intended use",
            "5 Specifications",
            "6 Operation picture",
            "7 Operation",
            "8 Maintenance",
            "9 End cover"
        ]
    else:
        tool_dir = BASE_DIR / "Cordless tools"
        order = [
            "1 Cover",
            "2a General safety",
            "2b Battery safety",
            "3 Icon",
            "4 Additional safety and Intended use",
            "5 Specifications",
            "6 Operation picture",
            "7 Operation",
            "8 Maintenance",
            "9 End cover"
        ]

    doc_paths = []
    for folder in order:
        folder_path = tool_dir / folder
        files = list(folder_path.glob("*.docx"))
        if len(files) != 1:
            raise FileNotFoundError(f"Ожидался 1 .docx в {folder_path}, найдено: {len(files)}")
        doc_paths.append(files[0])

    master = Document(doc_paths[0])
    composer = Composer(master)
    for path in doc_paths[1:]:
        composer.append(Document(path))

    # Сохраняем во временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        composer.save(tmp.name)
        return tmp.name

# === Веб-интерфейс ===
st.set_page_config(page_title="Сборщик инструкций УШМ", layout="centered")
st.title("🛠️ Сборщик инструкций УШМ")
st.write("Выберите тип инструмента и скачайте готовую инструкцию.")

tool_type = st.radio(
    "Тип инструмента:",
    options=["cordless", "corded"],
    format_func=lambda x: "Аккумуляторный" if x == "cordless" else "Сетевой"
)

if st.button("Собрать инструкцию"):
    try:
        output_path = collect_instruction(tool_type)
        with open(output_path, "rb") as f:
            st.download_button(
                label="⬇️ Скачать инструкцию",
                data=f,
                file_name=f"Инструкция_{'аккум' if tool_type == 'cordless' else 'сетевая'}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        os.unlink(output_path)  # удаляем временный файл
    except Exception as e:
        st.error(f"Ошибка: {e}")