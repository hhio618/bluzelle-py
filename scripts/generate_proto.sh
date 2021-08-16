#!/usr/bin/env bash

# Define variables
OUT=bluzelle/codec
PROTO=proto

# Get the missing Protobuf types files
# sh ./tool/get_proto.sh "$PROTO"

# Create required folders
rm -r -f "$OUT"
mkdir -p "$OUT"

# Generate the Protobuf implementation
PROTOC="python -m grpc_tools.protoc --python_out=$OUT --grpc_python_out=$OUT -I$PROTO"
proto_dirs=$(find "$PROTO" -path -prune -o -name '*.proto' -print0 | xargs -0 -n1 dirname | sort | uniq)
for dir in $proto_dirs; do
  $PROTOC -I$PROTO \
  $(find "${dir}" -maxdepth 1 -name '*.proto')
done


# Delete no longer required Protobuf folders
# rm -rf "$PROTO"
