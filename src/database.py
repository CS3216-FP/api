import uuid
from contextlib import contextmanager

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    create_engine,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import UniqueConstraint

from src.config import APP_CONFIG

_base = declarative_base()


class Base(_base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    @property
    def additional_things_to_dict(self):
        return {}

    def asdict(self):
        d = {}
        columns = self.__table__.columns.keys()

        for col in columns:
            item = getattr(self, col)

            if isinstance(item, uuid.UUID):
                d[col] = str(item)
            else:
                d[col] = item

        for key, value in self.additional_things_to_dict.items():
            d[key] = value

        return d


class User(Base):
    __tablename__ = "users"

    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    can_buy = Column(Boolean, nullable=False, server_default="t")
    can_sell = Column(Boolean, nullable=False, server_default="t")
    is_committee = Column(Boolean, nullable=False, server_default="t")

    sell_orders = relationship("SellOrder", back_populates="user")
    buy_orders = relationship("BuyOrder", back_populates="user")
    bans_as_buyer = relationship(
        "BannedPair", back_populates="buyer", foreign_keys="[BannedPair.buyer_id]"
    )
    bans_as_seller = relationship(
        "BannedPair", back_populates="seller", foreign_keys="[BannedPair.seller_id]"
    )
    seller = relationship(
        "ChatRoom", foreign_keys="ChatRoom.seller_id", back_populates="seller"
    )
    buyer = relationship(
        "ChatRoom", foreign_keys="ChatRoom.buyer_id", back_populates="buyer"
    )
    author = relationship(
        "Chat", foreign_keys="Chat.author_id", back_populates="author"
    )


class Security(Base):
    __tablename__ = "securities"

    name = Column(String, nullable=False, unique=True)

    sell_orders = relationship("SellOrder", back_populates="security")
    buy_orders = relationship("BuyOrder", back_populates="security")


class SellOrder(Base):
    __tablename__ = "sell_orders"

    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    security_id = Column(UUID, ForeignKey("securities.id"), nullable=False)
    number_of_shares = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    round_id = Column(UUID, ForeignKey("rounds.id"))

    @property
    def additional_things_to_dict(self):
        return {"security_name": self.security.name}

    user = relationship("User", back_populates="sell_orders")
    matches = relationship("Match", back_populates="sell_order")
    security = relationship("Security", back_populates="sell_orders", lazy="joined")
    round = relationship("Round", back_populates="sell_orders")


class BuyOrder(Base):
    __tablename__ = "buy_orders"

    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    security_id = Column(UUID, ForeignKey("securities.id"), nullable=False)
    number_of_shares = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    round_id = Column(UUID, ForeignKey("rounds.id"))

    @property
    def additional_things_to_dict(self):
        return {"security_name": self.security.name}

    user = relationship("User", back_populates="buy_orders")
    matches = relationship("Match", back_populates="buy_order")
    security = relationship("Security", back_populates="buy_orders", lazy="joined")
    round = relationship("Round", back_populates="buy_orders")


class Match(Base):
    __tablename__ = "matches"

    buy_order_id = Column(UUID, ForeignKey("buy_orders.id"), nullable=False)
    sell_order_id = Column(UUID, ForeignKey("sell_orders.id"), nullable=False)
    number_of_shares = Column(Float)
    price = Column(Float)

    buy_order = relationship("BuyOrder", back_populates="matches")
    sell_order = relationship("SellOrder", back_populates="matches")


class Round(Base):
    __tablename__ = "rounds"

    end_time = Column(DateTime(timezone=True), nullable=False)
    is_concluded = Column(Boolean, nullable=False)

    buy_orders = relationship("BuyOrder", back_populates="round")
    sell_orders = relationship("SellOrder", back_populates="round")


class BannedPair(Base):
    __tablename__ = "banned_pairs"

    buyer_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    seller_id = Column(UUID, ForeignKey("users.id"), nullable=False)

    buyer = relationship(
        "User", back_populates="bans_as_buyer", foreign_keys=[buyer_id]
    )
    seller = relationship(
        "User", back_populates="bans_as_seller", foreign_keys=[seller_id]
    )

    __table_args__ = (UniqueConstraint("buyer_id", "seller_id"),)


class ChatRoom(Base):
    __tablename__ = "chat_room"

    seller_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    buyer_id = Column(UUID, ForeignKey("users.id"), nullable=False)

    seller = relationship("User", foreign_keys=[seller_id], back_populates="seller")
    buyer = relationship("User", foreign_keys=[buyer_id], back_populates="buyer")
    room = relationship("Chat", back_populates="room")

    __table_args__ = (UniqueConstraint("seller_id", "buyer_id"),)


class Chat(Base):
    __tablename__ = "chat"

    chat_room_id = Column(UUID, ForeignKey("chat_room.id"), nullable=False)
    message = Column(Text)
    author_id = Column(UUID, ForeignKey("users.id"), nullable=False)

    room = relationship("ChatRoom", back_populates="room")
    author = relationship("User", foreign_keys=[author_id], back_populates="author")


engine = create_engine(APP_CONFIG["DATABASE_URL"])


Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
