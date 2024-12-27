# Imagspeech

## Experiment
Программа для предъявления стимулов и записи данных

### Установка

1. Установить Python 3.10 \
    https://www.python.org/downloads/release/python-31010/

2. Cоздать виртуальную среду
   ```bash
   <path/to/python>/Python310/python.exe -m venv venv_experiment

3. При необходимости - изменить права доступа
   ```bash
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

4. Активировать виртуальную среду
   ```bash
   venv_experiment/Scripts/activate

5. Установка зависимостей
   ```bash
    pip install -r /experiment/requirements.txt

6. Распаковать архив `sound.zip` в папку `imagspeech/experiment/resource/`

### Запуск

1. Активировать виртуальную среду
   ```bash
   venv_experiment/Scripts/activate

2. Перейти в директорию
   ```bash
   cd imagspeech/experiment/core

3. Запустить программу
   ```bash
   python main.py
