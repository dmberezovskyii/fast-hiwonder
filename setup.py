from setuptools import setup, find_packages

setup(
    name="turbopi_fast_sdk",
    version="0.1.0",
    description="Це Python SDK для керування апаратним забезпеченням Turbopi через швидку комунікацію.",
    long_description=open('README.md').read(),  # Довгий опис буде зчитуватися з README.md
    long_description_content_type='text/markdown',
    author="Ваше ім'я",
    author_email="ваш_email@example.com",
    license="MIT",
    url="https://github.com/yourusername/turbopi_fast_sdk",
    packages=find_packages(),
    install_requires=[
        # Ваші залежності
    ],
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
