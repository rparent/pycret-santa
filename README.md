This package will help you organize a [Secret Santa][wiki-article] and keep the randomly assigned persons secret to everybody.

**Installation**

    python setup.py install

or directly with `pip`

    pip install pycret-santa


**How to run it**

Once the package is installed, create your config file and then simply run

    secretsanta <path_to_your_config_file>

The config file is written in yaml, an example is available in pycret_santa/sample.yaml.


**Tests**

You can launch tests by running

    python setup.py nosetests


[wiki-article]: http://en.wikipedia.org/wiki/Secret_Santa
