import boto
import pp

cert_list = list()

def get_cert_elb_dict():
    global cert_list
    cert_elb_dict = dict()
    c = boto.connect_elb()
    elbs = c.get_all_load_balancers()
    for lb in elbs:
        listeners = lb.listeners
        lb = lb.name.encode('utf-8')
        for listener in listeners:
            if listener.ssl_certificate_id:
                cert_name = listener.ssl_certificate_id.split('/')[-1].encode('utf-8')
                cert_list.append(cert_name)
                cert_list = set(cert_list)
                cert_list = list(cert_list)
                if cert_name in cert_elb_dict:
                    cert_elb_dict[cert_name].append(lb)
                else:
                    cert_elb_dict[cert_name] = [lb]
    return cert_elb_dict

def get_cert_exp_dict(cert_list):
    cert_exp_dict = dict()
    conn = boto.connect_iam()
    for cert_name in cert_list:
        metadata = conn.get_server_certificate(cert_name)['get_server_certificate_response']['get_server_certificate_result']['server_certificate']['server_certificate_metadata']
        expiration_date = metadata.expiration.encode('utf-8')
        cert_exp_dict[cert_name] = expiration_date
    return cert_exp_dict

def create_json(cert_elb_dict, cert_exp_dict):
    cert_result = []
    for cert, elbs in cert_elb_dict.iteritems():
        cert_result.append({'cert_name':cert, 'elbs': elbs, 'expiration': cert_exp_dict[cert]})
    return cert_result

cert_elb_dict = get_cert_elb_dict()
cert_exp_dict = get_cert_exp_dict(cert_list)
pp(create_json(cert_elb_dict, cert_exp_dict))
