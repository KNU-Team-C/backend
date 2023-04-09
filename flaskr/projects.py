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
    is_public = bool(data['isPublic'])
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
    new_title = data.get('title', None)
    new_url = data.get('url', None)
    new_description = data.get('description', None)
    new_logo_url = data.get('logo_url', None)
    new_is_public = bool(data.get('is_public', None))
    new_company_id = data.get('company_id', None)
    if new_title is not None:
        project.title = new_title
    if new_url is not None:
        project.url = new_url
    if new_description is not None:
        project.description = new_description
    if new_logo_url is not None:
        project.logo_url = new_logo_url
    if new_is_public is not None:
        project.is_public = new_is_public
    if new_company_id is not None:
        project.company_id = new_company_id
    technologies_id = data.get('technologies', None)
    industries_id = data.get('industries', None)
    attachments_id = data.get('attachments', None)

    if technologies_id is not None:
        new_technologies = []
        for technology_id in technologies_id:
            technology = Technology.query.filter(Technology.id == technology_id).first()
            if technology is not None:
                new_technologies.append(technology)
        project.technologies = new_technologies

    if industries_id is not None:
        new_industries = []
        for industry_id in industries_id:
            industry = Industry.query.filter(Industry.id == industry_id).first()
            if industry is not None:
                new_industries.append(industry)
        project.industries = new_industries

    if attachments_id is not None:
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
    project = db.session.query(Project).filter(Project.id == project_id).first()
    db.session.delete(project)
    db.session.commit()

    response = {
        "message": "delete completed!"
    }
    return jsonify(response)
