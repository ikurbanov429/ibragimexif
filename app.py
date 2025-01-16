from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import piexif
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

def copy_exif_and_quality(source_image_path, target_image_path):
    """
    Копирует EXIF-данные и параметры качества из исходного изображения в целевое.
    :param source_image_path: Путь к исходному изображению.
    :param target_image_path: Путь к целевому изображению.
    """
    # Открываем исходное изображение
    source_image = Image.open(source_image_path)

    # Получаем EXIF-данные
    exif_data = piexif.load(source_image.info.get("exif", b""))

    # Открываем целевое изображение
    target_image = Image.open(target_image_path)

    # Сохраняем целевое изображение с EXIF-данными и качеством исходного
    target_image.save(target_image_path, exif=piexif.dump(exif_data), quality=100)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    download_link = None

    if request.method == 'POST':
        if 'source_image' not in request.files or 'target_image' not in request.files:
            message = "Ошибка: файлы не загружены."
            return render_template('index.html', message=message, download_link=download_link)

        source_image = request.files['source_image']
        target_image = request.files['target_image']

        if source_image.filename == '' or target_image.filename == '':
            message = "Ошибка: файлы не выбраны."
            return render_template('index.html', message=message, download_link=download_link)

        # Очистка имен файлов
        source_filename = secure_filename(source_image.filename)
        target_filename = source_filename  # Используем имя исходного файла

        source_path = os.path.join(app.config['UPLOAD_FOLDER'], source_filename)
        target_path = os.path.join(app.config['UPLOAD_FOLDER'], target_filename)

        # Сохраняем загруженные файлы
        source_image.save(source_path)
        target_image.save(target_path)

        # Копируем EXIF-данные и параметры качества
        copy_exif_and_quality(source_path, target_path)

        message = "Успешно"
        download_link = target_filename

    return render_template('index.html', message=message, download_link=download_link)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import piexif
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

def copy_exif_and_quality(source_image_path, target_image_path):
    """
    Копирует EXIF-данные и параметры качества из исходного изображения в целевое.
    :param source_image_path: Путь к исходному изображению.
    :param target_image_path: Путь к целевому изображению.
    """
    # Открываем исходное изображение
    source_image = Image.open(source_image_path)

    # Получаем EXIF-данные
    exif_data = piexif.load(source_image.info.get("exif", b""))

    # Открываем целевое изображение
    target_image = Image.open(target_image_path)

    # Сохраняем целевое изображение с EXIF-данными и качеством исходного
    target_image.save(target_image_path, exif=piexif.dump(exif_data), quality=100)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    download_link = None

    if request.method == 'POST':
        if 'source_image' not in request.files or 'target_image' not in request.files:
            message = "Ошибка: файлы не загружены."
            return render_template('index.html', message=message, download_link=download_link)

        source_image = request.files['source_image']
        target_image = request.files['target_image']

        if source_image.filename == '' or target_image.filename == '':
            message = "Ошибка: файлы не выбраны."
            return render_template('index.html', message=message, download_link=download_link)

        # Очистка имен файлов
        source_filename = secure_filename(source_image.filename)
        target_filename = secure_filename(target_image.filename)

        source_path = os.path.join(app.config['UPLOAD_FOLDER'], source_filename)
        target_path = os.path.join(app.config['UPLOAD_FOLDER'], target_filename)

        # Сохраняем загруженные файлы
        source_image.save(source_path)
        target_image.save(target_path)

        # Копируем EXIF-данные и параметры качества
        copy_exif_and_quality(source_path, target_path)

        message = "Успешно!"
        download_link = target_filename

    return render_template('index.html', message=message, download_link=download_link)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)