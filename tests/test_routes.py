from flask import Flask, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
from service import app, db
from service.models import Account

# Base URL for accounts
BASE_URL = "/accounts"

# Home route with redirect to HTTPS
@app.route("/", methods=["GET"])
def index():
    """Home Page with redirect"""
    return redirect("https://localhost:5000/")

@app.route("/health", methods=["GET"])
def health():
    """Health Check"""
    return jsonify(status="OK"), 200

@app.route(BASE_URL, methods=["POST"])
def create_account():
    """Create an Account"""
    data = request.get_json()
    try:
        account = Account(
            name=data["name"],
            email=data["email"],
            address=data["address"],
            phone_number=data["phone_number"],
        )
        db.session.add(account)
        db.session.commit()

        return jsonify(account.serialize()), 201, {"Location": f"{BASE_URL}/{account.id}"}
    except Exception as e:
        db.session.rollback()
        return jsonify(message="Failed to create account", error=str(e)), 400

@app.route(BASE_URL, methods=["GET"])
def list_accounts():
    """List all Accounts"""
    accounts = Account.query.all()
    return jsonify([account.serialize() for account in accounts]), 200

@app.route(f"{BASE_URL}/<int:id>", methods=["GET"])
def read_account(id):
    """Read an Account by ID"""
    account = Account.query.get(id)
    if account:
        return jsonify(account.serialize()), 200
    return jsonify(message="Account not found"), 404

@app.route(f"{BASE_URL}/<int:id>", methods=["PUT"])
def update_account(id):
    """Update an Account by ID"""
    account = Account.query.get(id)
    if account:
        data = request.get_json()
        account.name = data.get("name", account.name)
        account.email = data.get("email", account.email)
        account.address = data.get("address", account.address)
        account.phone_number = data.get("phone_number", account.phone_number)

        db.session.commit()
        return jsonify(account.serialize()), 200
    return jsonify(message="Account not found"), 404

@app.route(f"{BASE_URL}/<int:id>", methods=["DELETE"])
def delete_account(id):
    """Delete an Account by ID"""
    account = Account.query.get(id)
    if account:
        db.session.delete(account)
        db.session.commit()
        return "", 204
    return jsonify(message="Account not found"), 404
