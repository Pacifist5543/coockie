from flask import Flask, make_response, request, session
import secrets 

from user import User, create_user_table
from post import Post, create_post_table

create_user_table()
create_post_table()

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route('/')
def index_page():
    return ""
    

@app.route("/get")
def get_page():
    return 


app.run(host='0.0.0.0', port=8080, debug= True)



