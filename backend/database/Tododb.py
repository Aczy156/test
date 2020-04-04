from backend.models import Todo
import backend.config as config
from backend.models import Todo


def dataComputeOne(sqlString):
    cursor = config.connection.cursor()
    cursor.execute(sqlString)
    result = cursor.fetchone()
    return result


def dataComputeAll(sqlString):
    cursor = config.connection.cursor()
    cursor.execute(sqlString)
    result = cursor.fetchall()
    return result


def getTodoById(id):
    queryUserSql = "SELECT `id`,`text`, `done`, `user_id` FROM `todolog` WHERE id='" + id + "'"
    result = dataComputeOne(queryUserSql)
    return ''


def getTodoListByUserId(user_id):
    queryUserSql = "SELECT `id`,`username`, `password`, `user_id` FROM `todolog` WHERE user_id='" + user_id + "'"
    result = dataComputeAll(queryUserSql)
    print(queryUserSql)
    list = []
    for row in result:
        list.append(Todo(id=row[0], text=row[1], done=row[2], user_id=row[3]))
    return list
