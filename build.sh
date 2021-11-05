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

  --lint)
    pylint -j0 --disable=C0209,C0116,C0115,E0401,R0801,C0103,R0903 `find {src,test}|grep .py$|xargs`
    ;;

  --test)
    export PYTHONPATH=$PYTHONPATH:src/beoremote; coverage run --source=./src,./test -m pytest
    coverage report
    coverage html -d coverage_html
    ;;
esac
