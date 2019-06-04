# services/users/project/tests/test_users.py


import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.utils import add_user  # nuevo



class TestUserService(BaseTestCase):
    """Tests para el servicio Users."""

    def test_users(self):
        """Asegurando que la ruta /ping  se comporta
        correctamente."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_users(self):
        """Asegurar que un nuevo usuario pueda ser
        agregado a la base de datos."""
        with self.client:
            response = self.client .post(
                '/users',
                data=json.dumps({
                    'username': 'ldragons',
                    'email': 'nickmostacero@upeu.edu.pe',
                    'password': 'greaterthaneight'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn(
                'nickmostacero@upeu.edu.pe ha sido arreglado', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Asegurando que se produzca un error si el
        objeto json esta vacio."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('carga invalida.', data['message'])
            self.assertIn('fallo', data['status'])

    def test_add_user_invalid_json_keys(self):
        """Asegurando que se produzca un error si el
        objeto json no tiene una clave username."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'email': 'nickmostacero@upeu.edu.pe',
                    'password': 'greaterthaneight'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('carga invalida.', data['message'])
            self.assertIn('fallo', data['status'])

    def test_add_user_duplicate_email(self):
        """Asegurando que se produzca un error si el email ya existe"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'ldragons',
                    'email': 'nickmostacero@upeu.edu.pe',
                    'password': 'greaterthaneight'
                }),
                content_type='application/json',
            )
            response = self .client.post(
                '/users',
                data=json.dumps({
                    'username': 'ldragons',
                    'email': 'nickmostacero@upeu.edu.pe',
                    'password': 'greaterthaneight'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Lo siento. El email ya existe.', data['message'])
            self.assertIn('fallo', data['status'])

    def test_single_user(self):
        """ Asegurando de que el usuario individual se
        comporte correctamente."""
        user = add_user('ldragons', 'nickmostacero@upeu.edu.pe', 'greaterthaneight')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('ldragons', data['data']['username'])
            self.assertIn('nickmostacero@upeu.edu.pe', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Asegúrese de que se arroje un error si no se
        proporciona una identificación."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El usuario no existe', data['message'])
            self.assertIn('fallo', data['status'])

    def test_single_user_incorrect_id(self):
        """Asegurando de que se arroje un error
        si la identificación no existe."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El usuario no existe', data['message'])
            self.assertIn('fallo', data['status'])

    def test_all_users(self):
        """ Asegurando de que todos los usuarios se
        comporten correctamente."""
        add_user('ldragons', 'nickmostacero@upeu.edu.pe', 'greaterthaneight')
        add_user('brayan', 'pibex.g.m@hotmail.es', 'greaterthaneight')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('ldragons', data['data']['users'][0]['username'])
            self.assertIn(
                'nickmostacero@upeu.edu.pe', data['data']['users'][0]['email'])
            self.assertIn('brayan', data['data']['users'][1]['username'])
            self.assertIn(
                'pibex.g.m@hotmail.es', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

    def test_main_no_users(self):
        """Asegurando que la ruta principal funcione
        correctamente cuando no hay usuarios añadidos a la base de datos"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Todos los usuarios', response.data)
        self.assertIn(b'<p>No hay usuarios!</p>', response.data)

    def test_main_with_users(self):
        """Asegurando que la ruta principal funcione
        correctamente cuando un usuario es correctamente
        agregado a la base de datos"""
        add_user('ldragons', 'nickmostacero@upeu.edu.pe', 'greaterthaneight')
        add_user('brayan', 'pibex.g.m@hotmail.es', 'greaterthaneight')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Todos los usuarios', response.data)
            self.assertNotIn(b'<p>No hay usuarios!</p>', response.data)
            self.assertIn(b'ldragons', response.data)
            self.assertIn(b'brayan', response.data)

    def test_main_add_user(self):
        """Asegurando que un nuevo usuarios pueda ser
        agregado a la db mediante un POST request"""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(
                    username='ldragons',
                    email='nickmostacero@upeu.edu.pe',
                    password='greaterthaneight'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Todos los usuarios', response.data)
            self.assertNotIn(b'<p>No hay usuarios!</p>', response.data)
            self.assertIn(b'ldragons', response.data)


if __name__ == '__main__':
    unittest.main()
