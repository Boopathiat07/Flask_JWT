from flask import jsonify


class ErrorHandling():
    def handle_server_request(e):
        return jsonify({"message":e}), 500
    
    def hanlde_bad_request(e):
        return jsonify({"message":e}), 400
    
    def handle_unauthorize(e):
        return jsonify({"message":e}), 401

    def handle_forbidden(e):
        return jsonify({"message" :e}), 403
    
    def handle_not_found(e):
        return jsonify({"message":e}), 404
