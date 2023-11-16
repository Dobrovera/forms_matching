# Запросы UserForm

curl -X POST -d "username=some_username&user_email=someemail@.gmail.com&user_phone=+7 999 999 99 99&last_visit=2022-01-12" http://localhost:5000/get_form # Корректный запрос для UserForm
curl -X POST -d "username=some_username&user_email=someemail@.gmail.com&user_phone=+7 999 999 99&last_visit=2022-01-12" http://localhost:5000/get_form # Некорректный запрос для UserForm, неверно указан телефон (не хватает символов)


# Запросы OrderForm

curl -X POST -d "client_email=some.email@.gmail.com&user_phone=+7 999 999 99 99&order_date=01.01.2022&comment=some_text" http://localhost:5000/get_form # Корректный запрос для OrderForm
curl -X POST -d "client_email=some.email@.gmail.com&user_phone=+7 999 999 99 99&order_date=46.01.2022&comment=some_text" http://localhost:5000/get_form # Некорректный запрос для OrderForm, неверно указана дата (46-й день января)


# Запросы ContactForm

curl -X POST -d "contact_email=someemail@.mail.com&contact_phone=+7 999 999 99 99" http://localhost:5000/get_form # Корректный запрос для ContactForm
curl -X POST -d "contact_email=someemail@.mail.com&contact_phone=+7 999 999 99 99&name=some_text" http://localhost:5000/get_form # Корректный запрос для ContactForm, в запросе указано больше полей, чем в форме
curl -X POST -d "contact_email=someemail@.mail&contact_phone=+7 999 999 99 99" http://localhost:5000/get_form # Некорректный запрос для ContactForm, неверно указан email
