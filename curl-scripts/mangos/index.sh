#!/bin/bash

curl "http://localhost:8000/characters" \
  --include \
  --request GET \
  --header "Authorization: Token ${TOKEN}"

echo
