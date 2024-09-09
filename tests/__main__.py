import requests
import unittest

BASE_URL = 'http://localhost:8000/api/v1'

class UserTestCase(unittest.TestCase):
    '''Testes para os endpoint's users/ e users/{user_id}'''

    def test_create_user(self):
        '''Criando um usuário'''

        response = requests.post(BASE_URL+'/users', json = {
            "name": "João Antonio",
            "email": "example@gmail.com",
            "password": "12345",
            "is_admin": False
        })

        assert response.status_code == 201

    def test_create_invalid_user(self):
        '''
        Criando um usuário com dados invalido

        falta o attr 'email' e o attr 'password' deve ser uma string
        '''
        
        response = requests.post(BASE_URL+'/users', json = {
            "name": "João Antonio",
            "password": 12345,
            "is_admin": False
        })

        assert response.status_code == 400

    def test_get_user(self):
        '''Buscando um usuário'''

        response = requests.get(BASE_URL+'/users/1')

        assert response.status_code == 200

    def test_get_invalid_user(self):
        '''Buscando um usuário não registrado'''

        response = requests.get(BASE_URL+'/users/any')

        assert response.status_code == 404

    def test_update_user(self):
        response = requests.put(BASE_URL+'/users/1', json = {
            "name": "Jovani"
        })

        assert response.json()['name'] == 'Jovani' and response.status_code == 200

    def test_delete_user(self):
        response = requests.delete(BASE_URL+'/users/1')

        assert response.status_code == 200

class AuthTestCase(unittest.TestCase):
    def test_login(self):
        '''fazendo o login'''

        response = requests.post(BASE_URL+'/auth/login', json = {
            "email": "albinondjonale1@gmail.com",
            "password": "12345"
        })

        assert response.status_code == 200

    def test_inavalid_login(self):
        '''fazendo o login com dados incorretos'''

        response = requests.post(BASE_URL+'/auth/login', json = {
            "email": "albinondjonale1@gmail.com",
            "password": "1245"
        })

        assert response.status_code == 403

    def test_logout(self):
        '''fazendo o logout'''

        response = requests.post(BASE_URL+'/auth/logout/1')

        assert response.status_code == 200

    def test_invalid_logout(self):
        '''fazendo o logout de um usuario não registrado'''

        response = requests.post(BASE_URL+'/auth/logout/any')

        assert response.status_code == 404

class ProjectTestCase(unittest.TestCase):
    '''Testes para os endpoint's projects/ e projects/{project_id}'''

    def test_create_project(self):
        response = requests.post(BASE_URL+'/projects', json = {
            "title": "desenvolver o app 'Gestor de Projecto'",
            "description": "O 'Gestor de Projecto' é um app web com a função de gerenciar projectos de toda natureza",
            "admin_id": 1,
            "started": "2024-07-27"
        })

        assert response.status_code == 201

    def test_create_invalid_project(self):
        '''
        Criando um projeto com dados invalido

        falta o attr 'description' e o attr 'admin_id' deve ser um inteiro
        '''
        
        response = requests.post(BASE_URL+'/projects', json = {
            "title": "desenvolver o app 'Gestor de Projecto'",
            "admin_id": '1',
            "started": "2024-07-27"
        })

        assert response.status_code == 400

    def test_get_project(self):
        response = requests.get(BASE_URL+'/projects/1')

        assert response.status_code == 200

    def test_get_invalid_project(self):
        response = requests.get(BASE_URL+'/projects/any')

        assert response.status_code == 404

    def test_update_project(self):
        response = requests.put(BASE_URL+'/projects/1', json = {
            "budget": 500.0
        })

        assert response.json()['budget'] == 500.0 and response.status_code == 200

    def test_delete_project(self):
        response = requests.delete(BASE_URL+'/projects/1')

        assert response.status_code == 200

unittest.main()