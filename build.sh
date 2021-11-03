#!/bin/bash

case $1 in
  --doc)
    docker run --rm -it \
    -v ${PWD}/beoremote-halo-spec.yaml:/app/asyncapi.yml \
    -v ${PWD}/output:/app/output \
    asyncapi/generator -o output /app/asyncapi.yml --force-write -p singleFile=true @asyncapi/html-template

    cp output/index.html index.html
    ;;

  --pip-package)
    python3 -m build
    ;;

  --test)
    coverage run --source=./src,./test -m pytest && coverage report
    ;;
esac
