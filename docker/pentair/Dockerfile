# specify the node base image with your desired version node:<version>
FROM balenalib/raspberrypi3-debian-node:latest
# replace this with your application's default port


ENV SL_IP_ADDRESS=192.168.87.3
ENV SL_PORT=80
ENV SL_NAME=
ENV FEATURES_LOCATION=


WORKDIR /usr/src/app
COPY screenlogic-api/package*.json ./
COPY screenlogic-api/*.js ./

RUN npm install

EXPOSE 3000 1444/udp

CMD ["node", "server.js"]


