from Api.database import db
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles

@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"

user_endorses_log = db.Table('user_endorses_log',
    db.Column('log_id',db.Integer, db.ForeignKey('log.id'), primary_key=True),
    db.Column('endorsers',db.Integer, db.ForeignKey('users.id')))
