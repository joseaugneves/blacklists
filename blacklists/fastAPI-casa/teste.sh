echo "--- get root"

curl -X 'GET' \
  'http://localhost:8001/' \
  -H 'accept: application/json'

echo "\n--- get item"

curl -s -X 'GET' "http://localhost:8001/items/1" -H 'accept: application/json'

echo "\n--- get item with name"

curl -s -X 'GET' "http://localhost:8001/items/1?q=teste1" -H 'accept: application/json'

echo "\n--- Post item"

curl -X 'POST' \
  'http://localhost:8001/items/?status_code=201' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "item": {
    "item_id": 0,
    "item_name": "ola asdasdasd"
  }
}'

