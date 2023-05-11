from models import(Base, session, Product, engine)


if __name__ == '__main__':
    Base.metadata.create_all(engine)