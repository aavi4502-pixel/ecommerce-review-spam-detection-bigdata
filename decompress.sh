#!/bin/bash
echo "Starting decompression..." > /tmp/decompression_status.log
hdfs dfs -text /project/input/All_Amazon_Review.json.gz | hdfs dfs -put - /project/input/All_Amazon_Review_Uncompressed.json
if [ $? -eq 0 ]; then
    echo "SUCCESS: Decompression finished!" >> /tmp/decompression_status.log
else
    echo "FAILED: Decompression failed!" >> /tmp/decompression_status.log
fi
