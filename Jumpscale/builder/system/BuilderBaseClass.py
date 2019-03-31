from Jumpscale import j

BaseClass = j.application.JSBaseClass



class builder_method(object):

    def __init__(self, **kwargs_):
        if "log" in kwargs_:
            self.log = j.data.types.bool.clean(kwargs_["log"])
        else:
            self.log = True
        if "done_check" in kwargs_:
            self.done_check = j.data.types.bool.clean(kwargs_["done_check"])
        else:
            self.done_check = True

    def __call__(self, func):

        def wrapper_action(*args, **kwargs):
            builder=args[0]
            if "reset" in kwargs:
                builder.reset()
                kwargs.pop("reset")
            args=args[1:]
            name= func.__name__
            if self.log:
                builder._log_debug("do once:%s"%name)
            if name is not "_init":
                builder._init()
            if name == "install":
                builder.build()
            if name == "sandbox":
                builder.install()
                #only use "main" client, because should be generic usable
                zhub_client = kwargs.get("zhub_client", None)
                if not zhub_client:
                    if not j.clients.zhub.exists(name="main"):
                        raise RuntimeError("cannot find main zhub client")
                    zhub_client = j.clients.zhub.get(name="main")
                    zhub_client.ping() #should do a test it works
                kwargs["zhub_client"] = zhub_client

            if "reset" in kwargs:
                reset = kwargs["reset"]
            else:
                reset = False

            if name in ["start", "stop", "running"]:
                self.done_check = False

            if not self.done_check or not builder._done_check(name, reset):
                if self.log:
                    builder._log_debug("action:%s() start"%name)
                res = func(builder,*args,**kwargs)

                if name == "sandbox":
                    res = builder._flist_create(zhub_client=zhub_client)

                if self.done_check:
                    builder._done_set(name)

                if self.log:
                    builder._log_debug("action:%s() done -> %s"%(name,res))

                return res
            else:
                builder._log_debug("action:%s() no need to do, was already done"%name)

        return wrapper_action


class BuilderBaseClass(BaseClass):
    """
    doc in /sandbox/code/github/threefoldtech/jumpscaleX/docs/Internals/Builders.md
    """
    def __init__(self):
        BaseClass.__init__(self)
        if hasattr(self.__class__,"NAME"):
            assert isinstance(self.__class__.NAME,str)
            self.DIR_BUILD = "/tmp/builders/{}".format(self.__class__.NAME)
            self.DIR_SANDBOX = "/tmp/package/{}".format(self.__class__.NAME)

    @property
    def bash(self):
        return j.builder.system.bash


    def _replace(self, txt,args={}):
        """

        :param txt:
        :return:
        """
        for key,item in self.__dict__.items():
            if key.upper() == key:
                args[key] = item
        return j.core.tools.text_replace(content=txt, args=args, text_strip=True)

    def _execute(self, cmd, die=True, args={}, timeout=600,
                 profile=True, replace=True, showout=True, interactive=False):
        """

        :param cmd:
        :param die:
        :param showout:
        :param profile:
        :param replace:
        :param interactive:
        :return: (rc, out, err)
        """
        self._log_debug(cmd)
        if replace:
            cmd = self._replace(cmd,args=args)
        if cmd.strip() == "":
            raise RuntimeError("cmd cannot be empty")
        if profile:
            cmd="%s\n%s"%(self.bash.profile,cmd)

        return j.sal.process.execute(cmd, cwd=None, timeout=timeout, die=die,
                                             args=args, interactive=interactive, replace=False, showout=showout)

    def _copy(self, src, dst, deletefirst=False,ignoredir=None,ignorefiles=None,deleteafter=False):
        """
        
        :param src: 
        :param dst: 
        :param deletefirst: 
        :param ignoredir: the following are always in, no need to specify ['.egg-info', '.dist-info', '__pycache__']
        :param ignorefiles: the following are always in, no need to specify: ["*.egg-info","*.pyc","*.bak"]
        :param deleteafter, means that files which exist at destination but not at source will be deleted
        :return: 
        """
        src = self._replace(src)
        dst = self._replace(dst)
        if j.builder.tools.file_is_dir:
            j.builder.tools.copyTree(src, dst, keepsymlinks=False, deletefirst=deletefirst, overwriteFiles=True,
                                 ignoredir=ignoredir, ignorefiles=ignorefiles, recursive=True, rsyncdelete=deleteafter,
                                 createdir=True)
        else:
            j.builder.tools.file_copy(src, dst, recursive=False, overwrite=True)

    def _write(self, path, txt):
        """
        will use the replace function on text and on path
        :param path:
        :param txt:
        :return:
        """
        path = self._replace(path)
        txt = self._replace(txt)
        j.shell()


    @property
    def system(self):
        return j.builder.system

    @property
    def tools(self):
        """
        Builder tools is a set of tools to perform the common tasks in your builder (e.g read a file
        , write to a file, execute bash commands and many other handy methods that you will probably need in your builder)
        :return:
        """
        return j.builder.tools

    def reset(self):
        """
        reset the state of your builder, important to let the state checking restart
        :return:
        """
        self._done_reset()

    @builder_method()
    def build(self):
        """
        :return:
        """
        return

    @builder_method()
    def install(self):
        """
        will build as first step
        :return:
        """
        return

    @builder_method()
    def sandbox(self, zhub_client=None):
        '''
        when zhub_client None will look for j.clients.get("test"), if not exist will die
        '''
        return

    @property
    def startup_cmds(self):
        raise RuntimeError("not implemented")

    @builder_method()
    def start(self):
        for startupcmd in self.startup_cmds:
            startupcmd.start()

    @builder_method()
    def stop(self):
        for startupcmd in self.startup_cmds:
            startupcmd.stop()

    @builder_method()
    def running(self):
        for startupcmd in self.startup_cmds:
            if startupcmd.running() == False:
                return False
        return True

    @builder_method()
    def _flist_create(self, zhub_client=None):
        """
        build a flist for the builder and upload the created flist to the hub

        This method builds and optionally upload the flist to the hub

        :param hub_instance: zerohub client to use to upload the flist, defaults to None if None
        the flist will be created but not uploaded to the hub
        :param hub_instance: j.clients.zhub instance, optional
        :return: the flist url
        """

        # self.copy_dirs(self.root_dirs, self.DIR_PACKAGE)
        # self.write_files(self.root_files, self.DIR_PACKAGE)

        # if self.startup:
        #     #TODO differently, use info from self.startup_cmds
        #     file_dest = j.sal.fs.joinPaths(self.DIR_PACKAGE, '.startup.toml')
        #     j.builder.tools.file_ensure(file_dest)
        #     j.builder.tools.file_write(file_dest, self.startup)

        j.shell()

        j.tools.sandboxer.copyTo(src, dst)


        if j.core.platformtype.myplatform.isLinux:
            ld_dest = j.sal.fs.joinPaths(self.DIR_PACKAGE, 'lib64/')
            j.builder.tools.dir_ensure(ld_dest)
            j.sal.fs.copyFile('/lib64/ld-linux-x86-64.so.2', ld_dest)

        # if zhub_client:
        #for now only upload to HUB
        self._log_info("uploading flist to the hub")
        return zhub_client.sandbox_upload(self.NAME, self.DIR_PACKAGE)
        # else:
        #     tarfile = '/tmp/{}.tar.gz'.format(self.NAME)
        #     j.sal.process.execute('tar czf {} -C {} .'.format(tarfile, self.DIR_PACKAGE))
        #     return tarfile



    def clean(self):
        """
        removes all files as result from building
        :return:
        """
        raise RuntimeError("not implemented")

    def uninstall(self):
        """
        optional, removes installed, build & sandboxed files
        :return:
        """
        raise RuntimeError("not implemented")

    def test(self):
        """
        -  a basic test to see if the build was successfull
        - will automatically call start() at start
        - is optional
        """
        raise RuntimeError("not implemented")

    def test_api(self,ipaddr="localhost"):
        """
        - will test the api on specified ipaddr e.g. rest calls, tcp calls, port checks, ...
        """
        raise RuntimeError("not implemented")

    def test_zos(self,zhub_client,zos_client):
        """

        - a basic test to see if the build was successfull
        - will automatically call sandbox(zhub_client=zhub_client) at start
        - will start the container on specified zos_client with just build flist
        - will call .test_api() with ip addr of the container

        """
        raise RuntimeError("not implemented")
