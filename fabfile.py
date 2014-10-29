"""
On local machine:
$ source env/bin/activate
$ fab deploy
"""

import time

from fabric.api import *

env.hosts = ['121.40.126.220']
env.user = 'ecs-user'
env.password = 'Bclt2014'
env.code_dir = '/home/ecs-user/zhiwehu'
env.project_div = '/home/ecs-user/zhiwehu/zhiwehu'
env.virtualenv = '/home/ecs-user/env'


def pull():
    "Pull new code"
    with cd(env.code_dir):
        run('git checkout gunicorn_start.bash')
        run('git pull origin master')
        run('chmod +x gunicorn_start.bash')


def update_requirements():
    "Update requirements in the virtualenv."
    with cd(env.code_dir):
        with prefix("source %s/bin/activate" % (env.virtualenv)):
            run("pip install -r requirements.txt")


def syncdb():
    with cd(env.project_div):
        with prefix("source %s/bin/activate" % (env.virtualenv)):
            run('python manage.py syncdb --settings=config.settings.production')


def migrate(app=None):
    with cd(env.project_div):
        with prefix("source %s/bin/activate" % (env.virtualenv)):
            if app:
                run('python manage.py migrate --settings=config.settings.production --noinput %s' % app)
            else:
                run('python manage.py migrate --settings=config.settings.production --noinput')


def collectstatic():
    with cd(env.project_div):
        with prefix("source %s/bin/activate" % (env.virtualenv)):
            run('python manage.py collectstatic --settings=config.settings.production --noinput')


def restart():
    "Restart (or just start) the server"
    with cd(env.project_div):
        with prefix("source %s/bin/activate" % (env.virtualenv)):
            run('supervisorctl restart gunicorn')

    run('sudo service nginx restart')

    # so it has time to reload
    time.sleep(3)


def deploy():
    pull()
    update_requirements()
    syncdb()
    migrate()
    collectstatic()
    restart()
