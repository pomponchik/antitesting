@hookimpl
def pytest_collection_modifyitems(session: Session, config: Config, items: List[Item]) -> None:
    filtered = [x for x in items if x not in collector]

    print(len(filtered))
    pass
