import fix_path

from celery.concurrency.base import BasePool, monotonic, \
        WorkerShutdown, WorkerTerminate, WorkerLostError, ExceptionInfo

#import geventreactor; geventreactor.install()
#import gevent

from twisted.internet import defer
from threading import Thread
from geoffrey.tasks import *

import os

class txPool(BasePool):

    def __init__(self, *args, **kwargs):
        super(txPool, self).__init__(*args, **kwargs)
        self.reactor_thread = Thread(target=reactor.run, args=(False,))

    def _get_info(self):
        return {'max-concurrency': 1,
                'processes': [os.getpid()],
                'max-tasks-per-child': None,
                'put-guarded-by-semaphore': True,
                'timeouts': ()}

    def on_start(self):
        self.reactor_thread.start()

    def on_stop(self):
        reactor.callFromThread(reactor.stop)

    def on_apply(self, target, args=(), kwargs={}, callback=None,
                 accept_callback=None, pid=None, getpid=os.getpid,
                 propagate=(), monotonic=monotonic, **_):
        def _apply():
            if accept_callback:
                accept_callback(pid or getpid(), monotonic())
            try:
                ret = target(*args, **kwargs)
            except propagate:
                raise
            except Exception:
                raise
            except (WorkerShutdown, WorkerTerminate):
                raise
            except BaseException as exc:
                try:
                    reraise(WorkerLostError, WorkerLostError(repr(exc)),
                            sys.exc_info()[2])
                except WorkerLostError:
                    callback(ExceptionInfo())
            else:
                if isinstance(ret, defer.Deferred):
                    ret.addCallback(callback)
                else:
                    callback(ret)

        return reactor.callFromThread(_apply)


def main():
    worker(app=app).run(loglevel='info', pool_cls=txPool)


if __name__ == '__main__':
    main()

