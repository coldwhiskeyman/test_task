import re
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from pydantic import create_model

import database
import responses
import schemas

app = FastAPI(
    title='TestTask',
    description='Тестовое задание FastAPI+MongoDB',
    version='0.0.1',
)

SIMPLE_PARAMS = ['email', 'company', 'job_title']
GENDERS = ['male', 'female', 'non binary']
query_params = {
    'name': (Optional[str], None),
    'email': (Optional[str], None),
    'company': (Optional[str], None),
    'job_title': (Optional[str], None),
    'gender': (Optional[str], None),
    'join_date_start': (Optional[str], None),
    'join_date_end': (Optional[str], None),
    'salary_min': (Optional[int], None),
    'salary_max': (Optional[int], None),
    'age_min': (Optional[int], None),
    'age_max': (Optional[int], None),
}

query_model = create_model("Query", **query_params)


@app.get(
    '/',
    response_model=List[schemas.Employee],
    summary='Получение списка сотрудников',
    description='Получение списка сотрудников согласно примененному фильтру',
    responses={
        400: {'model': responses.InvalidGender}
    },
)
async def get_employee_list(params: query_model = Depends()):
    """
    Получение списка сотрудников.
    Метод принимает следующие параметры поисковой строки (все являются необязательными):

    - **name**: Имя или фамилия сотрудника (string)
    - **email**: Адрес электронной почты (string)
    - **company**: Название компании (string)
    - **job_title**: Должность (string)
    - **gender**: Пол сотрудника (string)
    - **join_date_start**: Начальная дата выхода на должность в формате ДД-ММ-ГГГГ (string)
    - **join_date_end**: Конечная дата выхода на должность в формате ДД-ММ-ГГГГ (string)
    - **salary_min**: Минимальная зарплата (integer)
    - **salary_max**: Максимальная зарплата (integer)
    - **age_min**: Минимальный возраст (integer)
    - **age_max**: Максимальный возраст (integer)

    Возвращает список сотрудников согласно запросу
    """
    params_dict = params.dict()
    query_dict = make_query(params_dict)
    return await database.get_employee_list(query_dict)


def make_query(params):
    result = prepare_result(params)
    for key, value in params.items():
        if not value:
            continue
        if key in SIMPLE_PARAMS:
            result[key] = value
        elif key == 'name':
            result['name'] = re.compile(f'.*{value}.*')
        elif key == 'gender' and check_gender(value):
            result['gender'] = value
        elif key == 'join_date_start':
            result['join_date']['$gte'] = datetime.strptime(value, '%d-%m-%Y').isoformat()
        elif key == 'join_date_end':
            result['join_date']['$lte'] = datetime.strptime(value, '%d-%m-%Y').isoformat()
        elif key == 'salary_min':
            result['salary']['$gte'] = value
        elif key == 'salary_max':
            result['salary']['$lte'] = value
        elif key == 'age_min':
            result['age']['$gte'] = value
        elif key == 'age_max':
            result['age']['$lte'] = value
    return result


def prepare_result(params):
    result = {}
    if params['join_date_start'] or params['join_date_end']:
        result['join_date'] = {}
    if params['salary_min'] or params['salary_max']:
        result['salary'] = {}
    if params['age_min'] or params['age_max']:
        result['age'] = {}
    return result


def check_gender(gender):
    if gender in GENDERS:
        return True
    else:
        raise HTTPException(status_code=400, detail='Invalid gender')
