import math
from uuid import uuid4
from sqlalchemy import update as sql_update, delete as sql_delete
from sqlalchemy.sql import select, or_, text, func, column
from app.schema import PersonCreate, PageResponse
from app.config import db, commit_rollback
from app.model import Person


class PersonRepository:

    @staticmethod
    async def create(create_form: PersonCreate):
        """ Create person data """
        db.add(Person(
            id=str(uuid4()),
            name=create_form.name,
            sex=create_form.sex,
            birth_date=create_form.birth_date,
            birth_place=create_form.birth_place,
            country=create_form.country
        ))
        await commit_rollback()

    @staticmethod
    async def get_person_by_id(person_id: int):
        """ Retrieve person data by id"""
        query = select(Person).where(Person.id == person_id)
        return (await db.execute(query)).scalar_one_or_none()

    @staticmethod
    async def update(person_id: int, update_form: PersonCreate):
        """ Update person data """
        query = sql_update(Person) \
            .where(Person.id == person_id) \
            .values(**update_form) \
            .execute_options(synchronize_session=True)
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def delete(person_id: int):
        """ Delete person data by id"""
        query = sql_delete(Person).where(Person.id == person_id)
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def get_all(
        page: int = 1,
        limit: int = 10,
        columns: str = None,
        sort: str = None,
        filter: str = None
    ):
        """ Retrieve all persons """
        query = select(from_obj=Person, columns="*")

        # Select columns dynamically
        if columns is not None and columns != "all":
            # We need column format data like this -> [column(id), column(name) ...]
            query = select(from_obj=Person, columns=convert_columns(columns))

        # Select filter dynamically
        if filter is not None and filter != "null":
            # We need filter format data like this -> {'name': 'an', 'country': 'an'}

            # Convert string to dict format
            criteria = dict(x.split("*") for x in filter.split('-'))

            criteria_list = []

            # Check every key in dict. Are there any table attributes that same as the dict key?
            for attr, value in criteria.items():
                _attr = getattr(Person, attr)

                # filter format
                search = "%{}%".format(value)

                # criteria list
                criteria_list.append(_attr.like(search))

            query = query.filter(or_(*criteria_list))

        # Select sort dynamically
        if sort is not None and sort != "null":
            # We need sort format data like this -> ['id','name']
            query = query.order_by(text(convert_sort(sort)))

        # Count query
        count_query = select(func.count(1)).select_from(query)

        offset_page = page - 1
        # Pagination
        query = (query.offset(offset_page * limit).limit(limit))

        # Total record
        total_record = (await db.execute(count_query)).scalar() or 0

        # Total page
        total_page = math.ceil(total_record / limit)

        # Result
        result = (await db.execute(query)).fetchall()

        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_page,
            total_record=total_record,
            content=result
        )


def convert_sort(sort: str) -> str:
    """ Convert sort string to sqlalchemy sort string """
    return ','.join(sort.split('-'))


def convert_columns(columns: str) -> list:
    """ Convert columns string to list """
    return list(map(lambda x: column(x), columns.split('-')))
