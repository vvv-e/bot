start = 'Вы открыли <b>Панель администратора</b>'

def statistick(count):
    text = f'Количество пользователей бота: <pre>{count}</pre>'
    return text


ban_from_admin_start = '''Укажите ID пользователя, которого хотите заблокировать!

<i>Пример: 1046276866

Если не хотите блокировать пользователя, нажмите /cancel</i>'''

ban_from_admin_except = '''❗️ Ошибка. Указывайте цифрами ❗️
Укажите ID пользователя, которого хотите заблокировать!

<i>Пример: 1046276866

Если не хотите блокировать пользователя, нажмите /cancel</i>'''

ban_from_admin_cancel = '❌ Вы отменили блокировку'

ban_from_admin_finaly = '✅ Вы успешно заблокировали пользователя!'

ban = 'Вы заблокированы!'