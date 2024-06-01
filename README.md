# Skibidi Query Engine - User Instruction

Hi! Welcome in skibidi project. This is where you can zapoznać się z działaniem library. We work with **pdm** so need to install it
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

## Installing the Package

1. **Install the package**
```bash
pdm install -G :all  # tutaj to trzeba podmienić
```

## Building Documentation with Sphinx

1. **Navigate to the `docs` directory**
```bash
cd docs
```
2. **Make HTML documentation**
```bash
make html
```

## Running Tests with Tox and Pytest
1. **Run all tests with Tox**
```bash
tox
```
2. **Run tests with Pytest**
```bash
pytest
```
