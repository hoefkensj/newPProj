import click


@click.group()
def cli():
    """NewThon CLI entrypoint."""
    pass


@cli.command()
def hello():
    """Say hello from NewThon CLI."""
    click.echo("Hello from NewThon CLI!")


if __name__ == "__main__":
    cli()
