from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="uptrain",
    version="0.3.2",
    description="UpTrain - ML Observability and Retraining Framework",
    long_description=long_description,
    # The project's main homepage.
    url="https://github.com/uptrain-ai/uptrain",
    # Author details
    maintainer="UpTrain AI Team",
    maintainer_email="uptrain.ai@gmail.com",
    # Choose your license
    license="Apache License 2.0",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: Apache Software License",
        # Specify the Python versions you support here. In particular, ensure
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="uptrain ai retraining ML observability",
    packages=find_packages(),
    package_data={"": ["*.pyi"]},
    install_requires=[
        "tqdm>=4.0",
        "pydantic<1.10.10",
        "aiolimiter>=1.1",
        "loguru",
        "lazy_loader",
        "networkx",
        "polars>=0.18",
        "deltalake>=0.9",
        "numpy>=1.23.0",
        "pyarrow>=10.0.0",
        "plotly>=5.0.0",
        "streamlit>=1.23",
        "httpx>=0.24.1",
        "openai>=0.27",
        "evals @ git+https://github.com/openai/evals.git",
    ],
    tests_require=["pytest>=7.0"],
)
