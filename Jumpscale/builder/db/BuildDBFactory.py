from Jumpscale import j

from .BuilderEtcd import BuilderEtcd
from .BuilderMariadb import BuilderMariadb
from .BuilderZdb import BuilderZdb
from .BuilderCockroachDB import BuilderCockroachDB
from .BuilderTIDB import BuilderTIDB
from .BuilderPostgresql import BuilderPostgresql


class BuildDBFactory(j.builder.system._BaseFactoryClass):

    __jslocation__ = "j.builder.db"

    def _init(self):

        self.etcd = BuilderEtcd()
        self.mariadb = BuilderMariadb()
        self.zdb = BuilderZdb()
        self.cockroachdb = BuilderCockroachDB()
        self.tidb = BuilderTIDB()
        self.postgres = BuilderPostgresql()
