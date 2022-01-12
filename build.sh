#!/bin/bash

case $1 in
  --doc)
    docker run --rm -it \
    -v ${PWD}/beoremote-halo-spec.yaml:/app/asyncapi.yml \
    -v ${PWD}/output:/app/output \
    asyncapi/generator -o output /app/asyncapi.yml --force-write -p singleFile=true @asyncapi/html-template

    cp output/index.html index.html
    ;;

  --pip)
    python3 -m build
    ;;

  --venv)
    python3 -m venv env
    ;;

  --lint)
    pre-commit run --all-files
    ;;

  --test)
    export PYTHONPATH=$PYTHONPATH:src; coverage run --source=./beoremote,./tests -m pytest
    coverage report
    coverage html -d coverage_html
    ;;
esac
