from flask import Flask, request, jsonify, render_template
import util_processing
import validators
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json


app = Flask(__name__)

# Creating a database to store the whois data
DATABASE_URL = "sqlite:///whois_data.db"  
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Creating a table to store the whois data
class WhoisData(Base):
    __tablename__ = 'whois_data'
    domain_name = Column(String, primary_key=True)
    status = Column(String, nullable=False)
    details = Column(Text, nullable=False)  

Base.metadata.create_all(engine)


# Creating a route to lookup whois data
@app.route('/lookup_whois', methods=['GET'])
def lookup_whois():
    domain_name = request.args.get('domain_name')

    # Checking if the domain_name query parameter is provided
    if not domain_name:
        return jsonify({'error': 'domain_name query parameter is required'}), 400
    
    # Checking if the domain_name is a valid domain name or IP address
    if not validators.domain(domain_name) and not validators.ip_address.ipv4(domain_name) and not validators.ip_address.ipv6(domain_name):
        return jsonify({'error': 'Invalid domain name or IP address'}), 400
    
    try:      
        
        response = util_processing.get_dictionary(domain_name)

        response_json = json.dumps(response)

        # Storing the whois data in the database
        whois_data = WhoisData(
            domain_name=domain_name,
            status=response.get('status', 'unknown'),
            details=response_json
        )
        session.merge(whois_data)  
        session.commit()
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
