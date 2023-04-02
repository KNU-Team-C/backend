from flask import jsonify, Blueprint, request

from flaskr.auth import token_required
from flaskr.database import db
from flaskr.models import Project, Technology, Industry, Attachment

bp = Blueprint("projects", __name__, url_prefix="/projects")


@bp.route('', methods=['POST'])
@token_required
def create_project(current_user):
    data = request.get_json()
    title = data['title']
    url = data['url']
    description = data['description']
    is_public = data['isPublic']
    technologies_id = data['technologies']
    industries_id = data['industries']
    attachments_id = data['attachments']
    company_id = data['company']

    project = Project(title=title, url=url, description=description, is_public=is_public, company_id=company_id)

    for technology_id in technologies_id:
        technology = Technology.query.filter(Technology.id == technology_id).first()
        if technology is not None:
            project.technologies.append(technology)

    for industry_id in industries_id:
        industry = Industry.query.filter(Industry.id == industry_id).first()
        if industry is not None:
            project.industries.append(industry)

    for attachment_id in attachments_id:
        attachment = Attachment.query.filter(Attachment.id == attachment_id).first()
        if attachment is not None:
            project.attachments.append(attachment)

    db.session.add(project)
    db.session.commit()

    response = project.get_info()
    return jsonify(response)
