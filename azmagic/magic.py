import shlex
import os

import pandas as pd

from typing import Any, Union

from azure.cli.core import get_default_cli
from IPython.core.magic import line_magic, Magics, magics_class


@magics_class
class AzMagic(Magics):

    @line_magic
    def az(self, line: str) -> Union[Any, pd.DataFrame, None]:
        """Implementation of `%az` line magic

        Parameters
        ----------
        line : str
            Arguments to the line magic

        Returns
        -------
        Union[Any, pd.DataFrame, None]
            If the result from the `azcli` command is a List[Dict], then
            this function will attempt to convert them into a `pd.DataFrame`.

            If the `azcli` command raises a SystemExit exception with an error
            code of 0 (a "successful error"), such as when passing the `--help`
            flag, then this function returns `None`.

            Otherwise, this function returns whatever object is the result
            of the `azcli` command.

        Raises
        ------
        SystemExit
            Indicates the `azcli` command was not successful.
        """

        args = shlex.split(line)
        az_cli = get_default_cli()
        out_file = open(os.devnull, "w")

        try:
            exit_code = az_cli.invoke(args, out_file=out_file)

            if exit_code == 0:
                result = az_cli.result.result

                if isinstance(result, list):
                    # If we get back a list of dicts,
                    # then return a pandas DataFrame
                    return pd.json_normalize(result)

                elif isinstance(result, dict):
                    # If we get back an OData response,
                    # attempt to return the `value` array
                    # as a pandas DataFrame.
                    if "@odata.context" in result and "value" in result:
                        return pd.json_normalize(result["value"])
                    else:
                        return result
                else:
                    return result

        except SystemExit as exc:

            # Using the --help flag will raise
            # a SystemExit, but with a successful
            # error code. We don't want to show
            # this exception to the user in the
            # notebook.

            if az_cli.result.error.code == 0:

                return
            else:
                raise exc



def load_ipython_extension(ipython):
    """
    Any module file that defines a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.

    To manually register this magics class, you can run the following
    from a Jupyter notebook or other IPython session:

    ```python
    from IPython import get_ipython

    ip = get_ipython()
    load_ipython_extension(ip)
    ```

    Parameters
    ----------
    ipython : ipykernel.zmqshell.ZMQInteractiveShell
        The current IPython shell/session.
    """
    ipython.register_magics(AzMagic)
