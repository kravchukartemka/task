import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Загрузка учетных данных из файла ключа службы Google API
key = service_account.Credentials.from_service_account_file('key.json')
# Создание экземпляра API-клиента
user = build('tasks', 'v1', credentials=key)

# Получение списка всех задач
results = user.tasks().list(tasklist='@default').execute()
tasks = results.get('items', [])
# Перебор всех задач и установка срока выполнения, если дата не указана
for task in tasks:
    task_id = task['id']
    title = task['title']
    due = task.get('due')
    if not due:
        # Установка срока выполнения через час от текущего времени
        due = (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat()
        user.tasks().update(tasklist='@default', task=task_id, body={'due': due}).execute()
        print(f'Срок выполнения задачи "{title}" установлен на {due}')
user.close()