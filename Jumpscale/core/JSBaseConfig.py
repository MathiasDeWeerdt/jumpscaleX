from Jumpscale import j
from .JSBase import JSBase

class JSBaseConfig(JSBase):


    def __init__(self,dataobj=None,factory=None):
        JSBase.__init__(self,init=False)
        if factory is None:
            raise RuntimeError("factory cannot be None")

        self.factory = factory
        self.data = dataobj

        if self.data is None:
            self._logger.debug("new obj")
            self.data = self.factory._model.new()
            #does not exist yet
            self._data_trigger_new()
            self._isnew = True
        else:
            self._isnew = False

        self._init()

    def _empty_js_obj(self):
        self.__dict__["factory"] = None
        self.__dict__["data"] = None

    @property
    def _id(self):
        return self.data.id
        # if self._id_ is None:
        #     self._id_ = self.factory._model.bcdb.name+"_%s"%self.data.id
        # return self._id_

    def save(self):
        self.data.save()

    def delete(self):
        self.data.model.delete(self.data)
        self.factory._children.pop(self.name)

    def data_update(self,**kwargs):
        self.data.data_update(data=kwargs)
        self.data.save()


    def _data_trigger_new(self):
        pass

    def edit(self):
        path = j.core.tools.text_replace("{DIR_TEMP}/js_baseconfig_%s.toml"%self.__location__)
        data_in = self.data._toml
        j.sal.fs.writeFile(path,data_in)
        j.core.tools.file_edit(path)
        data_out = j.sal.fs.readFile(path)
        if data_in != data_out:
            self._logger.debug("'%s' instance '%s' has been editted (changed)"%(self.factory.__jslocation__,self.data.name))
            data2 = j.data.serializers.toml.loads(data_out)
            self.data.data_update(data2)
            self.data.save()
        j.sal.fs.remove(path)

    def view(self):
        path = j.core.tools.text_replace("{DIR_TEMP}/js_baseconfig_%s.toml"%self.__location__)
        data_in = self.data._toml
        j.tools.formatters.print_toml(data_in)


    def __getattr__(self, attr):
        # if self.factory._model is None:
        #     return self.__getattribute__(attr)
        if attr in self.factory._model.schema.propertynames:
            return self.data.__getattribute__(attr)
        return self.__getattribute__(attr)
        # raise RuntimeError("could not find attribute:%s"%attr)

    def __dir__(self):
        r = self.factory._model.schema.propertynames
        for item in self.__dict__.keys():
            if item not in r:
                r.append(item)
        return r

    def __setattr__(self, key, value):
        if "data" in self.__dict__ and key in self.factory._model.schema.propertynames:
            # if value != self.data.__getattribute__(key):
            self._logger.debug("SET:%s:%s"%(key,value))
            self.__dict__["data"].__setattr__(key,value)

        self.__dict__[key]=value


    def __str__(self):
        try:
            out = "%s\n%s\n"%(self.__class__.__name__,self.data)
        except:
            out = str(self.__class__)+"\n"
            out+=j.core.text.prefix(" - ", self.data)
        return out

    __repr__ = __str__
