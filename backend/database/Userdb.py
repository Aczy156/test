from backend import config
from backend.models import User


def dataCompute(sqlString):
    cursor = config.connection.cursor()
    cursor.execute(sqlString)
    result = cursor.fetchone()
    return result


def getUserById(id):
    queryUserSql = "SELECT `id`,`username`, `password` FROM `user` WHERE id='" + id + "'"
    result = dataCompute(queryUserSql)
    return User(id=result['id'], username=result['username'], password=result['password'])


def getUserByUsername(username):
    queryUserSql = "SELECT `id`,`username`, `password` FROM `user` WHERE username='" + username + "'"
    result = dataCompute(queryUserSql)
    return User(id=result['id'], username=result['username'], password=result['password'])
