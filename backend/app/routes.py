# from flask import Blueprint, jsonify
# from .models import NavSnapshot


# from flask import request
# from app.models import Purchase, Config
# from app.services.nav import calculate_nav_snapshot
# from app import db


from flask import Blueprint, jsonify, request
from app import db
from app.models import NavSnapshot, Purchase, Config, Sale
from app.services.nav import calculate_nav_snapshot

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


@main.route('/api/buy', methods=['POST'])
def buy_shares():
    data = request.get_json()
    amount_usd = float(data.get('amount_usd', 0))
    if amount_usd <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    nav_data = calculate_nav_snapshot()
    nav = nav_data["nav_per_share"]

    FEE_RATE = 0.01  # 1%
    fee = amount_usd * FEE_RATE
    net_amount = amount_usd - fee

    shares_issued = net_amount / nav

    # Save purchase
    purchase = Purchase(
        amount_usd=amount_usd,
        shares_issued=shares_issued,
        fee_applied=fee
    )
    db.session.add(purchase)

    # Update total_shares
    total_config = Config.query.filter_by(key="total_shares").first()
    total_config.value += shares_issued
    db.session.commit()

    return jsonify({
        "shares_issued": round(shares_issued, 6),
        "fee_applied": round(fee, 2),
        "nav_used": nav,
        "new_total_shares": round(total_config.value, 2)
    })


# @main.route('/api/sell', methods=['POST'])
# def sell_shares():
#     data = request.get_json()
#     shares_to_sell = float(data.get('shares', 0))
#     if shares_to_sell <= 0:
#         return jsonify({"error": "Invalid number of shares"}), 400

#     total_config = Config.query.filter_by(key="total_shares").first()
#     if shares_to_sell > total_config.value:
#         return jsonify({"error": "Not enough shares in the system"}), 400

#     nav_data = calculate_nav_snapshot()
#     nav = nav_data["nav_per_share"]

#     gross_amount = shares_to_sell * nav
#     FEE_RATE = 0.01
#     fee = gross_amount * FEE_RATE
#     net_amount = gross_amount - fee

#     # Record sale
#     sale = Sale(
#         shares_sold=shares_to_sell,
#         amount_returned_usd=net_amount,
#         fee_applied=fee
#     )
#     db.session.add(sale)

#     # Update total_shares
#     total_config.value -= shares_to_sell
#     db.session.commit()

#     return jsonify({
#         "shares_sold": round(shares_to_sell, 6),
#         "amount_returned_usd": round(net_amount, 2),
#         "fee_applied": round(fee, 2),
#         "nav_used": nav,
#         "remaining_total_shares": round(total_config.value, 2)
#     })

@main.route('/api/sell', methods=['POST'])
def sell_shares():
    data = request.get_json()
    shares_to_sell = float(data.get('shares', 0))
    if shares_to_sell <= 0:
        return jsonify({"error": "Invalid number of shares"}), 400

    total_config = Config.query.filter_by(key="total_shares").first()
    if shares_to_sell > total_config.value:
        return jsonify({"error": "Not enough shares in the system"}), 400

    nav_data = calculate_nav_snapshot()
    nav = nav_data["nav_per_share"]

    # 📌 Fetch watermark
    watermark = Config.query.filter_by(key="high_nav_watermark").first()
    performance_fee = 0
    PERFORMANCE_FEE_RATE = 0.2  # 20% of profit above watermark

    # Only apply if NAV exceeds watermark
    if nav > watermark.value:
        excess_profit_per_share = nav - watermark.value
        profit_usd = shares_to_sell * excess_profit_per_share
        performance_fee = profit_usd * PERFORMANCE_FEE_RATE

    # 📌 Total fees = flat + performance
    gross_amount = shares_to_sell * nav
    FEE_RATE = 0.01  # 1%
    flat_fee = gross_amount * FEE_RATE
    total_fee = flat_fee + performance_fee

    net_amount = gross_amount - total_fee

    print("DEBUG >> NAV:", nav, "High Watermark:", watermark.value)


    # Record sale
    sale = Sale(
        shares_sold=shares_to_sell,
        amount_returned_usd=net_amount,
        fee_applied=total_fee
    )
    db.session.add(sale)

    # Update total_shares
    total_config.value -= shares_to_sell
    db.session.commit()

    return jsonify({
        "shares_sold": round(shares_to_sell, 6),
        "amount_returned_usd": round(net_amount, 2),
        "flat_fee": round(flat_fee, 2),
        "performance_fee": round(performance_fee, 2),
        "nav_used": nav,
        "remaining_total_shares": round(total_config.value, 2)
        
    })



@main.route('/api/config', methods=['GET'])
def get_config():
    config_values = Config.query.all()
    return jsonify([
        { "key": cfg.key, "value": round(cfg.value, 6) }
        for cfg in config_values
    ])
