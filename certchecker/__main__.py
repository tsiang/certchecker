import click

from certchecker import CertChecker

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
