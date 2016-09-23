# FIWARE API Blueprint renderer RELEASE NOTES

## Version v0.3.2.1
### Release date 23/09/2016

### Fixed bugs
* During PDF generation, if links or inline codes are too long, they are broken into multiple lines.

---- 

## Version v0.3.1.1
### Release date 22/09/2016

### Fixed bugs
* During PDF generation, if links or inline codes are too long, they are broken into multiple lines.

---- 

## Version v0.3.2
### Release date 05/02/2016 

### New features
* Added Quick Start Guide (with Docker) to README.md
* Now, all metadata are mandatory (except PREVIOUS_VERSION).
* License section added.
* Now, Copyright and License are mandatory.
* Repository transfered to FIWARE organization.
* Docker image available in Docker Hub.

### Fixed bugs
* Unified name styles for files and folders


## Version v0.3.1
### Release date 17/12/2015 

### New features
* Added URI parameters instantiation for requests with no URI specified.
* Payload definitions moved from examples to specifications.
* Now FABRE instantiates an example request and response body if its specification has defined values.
* Changed output format for "fabre --version-dependencies".
* Added support to use defined data structures inside resources.
* Added a Dockerfile that allows use FABRE using a docker VM.
* Now the project uses continuos integration using Travis CI <http://travis-ci.org>.
* Added support for external CSS loading via metadata keywords **CSS** and **CSS-PDF**.
* Link to github source code will be generated from metadatum keyword **GITHUB_SOURCE**.
* Now response blocks are paired with request blocks.
* Now request examples do not get listed under the action definition. All requests are considered examples unless they end their ID with **-no-example**.
* Output PDF files will not add navigability links between sections.
* Output PDF files will not expand links inside the content of sections but they will be expanded in the **References** section.
* Apiary project and github source links now appear in the **References** section.
* PDF TOC now starts from API Summary section

### New dependencies
* [lxml](http://lxml.de/)
* [cssselect](https://github.com/SimonSapin/cssselect/)
* [pyquery](https://github.com/gawel/pyquery/)

### Fixed bugs
* All instances of 'not required' changed to 'optional'.
* All description sections get properly parsed to markdown.
* Added support to render description from 'Data Structures' section (left separate by drafter v0.1.9).
* Removed *.py and *.pyc files from the generated sited.
* Fixed some reference links that appear together.
* Avoid duplicating links in the reference sections.
* When TITLE metadatum is not defined, the H1 title is the first markdown title found in the document.
* Fixed wrong separation of files for APIB and extra sections.
* Fixed wrong condition check when rendering section "Common Payload Definitions".
* Fixed wrong link generation for latest version.
* Fixed ordination of recursive payload parameters.
* Fix generation of empty sections in Examples section when examples are not defined.
* Fix generation of Example section only when the apib has examples defined.
* Fix bug with extra sections separation from APIB specification.

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

