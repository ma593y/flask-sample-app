import re
from datetime import date
from sqlalchemy import or_
from models.vehicles_model import VehiclesModel



def get_vehicles_query_filters(request_args):
    filter_args = {
        "make": request_args.get("make", default='', type=str).strip('[]').lower(),
        "model": request_args.get("model", default='', type=str).strip('[]').lower(),
        "color": request_args.get("color", default='', type=str).strip('[]').lower(),
        "fuel_type": request_args.get("fuel_type", default='', type=str).strip('[]').lower(),
        "transmission": request_args.get("transmission", default='', type=str).strip('[]').lower(),
        "year": request_args.get("year", default=0, type=int),
        "year_min": request_args.get("year_min", default=0, type=int),
        "year_max": request_args.get("year_max", default=0, type=int),
        "price": request_args.get("price", default=0, type=int),
        "price_min": request_args.get("price_min", default=0, type=int),
        "price_max": request_args.get("price_max", default=0, type=int),
        "mileage": request_args.get("mileage", default=0, type=int),
        "mileage_min": request_args.get("mileage_min", default=0, type=int),
        "mileage_max": request_args.get("mileage_max", default=0, type=int),
        "tank_capacity": request_args.get("tank_capacity", default=0, type=int),
        "tank_capacity_min": request_args.get("tank_capacity_min", default=0, type=int),
        "tank_capacity_max": request_args.get("tank_capacity_max", default=0, type=int),
        "engine_capacity": request_args.get("engine_capacity", default=0, type=int),
        "engine_capacity_min": request_args.get("engine_capacity_min", default=0, type=int),
        "engine_capacity_max": request_args.get("engine_capacity_max", default=0, type=int),
    }

    query_filters = []
    if filter_args["make"]:
        print("make:", [x for x in filter_args["make"].split(',') if x.strip().isalpha()])
        query_filters.append(VehiclesModel.vehicle_make.in_([x.strip() for x in filter_args["make"].split(',') if x.strip().isalpha()]))
    
    if filter_args["model"]: 
        print("model:", [x for x in filter_args["model"].split() if x.strip().isalnum()])
        query_filters.append(or_(*[VehiclesModel.vehicle_model.like(f"%{x.strip()}%") for x in filter_args["model"].split() if x.strip().isalnum()]))
    
    if filter_args["color"]:
        print("color:", [x for x in filter_args["color"].split(',') if re.match(r"[a-zA-Z ]*$", x.strip())])
        query_filters.append(VehiclesModel.vehicle_color.in_([x.strip() for x in filter_args["color"].split(',') if re.match(r"[a-zA-Z ]*$", x.strip())]))
    
    if filter_args["fuel_type"]:
        print("fuel_type:", [x for x in filter_args["fuel_type"].split(',') if x.strip().isalpha()])
        query_filters.append(VehiclesModel.vehicle_fuel_type.in_([x.strip() for x in filter_args["fuel_type"].split(',') if x.strip().isalpha()]))
    
    if filter_args["transmission"]:
        print("transmission:", [x for x in filter_args["transmission"].split(',') if x.strip().isalpha()])
        query_filters.append(VehiclesModel.vehicle_transmission.in_([x.strip() for x in filter_args["transmission"].split(',') if x.strip().isalpha()]))
    

    if filter_args["year"] and (filter_args["year"] >= 1990) and (filter_args["year"] <= date.today().year):
        print("year:", filter_args["year"])
        query_filters.append(VehiclesModel.vehicle_year==filter_args["year"])
    else:
        if filter_args["year_min"] and (filter_args["year_min"] >= 1990) and (filter_args["year_min"] <= date.today().year):
            print("year_min:", filter_args["year_min"])
            query_filters.append(VehiclesModel.vehicle_year>=filter_args["year_min"])
        
        if filter_args["year_max"] and (filter_args["year_max"] >= 1990) and (filter_args["year_max"] <= date.today().year):
            print("year_max:", filter_args["year_max"])
            query_filters.append(VehiclesModel.vehicle_year<=filter_args["year_max"])
    
    if filter_args["price"] and (filter_args["price"] >= 0):
        print("price:", filter_args["price"])
        query_filters.append(VehiclesModel.vehicle_price==filter_args["price"])
    else:
        if filter_args["price_min"] and (filter_args["price_min"] >= 0):
            print("price_min:", filter_args["price_min"])
            query_filters.append(VehiclesModel.vehicle_price>=filter_args["price_min"])
        
        if filter_args["price_max"] and (filter_args["price_max"] >= 0):
            print("price_max:", filter_args["price_max"])
            query_filters.append(VehiclesModel.vehicle_price<=filter_args["price_max"])
    
    if filter_args["mileage"] and (filter_args["mileage"] >= 0):
        print("mileage:", filter_args["mileage"])
        query_filters.append(VehiclesModel.vehicle_mileage==filter_args["mileage"])
    else:
        if filter_args["mileage_min"] and (filter_args["mileage_min"] >= 0):
            print("mileage_min:", filter_args["mileage_min"])
            query_filters.append(VehiclesModel.vehicle_mileage>=filter_args["mileage_min"])
        
        if filter_args["mileage_max"] and (filter_args["mileage_max"] >= 0):
            print("mileage_max:", filter_args["mileage_max"])
            query_filters.append(VehiclesModel.vehicle_mileage<=filter_args["mileage_max"])
    
    if filter_args["tank_capacity"] and (filter_args["tank_capacity"] >= 0):
        print("tank_capacity:", filter_args["tank_capacity"])
        query_filters.append(VehiclesModel.vehicle_tank_capacity==filter_args["tank_capacity"])
    else:
        if filter_args["tank_capacity_min"] and (filter_args["tank_capacity_min"] >= 0):
            print("tank_capacity_min:", filter_args["tank_capacity_min"])
            query_filters.append(VehiclesModel.vehicle_tank_capacity>=filter_args["tank_capacity_min"])
        
        if filter_args["tank_capacity_max"] and (filter_args["tank_capacity_max"] >= 0):
            print("tank_capacity_max:", filter_args["tank_capacity_max"])
            query_filters.append(VehiclesModel.vehicle_tank_capacity<=filter_args["tank_capacity_max"])
    
    if filter_args["engine_capacity"] and (filter_args["engine_capacity"] >= 0):
        print("engine_capacity:", filter_args["engine_capacity"])
        query_filters.append(VehiclesModel.vehicle_engine_capacity==filter_args["engine_capacity"])
    else:
        if filter_args["engine_capacity_min"] and (filter_args["engine_capacity_min"] >= 0):
            print("engine_capacity_min:", filter_args["engine_capacity_min"])
            query_filters.append(VehiclesModel.vehicle_engine_capacity>=filter_args["engine_capacity_min"])
        
        if filter_args["engine_capacity_max"] and (filter_args["engine_capacity_max"] >= 0):
            print("engine_capacity_max:", filter_args["engine_capacity_max"])
            query_filters.append(VehiclesModel.vehicle_engine_capacity<=filter_args["engine_capacity_max"])
    
    return query_filters


