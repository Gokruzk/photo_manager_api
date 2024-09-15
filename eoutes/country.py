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
            return countries
        except:
            return False
