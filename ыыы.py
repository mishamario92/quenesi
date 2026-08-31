import os
import re
from PIL import Image
import htmlmin


def optimize_website():
    # Получаем текущую папку, где лежит скрипт
    current_dir = os.path.dirname(os.path.abspath(__file__))

    print("🚀 Запуск оптимизации сайта...")

    # Регулярное выражение для поиска тегов <script> без атрибутов загрузки
    script_regex = re.compile(r'<script\s*>(.*?)</script>', re.DOTALL)

    for root, dirs, files in os.walk(current_dir):
        # Пропускаем системные папки, чтобы не сломать их
        if '.git' in root or '.idea' in root:
            continue

        for file in files:
            file_path = os.path.join(root, file)
            ext = file.lower().split('.')[-1]

            # --- 1. СЖАТИЕ КАРТИНОК (PNG и JPG) БЕЗ ИЗМЕНЕНИЯ ФОРМАТА ---
            if ext in ['png', 'jpg', 'jpeg']:
                try:
                    img = Image.open(file_path)
                    original_size = os.path.getsize(file_path)

                    if ext == 'png':
                        # Для PNG используем максимальное сжатие палитры (optimize=True)
                        img.save(file_path, format="PNG", optimize=True)
                    else:
                        # Для JPG снижаем качество до 80-85% (визуально разницы нет, а вес падает в 3-5 раз)
                        img.convert('RGB').save(file_path, format="JPEG", quality=85, optimize=True)

                    new_size = os.path.getsize(file_path)
                    saved = original_size - new_size
                    if saved > 0:
                        print(f"📷 Сжата картинка: {file} (Сэкономлено: {saved // 1024} КБ)")
                except Exception as e:
                    print(f"❌ Ошибка сжатия картинки {file}: {e}")

            # --- 2. СЖАТИЕ HTML И ВСТРОЕННОГО JAVASCRIPT ---
            elif ext == 'html':
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    original_size = len(content.encode('utf-8'))

                    # Шаг А: Автоматически оборачиваем встроенный JS в DOMContentLoaded, если этого еще нет
                    def wrap_js(match):
                        js_code = match.group(1).strip()
                        # Если код уже обернут или он пустой, не трогаем его
                        if "DOMContentLoaded" in js_code or not js_code:
                            return match.group(0)
                        return f"<script>document.addEventListener('DOMContentLoaded',()=>{{\n{js_code}\n}});</script>"

                    updated_content = script_regex.sub(wrap_js, content)

                    # Шаг Б: Минифицируем HTML (удаляем лишние пробелы, отступы и комментарии)
                    minified_html = htmlmin.minify(updated_content, remove_comments=True, remove_empty_space=True)

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(minified_html)

                    new_size = len(minified_html.encode('utf-8'))
                    saved = original_size - new_size
                    print(f"📄 Оптимизирован HTML: {file} (Уменьшен на: {saved // 1024} КБ)")
                except Exception as e:
                    print(f"❌ Ошибка оптимизации HTML {file}: {e}")

    print("✨ Оптимизация успешно завершена! Теперь можно отправлять код на GitHub.")


if __name__ == "__main__":
    optimize_website()
