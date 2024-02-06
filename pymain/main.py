
def execute_elisa_config_script():
    from elisa_client_api_script import elisa_config
    import runpy
    runpy.run_module(elisa_config, run_name="__main__")


def execute_elisa_get_script():
    from elisa_client_api.bin import elisa_get
    import runpy
    runpy.run_module(elisa_get, run_name="__main__")

def execute_elisa_insert_script():
    import elisa_client_api_script
    # from elisa_client_api_script import elisa_insert
    import runpy
    runpy.run_module(elisa_client_api_script.elisa_insert, run_name="__main__")

def execute_elisa_reply_script():
    from elisa_client_api_script import elisa_reply
    import sys
    print(sys.path)
    import runpy
    runpy.run_module(elisa_reply, run_name="__main__")

def execute_elisa_update_script():
    from elisa_client_api_script import elisa_update
    import sys
    print(sys.path)
    import runpy
    runpy.run_module(elisa_update, run_name="__main__")


