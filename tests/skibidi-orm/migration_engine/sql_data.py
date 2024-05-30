class SQLite3TablesData:
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


class PostgresTablesData:
    sql_table1 = SQLite3TablesData.sql_table1
    sql_table2 = SQLite3TablesData.sql_table2
    sql_table_primary_key_not_null = SQLite3TablesData.sql_table_primary_key_not_null
    sql_schema_with_fks = SQLite3TablesData.sql_schema_with_fks
    sql_table_user = SQLite3TablesData.sql_table_user
    sql_table_post = SQLite3TablesData.sql_table_post
    sql_table_comment = SQLite3TablesData.sql_table_comment
    sql_table_primary_key_not_null = SQLite3TablesData.sql_table_primary_key_not_null
    sql_simple_db = SQLite3TablesData.sql_simple_db
    sql_double_pk_db = SQLite3TablesData.sql_double_pk_db
    SQL_TABLE_MANY_COLUMNS1 = """
        CREATE TABLE table_many_columns1 (
            primary_key INTEGER PRIMARY KEY,
            text_not_null TEXT NOT NULL,
            text_nullabe TEXT,
            integer_not_null INTEGER NOT NULL,
            integer_nullable INTEGER,
            date_not_null DATE NOT NULL,
            date_nullable DATE
        );
"""
    SQL_TABLE_DIFFICULT_TYPES = """
        CREATE TABLE table_difficult_types (
            big_primary_key_alias serial8 PRIMARY KEY,
            bit_varying_alias VARBIT,
            bit_varying_alias_arg VARBIT(20),
            double_precision DOUBLE PRECISION,
            timestamp TIMESTAMP,
            timestamp_arg TIMESTAMP(2),
            timestamp_without_time_zone TIMESTAMP WITHOUT TIME ZONE,
            timestamp_without_time_zone_arg TIMESTAMP(3) WITHOUT TIME ZONE,
            timestamp_with_time_zone_alias TIMESTAMPTZ,
            timestamp_with_time_zone_arg_alias TIMESTAMPTZ(3),
            charachter_varying CHARACTER VARYING,
            charachter_varying_arg CHARACTER VARYING(40),
            charachter_varying_alias VARCHAR,
            charachter_varying_alias_args VARCHAR(40)
        );
"""
    SQL_TABLE_DIFFERECT_CONSTRAINTS = """
        CREATE TABLE table_different_constraints (
            primary_key INTEGER PRIMARY KEY,
            integer_not_nullable INTEGER NOT NULL,
            text_nullable TEXT,
            unique_column INTEGER UNIQUE,
            unique_not_nullable INTEGER NOT NULL UNIQUE,
            check_other_column INTEGER CHECK (integer_not_nullable > 100),
            default_column INTEGER DEFAULT 1,
            not_null_unique_check_column INTEGER NOT NULL UNIQUE CHECK (not_null_unique_check_column > 100),
            not_null_unique INTEGER NOT NULL UNIQUE,
            not_null_default INTEGER NOT NULL DEFAULT 1,
            not_null_unique_check_default INTEGER NOT NULL UNIQUE DEFAULT 1 CHECK (not_null_unique_check_default > 100)
        );
"""
    SQL_TABLE_SERIALS = """
        CREATE TABLE table_serials (
            serial_pk SERIAL PRIMARY KEY,
            bigserial BIGSERIAL
        );
"""
    SQL_TABLE_DEFAULTS = """
        CREATE TABLE table_defaults (
            primary_key INTEGER PRIMARY KEY,
            integer_default INTEGER DEFAULT 1,
            text_default TEXT DEFAULT 'default',
            date_default DATE DEFAULT CURRENT_DATE,
            timestamp_default TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            timestamp_default_lowercase TIMESTAMP DEFAULT current_timestamp
        );
    """
    SQL_TABLE_SIMPLE_FOREIGN_KEYS = [
        """
        CREATE TABLE authors (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );
        """,
        """
        CREATE TABLE books (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            year INT,
            author_id_foreign_key INT,
            FOREIGN KEY (author_id_foreign_key) REFERENCES authors (id)
        );
        """,
    ]
    SQL_TABLE_FKS_MORE_COMPLEX = [
        """
        CREATE TABLE departments (
            department_id SERIAL PRIMARY KEY
        );
        """,
        """
        CREATE TABLE employees (
            employee_id SERIAL PRIMARY KEY,
            department_id INTEGER NOT NULL,
            CONSTRAINT fk_department
                FOREIGN KEY (department_id)
                REFERENCES Departments(department_id)
        );
        """,
        """
        CREATE TABLE projects (
            project_id SERIAL PRIMARY KEY,
            project_name VARCHAR(255) NOT NULL,
            lead_employee_id INTEGER NOT NULL,
            support_department_id INTEGER NOT NULL,
            FOREIGN KEY (lead_employee_id) REFERENCES Employees(employee_id),
            FOREIGN KEY (support_department_id) REFERENCES Departments(department_id)
        );
        """,
    ]


class SQLite3InsertData:
    sql_simple_insert = [
        """
        INSERT INTO users (user_id, username) VALUES
        (1, 'test1'),
        (2, 'test2'),
        (3, 'test3')
    ;
    """
    ]


class PostgresInsertData:
    sql_simple_insert = SQLite3InsertData.sql_simple_insert
