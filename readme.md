# BeerLab Purtov

## Перед запуском

---

0. Положить в корень проекта файл `.env` (написать мне в ЛС) и создать БД с данными из этого файла (или подредачить под
   свои)
1. Создать виртуальную среду

- На Windows:

```shell
python -m venv .venv
```

- На Linux:

```shell
python3 -m venv .venv
```

2. Запустить виртуальную среду

- На Windows:

```shell
.venv/Scripts/activate
```

- На Linux:

```shell
source .venv/bin/activate
```

3. Установить зависимости

- На Windows:

```shell
pip install -r requirements.txt
```

- На Linux:

```shell
pip3 install -r requirements.txt
```

4. Создать миграции

```shell
aerich init-db
aerich upgrade
```

5. Наполнить ДБ данными, используя файл [db_data_filler.sql](scripts%2Fdb_data_filler.sql)

## Запуск

---

```shell
uvicorn --app-dir ./src main:app --host 0.0.0.0 --port 80
```

## Документация к API

---

После запуска, доки находятся по адресу

```
http://localhost:80/docs
```
