from setuptools import setup, find_packages

setup(
    name="voicesep",
    version="1.0.0",
    description="Voice separation utility",
    packages=find_packages()
    install_requres=[
        "h5py",
        "music21",
        "numpy",
        "theano"
    ]
)
