from datetime import datetime

from flask import Blueprint, request, jsonify
from flaskr import db
from flaskr.auth import token_required
from flaskr.models import UserReport, CompanyReport

bp = Blueprint('reports', __name__, '/')

@bp.route('/user_report', methods=['POST'])
@token_required
def create_user_report(current_user):
    data = request.get_json()

    report_message = data.get('report_message')
    reported_user_id = data.get('reported_user_id')

    if not all([report_message, reported_user_id]):
        return jsonify({"error": "Missing required fields"}), 400

    user_report = UserReport(
        report_message=report_message,
        plaintiff_id=current_user.id,
        reported_user_id=reported_user_id,
        date_created=datetime.now()
    )

    db.session.add(user_report)
    db.session.commit()

    return jsonify({"success": "User report created"}), 201

@bp.route('/company_report', methods=['POST'])
@token_required
def create_company_report(current_user):
    data = request.get_json()

    report_message = data['report_message']
    company_id = data['company_id']

    print(report_message, company_id)

    if not all([report_message, company_id]):
        return jsonify({"error": "Missing required fields"}), 400

    company_report = CompanyReport(
        report_message=report_message,
        user_id=current_user.id,
        company_id=company_id,
        date_created=datetime.now()
    )

    db.session.add(company_report)
    db.session.commit()

    return jsonify({"success": "Company report created"}), 201

@bp.route('/user_report', methods=['GET'])
@token_required
def get_user_reports(current_user):
    if not current_user.is_staff:
        return jsonify({"error": "Insufficient rights to view user reports"}), 403

    user_reports = UserReport.query.all()

    response = [user_report.get_info() for user_report in user_reports]

    return jsonify(response), 200

@bp.route('/user_report/<int:user_id>', methods=['GET'])
@token_required
def get_user_report(current_user, user_id):
    if not current_user.is_staff:
        return jsonify({"error": "Insufficient rights to view user reports"}), 403

    user_report = UserReport.query.get(reported_user_id=user_id)

    if not user_report:
        return jsonify({"error": "User report not found"}), 404

    response = user_report.get_info()

    return jsonify(response), 200

@bp.route('/company_report', methods=['GET'])
@token_required
def get_company_reports(current_user):
    if not current_user.is_staff:
        return jsonify({"error": "Insufficient rights to view company reports"}), 403

    company_reports = CompanyReport.query.all()

    response = [company_report.get_info() for company_report in company_reports]

    return jsonify(response), 200

@bp.route('/company_report/<int:company_id>', methods=['GET'])
@token_required
def get_company_report(current_user, company_id):
    if not current_user.is_staff:
        return jsonify({"error": "Insufficient rights to view company reports"}), 403

    company_report = CompanyReport.query.get(company_id)

    if not company_report:
        return jsonify({"error": "Company report not found"}), 404

    response = company_report.get_info()

    return jsonify(response), 200

@bp.route('/user_report/resolve/<int:report_id>', methods=['POST'])
@token_required
def resolve_user_report(current_user, report_id):
    if not current_user.is_staff:
        return jsonify({"error": "Insufficient rights to resolve user reports"}), 403

    user_report = UserReport.query.get(report_id)

    if not user_report:
        return jsonify({"error": "User report not found"}), 404

    user_report.is_resolved = True
    user_report.date_resolved = datetime.now()

    db.session.commit()

    return jsonify({"success": "User report resolved"}), 200

@bp.route('/company_report/resolve/<int:report_id>', methods=['POST'])
@token_required
def resolve_company_report(current_user, report_id):
    if not current_user.is_staff:
        return jsonify({"error": "Insufficient rights to resolve company reports"}), 403

    company_report = CompanyReport.query.get(report_id)

    if not company_report:
        return jsonify({"error": "Company report not found"}), 404

    company_report.is_resolved = True
    company_report.date_resolved = datetime.now()

    db.session.commit()

    return jsonify({"success": "Company report resolved"}), 200