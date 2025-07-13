def update_session_data(state, key):
    new_session = dict(state["session"])  # copy to avoid in-place mutation
    value = state.get(key, {})  # get value from state if exists
    new_session["data"][key] = value

    print("Updated session data:", new_session["data"])

    # return a new session dict or class depending on expected shape
    return new_session
