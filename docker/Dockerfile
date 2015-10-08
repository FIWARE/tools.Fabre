# Fabre Dockerfile
# https://github.com/FiwareULPGC/fiware-api-blueprint-renderer
#
# Usage for HTML output:
#
#     docker run -it --rm -v /home/login/project/doc/apib:/apib fabre -i /apib/spec.apib -o /apib/html
#
# Usage for PDF output:
#
#     docker run -it --rm -v /home/login/project/doc/apib:/apib fabre -i /apib/spec.apib -o /apib/spec.pdf --pdf
#

FROM ubuntu

RUN apt-get update -y && apt-get install -y git python python-pip wget build-essential

# Install drafter
RUN git clone --recursive --branch v0.1.9 --depth 1 git://github.com/apiaryio/drafter.git && cd drafter && ./configure && make drafter && make install && cd

# Install Fabre
RUN git clone --depth 1 git://github.com/FiwareULPGC/fiware-api-blueprint-renderer.git && cd fiware-api-blueprint-renderer && python setup.py install && cd

# Install wkhtmltopdf
RUN apt-get install -y -f fontconfig libfontconfig1 libfreetype6 libjpeg-turbo8 libxrender1 xfonts-base xfonts-75dpi
RUN wget http://download.gna.org/wkhtmltopdf/0.12/0.12.2.1/wkhtmltox-0.12.2.1_linux-trusty-amd64.deb && dpkg -i wkhtmltox-0.12.2.1_linux-trusty-amd64.deb

ENTRYPOINT ["fabre"]
