import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Connecting...")

try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password=''
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Wrong user or password')
    else:
        print(err.msg)

cursor = conn.cursor()

cursor.execute('DROP DATABASE IF EXISTS `jogoteca`')

cursor.execute('CREATE DATABASE `jogoteca`')

cursor.execute('USE `jogoteca`')

# Create Tables

TABLES = {}

TABLES['Jogos'] = ('''
    CREATE TABLE `jogos` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `nome` VARCHAR(50) NOT NULL,
        `categoria` VARCHAR(40) NOT NULL,
        `console` VARCHAR(20) NOT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''
)

TABLES['Usuarios'] = ('''
    CREATE TABLE `usuarios` (
        `nome` VARCHAR(50) NOT NULL,
        `nickname` VARCHAR(50) NOT NULL,
        `senha` VARCHAR(100) NOT NULL,
        PRIMARY KEY (`nickname`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''
)

for table_name in TABLES:
    table_sql = TABLES[table_name]
    try:
        print('Creating table {}'.format(table_name), end=' ')
        cursor.execute(table_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Error: Table already exists')
        else:
            print(err.msg)
    else:
        print('OK')

# Insert Users

users_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s);'
users = [
    ('Paulo','paulo',generate_password_hash('teste').decode('utf8')),
    ('Lucas','lucas',generate_password_hash('teste').decode('utf8')),
    ('João','joao',generate_password_hash('teste').decode('utf8'))
]

cursor.executemany(users_sql, users)

cursor.execute('select * from jogoteca.usuarios;')
print(' ----------------- Usuários ------------------- ')
for user in cursor.fetchall():
    print(user[1])

# Inser Games

games_sql = 'INSERT INTO jogos (nome, categoria, console) VALUES (%s, %s, %s);'
games = [
    ('Tetris', 'Puzzle', 'Atari'),
    ('God of War','Hack n Slash', 'PS2'),
    ('Mortal Kombat', 'Fight', 'PS2'),
    ('Valorant', 'FPS', 'PC')
]

cursor.executemany(games_sql, games)

cursor.execute('select * from jogos')
print('  -------- Jogos ----------- ')
for game in cursor.fetchall():
    print(game[1])


# Commit and close
conn.commit()

cursor.close()
conn.close()