#!/bin/bash

for i in {1..48}
do
    echo "Pooling games...."
    python3 ./ncaa_player_pool/ui.py
    aws s3 cp ./test/index.html s3://brianhop.info/page/ncaa/ --acl public-read --profile brianhop.info
    echo "sleep for 15 min"
    sleep 900
done
