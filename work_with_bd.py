from sqlalchemy.orm import Session
from sqlalchemy import select
from database import engine, Object, House


def add_to_db(for_object, for_house):
    with Session(engine) as session:
        check_house = select(House).where(House.address == for_house["address"])
        result = session.execute(check_house)
        results = result.scalars().all()
        new_house = True
        for i in results:
            if i.address == for_house["address"]:
                new_house = False
                house_id = i.id
                break

        check_object = select(Object).where(Object.offer_id == for_object["offer_id"])
        result_check_object = session.execute(check_object)
        results_check_object = result_check_object.scalars().all()
        new_object = True
        new_price = True
        for j in results_check_object:
            if j.offer_id == for_object["offer_id"]:
                new_object = False
                if j.price == for_object["price"]:
                    new_price = False
                    break

        if new_house:
            new_record = House(
                address=for_house["address"],
                year_house=for_house["year_house"],
                floors_count=for_house["floors_count"],
                house_material_type=for_house["house_material_type"],
                object=[Object(
                    category=for_object["category"],
                    price=for_object["price"],
                    total_area=for_object["total_area"],
                    floor_num=for_object["floor_num"],
                    offer_id=for_object["offer_id"]
                )],
            )
            session.add(new_record)
            session.commit()
        else:
            if new_object:
                new_record = Object(
                    category=for_object["category"],
                    price=for_object["price"],
                    total_area=for_object["total_area"],
                    floor_num=for_object["floor_num"],
                    offer_id=for_object["offer_id"],
                    house_id=house_id
                )
                session.add(new_record)
                session.commit()

            else:
                if new_price:
                    update_object = select(Object).where(Object.offer_id == for_object["offer_id"])
                    session.scalars(update_object).one().price = for_object["price"]
                    session.commit()
