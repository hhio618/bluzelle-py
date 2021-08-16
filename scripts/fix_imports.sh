#!/usr/bin/env bash
find bluzelle/codec -name '*.py' | xargs -I{} sed -i -r 's/^from (.*) import (.+_pb2.*)/from bluzelle.codec.\1 import \2/g' {}
# Fix google imports
find bluzelle/codec -name '*.py' | xargs -I{} sed -i -r 's/^from .*(.*google\.protobuf.*) import (.+_pb2.*)/from \1 import \2/g' {}