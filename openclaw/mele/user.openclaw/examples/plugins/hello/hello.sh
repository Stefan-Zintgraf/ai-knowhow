#!/usr/bin/env bash
if [[ -n "$1" ]]; then
  echo "hello world from hello.sh (received text: \"$1\")"
else
  echo "hello world from hello.sh"
fi
