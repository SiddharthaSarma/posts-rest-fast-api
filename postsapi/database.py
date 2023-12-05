import databases
import sqlalchemy

metadata = sqlalchemy.MetaData()

# Create tables
posts_table = sqlalchemy.Table(
  "posts",
  metadata,
  sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
  sqlalchemy.Column('body', sqlalchemy.String)
)

comments_table = sqlalchemy.Table(
  "comments",
  metadata,
  sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
  sqlalchemy.Column('body', sqlalchemy.String),
  sqlalchemy.Column('post_id', sqlalchemy.ForeignKey('posts.id'), nullable=False)
)

engine = sqlalchemy.create_engine(
  'sqlite:///posts.db',
  connect_args={'check_same_thread': False}
)

metadata.create_all(engine)

database = databases.Database(
  'sqlite:///posts.db',
  force_rollback=False
)