pyzkillredisq is a python module that will download from the zkillboard redisq queue and insert documents into a MongoDB collection

python3.6 was used to create the module

instructions to automate this script are available in the getkillscron.sh comments

I omit many fields from the zkill redisq url as I am only interested in what is lost

mdb.py setup

creds = {
    "ip": "mongoip or url",
    "port": "port",
    "un": "username",
    "pw": "password"
}

zkillurl = ('Your customized zkillredisq URL')