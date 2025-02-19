from setuptools import setup, find_packages

# Read dependencies from base.txt
def read_requirements(filename):
    with open(filename, "r") as f:
        return f.read().splitlines()

setup(
    name="BDA",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=read_requirements("requirements/base.txt"),
    extras_require={
        "dev": read_requirements("requirements/dev.txt"),
    },
    entry_points={
        "console_scripts": [
            "run_cleaner=src.data_ingestion.cleaner:main",
            "run_combine=src.data_ingestion.combine_data:main",
            "run_upload=src.data_ingestion.upload_csv:main",
            "run_viz=src.data_viz.data_viz:main",
            "run_pipeline=src.main:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

