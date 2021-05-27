import pytest

from models import Todo


class TestTodoAPI:

    @pytest.mark.django_db(transaction=True)
    def test_todo_not_found(self, user_client, username):
        response = user_client.get(f'/todos/{username}/')

        assert response.status_code != 404, (
            'Страница `/todos/{username}/` не найдена'
        )


    @pytest.mark.django_db(transaction=True)
    def test_todo_get(self, user_client, username):
        response = user_client.get(f'/todos/{username}/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/todos/{username}/` с токеном авторизации возвращается статус 200'
        )

        test_data = response.json()

        assert type(test_data) == list, (
            'Проверьте, что при GET запросе на `/todos/{username}/` возвращается список'
        )

        assert len(test_data) == Todo.objects.filter(username=username).count(), (
            'Проверьте, что при GET запросе на `/todos/{username}/` возвращается весь список памяток'
        )

        todo = Todo.objects.filter(username=username)[0]
        test_todo = test_data[0]
        assert 'id' in test_todo, (
            'Проверьте, что поле `id` существует в тестовых данных'
        )
        assert 'text' in test_todo, (
            'Проверьте, что поле `text` существует в тестовых данных'
        )
        assert 'status' in test_todo, (
            'Проверьте, что поле `status` существует в тестовых данных'
        )
        assert 'username' in test_todo, (
            'Проверьте, что поле `username` существует в тестовых данных'
        )
        assert test_todo['username'] == todo.username, (
            'Проверьте, что поле `username` совпадает'
        )


    @pytest.mark.django_db(transaction=True)
    def test_todo_create(self, user_client, username, user):
        todo_count = Todo.objects.count()
        status = ['TODO', 'INPROGRESS', 'DONE', 'CANCELED']

        data = {}
        response = user_client.post(f'/todos/{username}/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе на `/todos/{username}/` с не правильными данными возвращается статус 400'
        )

        data = {'text': 'Написать тесты для API', 'status': 'INPROGRESS'}
        response = user_client.post(f'/todos/{username}/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе на `/todos/{username}/` с правильными данными возвращается статус 201'
        )

        test_data = response.json()

        assert test_data.get('text') == data['text'], (
            'Проверьте, что при POST запросе на `/todos/{username}/` текст совпадает'
        )

        assert type(test_data) == dict, (
            'Проверьте, что при POST запросе на `/todos/{username}/` возвращается словарь с данными новой памятки'
        )

        assert test_data.get('username') == user.username, (
            'Проверьте, что при POST запросе на `/todos/{username}/` создается памятка от авторизованного пользователя'
        )

        assert test_data.get('status') in status, (
            'Проверьте, что при POST запросе на `/todos/{username}/` в статусе указано корректное значение'
        )

        assert todo_count + 1 == Todo.objects.filter(username=username).count(), (
            'Проверьте, что при POST запросе на `/todos/{username}/` создается памятка'
        )

    @pytest.mark.django_db(transaction=True)
    def test_todo_get_current(self, user_client, todo, user, username):
        response = user_client.get(f'/todos/{username}/{todo.id}/')

        assert response.status_code == 200, (
            'Страница `/todos/{username}/{id}/` не найдена'
        )

        test_data = response.json()
        assert test_data.get('text') == todo.text, (
            'Не найдено или не правильное значение поля `text`'
        )
        assert test_data.get('text') == todo.status, (
            'Не найдено или не правильное значение поля `status`'
        )
        assert test_data.get('username') == user.username, (
            'Не найдено или не правильное значение поля `username`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_todo_patch_current(self, user_client, username, todo):
        response = user_client.patch(f'/todos/{username}/{todo.id}/',
                                     data={'text': 'Поменяли текст памятки', 'status': 'DONE'})
        status = ['TODO', 'INPROGRESS', 'DONE', 'CANCELED']

        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/todos/{username}/{id}/` возвращаете статус 200'
        )

        test_todo = Todo.objects.filter(id=todo.id)

        assert test_todo, (
            'Проверьте, что при PATCH запросе `/todos/{username}/{id}/` вы не удалили памятку'
        )

        assert test_todo.get('text') == 'Поменяли текст памятки', (
            'Проверьте, что при PATCH запросе `/todos/{username}/{id}/` вы изменяете памятку'
        )

        assert test_todo.get('status') in status, (
            'Проверьте, что при POST запросе на `/todos/{username}/{id}/` в статусе указано корректное значение'
        )


    @pytest.mark.django_db(transaction=True)
    def test_todo_delete_current(self, user_client, username, todo):
        response = user_client.delete(f'/todos/{username}/{todo.id}/')

        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе `/todos/{username}/{id}/` возвращаете статус 204'
        )

        test_todo = Todo.objects.filter(id=todo.id)

        assert not test_todo, (
            'Проверьте, что при DELETE запросе `/todos/{username}/{id}/` вы удалили памятку'
        )
