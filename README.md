Реализация тестов для API TODO с помощью библиотеки pytest. 

Тесты написаны исходя из того, что сам REST API-сервис TODO реализован на фреймворке Django.
В файле models.py создана модель Todo, на основе которой осуществляются CRUD-операции.

В файле tests.py находятся тесты, написанные для управления контентом:

Получить все памятки пользователя GET /todos/<username: str>
Получить памятку пользователя по Id памятки: GET /todos/<username: str>/<todo_id: int>
Создать памятку POST /todos/<username: str>/<todo_id: int> {«text»: str, «status»: str}
поле статус может содержать только значения: 'TODO', 'INPROGRESS', 'DONE', 'CANCELED'
Редактировать памятку PUT /todos/<username: str>/<todo_id: int> {«text»: str, «status»: str}
Удалить памятку DELETE /todos/<username: str>/<todo_id: int>
