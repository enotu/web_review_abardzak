Проект парсящий подраздел LMS Пермского Университета, доступную без регистрации и вытягивающее из него расписание.
Имеет главную страницу на 0.0.0.0/5000 где предлагается выбор группы, после отправляет на раздел с расписанием
Для парсинга использует BeautifulSoup
Данные парсит в PostgreSQL
Работает в Docker контейнере, бекенд в одном, а база данных в другом.