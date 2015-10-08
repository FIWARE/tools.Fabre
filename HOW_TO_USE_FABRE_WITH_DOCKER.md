# How to use FABRE with Docker

A dockerfile that allows to create a virtual machine with FABRE is provided in the docker directory. This document has the basic guidelines to use this new feature.

## Steps

### Build docker image
From the project directory execute:

```
sudo docker build -t fabre:0.3.0 docker/
```

### Create directories for docker volume and populate them with the apib file. 
In this case we use the provided apib examples.

```
mkdir -p /var/tmp/test-fabre-docker/apib/html
```

```
cp -R apib-example/* /var/tmp/test-fabre-docker/apib
```

### Run FABRE with the docker image
```
docker run -it --rm -v /var/tmp/test-fabre-docker/apib:/apib -v /var/tmp/test-fabre-docker/apib/html:/html fabre:0.3.0 -i /apib/fiware-ngsi-v2.apib -o /html/fiware-ngsi-v2
```

Note that the host  ```/var/tmp/test-fabre-docker/apib``` directory is linked to the VM machine ```/apib``` directory.

The output is saved to ```/html/fiware-ngsi-v2``` in the virtual machine that corresponds to ```/var/tmp/test-fabre-docker/apib/html/fiware-ngsi-v2``` in the host.


# Other considerations

You can use previous versions of FABRE if you changes the version in:

*    Dockerfile: ```ENV FABRE_VERSION <version>```

*    Build docker image step: ```sudo docker build -t fabre:<verion> docker/```

*    Run FABRE step: ```docker run ..... fabre:<version> ......``` 