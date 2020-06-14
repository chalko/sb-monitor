# Use the official image as a parent image.
FROM balenalib/raspberrypi3-debian:latest

# Set the working directory.
WORKDIR /usr/src/app

RUN install_packages collectd


COPY collectd.conf /etc/collectd/collectd.conf
COPY collectd.conf.d /etc/collectd/collectd.conf.d

EXPOSE 25826

# Run the specified command within the container.
CMD [ "/usr/sbin/collectd", "-f" ]
