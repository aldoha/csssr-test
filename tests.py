import configparser
import json
import unittest
import requests

from cerberus import Validator
from schema import hero_schema

v = Validator()
cfg = configparser.ConfigParser()
cfg.read('config.ini')


class SuperHeroesApi():
    def get_all_heroes(self):
        response = requests.get(
            '{api_url}/superheroes/'.format(api_url=cfg['api']['url']))
        return response

    def get_hero_by_id(self, hero_id):
        response = requests.get(
            '{api_url}/superheroes/{id}'.format(api_url=cfg['api']['url'], id=hero_id))
        return response


class TestGetRequests(unittest.TestCase):
    def test_get_superheroes(self):
        response = SuperHeroesApi().get_all_heroes()
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(data, [])

    def test_get_superhero_by_id(self):
        hero_id = cfg['test']['hero_id']
        response = SuperHeroesApi().get_hero_by_id(hero_id=hero_id)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], int(hero_id))
        self.assertTrue(v.validate(data, hero_schema))

    def test_get_superhero_by_nonexistent_id(self):
        nonexistent_hero_id = 1
        response = SuperHeroesApi().get_hero_by_id(hero_id=nonexistent_hero_id)
        data = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertIn(nonexistent_hero_id, data['id'])


if __name__ == '__main__':
    unittest.main()
