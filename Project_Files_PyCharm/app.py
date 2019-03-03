from flask import Flask, send_from_directory, jsonify, redirect, request
from products import getPopularProducts, getRecentProducts, getPersonalProducts, getProduct, getRecommendedProducts, getProductsOOS, getSimilarProducts

app = Flask(__name__)


@app.route('/')
def home():
    return redirect("/index.html", code=302)

@app.route('/<path:filename>')
def download_file(filename):
    return send_from_directory('static', filename, as_attachment=False)

@app.route('/popularproducts')
def popularproducts():
    return jsonify(getPopularProducts())

@app.route('/recentproducts')
def recentproducts():
    return jsonify(getRecentProducts())

@app.route('/productrecommendations', methods=["POST", "GET"])
def productrecommendations():
    attachedData = request.json
    return jsonify(getRecommendedProducts(attachedData))

@app.route('/productsimilar', methods=["POST", "GET"])
def productssimilar():
    attachedData = request.json
    return jsonify(getSimilarProducts(attachedData))

@app.route('/myproducts', methods=["POST", "GET"])
def myproducts():
    attachedData = request.json
    return jsonify(getProduct(attachedData))

@app.route('/productsOOS')
def productsOOS():
    return jsonify(getProductsOOS())

if __name__ == '__main__':
    app.run()
