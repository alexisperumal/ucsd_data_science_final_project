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
    leukocytes = db.Column(db.Float)
    platelets = db.Column(db.Float)
    monocytes = db.Column(db.Float)
    hematocrit = db.Column(db.Float)
    eosinophils  = db.Column(db.Float)
    red_blood_cells = db.Column(db.Float)
    hemoglobin = db.Column(db.Float)
    lymphocytes = db.Column(db.Float)
    mean_platelet_volume = db.Column(db.Float)

    def __init__(self, patient_age_quantile, leukocytes, platelets,
        monocytes, hematocrit, eosinophils, red_blood_cells,
        hemoglobin, lymphocytes, mean_platelet_volume):
        self.patient_age_quantile = patient_age_quantile
        self.leukocytes = leukocytes
        self.platelets = platelets
        self.monocytes = monocytes
        self.hematocrit = hematocrit
        self.eosinophils = eosinophils
        self.red_blood_cells = red_blood_cells
        self.hemoglobin = hemoglobin
        self.lymphocytes = lymphocytes
        self.mean_platelet_volume = mean_platelet_volume

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'patient_age_quantile', 'leukocytes', 'platelets',
            'monocytes', 'hematocrit', 'eosinophils', 'red_blood_cells',
            'hemoglobin', 'lymphocytes', 'mean_platelet_volume')

product_schema = ProductSchema()
products_schema = ProductSchema()


# Create a Product
@app.route('/product', methods=['POST'])
def add_product():
    patient_age_quantile = request.json['patient_age_quantile']
    leukocytes = request.json['leukocytes']
    platelets = request.json['platelets'] 
    monocytes = request.json['monocytes'] 
    hematocrit = request.json['hematocrit']
    eosinophils = request.json['eosinophils']
    red_blood_cells = request.json['red_blood_cells']
    hemoglobin = request.json['hemoglobin']
    lymphocytes = request.json['lymphocytes'] 
    mean_platelet_volume = request.json['mean_platelet_volume']

    new_product = Product(patient_age_quantile, leukocytes, platelets,
            monocytes, hematocrit, eosinophils, red_blood_cells,
            hemoglobin, lymphocytes, mean_platelet_volume)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

'''
# Get all Products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = product_schema.dump(all_products)
    return jsonify(result.data)
'''

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
