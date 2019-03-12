from Jumpscale import j


def main(self):
    """
    to run:

    kosmos 'j.data.types.test(name="jsxobj")' --debug
    """

    schema = """
        @url = despiegk.test
        llist = []
        llist2 = "" (LS) #L means = list, S=String
        llist3 = [1,2,3] (LF)
        nr = 4
        date_start = 0 (D)
        description = ""        
        llist4 = [1,2,3] (L)
        llist5 = [1,2,3] (LI)
        llist6 = "1,2,3" (LI)
        U = 0.0
        """

    schema_object = j.data.schema.get(schema_text=schema)

    tt = j.data.types.get("o","despiegk.test")

    o = tt.clean({})

    assert o.nr == 4
    assert tt.check(o)

    o2 = tt.clean({"nr":5})
    assert o2.nr == 5

    self._log_info("TEST DONE JSXOBJ")

    return ("OK")
