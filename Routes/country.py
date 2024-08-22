from Model.models import Ubication
from Config.db import conn


class CountriesRoutes:
    @staticmethod
    async def get_all() -> list[Ubication]:
        countries = await conn.prisma.ubication.find_many()
        return countries

    @staticmethod
    async def get_by_id(id: int) -> Ubication:
        country = await conn.prisma.ubication.find_first_or_raise(where={"cod_ubi": id})
        return country
