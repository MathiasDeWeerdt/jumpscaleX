from Jumpscale import j


def main(self):
    """
    to run:

    js_shell 'j.data.schema.test(name="storedprocedure")'
    """

    lua_test_file_path = "%s/tests/test.lua"%self._dirpath

    r = self.get()

    dd = r.storedprocedure_register("test1",3,lua_test_file_path)

    # #here script given to redis every time, not to use in production
    res = r.eval(j.sal.fs.readFile(lua_test_file_path),3,"a","b","c")
    assert res == b'OK abc'

    res = r.evalsha(dd["sha"],3,"a","b","c")
    assert res == b'OK abc'

    res = r.storedprocedure_execute("test1","a","b","c")
    assert res == b'OK abc'

    r.storedprocedure_debug("test1","a","b","c")

    j.shell()
