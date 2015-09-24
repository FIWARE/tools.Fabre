# Troubleshooting

 
## jinja2.exceptions.UndefinedError: list object has no element 0

Probably you have installed a newer version of Dratfer that is not compatible with FABRE.

### Steps

* Check the installed Drafter version with ```drafter --version```. If the version is greatest than **v0.1.9** you should downgrade Drafter.
* Install the latest compatible version of drafter with:
```
 git clone --recursive --branch v0.1.9 --depth 1 git://github.com/apiaryio/drafter.git
 cd drafter
 ./configure
 make drafter
 sudo make install

```


## wkhtmltopdf "cannot connect to X server"

Probably you have installed a older verson of wkhtmltopdf. It ussually occurs if you install wkhtmltopdf via package manager.

### Steps
* check the installed version of wkhtmltopdf with ```wkhtmltopdf --version```. If the version is lower than **0.12.2.1 (with patched qt)** or it is not QT parched (it should to appear in the version), you should download the latest version from <http://wkhtmltopdf.org/downloads.html>.


## Other errors

* Check if  you are using the laste version of FABRE. You can check the version of the current FABRE installation with ``` fabre --version```. If you do not have the latest version, install it following the instrucctions detailed in the [README](README.md) file.

* Check the system dependencies with ```fabre --version-dependencies```, it should return something like
```
PIP dependencies

	jinja2>=2.7.3
	markdown>=2.6.2
	mdx-linkify>=0.6

System dependencies

	Drafter 0.1.9
	wkhtmltopdf 0.12.2.1 (with patched qt)
```
You should ensure that Drafter version is exactly 0.1.9 and the wkhtmltopdf is greater or equal than 0.12.2.1 with patched qt.

If this guide does not solve your problem contact us at <fiware@ulpgc.es>