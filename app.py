import re

from tinydb import TinyDB, Query
from flask import Flask, request, jsonify
from datetime import datetime
from urllib.parse import unquote


app = Flask(__name__)


db = TinyDB('database.json')
User = Query()

# db.insert({
#     "name": "MyForm",
#     "field_name_1": "email",
#     "field_name_2": "phone"
# })


def is_valid_email(data):

    # Проверяем валидность email
    email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    return bool(re.match(email_pattern, data))


def is_valid_phone(data):

    # Проверяем на соответствие формату +7 xxx xxx xx xx
    phone_pattern = re.compile(r'^\+7\s\d{3}\s\d{3}\s\d{2}\s\d{2}$')
    return bool(re.match(phone_pattern, data))


def is_valid_date(data):

    # Проверяем на соответствие формату DD.MM.YYYY или YYYY-MM-DD
    try:
        datetime.strptime(data, '%d.%m.%Y')
        return True
    except ValueError:
        try:
            datetime.strptime(data, '%Y-%m-%d')
            return True
        except ValueError:
            return False


@app.route('/get_form', methods=['POST'])
def get_form():

    # Получаем на вход данные формата: f_name1=value1&f_name2=value2 и преобразуем в словарь
    data = request.get_data(as_text=True)
    data_list = data.split('&')
    data_dict = {}
    for pair in data_list:
        key, value = pair.split('=')
        data_dict[unquote(key)] = unquote(value)

    # Валидируем входные данные на соответствие типам
    field_types = {}
    for field, value in data_dict.items():
        if is_valid_date(value):
            field_types[field] = 'date'
        elif is_valid_phone(value):
            field_types[field] = 'phone'
        elif is_valid_email(value):
            field_types[field] = 'email'
        else:
            field_types[field] = 'text'

    # Проверяем форму в бд
    for template in db.all():
        template_fields = set(template.keys()) - {'name'}  # Исключаем поле с именем шаблона
        if template_fields.issubset(field_types.keys()):
            field_match = True
            for field in template_fields:
                if field_types[field] != template[field]:
                    field_match = False
                    break
            if field_match:
                print(f"template_name: {template['name']}")
                return jsonify({"template_name": template["name"]})

    return jsonify(field_types)


if __name__ == '__main__':
    app.run(debug=True)
