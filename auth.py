import hashlib,hmac,json,os,secrets
AUTH_FILE=os.path.join("data","users.json")
def _load():
 os.makedirs("data",exist_ok=True)
 if not os.path.exists(AUTH_FILE):return {}
 try:
  with open(AUTH_FILE,encoding="utf-8") as f:return json.load(f)
 except:return {}
def _save(x):
 with open(AUTH_FILE,"w",encoding="utf-8") as f:json.dump(x,f,indent=2)
def _hash(password,salt):
 return hashlib.pbkdf2_hmac("sha256",password.encode(),salt.encode(),120000).hex()
def register(username,password):
 u=username.strip().lower()
 if not u or len(password)<6:return False,"username/password invalid"
 users=_load()
 if u in users:return False,"user already exists"
 salt=secrets.token_hex(16);users[u]={"salt":salt,"password":_hash(password,salt)};_save(users);return True,"registered"
def login(username,password):
 u=username.strip().lower();x=_load().get(u)
 if not x:return False
 return hmac.compare_digest(x["password"],_hash(password,x["salt"]))
