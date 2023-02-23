# Yambd  


### Описание
API на базе REST для русского аналога IMDb.


### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Natulishka/api_yamdb.git
cd api_yamdb
```
Cоздать виртуальное окружение:

```
python -m venv venv
```
Aктивировать виртуальное окружение:
```
source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Выполнить миграции:

```
python manage.py migrate
```
Запустить проект:
```
python manage.py runserver
```
### Документация

Документацию и примеры запросов можно посмотреть по адресу http://127.0.0.1:8000/redoc/

### Авторы  
[Наталья Шульгина](https://github.com/Natulishka/)  
[Павел Иванов](https://github.com/Chasotcka)
