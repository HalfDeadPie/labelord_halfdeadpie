labelord package
================

labelord\.cli module
--------------------

.. automodule:: labelord.cli
    :members:
    :undoc-members:
    :show-inheritance:

``labelord.cli.cli(ctx, token, config)``

    Represents group of commands

    **Parameters**:

                    - **ctx** - context for passing the objects
                    - **token** - GitHub token
                    - **config** - Name of the configuration file

    **Subcommands**:

                    - **list_repos**
                    - **list_labels**
                    - **run**

``labelord.cli.list_repos(ctx)``

    List all the accessible repositories to the command line

    **Parameters**:

                    - **ctx** - context for passing the objects

``labelord.cli.list_labels(ctx, repository)``

    List all the labels from the selected repository

    **Parameters**:

                    - **ctx** - context for passing the objects
                    - **repository** - name of the accessible repository


``labelord.cli.run(ctx,mode, template_repo, verbose, dry_run, quiet, all_repos)``

    Actualises all the target repositories with the content of template. Template may be the another repository or the set of labels
    from the configuration file

    **Parameters**:

                    - **ctx** - context for passing the objects
                    - **mode** - replace or update mode
                    - **template_repo** - repository set as template
                    - **verbose** - option for printing more information about operations
                    - **dry_run** - option for turning off the real changing
                    - **quiet** - option for turning off printing the outputs
                    - **all_repos** - the set of accessible repositories


labelord\.cli\_support module
-----------------------------

.. automodule:: labelord.cli_support
    :members:
    :undoc-members:
    :show-inheritance:

labelord\.unity module
----------------------

.. automodule:: labelord.unity
    :members:
    :undoc-members:
    :show-inheritance:

labelord\.web module
--------------------

.. automodule:: labelord.web
    :members:
    :undoc-members:
    :show-inheritance:

labelord\.web\_support module
-----------------------------

.. automodule:: labelord.web_support
    :members:
    :undoc-members:
    :show-inheritance:
