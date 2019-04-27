from Jumpscale import j
builder_method = j.builder.system.builder_method


class BuilderBootstrapBot(j.builder.system._BaseClass):
    """
    specs:

        - build all required components (only work on ub 1804) using self.build
        - sandbox to sandbox dir
        - create flist
        - in self.test_zos() start the created flist & do the network tests for the openresty

    """
    NAME = "bootstrapbot"

    @builder_method()
    def _init(self):
        pass

    @builder_method()
    def build(self, reset=False):
        """
        kosmos 'j.tools.sandboxer.sandbox_build()'

        will build python & openresty & copy all to the right git sandboxes works for Ubuntu only
        :return:
        """
        j.builder.apps.digitalme.build(reset=reset)
        j.builder.db.zdb.build(reset=reset)

    @builder_method()
    def install(self):
        """
        Installs the zdb binary to the correct location
        """
        j.builder.db.zdb.install()

    @builder_method()
    def sandbox(self, reset=False, zhub_client=None, flist_create=True, merge_base_flist="tf-autobuilder/threefoldtech-jumpscaleX-development.flist"):
        j.builder.apps.digitalme.sandbox(reset=True)
        j.tools.sandboxer.copyTo(j.builder.apps.digitalme.DIR_SANDBOX, self.DIR_SANDBOX)

        j.builder.db.zdb.sandbox(reset=True)
        j.tools.sandboxer.copyTo(j.builder.db.zdb.DIR_SANDBOX,  self.DIR_SANDBOX)

        file = self.tools.joinpaths(j.sal.fs.getDirName(__file__), 'templates', 'bot_nacl_configure.toml')
        file_dest = self.tools.joinpaths(self.DIR_SANDBOX, 'bot_configure.toml')
        self._copy(file, file_dest)


        startup_file = self.tools.joinpaths(j.sal.fs.getDirName(__file__), 'templates', 'bot_startup.toml')
        file_dest = self.tools.joinpaths(self.DIR_SANDBOX, '.startup.toml')
        self._copy(startup_file, file_dest)

        startup_file = self.tools.joinpaths(j.sal.fs.getDirName(__file__), 'templates', 'bootstrapbot_startup.sh')
        file_dest = self.tools.joinpaths(self.DIR_SANDBOX, 'bot_startup.sh')
        self._copy(startup_file, file_dest)

