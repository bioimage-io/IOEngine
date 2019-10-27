"""Install package."""
from pathlib import Path

import setuptools

PROJECT_DIR = Path(__file__).parent.resolve()
LONG_DESCR = (PROJECT_DIR / "README.md").read_text(encoding="utf-8")
REQUIRES = ["imageio", "numpy", "pyyaml", "torch", "tqdm"]

setuptools.setup(
    name="unet2d",
    version="0.1.0",
    author="bioimage-io authors",
    author_email="example@email.com",
    description="Example unet2d model for the model zoo",
    long_description=LONG_DESCR,
    packages=setuptools.find_packages(),
    install_requires=REQUIRES,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
