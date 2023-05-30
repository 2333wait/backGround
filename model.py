from  extension import db


#创建导入字段
class merged(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    is_moving = db.Column(db.String(255), nullable=False)
    x_coord = db.Column(db.String(255), nullable=False)
    y_coord= db.Column(db.String(255), nullable=False)
    shape_x = db.Column(db.String(255), nullable=False)
    shape_y = db.Column(db.String(255), nullable=False)
    shape_z = db.Column(db.String(255), nullable=False)
    orientation = db.Column(db.String(255), nullable=False)
    velocity = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    heading = db.Column(db.String(255), nullable=False)
    time_meas = db.Column(db.String(255), nullable=False)
    ms_no = db.Column(db.String(255), nullable=False)
    time_diff = db.Column(db.String(255), nullable=False)