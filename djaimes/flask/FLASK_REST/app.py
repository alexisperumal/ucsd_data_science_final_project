from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' + 
    os.path.join(basedir, 'db.sqlite'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_age_quantile = db.Column(db.Float)

    def __init__(self, patient_age_quantile):
    	self.patient_age_quantile = patient_age_quantile

#Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'patient_age_quantile')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create a Product
@app.route('/product', methods=['POST'])
def add_product():
	patient_age_quantile = request.json['patient_age_quantile']
	new_product = Product(patient_age_quantile)
	db.session.add(new_product)
	db.session.commit()
	return product_schema.jsonify(new_product)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)