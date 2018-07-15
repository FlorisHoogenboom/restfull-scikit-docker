from setuptools import setup

setup(
    name='restfull-scikit-docker',
    version='0.1',
    packages=[], # Setup.py merely serves as a tool for testing and specifying dependencies.
    url='https://github.com/FlorisHoogenboom/restfull-scikit-docker',
    license='MIT',
    author='Floris Hoogenboom',
    author_email='floris.hoogenboom@futurefacts.nl',
    description='A simple RESTfull wraper for Scikit-learn models.',
    install_requires = [
        'numpy',
        'scipy',
        'scikit-learn',
        'marshmallow',
        'flask',
        'werkzeug',
        'flask_json',
        'keras',
        'datauri'
    ],
    test_requires = [
        'nose'
    ]
)
