
from create_app import db
from dbModels import Polygon_table, Restaurant
from flask import Blueprint, request
from geoalchemy2 import WKTElement
from geoalchemy2.shape import to_shape
from shapely.geometry import Point, Polygon
from sqlalchemy import func
from errorhandling import ErrorHandling
from response import response
from geopy.distance import geodesic


geo_view = Blueprint('geo_view', __name__,url_prefix="/api/v4")

@geo_view.route("/addpolygon")
def insert_polygon():
    try:
        # points = [
        #     Point(77.63562941963538, 12.970354305605678),
        #     Point(77.63686832927202, 12.968676601777855),
        #     Point(77.64116497333104, 12.967170137185464),
        #     Point(77.64748253381863, 12.96756454815732),
        #     Point(77.64801851600187, 12.969037830830553),
        #     Point(77.64885324235279, 12.972703071955731),
        #     Point(77.62306975225019, 12.978398487151573),
        #     Point(77.62866561341723, 12.977868234184685),
        #     Point(77.64068244708565, 12.979448563163986),
        #     Point(77.6466421908762, 12.979089548083492)
        # ]
        data = request.get_json()
        id = data['id']
        name = data['name']
        polygon_points = data['polygon_values'] 
        points = []
    
        for point in polygon_points:
            points.append(Point(point.get('longitude'), point.get('latitude')))
    
    
        polygon_geom = Polygon([[point.x, point.y] for point in points])
        wkt_element = WKTElement(polygon_geom.wkt, srid=4326)
        polygon1 = Polygon_table(id= id, name=name, geom= wkt_element)
    
        db.session.add(polygon1)
        db.session.commit()
        
        return response.function("Polygon Created")
    
    except Exception as e:
        return ErrorHandling.handle_server_request(str(e))

@geo_view.route("/check_point_in_polygon")
def is_point_inside_polygon():
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
    
        user_point = Point(longitude, latitude)
        
        polygon_id = 21
        polygon = db.session.query(Polygon_table).filter_by(id=polygon_id).first()
        # polygon = db.session.query(Polygon_table).all()

        if polygon:
            polygon_shapely = to_shape(polygon.geom)
    
            is_inside = user_point.within(polygon_shapely)
            
            if(is_inside):
                return response.function("Inside the radius")
            
            return ErrorHandling.hanlde_bad_request("Outside the radius")
        else:
            return ErrorHandling.hanlde_bad_request("Server Range Found")
        
    except Exception as e:
        return ErrorHandling.handle_server_request(str(e))


@geo_view.route("/add_restaruant")
def insert_restaruant():
    try:
        data = request.get_json()
    
        id = data['id']
        name = data['name']
        distance = data['distance']
        latitude = data['latitude']
        longitude = data['longitude']
        
        print(latitude, longitude)
        location = func.ST_GeomFromText('POINT({} {})'.format(longitude, latitude))
    
        address = data['address']
    
        restaruant = Restaurant(id=id, name=name, distance=distance, location=location, address=address)
    
        db.session.add(restaruant)
    
        db.session.commit()
    
        return "Restuarant added"
    
    except Exception as e:
        return ErrorHandling.handle_server_request(str(e))


def format_distance(distance_km):
    if distance_km < 1:
        distance_meters = distance_km * 1000
        return f"{distance_meters:.2f} meters"
    else:
        return f"{distance_km:.2f} kilometers"
    

@geo_view.route("/restaruants_nearby")
def user_surrounded_restaruants():
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')

        user_location = (latitude, longitude)
        
        maximum_distance_km = 10 
        
        nearby_restaurants_query = db.session.query(
            Restaurant,
            func.ST_X(Restaurant.location).label('longitude'),
            func.ST_Y(Restaurant.location).label('latitude')
        )
        
        nearby_restaurants = []

        if(nearby_restaurants is None):
            return ErrorHandling.hanlde_bad_request("NO Restaruant found in the Radius")
        
        for restaurant, restaurant_longitude, restaurant_latitude in nearby_restaurants_query:
            restaurant_location = (restaurant_latitude, restaurant_longitude)
            distance_km = geodesic(user_location, restaurant_location).kilometers
            if distance_km <= maximum_distance_km:

                dis = "%.2f" % distance_km + " km"
                print(restaurant.name)
                nearby_restaurants.append({
                    'name': restaurant.name,
                    'distance' : dis
                })
        
        return response.function(nearby_restaurants)
    
    except Exception as e:
        return ErrorHandling.handle_server_request(str(e))


@geo_view.route("/sortingbydistance")
def sorting_restaurant():
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
    
        user_location = func.ST_GeomFromText('POINT({} {})'.format(longitude, latitude))
    
        nearby_restaurants_query = db.session.query(
            Restaurant,
            func.ST_Distance(Restaurant.location, user_location).label('distance')
        ).order_by(
            'distance'
        )
        
        nearby_restaurants = nearby_restaurants_query.all()
        
        if nearby_restaurants is None:
            return "None"
        
        restaurant_list = []
        for restaurant, distance in nearby_restaurants:
    
            distance_km = distance * 111.32
            formatted_distance = format_distance(distance_km)
    
            res = f"Restaurant: {restaurant.name}, Distance: {formatted_distance} degrees"
    
            restaurant_list.append(res)
    
        return restaurant_list
    
    except Exception as e:
        return ErrorHandling.handle_server_request(str(e))