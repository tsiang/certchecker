import boto
import datetime

class CertChecker():
    def __init__(self, profile):
        self.profile = profile
        self.cert_list = list()
        self.cert_elb_dict = self.get_cert_elb_dict()
        self.cert_exp_dict = self.get_cert_exp_dict()
        self.result = self.create_result()

    def get_cert_elb_dict(self):
        cert_elb_dict = dict()
        c = boto.connect_elb(profile_name=self.profile)
        elbs = c.get_all_load_balancers()
        for lb in elbs:
            listeners = lb.listeners
            lb = lb.name.encode('utf-8')
            for listener in listeners:
                if listener.ssl_certificate_id:
                    cert_name = listener.ssl_certificate_id.split('/')[-1].encode('utf-8')
                    self.cert_list.append(cert_name)
                    self.cert_list = set(self.cert_list)
                    self.cert_list = list(self.cert_list)
                    if cert_name in cert_elb_dict:
                        cert_elb_dict[cert_name].append(lb)
                    else:
                        cert_elb_dict[cert_name] = [lb]
        return cert_elb_dict

    def get_cert_exp_dict(self):
        cert_exp_dict = dict()
        conn = boto.connect_iam(profile_name=self.profile)
        for cert_name in self.cert_list:
            metadata = conn.get_server_certificate(cert_name)['get_server_certificate_response']['get_server_certificate_result']['server_certificate']['server_certificate_metadata']
            expiration_date = metadata.expiration.encode('utf-8')
            date_string = datetime.datetime.strptime(expiration_date, "%Y-%m-%dT%H:%M:%SZ")
            formatted_expiration_date = date_string.strftime('%B %d, %Y %H:%M')
            cert_exp_dict[cert_name] = formatted_expiration_date
        return cert_exp_dict

    def create_result(self):
        cert_result = []
        for cert, elbs in self.cert_elb_dict.iteritems():
            cert_result.append({'cert_name':cert, 'elbs': elbs, 'expiration': self.cert_exp_dict[cert]})
        return cert_result

