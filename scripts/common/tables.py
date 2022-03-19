from sqlalchemy import Column, Integer, String, Date, cast
from sqlalchemy.orm import declarative_base, column_property

Base = declarative_base()

class DriveAll(Base):
    __tablename__ = "drive"

    trip_id = Column(String(55))
    datetime = Column(String(55))
    vehicle_spec_id = Column(Integer)
    engine_coolant_temp = Column(Integer)
    eng_load = Column(Integer)
    fuel_level = Column(Integer)
    iat = Column(Integer)
    rpm = Column(Integer)
    lat = Column(Integer)
    long = Column(Integer)
    velocity = Column(Integer)
    # Create a unique transaction id
    # transaction_id = column_property(
    #     date_of_sale + "_" + address + "_" + county + "_" + price
    # )

class VehicleAll(Base):
    __tablename__ = "vehicle"

    id = Column(Integer, primary_key=True)
    vehicle_spec_id = Column(Integer)
    year = Column(Integer)
    make = Column(String(55))
    model = Column(String(55))
    drivetrain = Column(Integer)
    max_torque = Column(Integer)
    max_horsepower = Column(Integer)
    max_horsepower_rpm = Column(Integer)
    max_torque_rpm = Column(Integer)
    engine_displacement = Column(Integer)
    fuel_type = Column(Integer)
    fuel_tank_capacity = Column(Integer)
    fuel_economy_city = Column(Integer)
    fuel_economy_highway = Column(Integer)
    cylinders = Column(Integer)
    forced_induction = Column(Integer)
    device_generation = Column(Integer)
    # # Create a unique transaction id
    # # all non-string columns are casted as string
    # transaction_id = column_property(
    #     cast(date_of_sale, String) + "_" + address + "_" + county + "_" + cast(price, String)
    # )