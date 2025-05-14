import json

from homework.src.schemas import Recipes
from homework.test.conftest import client


def test_find_recipes(client):
    response = client.get('/recipes')
    assert response.status_code == 200


def test_find_recipe_by_id(client):
    response = client.get('/recipes/1')
    expected_data = [{
        'name': 'test',
        'time_dish': 2,
        'ingredients': 'test',
        'description': 'test'
    }]
    assert response.status_code == 200
    assert response.json() == expected_data


def test_add_recipes(client):
    recipes = {
        'name': 'post',
        'time_dish': 2,
        'ingredients': 'test',
        'description': 'test'
    }
    response = client.post('/recipes', json=recipes)
    expected_data = {
        'name': 'post',
        'time_dish': 2,
        'ingredients': 'test',
        'description': 'test'
    }
    assert response.json() == expected_data
