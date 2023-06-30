import os
import ffmpeg
import sys


def process_sequence(sequence_path, output_directory):
    # Извлекаем имя секвенции из пути
    sequence_name = os.path.basename(sequence_path)
    # Удаляем расширение файла, чтобы получить имя секвенции
    sequence_name = os.path.splitext(sequence_name)[0]

    # Создаем папку для сохранения видеофайла
    output_folder = os.path.join(output_directory, sequence_name)
    os.makedirs(output_folder, exist_ok=True)

    # Определяем паддинг на основе первого файла в секвенции
    first_frame = os.listdir(sequence_path)[0]
    padding = len(first_frame.split("_")[-1].split(".")[0])

    # Формируем путь для выходного видеофайла
    output_file = os.path.join(output_folder, f"{sequence_name}.mov")

    # Формируем паттерн для входных файлов ffmpeg
    input_pattern = os.path.join(sequence_path, f"img_{'#' * padding}.jpg")

    print(f"Sequence: {sequence_name}")
    print(f"Input Pattern: {input_pattern}")
    print(f"Output File: {output_file}")

    # Используем ffmpeg-python для создания видеофайла
    try:
        ffmpeg.input(input_pattern, pattern_type='glob', framerate=25)\
            .output(output_file, vcodec='mjpeg', movflags='faststart')\
            .run()
        print("Video created successfully.")
    except ffmpeg.Error as e:
        print(f"An error occurred while creating the video: {e.stderr.decode('utf-8')}")


def process_directory(directory):
    # Обходим все элементы в указанной директории
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        # Если элемент является директорией, рекурсивно обрабатываем его
        if os.path.isdir(item_path):
            process_directory(item_path)
        else:
            # Если элемент является файлом с расширением .jpg, обрабатываем его как секвенцию
            if item.lower().endswith(".jpg"):
                sequence_path = os.path.dirname(item_path)
                process_sequence(sequence_path, directory)


# Проверяем переданный аргумент
if len(sys.argv) != 2:
    print("Неверное количество аргументов. Укажите путь до папки.")
    sys.exit(1)

input_directory = sys.argv[1]

# Проверяем, существует ли указанная папка
if not os.path.isdir(input_directory):
    print("Указанная папка не существует.")
    sys.exit(1)

# Обрабатываем папку
process_directory(input_directory)
