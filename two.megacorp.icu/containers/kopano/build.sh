#!/bin/bash
set -e

podman build base -t kopano-base:latest
#podman build archiver -t kopano-archiver:latest
podman build core -t kopano-core:latest
podman build webapp -t kopano-webapp:latest
podman build webapp-frontend -t kopano-webapp-frontend:latest
podman build search -t kopano-search:latest
podman build spooler -t kopano-spooler:latest
podman build dagent -t kopano-dagent:latest
podman build gateway -t kopano-gateway:latest
podman build z-push -t kopano-z-push:latest
podman build z-push-frontend -t kopano-z-push-frontend:latest
podman build ical -t kopano-ical:latest
podman build kdav -t kopano-kdav:latest
podman build kdav-frontend -t kopano-kdav-frontend:latest
podman build spamd -t kopano-spamd:latest
#podman build db -t kopano-db:latest
