from PIL import Image, ImageDraw, ImageFont
from docx import Document
import os

# Словарь с длинами строк. Включите сюда желаемые длины для каждой строки.
line_lengths = {
    1: 15,   # Первая строка, минимальная длина
    2: 25,   # Увеличили длину
    3: 29,   # Увеличили длину
    4: 33,   # Увеличили длину
    5: 36,   # Увеличили длину
    6: 39,   # Увеличили длину
    7: 42,   # Увеличили длину
    8: 45,   # Увеличили длину
    9: 45,  # Увеличили длину
    10: 48,  # Увеличили длину
    11: 48,  # Увеличили длину
    12: 50,  # Установили как было
    13: 50,  # Увеличили длину
    14: 50,  # Увеличили длину
    15: 50,  # Увеличили длину
    16: 50,  # Установили как было
    17: 48,  # Увеличили длину
    18: 48,  # Увеличили длину
    19: 45,  # Увеличили длину
    20: 45,  # Увеличили длину
    21: 42,  # Увеличили длину
    22: 39,  # Увеличили длину
    23: 36,  # Увеличили длину
    24: 33,  # Установили как было
    25: 29,  # Увеличили длину
    26: 25,  # Увеличили длину
    27: 15   # Установили как было
}


def create_text_inside_circle(output_dir, text, number_questions, image_size=320, font_size=20, padding=20):
    # Убедимся, что папка для сохранения существует
    os.makedirs(output_dir, exist_ok=True)

    # Загружаем шрифт
    try:
        font_text = ImageFont.truetype("DejaVuSans.ttf", font_size)
        font_numb = ImageFont.truetype("DejaVuSans.ttf", 80)
    except IOError:
        print("Шрифт DejaVuSans.ttf не найден. Убедитесь, что шрифт установлен.")
        return

    # Разбиваем текст на слова
    words = text.split()
    lines = []
    current_line = ""
    line_index = 1  # Индекс строки для проверки в словаре

    # Определяем максимальное количество строк, которые помещаются на изображении
    max_lines_per_image = len(line_lengths) # Учитываем отступы
    # Разбиваем текст с учетом длины строк из словаря
    for word in words:
        max_length = line_lengths.get(line_index, 50)  # Даем максимальную длину для текущей строки

        if len(current_line + " " + word) <= max_length:  # Проверяем, можно ли добавить слово в строку
            current_line += " " + word if current_line else word
        else:
            # current_line = str(line_index) + current_line
            lines.append(current_line)  # Добавляем строку в список
            current_line = word  # Начинаем новую строку с текущего слова
            line_index += 1  # Переходим к следующей строке
            if line_index > max_lines_per_image:
                line_index = 1


    total_images = (len(lines) // max_lines_per_image) + (1 if len(lines) % max_lines_per_image != 0 else 0)

    # Создаем изображения
    for image_num in range(total_images):
        # Создаем новое изображение
        image = Image.new("RGBA", (320, 320), (0, 0, 0, 255))
        draw = ImageDraw.Draw(image)

        # Определяем центр и радиус круга
        center = image_size // 2
        radius = image_size

        # Рисуем окружность
        draw.ellipse(
            (0, 0, radius, radius),
            outline="white",
            width=2
        )

        text_numb = f"{number_questions}.{image_num + 1}"
        color = (204,183,97)
        transparency = 255  # Прозрачность, 128 из 255
        color_with_alpha = (*color, transparency)  # Добавляем альфа-канал

        bbox = draw.textbbox((0, 0), text_numb, font=font_numb)
        line_width = bbox[2] - bbox[0]
        x = center - line_width // 2  # Центрируем строку по горизонтали
        y = center - line_width // 2  
        draw.text((x , y), text_numb, font=font_numb, fill=color_with_alpha)


        # Располагаем текст по центру
        start_line_index = image_num * max_lines_per_image
        end_line_index = (image_num + 1) * max_lines_per_image
        lines_to_draw = lines[start_line_index:end_line_index]

        y_start = padding  # Начальная Y-координата для центрирования текста

        for i, line in enumerate(lines_to_draw):
            bbox = draw.textbbox((0, 0), line, font=font_text)
            line_width = bbox[2] - bbox[0]
            x = center - line_width // 2  # Центрируем строку по горизонтали
            y = y_start + i * font_size  # Смещаем строку вниз
            draw.text((x, y), line, font=font_text, fill="white")


        # Сохраняем изображение
        output_path = os.path.join(output_dir, f"{number_questions}_{image_num + 1}.png")
        image.save(output_path)
        print(f"Вопрос {number_questions}, Изображение {image_num + 1} сохранено: {output_path}")

def split_docx_by_headers(file_path):
    # Открываем документ
    doc = Document(file_path)

    blocks = []  # Список для хранения блоков текста
    current_block = []  # Временный список для хранения текста одного блока

    for para in doc.paragraphs:
        # Проверяем, является ли параграф заголовком (например, заголовок 1)
        if para.style.name.startswith('Heading'):
            if current_block:
                blocks.append("\n".join(current_block))  # Добавляем текущий блок в список
            current_block = [para.text]  # Новый блок начинается с заголовка
        else:
            current_block.append(para.text)  # Добавляем обычный параграф в текущий блок

    # Добавляем последний блок в список, если он не пуст
    if current_block:
        blocks.append("\n".join(current_block))

    return blocks

def main():
    file_path = "Зачет _вычислительные системы_ (1).docx"  # Укажите путь к вашему .docx файлу
    blocks = split_docx_by_headers(file_path)

    # Выводим разделенные блоки текста
    for idx, block in enumerate(blocks, 1):
        print(f"Block {idx}:\n")
        print(block)
        print("\n" + "="*50 + "\n")
        create_text_inside_circle(
            "images", 
            text= block,
            number_questions=idx,
            image_size=320,
            font_size=11,
            padding=10
        )
if __name__ == "__main__":
    main()
