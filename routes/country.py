from prisma.errors import RecordNotFoundError
from model.models import Ubication
from config.db import conn


class CountriesRoutes:
    @staticmethod
    async def get_all() -> list[Ubication]:
        try:
            countries = await conn.prisma.ubication.find_many()

            # clean null data from schema
            for country in countries:
                del country.Images
                del country.User

        except RecordNotFoundError:
            return []
        except Exception as e:
            print(e)
            return False
        else:
            return countries
