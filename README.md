# Skibidi Query Engine - User Instruction

Hi! Welcome to the skibidi project. This is where you can acknowledge how to use our library. We work with **pdm**, so firstly you need to install it.
```bash
pip install pdm
```


# Build the package
1. **Clone the repository**:
```bash
git clone https://github.com/sysy-inc/zprp-23z-python-orm
cd zprp-23z-python-orm
```
2. **Change the branch to *query-engine***
```bash
git checkout query-engine
```
3. **Install the dependencies**
```bash
pdm install
```
4. **Build the package**
```bash
pdm build
```

## Installing the package
1. **Install the package**
```bash
pip install skibidi_orm-0.1.0-py3-none-any.whl 
```

## Building Documentation with Sphinx

1. **Navigate to the `docs` directory**
```bash
cd docs
```
2. **Create HTML documentation**
```bash
pdm run make html
```

## Running tests with Tox and Pytest
1. **Run all tests with Tox**
```bash
tox
```
2. **Run all tests with Pytest**
```bash
pdm run pytest
```
