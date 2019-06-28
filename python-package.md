# Create python package

Here is the [link](https://packaging.python.org/tutorials/packaging-projects/) of tutorial.

Once the package is set up, to build the package, run

```command line
python3 setup.py sdist bdist_wheel
```

To upload to test pypi package repository, run

```command line
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

To upload to pypi package repository, run

```command line
python3 -m twine upload dist/*
```

To install from local

```command line
pip install .
```

To install from tar.gz

```command line
pip install openaihub.0.0.1.tar.gz
```

To install from test.pypi.org

```command line
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps openaihub
```