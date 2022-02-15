from setuptools import setup, find_packages

requirements = open('requirements.txt','r').read()

setup(
    name="Meduso Server + GUI",
    version="1.0.0",
    description="This is the backend server with the GUI for the Meduso tool. An open-source post-exploitation tool.",
    packages=find_packages(),
    install_requires=requirements
)