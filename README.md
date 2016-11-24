### Run instructions

On this machine:
```
scp * root@45.55.151.24:~/machen
scp .env root@45.55.151.24:~/machen
```

On the remote machine in tmux:

```
cd machen
conda create -n machen python=2 pip
source activate machen
pip install -r requirements.php
source activate .env
python tweet.py
```

### `.env` File

```
export MACHEN_CONSUMER_KEY=
export MACHEN_CONSUMER_SECRET=
export MACHEN_TOKEN=
export MACHEN_TOKEN_SECRET=
```