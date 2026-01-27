from Api.database import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles

@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"

user_endorses_log = Table(
    'user_endorses_log',
    db.Model.metadata,
    Column('log_id', Integer, ForeignKey('log.id'), primary_key=True),
    Column('endorsers', Integer, ForeignKey('users.id')),
    extend_existing=True
)
