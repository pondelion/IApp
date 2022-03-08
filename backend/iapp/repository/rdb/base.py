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

    def get_by_filter(self, db: Session, filter_conditions) -> List[ModelType]:
        if not isinstance(filter_conditions, list):
            filter_conditions = [filter_conditions]
        res = None
        for fc in filter_conditions:
            if res is None:
                res = db.query(self._model).filter(fc)
            else:
                res = res.filter(fc)
        return res.all()

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
        check_already_id_exists: bool = False,
        check_already_exists_filter_conditions = None,
    ) -> ModelType:
        if check_already_id_exists:
            db_data = self.get_by_id(db, id=data.id)
            if db_data:
                return db_data
        if check_already_exists_filter_conditions:
            db_data = self.get_by_filter(db, filter_conditions=check_already_exists_filter_conditions)
            if db_data:
                return db_data
        json_data = jsonable_encoder(data)
        db_data = self._model(**json_data)
        db.add(db_data)
        if commit:
            db.commit()
            db.refresh(db_data)
        return db_data

    def create_all(
        self,
        db: Session,
        *,
        data_list: List[CreateSchemaType],
        commit: bool = True,
        check_already_id_exists: bool = False,
        check_already_exists_filter_conditions_list = None,
    ) -> List[ModelType]:
        if check_already_id_exists:
            data_list_in_db = [self.get_by_id(db, id=data.id) for data in data_list]
            data_list = [data for data, data_in_db in zip(data_list, data_list_in_db) if data_in_db is None]
        if check_already_exists_filter_conditions_list:
            data_list_in_db = [
                self.get_by_filter(db, filter_conditions=check_already_exists_filter_conditions)
                for check_already_exists_filter_conditions in check_already_exists_filter_conditions_list
            ]
            data_list = [data for data, data_in_db in zip(data_list, data_list_in_db) if len(data_in_db) == 0]
        if len(data_list) == 0:
            return []
        db_data_list = [self._model(**jsonable_encoder(data)) for data in data_list]
        # db.add_all(db_data_list)
        db.bulk_save_objects(db_data_list, return_defaults=True)
        if commit:
            db.commit()
        return db_data_list

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
        filter_conditions,
        update_data: Union[UpdateSchemaType, Dict[str, Any]],
        commit: bool = True,
    ) -> int:
        if isinstance(update_data, dict):
            update_data_dict = update_data
        else:
            update_data_dict = update_data.dict(exclude_unset=True)
        if not isinstance(filter_conditions, list):
            filter_conditions = [filter_conditions]
        res = None
        for fc in filter_conditions:
            if res is None:
                res = db.query(self._model).filter(fc)
            else:
                res = res.filter(fc)
        updated = res.update(update_data_dict)
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

    def upsert(
        self,
        db: Session,
        *,
        data: CreateSchemaType,
        commit: bool = True,
    ) -> ModelType:
        return self.upsert_by_id(db, data=data, commit=commit)

    def upsert_by_id(
        self,
        db: Session,
        *,
        data: CreateSchemaType,
        commit: bool = True,
    ) -> ModelType:
        db_data = self.get_by_id(db, id=data.id)
        if db_data:
            self.update(db, db_data=db_data, update_data=data.__dict__)
        else:
            self.create(db, data=data)

    def upsert_by_filter_condition(
        self,
        db: Session,
        *,
        data: CreateSchemaType,
        filter_conditions,
        commit: bool = True,
    ) -> ModelType:
        db_data = self.get_by_filter(db, filter_conditions)
        if db_data:
            self.update(db, db_data=db_data, update_data=data.__dict__)
        else:
            self.create(db, data=data)
