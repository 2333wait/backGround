from flask_cors import *
from flask import Flask, request
from flask.views import MethodView
from flask import jsonify
from extension import db,cors
from sqlalchemy import func,Integer
from model import merged
import numpy as np
import datetime
import pymysql
import pymysql
app = Flask(__name__)
#允许跨域访问
CORS(app, supports_credentials=True)
# 设置连接URL
user = 'root'
password = '123456'
database = 'china2023'
# 动态追踪修改设置，如未设置只会提示警告
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/china2023'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)
cors.init_app(app)


#shuju生命数据变量
carList = [] #存放条件查询车辆点



#测试链接
@app.route('/')
def hellow_world():
    # 数据库查询
    result = merged.query.filter(merged.id == '146585964').count()
    print(result)
    return result

@app.route('/SelectData/',methods=['GET','POST'])
def allCars():
    if request.method == 'POST':
        #获取查询表单数据然后进行条件查询
        # 获取选择的降维算法和数据维度
        formTimeRange = request.json.get('timeRange')
        formTimeStep =  request.json.get('timeStap')
        timeStep = 0
        if(formTimeStep == '1'):#python条件查询注意变量格式
            timeStep = 3600000000
        if(formTimeStep ==' 0.5'):
            timeStep = 3600000000
        print(timeStep)
        resultCar = QueryByCriteria(formTimeRange,timeStep)
        print(resultCar)
        return {
            'status': 'success',
            'message': '查询成功',
            'results': resultCar
        }
    if request.method == 'GET':
        resultPost = []
        return {
            'status': 'success',
            'message': '查询成功',
            'results': resultPost
        }

#1681372799599885
#时间转换函数
def changeTime(timeStp):
    curr = timeStp/1000000
    dt = datetime.datetime.fromtimestamp(curr)

#定义条件查询
def QueryByCriteria(timeLong,timeStep):
    for i in range(1681340400099685,timeLong,timeStep):# start ,  stop , and  step
        carStepOne :[merged]= merged.query.filter(merged.time_meas == i).all()
        curr = [
            {
                'id': car.id,
                'is_moving':car.is_moving,
                'x_coord' :car.x_coord,
                'y_coord':car.y_coord,
                'shape_x' :car.shape_x,
                'shape_y' : car.shape_y,
                'shape_z' : car.shape_z,
                'orientation' :car.orientation,
                'velocity' :car.velocity,
                'type' : car.type,
                'heading' : car.heading,
                'time_meas' : car.time_meas,
                'ms_no' : car.ms_no,
                'time_diff' : car.time_diff,
            } for car in carStepOne
        ]
        carList.append(curr)
        print(len(carList))


    return carList


if __name__ == '__main__':
    app.run(debug=True)