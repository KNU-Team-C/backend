from flask import jsonify, Blueprint, request, make_response
from sqlalchemy import text

from flaskr.auth import token_required
from flaskr.database import db
from flaskr.models import Project, Technology, Industry, Attachment, Company
from flaskr.utils import filter_by_text, string_arg_to_ids_list

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

    if is_my_company(current_user, company_id):

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
    else:
        return make_response("You can't represent this company", 401)


@bp.route('/<project_id>', methods=['PUT'])
@token_required
def project_edit(current_user, project_id):
    data = request.get_json()
    query = db.session.query(Project)

    project = query.filter(Project.id == project_id).first()
    if is_my_company(current_user, project.company_id):
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
    else:
        return make_response('could not verify project', 401)


@bp.route('/<project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get(project_id)
    return make_response(jsonify(project.get_info()), 401)


@bp.route('', methods=['GET'])
def get_projects():
    return get_all_projects(request), 200


def get_all_projects(request, company_id=None):
    search_query = request.args.get('search_query', '', type=str)
    query = db.session.query(Project)
    query = filter_by_text(search_query, query, field='title')

    industries_ids = string_arg_to_ids_list(request.args.get('industries_ids', '', type=str))
    technologies_ids = string_arg_to_ids_list(request.args.get('technologies_ids', '', type=str))

    if company_id is not None:
        query = query.filter(text("company_id = :company_id").params(company_id=company_id))

    if len(industries_ids) > 0:
        query = query.filter(
            Project.industries.any(
                Industry.id.in_(industries_ids)
            )
        )
    if len(technologies_ids) > 0:
        query = query.filter(
            Project.technologies.any(
                Technology.id.in_(technologies_ids)
            )
        )

    projects = query.order_by(Project.date_created.desc()).all()
    return [p.get_info() for p in projects]


@bp.route('/<project_id>', methods=['DELETE'])
@token_required
def project_delete(current_user, project_id):
    project = Project.query.get(project_id)
    if is_my_company(current_user, project.company_id):
        db.session.delete(project)
        db.session.commit()

        response = {
            "message": "delete completed!"
        }
        return jsonify(response)
    else:
        return make_response('could not verify project', 401)


def is_my_company(user, company_id):
    query = db.session.query(Company)
    company = query.filter(Company.id == company_id).first()
    return company.user_id == user.id
