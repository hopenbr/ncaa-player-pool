#!/bin/bash
echo 'sleeping til 6:30 pm'
sleep 17992
for i in {1..20}
do
    echo "Pooling games...."
    python3 ./ncaa_player_pool/ui.py
    aws s3 cp ./test/index.html s3://brianhop.info/page/ncaa/ --acl public-read --profile brianhop.info
    echo "sleep for 15 min"
    sleep 900
done
