import click

from beoremote import backend_demo, beoremotehalo, discover

cli = click.Group()


@cli.command(help="Scan network for active Beoremote Halo.")
def scan():
    discover.discover()
    pass


@cli.command(help="Interactive Home Automation Demo")
@click.option("--hostname", required=True)
def demo(hostname):
    backend_demo.backend(hostname)
    pass


@cli.command(help="Connect to Halo and listen for events")
@click.option("--hostname", required=True)
def listen(hostname):
    remote = beoremotehalo.BeoRemoteHalo(hostname)
    remote.connect()
    pass


if __name__ == "__main__":
    cli()
