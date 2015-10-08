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

ENV FABRE_VERSION 0.3.0

RUN apt-get update -y && apt-get install -y unzip git python python-pip wget build-essential

# Install drafter
RUN git clone --recursive --branch v0.1.9 --depth 1 git://github.com/apiaryio/drafter.git && cd drafter && ./configure && make drafter && make install && cd

# Install Fabre
RUN wget https://github.com/FiwareULPGC/fiware-api-blueprint-renderer/archive/v$FABRE_VERSION.zip && unzip v$FABRE_VERSION.zip && cd fiware-api-blueprint-renderer-$FABRE_VERSION && python setup.py install && cd

# Install wkhtmltopdf
RUN apt-get install -y -f fontconfig libfontconfig1 libfreetype6 libjpeg-turbo8 libxrender1 xfonts-base xfonts-75dpi
RUN wget http://download.gna.org/wkhtmltopdf/0.12/0.12.2.1/wkhtmltox-0.12.2.1_linux-trusty-amd64.deb && dpkg -i wkhtmltox-0.12.2.1_linux-trusty-amd64.deb

ENTRYPOINT ["fabre"]
