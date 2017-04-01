import aiohttp

bind = '127.0.0.1:8081'
pidfile = '/tmp/astro.pid'
proc_name = 'moon'
workers = 1
worker_class = 'aiohttp.GunicornWebWorker'
# accesslog = 'log/access.log'
# errorlog = 'log/error.log'

