## People counting.
Тестовое задание по определению количества входов и выходов в магазине.

### Краткое описание
Код под подсчету входов и выходов разделяется на две части:
- Подсчет на основе видеофайла с использованием openCV2 и YOLOv8 + SORT
- Подсчет на основе JSON файла, в котором находится информация по ID и траекториям движения посетителя

### Установка

```sh
git clone https://github.com/chuvalniy/crowd-counter
```

Для работы с использованием openCV и YOLO необходимо установить дополнительные библиотеки.
```sh
pip install -r requirements.txt
```

### Как использовать
Для подсчета на основе видео запустить файл **src/predict/yolo.py**

Для подсчета на основе JSON запустить файл **src/predict/count.py**

### Результат выполнения алгоритма (JSON):
 - Количество входов: 7
 - Количество выходов: 7
 - Всего посетителей (за отрезок времени): 39 (?)

### Варианты улучшения алгоритмов

- Использовать маску для видео, чтобы модель не определяла объекты, которые не нужны для предсказания.
- Удалять информацию по id посетителей (словарь входы/выходы) по истечению N количества кадров.
- Попробовать использовать прямоугольную зону для обозначения входа/выхода вместо границ в виде линий.
- Перенести данные (видео, JSON) на облачное хранилище, чтобы не хранить их в git репозитории.
