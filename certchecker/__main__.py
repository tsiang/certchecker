import boto
import click

class CertChecker():
    def __init__(self, profile):
        self.profile = profile
        self.cert_list = None
        self.cert_elb_dict = self.get_cert_elb_dict()
        self.cert_exp_dict = self.get_cert_exp_dict()
        self.result = self.create_result(self.cert_elb_dict, self.cert_exp_dict)

    def get_cert_elb_dict(self):
        cert_elb_dict = dict()
        cert_list = list()
        c = boto.connect_elb(profile_name=self.profile)
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
        self.cert_list = cert_list
        return cert_elb_dict

    def get_cert_exp_dict(self):
        cert_exp_dict = dict()
        conn = boto.connect_iam(profile_name=self.profile)
        for cert_name in self.cert_list:
            metadata = conn.get_server_certificate(cert_name)['get_server_certificate_response']['get_server_certificate_result']['server_certificate']['server_certificate_metadata']
            expiration_date = metadata.expiration.encode('utf-8')
            cert_exp_dict[cert_name] = expiration_date
        return cert_exp_dict

    def create_result(self, cert_elb_dict, cert_exp_dict):
        cert_result = []
        for cert, elbs in cert_elb_dict.iteritems():
            cert_result.append({'cert_name':cert, 'elbs': elbs, 'expiration': cert_exp_dict[cert]})
        return cert_result

@click.command()
@click.option(
    '--profile',
    default='default',
    help="Section name in your boto config file"
)
def main(profile):
    cc = CertChecker(profile)
    print(cc.result)

if __name__ == "__main__":
    print(main())
