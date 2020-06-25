# Use the official image as a parent image.
FROM balenalib/raspberrypi3-debian:latest

# Set the working directory.
WORKDIR /usr/src/app

RUN install_packages collectd python-requests python-beautifulsoup


COPY collectd.conf /etc/collectd/collectd.conf
COPY arris_modem_types.db /etc/collectd/arris_modem_types.db
COPY collectd.conf.d /etc/collectd/collectd.conf.d
COPY modules /etc/collectd/modules

EXPOSE 25826

# Run the specified command within the container.
CMD [ "/usr/sbin/collectd", "-f" ]
