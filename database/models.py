from db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

# this creates a many to many relationship  
liked_posts = Table(
    "liked_post",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("user_id", Integer, ForeignKey("users.id"))
)
#post_id user_id


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner" )
    posts = relationship("Post", back_populates="author")
    posts_liked = relationship("Post", secondary=liked_posts, back_populates="liked_by_users")
# user.itemd -> list of items owned by user 
# 1:1 mapping : one item owned by one user 
# 1:many mapping : one user can own multiple items

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
#item.owner -> User who owns this item

#many: many mapping : one user can like multiple posts, one post can be likeed by multiple users

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    content = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")
    liked_by_users = relationship("User", secondary=liked_posts, back_populates="posts_liked")

