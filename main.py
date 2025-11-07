from sqlalchemy import create_engine, select, update, delete, Column, Table
from sqlalchemy import Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, Session, relationship
from datetime import datetime
import random

engine = create_engine('sqlite:///test.db')
Base = declarative_base()

# # KOD TWORZACY BAZE DANYCH BEZ RELACJI (cwiczenia II i III)
# # ==========================================================
# class Experiment(Base):
#     __tablename__ = 'experiments'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     title: Mapped[str] = mapped_column(String, nullable=False)
#     created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
#     exp_type: Mapped[int] = mapped_column("type", Integer, nullable=False)
#     finished: Mapped[bool] = mapped_column(Boolean, default=False)
#
#     def __repr__(self):
#         return f'id: {self.id} | title: {self.title} | created_at: {self.created_at} | type: {self.exp_type} | finished: {self.finished} | Data: {self.created_at}'
#
#
# class DataPoint(Base):
#     __tablename__ = 'datapoints'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     real_value: Mapped[float] = mapped_column(Float, nullable=False)
#     target_value: Mapped[float] = mapped_column(Float, nullable=False)
#
#     def __repr__(self):
#         return f'id: {self.id} | real_value: {self.real_value:.3f} | target_value: {self.target_value:.3f}'
#
#
# Base.metadata.create_all(engine)
#
# # ---- CREATE ----
# with Session(engine) as session:
#     listOfExperiments = [
#         Experiment(
#             title=f'Eksperyment nr {i + 1}',
#             created_at=datetime.now(),
#             exp_type=random.randint(1, 5),
#             finished=random.choice([True, False])
#         )
#         for i in range(2)
#     ]
#     session.add_all(listOfExperiments)
#
#     listOfDataPoints = [
#         DataPoint(
#             real_value=random.random(),
#             target_value=random.random()
#         )
#         for i in range(10)
#     ]
#     session.add_all(listOfDataPoints)
#
#     session.commit()
#
# # ---- READ ----
# with Session(engine) as session:
#     experimentsFromDatabase = session.scalars(select(Experiment)).all()
#     print('EXPERIMENTS:')
#     for exp in experimentsFromDatabase:
#         print(exp)
#
#     dataPointsFromDatabase = session.scalars(select(DataPoint)).all()
#     print('DATA POINTS:')
#     for dp in dataPointsFromDatabase:
#         print(dp)
#
# # ---- UPDATE ----
# with Session(engine) as session:
#     stmt = update(Experiment).values(finished=True)
#     session.execute(stmt)
#     session.commit()
#
# # ---- DELETE ----
# with Session(engine) as session:
#     stmt = delete(Experiment)
#     session.execute(stmt)
#     stmt = delete(DataPoint)
#     session.execute(stmt)
#     session.commit()
#
# Base.metadata.create_all(engine)

# KOD TWORZACY BAZE DANYCH Z RELACJAMI (cwiczenia IV i V)
# ========================================================

enrollments = Table(
    "enrollments",
    Base.metadata,
    Column("experiment_id", ForeignKey("experiments.id"), primary_key=True),
    Column("subject_id", ForeignKey("subjects.id"), primary_key=True)
)


class Experiment(Base):
    __tablename__ = 'experiments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    exp_type: Mapped[int] = mapped_column("type", Integer, nullable=False)
    finished: Mapped[bool] = mapped_column(Boolean, default=False)
    datapoints = relationship("DataPoint", back_populates="experiment")

    subjects = relationship(
        "Subject",
        secondary=enrollments,
        back_populates="experiments"
    )


class DataPoint(Base):
    __tablename__ = 'datapoints'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    real_value: Mapped[float] = mapped_column(Float, nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiments.id"), nullable=False)
    experiment = relationship("Experiment", back_populates="datapoints")


class Subject(Base):
    __tablename__ = 'subjects'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gdpr_accepted: Mapped[bool] = mapped_column(Boolean, default=False)

    experiments = relationship(
        "Experiment",
        secondary=enrollments,
        back_populates="subjects"
    )
