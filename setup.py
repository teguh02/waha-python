"""
Setup configuration for WAHA Python Plugin
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="waha-python",
    version="1.0.0",
    author="Teguh Rijanandi",
    author_email="teguhrijanandi02@gmail.com",
    description="Unofficial WhatsApp HTTP API (WAHA) Python Client - Complete implementation of WAHA API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/teguh02/waha-python",
    project_urls={
        "Bug Tracker": "https://github.com/teguh02/waha-python/issues",
        "Documentation": "https://waha.devlike.pro",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Chat",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
)

