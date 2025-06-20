from flask import Blueprint, jsonify
from .models import NavSnapshot

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify({"message": "NAV Tracker API is working!"})


@main.route('/api/nav/latest')
def get_latest_nav():
    latest = NavSnapshot.query.order_by(NavSnapshot.timestamp.desc()).first()
    if not latest:
        return jsonify({"error": "No NAV snapshot found"}), 404
    return jsonify(latest.to_dict())


@main.route('/api/nav/history')
def get_nav_history():
    history = NavSnapshot.query.order_by(NavSnapshot.timestamp.desc()).limit(30).all()
    return jsonify([entry.to_dict() for entry in history])
