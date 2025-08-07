# backend/setup.py

from setuptools import setup, find_packages

setup(
    name="shomer",
    version="0.1.0",
    packages=find_packages(where="."),  # vai encontrar o pacote shomer/
    install_requires=[
        "fastapi==0.95.0",
        "uvicorn[standard]==0.22.0",
        "opencv-python>=4.12.0",
        "ultralytics>=8.3.0",
        "insightface>=0.7.0",
        "onnxruntime>=1.13.0",
        "torch>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "shomer=shomer.main:main",  # expõe o comando 'shomer'
        ]
    },
)
