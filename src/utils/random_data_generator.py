import asyncio
import random
import string
from datetime import date, timedelta

from tortoise import Tortoise

from core.db.models import City, Manufacturer, Beer, User, Creds, Review
from core.settings import TORTOISE_ORM


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def random_date(start, stop=date.today()):
    return start + timedelta(days=random.randint(0, (stop - start).days))


async def generate_data():
    await Tortoise.init(config=TORTOISE_ORM)
    cities = []
    for _ in range(50):
        city = City(name=randomword(20))
        await city.save()
        cities.append(city)
    # await City.bulk_create(cities)

    manufacturers = []
    for _ in range(50):
        manufacturer = Manufacturer(name=randomword(200),
                                    year_of_creation=random.randint(1970, 2023),
                                    city=random.choice(cities))
        await manufacturer.save()
        manufacturers.append(manufacturer)
    # await Manufacturer.bulk_create(manufacturers)

    beers = []
    for _ in range(50):
        beer = Beer(name=randomword(30),
                    style=randomword(10),
                    alc=random.uniform(0, 20),
                    abv=random.uniform(0, 20),
                    plato=random.uniform(0, 20),
                    ibu=random.uniform(0, 20),
                    manufacturer=random.choice(manufacturers))
        await beer.save()
        beers.append(beer)
    # await Beer.bulk_create(beers)

    users = []
    for _ in range(50):
        user = User(username=randomword(10),
                    first_name=randomword(30),
                    last_name=randomword(30),
                    birthday=random_date(date(1970, 1, 1)))
        await user.save()
        users.append(user)
    # await User.bulk_create(users)

    creds = []
    for user in users:
        cred = Creds(login=randomword(20),
                     passwd=randomword(60),
                     user=user)
        await cred.save()
        creds.append(cred)
    # await Creds.bulk_create(creds)

    reviews = []
    for _ in range(50):
        reviews.append(Review(review=randomword(1000),
                              rating=random.randint(1, 5),
                              beer=random.choice(beers[15:25]),
                              user=random.choice(users)))
    await Review.bulk_create(reviews)


if __name__ == '__main__':
    asyncio.run(generate_data())
