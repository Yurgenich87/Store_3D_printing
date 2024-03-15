import os

folder_path = r'E:\PYTHON\Store_3d_printing\store_3d\media'  # Замените это на путь к вашей папке

# Получаем список файлов в папке
files = os.listdir(folder_path)

# Перебираем файлы и переименовываем их
for i, file_name in enumerate(files):
    # Формируем новое имя файла
    new_file_name = f'gallery-{i + 1}.png'
    # Составляем путь к старому и новому файлу
    old_file_path = os.path.join(folder_path, file_name)
    new_file_path = os.path.join(folder_path, new_file_name)
    # Переименовываем файл
    os.rename(old_file_path, new_file_path)
