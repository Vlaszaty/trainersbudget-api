from flask import Flask, json, request, jsonify
from bson.json_util import dumps
from flask.ext.cors import CORS

import pymongo

app = Flask(__name__)
app.debug = True
CORS(app)


@app.route('/')
def info():
    res = {"api_version": "0.1",
           "author": "Bas Vlaszaty"}
    return jsonify(res)


@app.route('/rates', methods=['GET'])
def get_rates():
    res = ""
    try:
        res = db.rates.find()
        return dumps(res)

    except Exception, e:
        print "Error inserting: %s" % e

    return jsonify(res)


@app.route('/rates', methods=['POST'])
def create_rate():
    res = ""
    try:
        rrid = request.json['rate_id'].upper()
        rate = request.json['rate']

        document = {"_id": rrid,
                    "rate": rate}

        tid = db.rates.insert_one(document).inserted_id
        print "Insert successfull: %s" % tid
        res = {"tid": str(tid)}

    except Exception, e:
        print "Error inserting: %s" % e

    return jsonify(res)


@app.route('/rates/<rate_id>', methods=['GET'])
def get_rate(rate_id):

    res = ""
    try:
        res = db.rates.find_one({"_id": rate_id.upper()})
        return dumps(res)
    except Exception, e:
        print "Error inserting: %s" % e

    return jsonify(res)


@app.route('/rates/<rate_id>', methods=['UPDATE'])
def update_rate(rate_id):
    res = ""
    try:
        res = db.rates.update({"_id": rate_id.upper()}, {"$set":{request.json}})
        return jsonify(res.matched_count)
    except Exception, e:
        print "Error updating: %s" % e

    return jsonify(res)


@app.route('/rates/<rate_id>', methods=['DELETE'])
def delete_rate(rate_id):
    res = ""
    try:
        result = db.rates.delete_one({"_id": rate_id.upper()})
        return jsonify({"deleted_count": result.deleted_count})
    except Exception, e:
        print "Error inserting: %s" % e

    return jsonify(res)


if __name__ == '__main__':

    try:
        conn = pymongo.MongoClient()
        print "Database connection successfull"

    except pymongo.errors.ConnectionFailure, e:
        print "Error connecting to database: %s" % e

    db = conn.trainersbudget
    app.run()
