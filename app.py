from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babelex import Babel

# 基本配置(语言/数据库/主题/名称)
app = Flask(__name__)
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
app.config['SECRET_KEY'] = '%2Fadmin%2Flottery%2F%3Fsort%3D0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='双色球', template_mode='bootstrap3')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Lottery(db.Model):
    """创建模型"""
    __tablename__ = 'lotteries'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    red1 = db.Column(db.Integer)
    red2 = db.Column(db.Integer)
    red3 = db.Column(db.Integer)
    red4 = db.Column(db.Integer)
    red5 = db.Column(db.Integer)
    red6 = db.Column(db.Integer)
    blue = db.Column(db.Integer)
    bonous = db.Column(db.Integer)

    def __unicode__(self):
        return self.desc

# 编写视图
class MyModelView(ModelView):
    columns = ('date','red1','red2','red3','red4','red5','red6','blue','bonous')
    column_searchable_list = columns
    column_filters = columns

# 注册视图
admin.add_view(MyModelView(Lottery, db.session))

if __name__ == "__main__":
    app.run()
