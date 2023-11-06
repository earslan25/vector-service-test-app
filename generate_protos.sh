#!/usr/bin/env bash

python3.9 -m grpc_tools.protoc -Iprotos/ --python_out=. --pyi_out=. --grpc_python_out=. protos/vector_service.proto protos/vector_models.proto
