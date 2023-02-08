from datetime import datetime

import requests

URL = 'http://127.0.0.1:8000/'


def test_all_employees():
    response = requests.get(URL)
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) > 0


def test_get_by_name():
    response = requests.get(f'{URL}?name=Flynn')
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) > 0
    assert 'Flynn' in response_data[0]['name']


def test_get_by_email():
    response = requests.get(f'{URL}?email=turpis.non@Nunc.edu')
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) > 0
    assert response_data[0]['email'] == 'turpis.non@Nunc.edu'


def test_get_by_company():
    response = requests.get(f'{URL}?company=Twitter')
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) > 0
    assert response_data[0]['company'] == 'Twitter'


def test_get_by_job_title():
    response = requests.get(f'{URL}?job_title=janitor')
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) > 0
    assert response_data[0]['job_title'] == 'janitor'


def test_get_by_gender():
    response = requests.get(f'{URL}?gender=male')
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) > 0
    assert response_data[0]['gender'] == 'male'


def test_invalid_gender():
    response = requests.get(f'{URL}?gender=unknown')
    assert response.status_code == 400
    response_data = response.json()
    assert response_data['detail'] == 'Invalid gender'


def test_get_by_join_date():
    response = requests.get(f'{URL}?join_date_start=01-01-2003&join_date_end=01-01-2006')
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) > 0
    join_date = datetime.fromisoformat(response_data[0]['join_date'])
    assert datetime(2003, 1, 1, tzinfo=join_date.tzinfo) <= join_date <= datetime(2006, 1, 1, tzinfo=join_date.tzinfo)


def test_get_by_age():
    response = requests.get(f'{URL}?age_min=30&age_max=50')
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) > 0
    assert 30 <= response_data[0]['age'] <= 50


def test_get_by_salary():
    response = requests.get(f'{URL}?salary_min=3000&salary_max=5000')
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) > 0
    assert 3000 <= response_data[0]['salary'] <= 5000
