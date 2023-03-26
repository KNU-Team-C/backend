from flask import request, jsonify, make_response, Blueprint
from flaskr.database import db
from flaskr.models import Company, Industry, Technology
from flaskr.admin_companies import flat_map
bp = Blueprint("user_company", __name__, url_prefix="/user")




@bp.route('/company',methods=['GET'])
def get_company():
    company_id = request.form["company_id"]
    query = db.session.query(Company)

    industries = db.session.query(Industry).all()
    technologies = db.session.query(Technology).all()
    company = query.filter(Company.id==company_id).first()

    result = {
        'id' : company.id,
        'name' : company.name,
        'email' : company.address,
        'phone_number' : company.phone_number,
        'logo_url' : company.logo_url,
        'location' : company.location,
        'description' : company.description,
        'is_blocked' : company.is_blocked,
        'is_verified' : company.is_verified,
        'industries': [{
                'id': industry.id,
                'name': industry.name
            } for industry in flat_map(lambda project: project.industries, company.projects)],
            'technologies': [{
                'id': technology.id,
                'name': technology.name
            } for technology in flat_map(lambda project: project.technologies, company.projects)]#,
        #'industries_all':[{
        #        'id': industry.id,
        #        'name': industry.name
        #    } for industry in industries],
        #'technologies_all':[{
        #        'id': technology.id,
        #        'name': technology.name
        #    } for technology in technologies]
        
    }
    return jsonify(result),200

@bp.route('/company',methods=['Post'])
def edit_company():
    data = request.form
    company_id = data["company_id"]
    query = db.session.query(Company)

    company = query.filter(Company.id==company_id).first()
    company.name = data['name']
    company.email = data['address']
    company.phone_number = data['phone_number']
    company.logo_url = data['logo_url']
    company.location = data['location']
    company.description = data['description']

    db.session.commit()
    
    return 200



