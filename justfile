types:
    pyright src

format:
    black **/*.py

lint:
    ruff check --fix 
