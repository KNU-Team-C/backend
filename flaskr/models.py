from sqlalchemy import Integer
from werkzeug.security import generate_password_hash

from flaskr.database import db
from flaskr.utils import flat_map
from sqlalchemy.orm import validates
import re

chats = db.Table('chats',
                 db.Column('chat_id', db.BigInteger, db.ForeignKey('chat.id'), primary_key=True),
                 db.Column('user_id', db.BigInteger, db.ForeignKey('user.id'), primary_key=True)
                 )


class UserReport(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    report_message = db.Column(db.Text)
    plaintiff_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    reported_user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True))
    is_resolved = db.Column(db.Boolean, default=False)
    date_resolved = db.Column(db.DateTime(timezone=True))

    def get_info(self):
        info = {
            'id': self.id,
            'message': self.report_message,
            'plaintiff': self.plaintiff.get_info(),
            'reportedUser': self.reported_user.get_info(),
            'dateCreated': self.date_created,
            'isResolved': self.is_resolved,
            'dateResolved': self.date_resolved
        }
        return info


class User(db.Model):
    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    companies = db.relationship('Company', backref='user', lazy=True)
    chats = db.relationship("Chat", secondary=chats, lazy='dynamic',
                            backref=db.backref('user', lazy=True))
    phone_number = db.Column(db.String(50))
    password = db.Column(db.String(300))
    ava_url = db.Column(db.String(2048))
    is_staff = db.Column(db.Boolean)
    is_blocked = db.Column(db.Boolean, default=False)
    date_joined = db.Column(db.DateTime(timezone=True), default=db.func.now())
    messages = db.relationship('Message', backref='user', lazy=True)
    userReportsPlaintiff = db.relationship('UserReport', backref='plaintiff', lazy=True,
                                           foreign_keys=[UserReport.plaintiff_id])
    userReportsReported = db.relationship('UserReport', backref='reported_user', lazy=True,
                                          foreign_keys=[UserReport.reported_user_id])
    companyReports = db.relationship('CompanyReport', backref='user', lazy=True)
    companyFeedbacks = db.relationship('CompanyFeedback', backref='user', lazy=True)

    def __init__(self, first_name: str, last_name: str, email: str, password: str, phone_number: str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self._generate_password_hash(password)
        self.temp_password = password
        self.phone_number = phone_number

    @validates("email")
    def validate_email(self, key, value):
        email_regex = re.compile('^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@'
                                '((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-'
                                'Z\-0-9]+\.)+[a-zA-Z]{2,}))$')
        if not email_regex.match(value):
            raise ValueError("failed email validation")
        return value

    @validates("temp_password")
    def validate_password(self, key, value):
        print(value)
        password_regex = re.compile('^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,300}$')
        if not password_regex.match(value):
            raise ValueError("failed password validation")
        return value

    @validates("first_name")
    def validate_first_name(self, key, value):
        first_name_regex = re.compile('^[a-zA-Z]+$')
        if not first_name_regex.match(value):
            raise ValueError("failed first name validation")
        return value

    @validates("last_name")
    def validate_last_name(self, key, value):
        last_name_regex = re.compile('^[a-zA-Z]+$')
        if not last_name_regex.match(value):
            raise ValueError("failed last name validation")
        return value

    @validates("phone_number")
    def validate_phone_number(self, key, value):
        phone_number_regex = re.compile('^\d{7,15}$')
        if not phone_number_regex.match(value):
            raise ValueError("failed phone number validation")
        return value

    @staticmethod
    def _generate_password_hash(password_plaintext: str):
        return generate_password_hash(password_plaintext)

    def get_info(self):
        info = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_blocked": self.is_blocked,
            "is_staff": self.is_staff,
            "ava_url": self.ava_url,
            "date_joined": self.date_joined,
            "email": self.email,
            "phone_number": self.phone_number,
        }
        return info


class Chat(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    chat_name = db.Column(db.String(100))
    ava_url = db.Column(db.String(2048))
    mini_ava_url = db.Column(db.String(2048))
    messages = db.relationship('Message', backref='chat', lazy=True)

    def get_info(self):
        # chat_name  should be user2 name

        info = {
            'id': self.id,
            'chat_name': self.chat_name,
            'ava_url': self.ava_url,
            'mini_ava_url': self.mini_ava_url,
        }
        return info

class Technology(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100))

    def get_info(self):
        info = {
            'id': self.id,
            'name': self.name
        }
        return info


class Attachment(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    link = db.Column(db.String(2048))
    extension = db.Column(db.String(100))
    project_id = db.Column(db.BigInteger, db.ForeignKey('project.id'),
                           nullable=False)


class Company(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phone_number = db.Column(db.String(50))
    employees_num = db.Column(db.BigInteger)
    logo_url = db.Column(db.String(2048))
    mini_logo_url = db.Column(db.String(2048))
    location = db.Column(db.String(100))
    description = db.Column(db.Text)
    is_blocked = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_verification_request_pending = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime(timezone=True), default=db.func.now())
    projects = db.relationship('Project', backref='company', lazy=True)
    companyFeedbacks = db.relationship('CompanyFeedback', backref='company', lazy=True)
    companyReports = db.relationship('CompanyReport', backref='company', lazy=True)
    sets = db.relationship('Set', backref='company', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def get_info(self):
        info = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "employees_num": self.employees_num,
            "location": self.location,
            "description": self.description,
            "user": self.user_id,
            "logo": self.logo_url,
            "is_blocked": self.is_blocked,
            "is_verified": self.is_verified,
            "date_created": self.date_created,
            'industries': [{
                'id': industry.id,
                'name': industry.name
            } for industry in flat_map(lambda project: project.industries, self.projects)],
            'technologies': [{
                'id': technology.id,
                'name': technology.name
            } for technology in flat_map(lambda project: project.technologies, self.projects)]
        }
        return info


class Industry(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100))

    def get_info(self):
        info = {
            'id': self.id,
            'name': self.name
        }
        return info


class Message(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    chat_id = db.Column(db.BigInteger, db.ForeignKey('chat.id'), nullable=False)
    message = db.Column(db.Text)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime(timezone=True))

    def get_info(self):
        info = {
            'id': self.id,
            'chat_id': self.chat_id,
            'message': self.message,
            'user_id': self.user_id,
            'date': self.date
        }
        return info


technologies = db.Table('technologies',
                        db.Column('technology_id', db.BigInteger, db.ForeignKey('technology.id'), primary_key=True),
                        db.Column('project_id', db.BigInteger, db.ForeignKey('project.id'), primary_key=True)
                        )

industries = db.Table('industries',
                      db.Column('industry_id', db.BigInteger, db.ForeignKey('industry.id'), primary_key=True),
                      db.Column('project_id', db.BigInteger, db.ForeignKey('project.id'), primary_key=True)
                      )

sets = db.Table('sets',
                db.Column('set_id', db.BigInteger, db.ForeignKey('set.id'), primary_key=True),
                db.Column('project_id', db.BigInteger, db.ForeignKey('project.id'), primary_key=True)
                )


class Project(db.Model):
    id = db.Column(db.BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    title = db.Column(db.String(100))
    url = db.Column(db.String(100))
    description = db.Column(db.Text)
    logo_url = db.Column(db.String(2048))
    is_public = db.Column(db.Boolean)
    technologies = db.relationship('Technology', secondary=technologies, lazy='subquery',
                                   backref=db.backref('project', lazy=True))
    industries = db.relationship('Industry', secondary=industries, lazy='subquery',
                                 backref=db.backref('project', lazy=True))
    sets = db.relationship('Set', secondary=sets, lazy='subquery', backref=db.backref('project', lazy=True))
    attachments = db.relationship('Attachment', backref='project', lazy=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    def get_info(self):
        query = db.session.query(Company)
        company = query.filter(Company.id == self.company_id).first()

        info = {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "description": self.description,
            "logo_url": self.logo_url,
            "is_public": self.is_public,
            "company": company.get_info(),
            "industries": [{"id": industry.id, "name": industry.name} for industry in self.industries],
            "technologies": [{"id": technology.id, "name": technology.name} for technology in self.technologies],
            "attachments": [{"id": attachment.id, "extension": attachment.extension} for attachment in self.attachments]
        }
        return info


class Set(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100))
    tokens = db.relationship('SetToken', backref='set', lazy=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))


class SetToken(db.Model):
    set_id = db.Column(db.BigInteger, db.ForeignKey('set.id'), nullable=False, primary_key=True)
    token = db.Column(db.String(100), primary_key=True)


class CompanyReport(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    report_message = db.Column(db.Text)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.BigInteger, db.ForeignKey('company.id'), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True))
    is_resolved = db.Column(db.Boolean, default=False)
    date_resolved = db.Column(db.DateTime(timezone=True))

    def get_info(self):
        info = {
            "id": self.id,
            "message": self.report_message,
            "userId": self.user_id,
            "companyId": self.company_id,
            "dateCreated": self.date_created,
            "isResolved": self.is_resolved,
            "dateResolved": self.date_resolved
        }
        return info


class CompanyFeedback(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    feedback = db.Column(db.Text)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.BigInteger, db.ForeignKey('company.id'), nullable=False)
    star = db.Column(db.Float)
    date_created = db.Column(db.DateTime(timezone=True))
