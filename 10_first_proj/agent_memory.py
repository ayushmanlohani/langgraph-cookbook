from langgraph.checkpoint.sqlite import SqliteSaver


def get_chechkpointer():
    # so we can save global and local checkpointer
    # global - means all memory and local - means in each chat / thread

    return SqliteSaver.from_conn_string(":memory")


def fet_thread_config():
    # so here we will  define how many threads are we gonna make
    # 1 means everything get stored in one history line basically
    # we can change it to have multiple thread and even many sqlitesaver folder
    # so to imagine - one history for everything and each folder for each chat

    config = {
        "configurable": {"thread_id": 1, "checkpoint_ns": ""}
    }
    return config
