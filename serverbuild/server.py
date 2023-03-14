from pyngrok import conf, ngrok


def get_https():
    ngrok.set_auth_token('')
    http_tunnel = ngrok.connect(50, bind_tls=True)
    return http_tunnel.data['public_url']
