from fabric.api import env, roles

from fusionbox.fabric.django.new import stage, deploy


def dev():
    env.project_name = 'airmozilla.dev'
    env.vassal_name = 'airmozilla_dev'

    return ['fusionbox@airmozilla.dev.fusionbox.com']


# def live():
#     env.project_name = 'airmozilla.com'
#     env.vassal_name = 'airmozilla_com'

#     return ['fusionbox@demo.airmozilla.com']


env.roledefs['dev'] = dev
#env.roledefs['live'] = live

stage = roles('dev')(stage)
#deploy = roles('live')(deploy)
