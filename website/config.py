from website.routes import main 
from flask import Flask
from website import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '7ebfa07e02b8fc7dba756a43e23b4a'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Mysql%40123@localhost/minor_project'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    with app.app_context():
        db.create_all()

    app.register_blueprint(main)

    return app
