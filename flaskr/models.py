from flaskr.database import db

chats = db.Table('chats',
                 db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'), primary_key=True),
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                 )


class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    chats = db.relationship("Chat", secondary=chats, lazy='subquery',
                            backref=db.backref('user', lazy=True))
    phone_number = db.Column(db.String(50))
    password = db.Column(db.String(100))
    ava_url = db.Column(db.String(2048))
    mini_ava_url = db.Column(db.String(2048))
    is_staff = db.Column(db.Boolean)
    is_blocked = db.Column(db.Boolean)
    date_joined = db.Column(db.DateTime(timezone=True))
    messages = db.relationship('Message', backref='user', lazy=True)


class Chat(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    chat_name = db.Column(db.String(100))
    ava_url = db.Column(db.String(2048))
    mini_ava_url = db.Column(db.String(2048))
    messages = db.relationship('Message', backref='chat', lazy=True)


class Technology(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'),
                           nullable=False)


class Attachment(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    link = db.Column(db.String(2048))
    extension = db.Column(db.String(100))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'),
                           nullable=False)


class Company(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(50))
    employees_num = db.Column(db.BigInteger)
    logo_url = db.Column(db.String(2048))
    mini_logo_url = db.Column(db.String(2048))
    location = db.Column(db.String(100))
    description = db.Column(db.String)
    is_verified = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime(timezone=True))
    projects = db.relationship('Project', backref='company', lazy=True)
    companyFeedbacks = db.relationship('CompanyFeedback', backref='company', lazy=True)
    userFeedbacks = db.relationship('UserFeedback', backref='company', lazy=True)
    sets = db.relationship('Set', backref='company', lazy=True)


class CompanyFeedback(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    feedback = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'),
                           nullable=False)
    is_report = db.Column(db.Boolean)


class Industry(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'),
                           nullable=False)


class Message(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    chat_id = db.Column(db.BigInteger, db.ForeignKey('chat.id'),
                        nullable=False)
    message = db.Column(db.String)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'),
                        nullable=False)
    mini_ava_url = db.Column(db.String(2048))
    date = db.Column(db.DateTime(timezone=True))


technologies = db.Table('technologies',
                        db.Column('technology_id', db.Integer, db.ForeignKey('technology.id'), primary_key=True),
                        db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True)
                        )

industries = db.Table('industries',
                      db.Column('industry_id', db.Integer, db.ForeignKey('industry.id'), primary_key=True),
                      db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True)
                      )

sets = db.Table('sets',
                db.Column('set_id', db.Integer, db.ForeignKey('set.id'), primary_key=True),
                db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True)
                )


class Project(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(100))
    url = db.Column(db.String(100))
    description = db.Column(db.String)
    logo_url = db.Column(db.String(2048))
    mini_logo_url = db.Column(db.String(2048))
    is_verified = db.Column(db.Boolean)
    technologies = db.relationship('Technology', secondary=technologies, lazy='subquery',
                                   backref=db.backref('project', lazy=True))
    industries = db.relationship('Industry', secondary=industries, lazy='subquery',
                                 backref=db.backref('project', lazy=True))
    sets = db.relationship('Set', secondary=sets, lazy='subquery',
                           backref=db.backref('project', lazy=True))
    attachments = db.relationship('Attachment', backref='project', lazy=True)


class Set(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100))
    tokens = db.relationship('SetToken', backref='set', lazy=True)


class SetTokens(db.Model):
    set_id = db.Column(db.BigInteger, db.ForeignKey('set.id'),
                       nullable=False, primary_key=True)
    token = db.Column(db.String(100), primary_key=True)


class UserFeedback(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    feedback = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'),
                           nullable=False)
    is_report = db.Column(db.Boolean)
