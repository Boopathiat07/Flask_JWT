from flask import jsonify

class response():
    def function(body):
        return jsonify({"message" : "Ok", "body" : body}), 200
