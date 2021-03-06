from Jumpscale import j

builder_method = j.builder.system.builder_method

class BuilderBitcoin(j.builder.system._BaseClass):
    NAME = "bitcoind"

    def _init(self):
        self.DIR_BUILD = self._replace("{DIR_VAR}/build/bitcoin")
        j.sal.fs.createDir(self.DIR_BUILD)

    @builder_method()
    def build(self): 

        j.builder.buildenv.install()
        self.profile_builder_select()

        # dependancies
        if self.tools.isUbuntu:
            j.builder.system.package.ensure('g++')
            self.system.package.mdupdate()
            self.system.package.install([
                "build-essential", "libtool", "autotools-dev", "pkg-config",
                "libboost-all-dev", "libqt5gui5", "libqt5core5a", "libqt5dbus5",
                "qttools5-dev", "qttools5-dev-tools", "libprotobuf-dev", "protobuf-compiler",
                "libqrencode-dev", "autoconf", "openssl", "libssl-dev", "libevent-dev", 
                "libminiupnpc-dev", "bsdmainutils"
            ])

        '''
        ' splitting build into 3 steps:
        ' - clone bitcoin source code -v 0.18
        ' - build & link berkly db libs with source code to activate wallet
        ' - executing installation scripts
        '''
        clone_bitcoin_script = """
                    cd {DIR_BUILD}
                    git clone https://github.com/bitcoin/bitcoin.git --branch 0.18
                    """
        self._execute(clone_bitcoin_script)

        # berkely db v4.8
        berkly_config = """
            cd {DIR_BUILD}
            wget 'http://download.oracle.com/berkeley-db/db-4.8.30.NC.tar.gz'
            tar -xzvf db-4.8.30.NC.tar.gz
            cd {DIR_BUILD}/db-4.8.30.NC/build_unix/
            ../dist/configure --enable-cxx --disable-shared --with-pic --prefix={DIR_BUILD}/bitcoin
            make install
            """
        self._execute(berkly_config)

        # tag v0.18
        script = """
        cd {DIR_BUILD}/bitcoin
        ./autogen.sh
        ./configure LDFLAGS="-L{DIR_BUILD}/bitcoin/lib/" CPPFLAGS="-I{DIR_BUILD}/bitcoin/include/"
        make
        make install
        """
        self._execute(script)

    @builder_method()
    def install(self):
        # bitcoin bins
        self._copy('{DIR_BUILD}/bitcoin/src/bitcoind', '{DIR_BIN}') 
        self._copy('{DIR_BUILD}/bitcoin/src/bitcoin-cli', '{DIR_BIN}') 
        self._copy('{DIR_BUILD}/bitcoin/src/bitcoin-wallet', '{DIR_BIN}')
        self._copy('{DIR_BUILD}/bitcoin/src/bitcoin-tx', '{DIR_BIN}') 

    @builder_method()
    def sandbox(self, zhub_client=None):
        self.profile_sandbox_select()
        self._copy('{DIR_BIN}/bitcoind', '{DIR_SANDBOX}') 
        self._copy('{DIR_BIN}/bitcoin-cli', '{DIR_SANDBOX}') 
        self._copy('{DIR_BIN}/bitcoin-wallet', '{DIR_SANDBOX}')
        self._copy('{DIR_BIN}/bitcoin-tx', '{DIR_SANDBOX}') 
    
    @property
    def startup_cmds(self):
        # bitcoin daemon
        cmd = j.tools.startupcmd.get(self.NAME, cmd='bitcoind')
        return [cmd]

    @builder_method()
    def stop(self):
        # killing the daemon
        j.sal.process.killProcessByName(self.NAME)

    @builder_method()
    def clean(self):
        self._remove(self.DIR_BUILD)
        self._remove(self.DIR_SANDBOX)

    '''
    testing running daemon
    add tests to bitcoin
    ''' 
    @builder_method()
    def test(self):
        
        if self.running():
            self.stop()

        self.start()
        assert self.running()

                    
        self._log_info("TEST SUCCESS: Bitcoin daemon is running")  