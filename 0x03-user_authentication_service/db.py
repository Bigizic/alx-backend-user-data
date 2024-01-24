#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def new(self, obj):
        """Adds current object to database
        """
        self._session.add(obj)

    def save(self):
        """Saves in the database the object
        """
        self._session.commit()

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database.
        """
        new_user = User()
        new_user.email = email
        new_user.hashed_password = hashed_password
        self.new(new_user)
        self.save()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Locates a user based on arbitrary keywords
        Return:
            - First fow found in the users table
        """
        try:
            query = self._session.query(User).filter_by(**kwargs).first()
            if query is None:
                raise NoResultFound
            return query
        except InvalidRequestError as e:
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user based on user_id
        """
        try:
            find_user = self.find_user_by(id=user_id)
            if find_user:
                attributes = ["id",
                              "email",
                              "hashed_password",
                              "session_id",
                              "reset_token"]
                valid_records = {
                        x: v for x, v in kwargs.items() if x in attributes
                }
                if valid_records:
                    for k, v in valid_records.items():
                        find_user.k = v
                        self.save()
                else:
                    raise ValueError
                return None
        except ValueError as e:
            raise e
