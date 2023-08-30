#!/bin/sh

export INGEST=_ingest
export DATALAKE=_datalake

if [ ! -d $INGEST ]; then
    mkdir $INGEST
fi
if [ ! -d $DATALAKE ]; then
    mkdir $DATALAKE
fi

python generate_dummy_metric.py -out $INGEST/2023/01/01/server_patching.json -threshold 0.5 -mappings Sydney Brisbane Melbourne
python generate_dummy_metric.py -out $INGEST/2023/02/01/server_patching.json -threshold 0.6 -mappings Sydney Brisbane Melbourne
python generate_dummy_metric.py -out $INGEST/2023/03/01/server_patching.json -threshold 0.65 -mappings Sydney Brisbane Melbourne
python generate_dummy_metric.py -out $INGEST/2023/04/01/server_patching.json -threshold 0.75 -mappings Sydney Brisbane Melbourne
python generate_dummy_metric.py -out $INGEST/2023/05/01/server_patching.json -threshold 0.8 -mappings Sydney Brisbane Melbourne
python generate_dummy_metric.py -out $INGEST/2023/06/01/server_patching.json -threshold 0.85 -mappings Sydney Brisbane Melbourne

python generate_dummy_metric.py -out $INGEST/2023/01/01/user_account_mfa.json -threshold 0.9 -mappings Sydney Brisbane Melbourne
python generate_dummy_metric.py -out $INGEST/2023/02/01/user_account_mfa.json -threshold 0.95 -mappings Sydney Brisbane Melbourne
python generate_dummy_metric.py -out $INGEST/2023/03/01/user_account_mfa.json -threshold 0.98 -mappings Sydney Brisbane Melbourne
python generate_dummy_metric.py -out $INGEST/2023/04/01/user_account_mfa.json -threshold 0.98 -mappings Sydney Brisbane Melbourne
python generate_dummy_metric.py -out $INGEST/2023/05/01/user_account_mfa.json -threshold 0.98 -mappings Sydney Brisbane Melbourne
python generate_dummy_metric.py -out $INGEST/2023/06/01/user_account_mfa.json -threshold 0.98 -mappings Sydney Brisbane Melbourne

python pipeline.py -ingest $INGEST -out $DATALAKE

python app.py