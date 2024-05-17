import os
import shutil
import pytest


@pytest.fixture
def clear_local_tmp_dir():
    if os.path.exists("./tmp"):
        shutil.rmtree("./tmp")
    os.mkdir("./tmp")
