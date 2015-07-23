# Fiware api blueprint renderer

Tool for parsing a FIWARE specification file and rendering it to a HTML page.

## Dependencies

* [Python 2](https://www.python.org/)
* [drafter](https://github.com/apiaryio/drafter)
* [Jinja2](http://jinja.pocoo.org/)
* [Python Markdown](http://pythonhosted.org/Markdown/)

## Install

Before using fabre, we need to install Drafter, an API Blueprint parser:

```
git clone --recursive git://github.com/apiaryio/drafter.git
cd drafter
./configure
make drafter
sudo make install
```

Once installed Drafter, we can download fabre and install it as a PIP package:

```
git clone git@github.com:FiwareULPGC/fiware-api-blueprint-renderer.git
cd fiware-api-blueprint-renderer
sudo python setup.py install
```

Now we can test fabre. As an example, we can run the following commands for generating a site from the given FIWARE specification template:

```
fabre apib-example/template-fiware-open-spec2.apib ~/out
```

Fabre arguments are listed below:

1. Path to the FIWARE API specification file.
2. Path to the destination directory where the generated web page will be generated.

**Note for developers:** fabre generates some temporary files on /var/tmp while rendering the final web page, and removes them afterwards. We can override this behaviour and make fabre to keep the temporary files by simply passing an extra “0” argument to the command call.

```
fabre apib-example/template-fiware-open-spec2.apib ~/out 0
```
