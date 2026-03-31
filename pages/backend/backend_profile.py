from flask import Flask, request, jsonify
import global_values
from scripts.database_sql import sql_users

def update_color():
    data = request.get_json()
    username = data.get("username")
    color_id = data.get("color_id")

    if not username or color_id is None:
        return jsonify({"success": False, "message": "Dati mancanti"}), 400

    try:
        sql_users.edit_user(global_values.conn, username, {"user_color": color_id})
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
    
    # TODO: Probabilmente questo non funzionerà su vercel e dovrà essere fatta funzione serverless dentro api