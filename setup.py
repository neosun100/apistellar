# -*- coding:utf-8 -*-
import os
import re
import string

from contextlib import contextmanager
from setuptools import setup, find_packages


def get_version(package):
    """
    Return package version as listed in `__version__` in `__init__.py`.
    """
    init_py = open(os.path.join(package, '__init__.py'),'r', encoding='UTF-8').read()
    mth = re.search("__version__\s?=\s?['\"]([^'\"]+)['\"]", init_py)
    if mth:
        return mth.group(1)
    else:
        raise RuntimeError("Cannot find version!")


def install_requires():
    """
    Return requires in requirements.txt
    :return:
    """
    try:
        with open("requirements.txt") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except OSError:
        return []

try:
    LONG_DESCRIPTION = open("README.rst").read()
except UnicodeDecodeError:
    LONG_DESCRIPTION = open("README.rst", encoding="utf-8").read()


@contextmanager
def cfg_manage(cfg_tpl_filename):
    if os.path.exists(cfg_tpl_filename):
        cfg_file_tpl = open(cfg_tpl_filename)
        buffer = cfg_file_tpl.read()
        try:
            with open(cfg_tpl_filename.rstrip(".tpl"), "w") as cfg_file:
                cfg_file.write(string.Template(buffer).substitute(
                    pwd=os.path.abspath(os.path.dirname(__file__))))
            yield
        finally:
            cfg_file_tpl.close()
    else:
        yield


with cfg_manage(__file__.replace(".py", ".cfg.tpl")):
    setup(
        name="apistellar",
        version=get_version("apistellar"),
        description="enhance apistar web framework. ",
        long_description=LONG_DESCRIPTION,
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.6",
            "Intended Audience :: Developers",
            "Operating System :: Unix",
        ],
        keywords="apistar",
        author="cn",
        author_email="cnaafhvk@foxmail.com",
        url="https://www.github.com/ShichaoMa/apistellar",
        entry_points={
            "console_scripts": [
                "apistar-create = apistellar:main",
                "apistar-console = apistellar:console",
                "apistar-routes = apistellar:show_routes"
            ]
        },
        license="MIT",
        packages=find_packages(exclude=("tests*",)),
        install_requires=install_requires(),
        include_package_data=True,
        zip_safe=True,
        setup_requires=["pytest-runner"],
        tests_require=["pytest-apistellar", "pytest-asyncio", "pytest-cov"]
    )
