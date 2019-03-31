from Jumpscale import j
import textwrap

builder_method = j.builder.system.builder_method


class BuilderDigitalME(j.builder.system._BaseClass):
    """
    specs:

        - build all required components (only work on ub 1804) using self.build
        - sandbox to sandbox dir
        - create flist
        - in self.test_zos() start the created flist & do the network tests for the openresty

    """
    NAME = "digitalme"

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
        j.builder.runtimes.python.build(reset=reset)
        j.builder.runtimes.lua.build()  # will build openresty & lua & openssl
        j.clients.git.pullGitRepo(url="https://github.com/threefoldtech/digitalmeX.git", branch="development")

    @builder_method()
    def sandbox(self, reset=False, zhub_client=None, flist_create=False):
        j.builder.runtimes.python.sandbox()
        j.builder.runtimes.lua.sandbox()
        j.tools.sandboxer.copyTo("/sandbox/var/build/sandbox/tfbot/", "{}/sandbox".format(self.DIR_PACKAGE))
        j.tools.sandboxer.copyTo(j.builder.runtimes.lua.DIR_PACKAGE,  self.DIR_PACKAGE)
        git_repo_path = "/sandbox/code/github/threefoldtech/digitalmeX"
        j.tools.sandboxer.copyTo(git_repo_path, j.sal.joinPaths(self.DIR_PACKAGE, git_repo_path[1:]))


    def test(self, zos_client=None):
        """

        :return:
        """

        self.build()
        flist = self.sandbox()  #will not upload to zhub_instance


        #create container and use this flist
        #see that openresty is working

    def test_zos(self, zos_client, zhubclient):
        flist = self.sandbox(zhub_client=zhubclient)
        container_id = zos_client.container.create(flist, name="test_digitalme").get()
        container_client = zos_client.cotainer.client(container_id)
        assert container_client.ping()


