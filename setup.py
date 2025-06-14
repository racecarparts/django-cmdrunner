from setuptools import setup, find_packages

setup(
    name="cmdrunner",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django>=3.2",
        "celery>=5.2",
    ],
    description="Django admin integration for running management commands with Celery",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Tom Wheeler",
    url="https://github.com/racearparts/cmdrunner",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
