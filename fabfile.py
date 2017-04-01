from fabric.api import run, env, cd, prefix, settings
from fabric.operations import local

env.hosts = ['83.220.170.91']
env.user = 'light'
env.activate = 'source ~/.virtualenvs/astro/bin/activate'
env.use_ssh_config = True

app_dir = "~/projects/aiohttp-astro"


def deploy():
    with cd(app_dir):
        with prefix(env.activate):
            run("git pull")
            with settings(warn_only=True):
                run('pip install -r requirements.txt')
                with cd('app/front'):
                    run('npm install')
                    run('npm run build')
                run('kill -HUP `cat /tmp/astro.pid`')

