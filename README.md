# bitcoind-regtest-docker-compose
docker-compose for running multi bitcoind regtest

> N=2 python3 init.py

> N=5 PORT=19000 RPC_PORT=19001 STEP=10 python3 init.py

> sudo docker-compose up

TODO: Need ELB service for a dozen of nodes & run with `sudo docker-compose up -scale=X`
