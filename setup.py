from setuptools import setup, find_packages

setup(
    name='PyLaunchBar',
    version='1.0.0',
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={
        "PyLaunchBar": ["config/*.json", "data/*.qml"]
    },
    install_requires=["PyQt5;python_version<'5.15.6'"],
    python_requires=">=3.8",
    url='',
    license='MIT',
    author='lorenzo',
    author_email='croceclaudio57@gmail.com',
    description='A simple bar launcher in python',
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "PyLaunchBar = PyLaunchBar.main:start",
        ]
    }
)
