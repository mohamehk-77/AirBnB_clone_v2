#!/usr/bin/python3
from sqlalchemy import Table, Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.amenity import Amenity

metadata = Base.metadata
place_amenity = Table('place_amenity', metadata,
                      Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reviews = relationship("Review", backref="place", cascade="all, delete")
    amenities = relationship("Amenity", secondary=place_amenity, viewonly=False)
    amenity_ids = []

    @property
    def reviews(self):
        from models.review import Review
        from models import storage
        """Returns the list of Review instances with place_id equals to the current Place.id"""
        all_reviews = storage.all(Review)
        place_reviews = [review for review in all_reviews.values() if review.place_id == self.id]
        return place_reviews

    @property
    def amenities(self):
        """Returns the list of Amenity instances with place_id equals to the Place.id"""
        from models import storage
        return [storage.get(Amenity, id) for id in self.amenity_ids]

    @amenities.setter
    def amenities(self, obj):
        from models.amenity import Amenity
        """Handles append method for adding an Amenity.id to the attribute amenity_ids"""
        if type(obj) is Amenity:
            self.amenity_ids.append(obj.id)
