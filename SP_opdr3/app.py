from flask import Flask, send_from_directory, jsonify, redirect, request
from mongodb_functions import getProductByID
from postgres_functions import getProdcutById_postgres
from postgres_algorithm_similarProduct import getSimilarProducts
from postgres_algorithm_mostPurchased import getMostPurchasedProducts
from postgres_algorithm_similarVisitor import getRecommendationFromSimilarVisitors
from postgres_algorithm_similarBrand import getProductsBasedOnBrand
from postgres_algorithm_date import getMostPopularThisWeek
app = Flask(__name__)


@app.route('/')
def home():
    return redirect("/index.html", code=302)

@app.route('/<path:filename>')
def download_file(filename):
    return send_from_directory('static', filename, as_attachment=False)


@app.route('/visitorfetchsimilar', methods=["POST", "GET"])
def visitorssimilar_postgres():
    attachedData = request.json
    return jsonify(getRecommendationFromSimilarVisitors(attachedData))

@app.route('/productfetchmongo', methods=["POST", "GET"])
def productssimilar_mongo():
    attachedData = request.json
    return jsonify(getProductByID(attachedData))

@app.route('/productfetchpostgres', methods=["POST", "GET"])
def productssimilar_postgres():
    attachedData = request.json
    return jsonify(getProdcutById_postgres(attachedData))

@app.route('/productfetchsimilarbrand', methods=["POST", "GET"])
def productssamebrand():
    attachedData = request.json
    return jsonify(getProductsBasedOnBrand(attachedData))

@app.route('/productsfetchsimilar', methods=["POST", "GET"])
def productssimilar():
    attachedData = request.json
    return jsonify(getSimilarProducts(attachedData))

@app.route('/popularproducts')
def productspopular():
    return jsonify(getMostPurchasedProducts())

@app.route('/popularproducts_thisweek')
def productspopular_thisweek():
    return jsonify(getMostPopularThisWeek())

if __name__ == '__main__':
    app.run()
