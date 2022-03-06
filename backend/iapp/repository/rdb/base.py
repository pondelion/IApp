from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from ...db.rdb import Session
from ...models.sqlalchemy.base import Base


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class BaseRDBRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self._model = model

    def get_all(self, db: Session) -> List[ModelType]:
        return db.query(self._model).all()

    def get_by_id(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self._model).filter(self._model.id == id).first()

    def get_by_filter(self, db: Session, filter_condition) -> Optional[ModelType]:
        return db.query(self._model).filter(filter_condition).all()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self._model).offset(skip).limit(limit).all()

    def create(
        self,
        db: Session,
        *,
        data: CreateSchemaType,
        commit: bool = True,
        check_already_exists: bool = False
    ) -> ModelType:
        if check_already_exists:
            db_data = self.get_by_id(db, id=data.id)
            if db_data:
                return db_data
        json_data = jsonable_encoder(data)
        db_data = self._model(**json_data)
        db.add(db_data)
        if commit:
            db.commit()
            db.refresh(db_data)
        return db_data

    def update(
        self,
        db: Session,
        *,
        db_data: ModelType,
        update_data: Union[UpdateSchemaType, Dict[str, Any]],
        commit: bool = True,
    ) -> ModelType:
        json_data = jsonable_encoder(db_data)
        if isinstance(update_data, dict):
            update_data_dict = update_data
        else:
            update_data_dict = update_data.dict(exclude_unset=True)
        for field in json_data:
            if field in update_data_dict:
                setattr(db_data, field, update_data_dict[field])
        # db.add(db_data)
        if commit:
            db.commit()
            db.refresh(db_data)
        return db_data

    def update_by_filter(
        self,
        db: Session,
        *,
        filter_condition,
        update_data: Union[UpdateSchemaType, Dict[str, Any]],
        commit: bool = True,
    ) -> int:
        if isinstance(update_data, dict):
            update_data_dict = update_data
        else:
            update_data_dict = update_data.dict(exclude_unset=True)
        updated = db.query(self._model).filter(filter_condition).update(update_data_dict)
        if commit:
            db.commit()
        return updated

    def remove(self, db: Session, *, id: int, commit: bool = True) -> ModelType:
        obj = db.query(self._model).get(id)
        db.delete(obj)
        if commit:
            db.commit()
        return ooj

    def exists(self, db: Session, *, id: int) -> bool:
        return True if db.query(self._model).get(id) else False

    def upsert(self, db: Session, *, data: CreateSchemaType, commit: bool = True) -> ModelType:
        db_data = self.get_by_id(db, id=data.id)
        if db_data:
            self.update(db, db_data=db_data, update_data=data.__dict__)
        else:
            self.create(db, data=data)
