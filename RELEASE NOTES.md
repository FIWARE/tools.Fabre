# FIWARE API Blueprint renderer RELEASE NOTES

## Version v0.3.1
### Release date <>/<>/2015 

### New features
* Added URI parameters instantiation for requests with no URI specified.
* Payload definitions moved from examples to specifications.
* Now FABRE instantiates an example request body if its specifications has defined values.

### New dependencies
*

### Fixed bugs
* All instances of 'optional' changed to 'not equired'.
* All description sections get properly parsed to markdown.
* Added support to render description from 'Data Structures' section (left separate by drafter v0.1.9).
* Removed *.py and *.pyc files from the generated sited.
* Fixed some reference links that appear together.
* Avoid duplicating links in the reference sections

### Known bugs
* **--dpi** option in wkhtmltopdf does not work correctly. Becasuse of that, FABRE could render different PDF files in different systems.

### Other actions
* Improvements in code structure.

----


## Version v0.3.0
### Release date 25/09/2015 

### New features
* Resizable table of contents
* Autorecognized links without Markdown format
* Added SPEC_URL metadatum: Now FABRE uses this parameter instead of HOST to generate the URI to the versions specification.
* Payloads and URI parameters are now shown in alphabetical order.
* Added the --version and --version-dependencies options. They show the current version of FABRE or the installed version of the FABRE dependencies respectively.
* Removed URI from the TOC of the PDF if the element already has a name.
* Removed parameters descriptions from examples.
* Removed "Common payload definition" from API summary
* URI parameters are now sorted alphabetically
* If a request identifier has an URI with parameters, they will be sorted.
* Added man page.
* Adeed troubleshooting file.
* Now the the FIWARE logo is fixed to the top left corner.
* Changed the style of rendered parameters and payload attributes.
* Action headers splitted into two lines.
* New top buttons leading to Apiary and Github pages.

### New dependencies
* [mdx_linkify](https://github.com/daGrevis/mdx_linkify)

### Fixed bugs
* Now, actions headers in the example section are h5 instead of h4.
* The line numbers of an error shown by Drafter may not correspond with the line number in the original input file.
* Missing extra sections are now correctly included in the output HTML file.
* Minor CSS fixes related to "go to example" buttons.
* HTML escaping of version metadata strings.
* Parameters definition now renders its markdown content.

### Known bugs
* **--dpi** option in wkhtmltopdf does not work correctly. Becasuse of that, FABRE could render different PDF files in different systems.

----
