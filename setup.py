"""Install package."""
from pathlib import Path

import setuptools

PROJECT_DIR = Path(__file__).parent.resolve()
LONG_DESCR = (PROJECT_DIR / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="BioEngine",
    version="0.1.0",
    url="https://github.com/bioimage-io/BioEngine",
    author="BioEngine Authors",
    author_email="example@email.com",
    description="Engine for the model zoo",
    long_description=LONG_DESCR,
    packages=setuptools.find_packages(),
    install_requires=["pyyaml"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
