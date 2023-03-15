from pyngrok import conf, ngrok
import os
ngrok_token = os.environ['NTOKEN']


def get_https():
    ngrok.set_auth_token(ngrok_token)
    http_tunnel = ngrok.connect(50, bind_tls=True)
    return http_tunnel.data['public_url']
