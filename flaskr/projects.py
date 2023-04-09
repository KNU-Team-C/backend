from flask import jsonify, Blueprint, request, make_response

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
    is_public = data['isPublic']
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
    else:
        return make_response('could not verify project', 401)


@bp.route('/<project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get(project_id)
    return make_response(jsonify(project.get_info()), 401)


@bp.route('', methods=['GET'])
def get_projects():
    search_query = request.args.get('search_query', '', type=str)
    query = db.session.query(Project)
    query = filter_by_text(search_query, query, field='title')

    industries_ids = string_arg_to_ids_list(request.args.get('industries_ids', '', type=str))
    technologies_ids = string_arg_to_ids_list(request.args.get('technologies_ids', '', type=str))

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

    projects = query.all()
    return jsonify([p.get_info() for p in projects]), 200


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
