from fastapi import APIRouter, Depends
from app.utils.template import Template
from app.core.settings import settings
import sqlalchemy
from sqlalchemy.schema import CreateTable, DropTable, CreateIndex
from app.repos.logs_repo import table as logs_repo
from app.repos.user_repo import table as user_repo


router = APIRouter()

@router.get("/system-init")
async def system_init(template: Template = Depends()):
    sql = ""

    repos = {
        logs_repo,
        user_repo,
    }

    engine = sqlalchemy.create_engine(settings.database_url)
    for table in repos:
        sql += str(DropTable(table).compile(engine)).strip()
        sql += ";\n"
        sql += str(CreateTable(table).compile(engine)).strip()
        sql += ";\n"
        for idx in table.indexes:
            sql += str(CreateIndex(idx).compile(engine)).strip()
            sql += ";\n"
        sql += "\n"

    return await template.response('system-init.j2', {
        "sql": sql
    })

