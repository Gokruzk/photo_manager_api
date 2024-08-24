from Model.models import Ubication
from Config.db import conn


class CountriesRoutes:
    @staticmethod
    async def get_all() -> list[Ubication]:
        try:
            countries = await conn.prisma.ubication.find_many()
            return countries
        except:
            return False
