#!/bin/bash
docker-compose exec configsvr-1 sh -c "mongosh < /scripts/init_configserver.js"

docker-compose exec shard1-1 sh -c "mongosh < /scripts/init_shard1.js"
docker-compose exec shard2-1 sh -c "mongosh < /scripts/init_shard2.js"
docker-compose exec router sh -c "mongosh < /scripts/init_router.js"
docker-compose exec router sh -c "mongosh --eval 'sh.enableSharding(\"mediatheque\")'"

docker-compose exec router sh -c "mongosh --eval 'sh.status()'"

