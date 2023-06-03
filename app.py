from flask_cors import *
from flask import Flask, request
from flask.views import MethodView
from flask import jsonify
from extension import db,cors
from sqlalchemy import func,Integer
from model import merged
import numpy as np
from datetime import datetime
from shapely.geometry import shape, Point
import pymysql
import json
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
        # 获取选择的时间范围，时间粒度，分析类型
        formTimeRange = request.json.get('timeRange')
        print(formTimeRange)
        formTimeStep =  request.json.get('timeStap')
        #判断车辆和行人，2是行人
        switchPeopleOrCar=2
        timeStep = 0
        if(formTimeStep == '1'):#python条件查询注意变量格式
            timeStep = 3600000000
        if(formTimeStep ==' 0.5'):
            timeStep = 3600000000/2
        resultCar = QueryByCriteriaTick(formTimeRange,timeStep)#返回每小时时刻的车辆轨迹
        resultCarRange0 = QueryByTimeRange(formTimeRange,switchPeopleOrCar)#返回时间阔度内的所有的车辆轨迹点
        resultCarRange = pointInTrack(resultCarRange0,1681340400099685,formTimeRange)#计算该时间范围内每个区域经过的的车辆数量
        print(resultCarRange)
        result ={
            'tickCar':resultCar,
            'areaCar':resultCarRange
        }
        return {
            'status': 'success',
            'message': '查询成功',
            'results': result
        }
    if request.method == 'GET':
        resultPost = []
        return {
            'status': 'success',
            'message': '查询成功',
            'results': resultPost
        }



#定义条件查询 查询每个时刻的轨迹点位置数组
def QueryByCriteriaTick(timeLong,timeStep):
    for i in range(1681340400099685,timeLong,timeStep):# start ,  stop , and  step
        carStepOne :[merged]= merged.query.filter(merged.time_meas == i).all()
        curr = [
            {
                'id': car.id,
                'is_moving':car.is_moving,
                'x_coord' :float(car.x_coord),
                'y_coord':float(car.y_coord),
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
        #print(carList[0][0]['x_coord'])
    return carList

#返回一个指定时间内按小时划分片段的轨迹点数组对象
def QueryByCriteriaArea(timeLong,timeStep,selectType):
    carList = []
    for i in range(1681340400099685,timeLong,timeStep):# start ,  stop , and  step
        carStepOne :[merged]= merged.query.filter(merged.time_meas.between(i,i+timeStep),merged.type != selectType).all()
        curr = [
            {
                'id': car.id,
                'is_moving':car.is_moving,
                'x_coord' :float(car.x_coord),
                'y_coord':float(car.y_coord),
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
        carList.append(curr)#fanhui返回一个指定时间内按小时划分片段的轨迹点数组对象
        print(carList[0][0]['x_coord'])
    return  carList

#查询指定时间范围内的所有车辆或者行人的轨迹位置，用来统计车流量或者人流量
def QueryByTimeRange(timeLong,selectType):
    carStepOne: [merged] = merged.query.filter(merged.time_meas.between(1681340400099685, timeLong),merged.type != selectType).all()
    curr = [
        [float(car.x_coord),float(car.y_coord)] for car in carStepOne
    ]
    return curr

#车流量计算
def pointInTrack(pointData,startTime,endTime):
    timeRange = calculateTime(startTime, endTime)
    print('11111111111')
    print(timeRange)
    with open('./mapData/crosswalkroad_with9road.geojson') as f:
        geojson_data = json.load(f)
        streeCarCount=[]
        for geoMap in geojson_data['features']:
            polygon = shape(geoMap['geometry'])
            count = 0
            for point in pointData:
                if polygon.contains(Point(point)):
                    count += 1
            datacURR = {
                'ID':geoMap['properties']['fid'],
                'carNum':count/timeRange   #车流量 = 指定区域车的数量/时间范围
            }
            streeCarCount.append(datacURR)
        print(streeCarCount)
        return streeCarCount

#geod地图三维转二维
def three2two(geojson_data):
    for feature in geojson_data['features']:
        if feature['geometry']['type'] == 'Point':
            coords = feature['geometry']['coordinates']
            feature['geometry']['coordinates'] = [coords[0], coords[1]]
        elif feature['geometry']['type'] == 'LineString':
            coords = feature['geometry']['coordinates']
            feature['geometry']['coordinates'] = [[coord[0], coord[1]] for coord in coords]
        elif feature['geometry']['type'] == 'Polygon':
            coords = feature['geometry']['coordinates']
            feature['geometry']['coordinates'] = [[[coord[0], coord[1]] for coord in ring] for ring in coords]
    return geojson_data

#最小时间戳1681340400099685
#最大时间戳1681372799599885
#时间转换函数
def changeTime(timeCurrent,timeStp):
    curr = timeCurrent/1000000
    dt = datetime.fromtimestamp(curr)
    dt = dt + datetime.timedelta(hours=timeStp)
    new_timestamp = int(dt.timestamp() * 1000000)
    return new_timestamp

#时间差计算函
def calculateTime(timeStart,timeEnd):
    datetime1 = datetime.fromtimestamp(timeStart / 1000000)
    datetime2 = datetime.fromtimestamp(timeEnd / 1000000)
    timedelta = datetime2 - datetime1
    hours = timedelta.total_seconds() / 3600
    return hours

if __name__ == '__main__':
    app.run(debug=True)