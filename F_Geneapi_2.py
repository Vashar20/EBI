# This code is OOP version of F_Geneapi.py

from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from json import dumps
import pymysql
from flask_restful import Resource, Api #, reqparse, abort

app = Flask(__name__)
api = Api(app)
    
#@api.route('/genes', methods=['GET'])
class Gene(Resource):

    def dbconnect(self):
        db = 'ensembl_website_97'
        usr = 'anonymous'
        pwd = ''
        port = '3306'
        db_url = 'ensembldb.ensembl.org'
        db_connect = create_engine('mysql+pymysql://' + usr + ':' + pwd + '@' + db_url + ':' + port + '/' + db)
        self.conn = db_connect.connect()    

    def get(self):
        method_test()

        # Mandatory parameter
        # parameters could be defined using reqparse
        self.gene = request.args['lookup']
    
        # Checking lookup length
        if (len(self.gene) < 3):
            return word_error(2)

        # Optional parameter   
        self.species = request.args.get('species')



        # Database connection
        self.dbconnect()

       
        # Without provided species parameter
        # This part could be rewritten using combination of query and filter if more request parameters would be considered.
        if self.species is None:
            query = self.conn.execute("select display_label, location, stable_id, species from gene_autocomplete where display_label LIKE '%s' "  % (self.gene+'%%'))
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}  #or need simple text results?
            return jsonify(result)
        # With provided species parameter
        # A list of full scientific name of all species in database could be provided to improve scpecies parameter assertion and correction.
        else:
            query = self.conn.execute("select display_label, location, stable_id, species from gene_autocomplete where display_label LIKE '%s' AND species = '%s' "  % (self.gene+'%%',self.species)) 
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            return jsonify(result)

# This error function could be replaced by abort(400)
@app.errorhandler(400)
def word_error(e):
    return 'Error 400 HTTP code  ----->   Lookup (gene) length should not be less than 3 characters'

# This error function could be replaced by abort(405)
@app.errorhandler(405)
def method_error(e):
    return  'Error 405 HTTP code  ----->   The service is available only for GET method'

# Checks the method of request
def method_test():
    if request.method in ['POST', 'PUT', 'PATCH']:
        return method_error(1)
    elif request.method == 'GET':
        pass
        


# Adding route of endpoint
api.add_resource(Gene, "/genes")
    
if __name__ == '__main__':
     app.run(port=5001)

  
