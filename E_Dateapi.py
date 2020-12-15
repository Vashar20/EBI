from flask import Flask, jsonify
from datetime import datetime
import json

api = Flask(__name__)
# Defining endpoint
@api.route('/date', methods=['GET'])
def get_date():
    date = datetime.now().strftime('%a %b %d %H:%M:%S BST %Y')
    d = {"date" : date}
     
    return jsonify(d)
    
    
if __name__ == '__main__':
    api.run()
