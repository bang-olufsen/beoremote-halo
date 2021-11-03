import click

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


# @cli.command()
# @click.option('--count', default=1)
# @click.pass_context
# def dist(ctx, count):
#     ctx.forward(test)
#     ctx.invoke(test, count=42)

if __name__ == "__main__":
    cli()
