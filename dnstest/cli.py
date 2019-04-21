import pydig

import click

from .validator import load_validated_yaml, InvalidConfig
from .check import Check


@click.command()
@click.argument('config')
@click.option('-n', '--nameserver', 'nameservers', multiple=True)
def run(config, nameservers):
    """
    Simple program that greets NAME for a total of COUNT times.
    """

    click.secho('Using config: {}'.format(config))

    # Load our config from disk
    try:
        config = load_validated_yaml(config)
    except InvalidConfig as e:
        click.secho(str(e), fg='red', err=True)
        return

    # Use the cli nameservers or whatever was defined in the config
    nameservers = nameservers or config.get('nameservers')

    if nameservers:
        click.secho('Using nameservers: {}'.format(', '.join(nameservers)))

    # Setup out custom resolver with our nameservers
    resolver = pydig.Resolver(nameservers=nameservers)

    # Default exit code is a success
    exit_code = 0

    # Loop over the loaded checks
    for check in config['checks']:

        # Convert to our check object
        check = Check(**check)

        # Log that we are running this check
        click.secho(str(check), nl=False)

        # Run all the tests for check
        results = list(check(resolver))

        # Number of successful tests
        success = results.count(None)

        # Get any errors out of the results
        errors = list(filter(None, results))

        # Print a dot for each successful test
        click.secho(' ' + '.' * success, fg='green', nl=False)

        # Print a F for each failed test
        click.secho(' ' + 'F' * len(errors), fg='red')

        # Loop over each error message
        for error in errors:
            exit_code = 1
            click.secho(str(error), fg='red', err=True)

    exit(exit_code)


def main():
    """
    Wrap the default run command with the auto env prefixer
    """
    run(auto_envvar_prefix='DNSTEST')
