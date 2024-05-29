sql_table1 = """
    CREATE TABLE table1 (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
"""
sql_table2 = """
    CREATE TABLE table2 (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
"""

sql_table_primary_key_not_null = """
    CREATE TABLE table_primary_key_not_null (
        id INTEGER PRIMARY KEY NOT NULL
    );
"""

sql_schema_with_fks = [
    """
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""",
    """
    CREATE TABLE posts (
        post_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        post_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
""",
    """
    CREATE TABLE comments (
        comment_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        user_idd INTEGER NOT NULL,
        post_id INTEGER NOT NULL,
        comment_text TEXT NOT NULL,
        comment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_idd, username) REFERENCES users(user_id, username),
        FOREIGN KEY (post_id) REFERENCES posts(post_id)
    );
""",
]

sql_table_user = """
    CREATE TABLE User (
        user_id INTEGER PRIMARY KEY,
        user_name TEXT NOT NULL
    );
"""
sql_table_post = """
    CREATE TABLE Post (
        post_id INTEGER PRIMARY KEY,
        post_name TEXT NOT NULL
    );
"""

sql_table_comment = """
    CREATE TABLE Comment (
        comment_id INTEGER PRIMARY KEY,
        comment_name TEXT NOT NULL
    );
"""

sql_table_primary_key_not_null = """
    CREATE TABLE table_primary_key_not_null (
        id INTEGER PRIMARY KEY NOT NULL
    );
"""


sql_simple_db = [
    """
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL
    );
"""
]

sql_double_pk_db = [
    """
    CREATE TABLE Orders (
        order_id INTEGER,
        product_id INTEGER,
        PRIMARY KEY (order_id, product_id)
    );
"""
]

sql_simple_insert = [
    """
    INSERT INTO users (user_id, username) VALUES
    (1, 'test1'),
    (2, 'test2'),
    (3, 'test3')
;
"""
]
