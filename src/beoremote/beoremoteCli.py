import click
from beoremotehalo import BeoRemoteHalo

from beoremote import discover

cli = click.Group()


@cli.command(help="Scan network for active Beoremote Halo.")
def scan():
    discover.discover()


@cli.command(help="Interactive Home Automation Demo")
@click.option("--hostname", required=True)
def demo(hostname):
    print(hostname)
    pass


@cli.command(help="Connect to Halo and listen for events")
@click.option("--hostname", required=True)
def listen(hostname):
    remote = BeoRemoteHalo(hostname)
    remote.connect()
    pass


if __name__ == "__main__":
    cli()
