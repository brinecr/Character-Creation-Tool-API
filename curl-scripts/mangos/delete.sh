#!/bin/bash

curl "http://localhost:8000/characters/${ID}" \
  --include \
  --request DELETE \
  --header "Authorization: Token ${TOKEN}"

echo
