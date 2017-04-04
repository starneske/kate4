#!/bin/bash
set -o allexport

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..

if [ -e .env ]; then
	source .env
fi
echo $KATE4_DOCKER_IMAGE_LOCAL

docker build -t $KATE4_DOCKER_IMAGE_LOCAL:$KATE4_IMAGE_VERSION . 
