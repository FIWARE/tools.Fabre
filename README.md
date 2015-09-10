# Fiware api blueprint renderer

Tool for parsing a FIWARE specification file and rendering it to a HTML page.

## Dependencies

* [Python 2](https://www.python.org/)
* [drafter](https://github.com/apiaryio/drafter)
* [Jinja2](http://jinja.pocoo.org/)
* [Python Markdown](http://pythonhosted.org/Markdown/)
* [wkhtmltopdf](http://wkhtmltopdf.org/)

## Install

Before using FABRE, we need to install Drafter, an API Blueprint parser:

```
git clone --recursive git://github.com/apiaryio/drafter.git
cd drafter
./configure
make drafter
sudo make install
```

wkhtmltopdf is needed for pdf conversion.
Installer can be downloaded from [wkhtmltopdf](http://wkhtmltopdf.org/downloads.html)

Once  Drafter and wkhtmltopdf are installed, we can download fabre and install it like a PIP package:

```
git clone git://github.com/FiwareULPGC/fiware-api-blueprint-renderer.git
cd fiware-api-blueprint-renderer
sudo python setup.py install
```

Now we can test fabre. As an example, we can run the following commands for generating a site from the given FIWARE specification template:

```
fabre -i apib-example/template-fiware-open-spec2.apib  -o ~/out
```

In order to generate a pdf file instead a html site the --pdf option should be used. When this option is used the -o parameter can specify the ouput folder unless the provided output ends with ".pdf", in that case the -o parameter references the output file.

Examples:

```
fabre -i apib-example/template-fiware-open-spec2.apib  -o ~/out --pdf
```

Renders the apib and saves it to ~/out/template-fiware-open-spec2.pdf


```
fabre -i apib-example/template-fiware-open-spec2.apib  -o ~/out/ouput.pdf --pdf
```

Renders the apib and saves it to ~/out/output.pdf


**Note for developers:** fabre generates some temporary files on /var/tmp while rendering the final web page, and removes them afterwards. We can override this behaviour and make fabre to keep the temporary files using the --no-clear-temp-dir option.

```
fabre -i apib-example/template-fiware-open-spec2.apib -o ~/out --no-clear-temp-dir
```

FABRE accepts the options listed below:

* **-i**, **--input**: Path to the FIWARE API specification file.
* **-o**, **--output**: Path to the destination directory where the output page will be generated. If the --pdf option is specified, this parameter specifies the output filename if it ends with ".pdf"
* **--pdf**: Save to pdf instead of a html site.
* **-t**, **--template** Path to the template to be used to render the API specification file. If it is not provided, a default template is used.
* **--no-clear-temp-dir**: This option is intended for debug purposes.

**NOTE:** FABRE expects an input file with UTF-8 enconding, providing another charset may cause errors.
