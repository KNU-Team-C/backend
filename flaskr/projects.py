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


@bp.route('/<project_id>', methods=['PUT'])
def project_edit(project_id):
    data = request.get_json()
    query = db.session.query(Project)

    project = query.filter(Project.id == project_id).first()
    project.title = data['title']
    project.url = data['url']
    project.description = data['description']
    project.logo_url = data['logo_url']
    project.is_public = data['is_public']
    project.company_id = data['company_id']
    technologies_id = data['technologies']
    industries_id = data['industries']
    attachments_id = data['attachments']

    new_techlogies = []
    for technology_id in technologies_id:
        technology = Technology.query.filter(Technology.id == technology_id).first()
        if technology is not None:
            new_techlogies.append(technology)
    project.technologies = new_techlogies

    new_industries = []
    for industrie_id in industries_id:
        industrie = Industry.query.filter(Industry.id == industrie_id).first()
        if industrie is not None:
            new_industries.append(industrie)
    project.industries = new_industries

    new_attachments = []
    for attachment_id in attachments_id:
        attachment = Attachment.query.filter(Attachment.id == attachment_id).first()
        if attachment is not None:
            new_attachments.append(attachment)
    project.attachments = new_attachments

    db.session.commit()

    response = project.get_info()
    return jsonify(response)


@bp.route('/<project_id>', methods=['DELETE'])
def project_delete(project_id):

    project = Project.query.get(project_id)
    db.session.delete(project)
    db.session.commit()

    response = {
        "message": "delete completed!"
    }
    return jsonify(response)


