FROM alpine
# load any public updates from Alpine packages
RUN apk update
# upgrade any existing packages that have been updated
RUN apk upgrade
# add/install python3 and related libraries
# https://pkgs.alpinelinux.org/package/edge/main/x86/python3
RUN apk add g++ python3-dev libffi-dev openssl-dev python3 git
RUN python3 -m ensurepip
# make a directory for our application
RUN mkdir -p /opt/odc-monitor
RUN git clone https://github.com/vijaya2911/mon /opt/odc-monitor
# move requirements file into the container
#COPY src /opt/odc-monitor
# install the library dependencies for this application
RUN pip3 install -r /opt/odc-monitor/src/requirements.txt
ENTRYPOINT ["python3"]
CMD ["/opt/odc-monitor/src/odcmonitor.py"]
