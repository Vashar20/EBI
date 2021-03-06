from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from json import dumps
import pymysql

api = Flask(__name__)
    
@api.route('/genes', methods=['GET'])
def get_gene():
    if request.method == 'GET':
        # Mandatory parameter
        gene = request.args['lookup']
        # Optional parameter   
        species = request.args.get('species')
        # Database connection
        db_connect = create_engine('mysql+pymysql://anonymous:@ensembldb.ensembl.org:3306/ensembl_website_97')
        conn = db_connect.connect()
        # Checking lookup length
        if len(gene) >= 3:
            # Without provided species parameter
            # This part could be rewritten using combination of query and filter if more request parameters would be considered.
            if species is None:
                query = conn.execute("select display_label, location, stable_id, species from gene_autocomplete where display_label LIKE '%s' "  % (gene+'%%'))
                result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}  #or need simple text results?
                return jsonify(result)
            # With provided species parameter
            # A list of full scientific name of all species in database could be provided to improve scpecies parameter assertion and correction.
            else:
                query = conn.execute("select display_label, location, stable_id, species from gene_autocomplete where display_label LIKE '%s' AND species = '%s' "  % (gene+'%%',species)) 
                result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
                return jsonify(result)
        else:
            # All Errors could be written using decorated errors flag in Flask.
            return '''
            Error 400 HTTP code.
            Lookup (gene) length should not be less than 3 characters
            '''
    # Raising Error if request method is not GET
    elif request.method in ['POST', 'PUT', 'PATCH']:
        return '''
        Error 405 HTTP code. The service is available only for GET methos
        '''


    
if __name__ == '__main__':
     api.run(port=5001)

  
