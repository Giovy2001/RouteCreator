from flask import Flask, request, jsonify
import global_values
from scripts.database_sql import sql_users, sql_routes

# TODO: Probabilmente questo non funzionerà su vercel e dovrà essere fatta funzione serverless dentro api
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
    

def get_profile():
    data = request.get_json()
    username = data.get("username")
    
    user_data: dict = sql_users.get_user(global_values.conn, username)
    routes_data: list = sql_routes.get_routes_from_author(global_values.conn, username)
    
    return {"user":user_data, "routes":routes_data}