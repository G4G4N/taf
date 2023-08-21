import click
from taf.api.repository import (
    add_dependency,
    remove_dependency
)


def attach_to_group(group):

    @group.group()
    def dependencies():
        pass

    @dependencies.command(context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    ))
    @click.argument("auth_path")
    @click.argument("dependency_name")
    @click.option("--branch-name", default=None, help="Name of the branch which contains the out-of-band commit")
    @click.option("--out-of-band-commit", default=None, help="Out-of-band commit SHA")
    @click.option("--dependency-path", default=None, help="Dependency's filesystem path")
    @click.option("--keystore", default=None, help="Location of the keystore files")
    @click.pass_context
    def add(ctx, auth_path, dependency_name, branch_name, out_of_band_commit, dependency_path, keystore):
        """Add a dependency (an authentication repository) to dependencies.json or update it if it was already added to this file.
        Update and sign targets metadata, snapshot and timestamp using yubikeys or keys loaded from the specified keystore location.
        Information that is added to dependencies.json includes out-of-band authentication commit and name
        of the branch which contains that commit. This out-of-band authentication commit represents a commit including and following
        which state of the authentication repository is expected to be valid at every commit. If the dependency does not exist
        on the disk, this command will still update dependencies.json, but will not be able to validate branch and out-of-band
        commit values, so it is strongly recommended to run the updater first and clone/update and validate the dependency.

        All additional information that should be saved as the dependency's custom content in `dependencies.json`
        is specified by providing additional options. Here is an example:

        `taf dependencies add auth-path namespace1/auth --branch-name main --out-of-band-commit d4d768da4e8f74f54c644923b7ed0e19a0faf3c5 --custom-property some-value --keystore keystore-path`

        In this case, custom-property: some-value will be added to the custom part of the dependency dependencies.json.

        If branch-name and out-of-band-commit are omitted, the default branch and its first commit will be written to dependencies.json.

        Dependency does not have to exist on the filesystem, but if it does, provided branch name and out-of-band commit sha
        will be validated, so it is recommended to run the updater first and update/clone and validate the dependency first.
        If the dependency's full path is not provided, it is expected to be located in the same
        library root directory as the authentication repository, in a directory whose name corresponds to its name.
        If dependency's parent authentication repository's path is `E:\\examples\\root\\namespace\\auth`, and the dependency's namespace prefixed name is
        `namespace1\\auth`, the target's path will be set to `E:\\examples\\root\\namespace1\\auth`.


        """
        custom = {ctx.args[i][2:]: ctx.args[i + 1] for i in range(0, len(ctx.args), 2)} if len(ctx.args) else {}
        add_dependency(
            auth_path=auth_path,
            dependency_name=dependency_name,
            branch_name=branch_name,
            out_of_band_commit=out_of_band_commit,
            dependency_path=dependency_path,
            keystore=keystore,
            custom=custom
        )

    @dependencies.command()
    @click.argument("auth_path")
    @click.argument("dependency-name")
    @click.option("--keystore", default=None, help="Location of the keystore files")
    def remove(auth_path, dependency_name, keystore):
        """Remove a dependency from dependencies.json.
        Update and sign targets metadata, snapshot and timestamp using yubikeys or keys loaded from the specified keystore location.

        `taf dependencies remove auth-path namespace1/auth --keystore keystore-path`

        """
        remove_dependency(auth_path, dependency_name, keystore)