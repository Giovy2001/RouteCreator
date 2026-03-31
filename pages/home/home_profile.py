from flask import render_template, request, redirect, url_for
from scripts.database_sql import sql_routes, sql_users
import global_values

def render_home_profile():
    username_created: str = request.args.get("username_created")
    username_changed: str = request.args.get("username_changed")
    
    username: str = request.args.get("username")
    if username_created:
        username = username_created
    elif username_changed:
        username = username_changed
    
    user_data: dict = sql_users.get_user(global_values.conn, username)
    routes_data: list = sql_routes.get_routes_from_author(global_values.conn, username)
    print(user_data)
    print(routes_data)
    
    if request.method == "POST":
        new_username: str = request.form.get("username-input")
        user_data: dict = sql_users.get_user(global_values.conn, new_username)
        
        if not user_data["exist"]:
            return redirect(url_for("render_create_user", username=new_username))
        else:
            return redirect(url_for("render_home_profile", username_changed=new_username))
    
    
    return render_template("home/profile.html", username_created=username_created, username_changed=username_changed, user_data=user_data, routes_data=routes_data)

def render_create_user():
    username: str = request.args.get("username")
    
    if request.method == "POST":        
        user_data: dict = {"user_color":0}
        user_data["user_name"] = request.form.get("username-input")
        
        existing_data: dict = sql_users.get_user(global_values.conn, user_data["user_name"])
        if not existing_data["exist"]:        
            sql_users.add_user(global_values.conn, user_data)
        
            return redirect(url_for("render_home_profile", username_created=user_data["user_name"]))
        else:
            ...
            # TODO: Avvisa che utente esiste già con quel nome
     
    return render_template("create_user.html", username=username)