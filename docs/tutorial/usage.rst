Usage
========================
This section provides some basic information how to use Labelord application. Here you can find summary of commands,
options, arguments and simple code examples.

The way how to use labelord::

    labelord [OPTIONS] COMMAND [ARGS]


Options
#########################

+-----------------+-----------------------------------+
|   **Option**    |          **Meaning**              |
+=================+===================================+
|  --c/---config  | Path of the auth config file      |
+-----------------+-----------------------------------+
|  --t/---token   | GitHub API token                  |
+-----------------+-----------------------------------+
|   ---version    | Show the version and exit.        |
+-----------------+-----------------------------------+
|   ---help       | Show help message and exit.       |
+-----------------+-----------------------------------+

--c/---config
----------------
This is the option to set the name of the configuration file. If this option isn't called and :ref:`github_token` is not set other way,
the application tries to uses default name of configuration file *config.cfg*. It's neccessary to name the configuration file
with *.cfg* extension. This option has lower priority than option **--t/---token**.

--t/---token
----------------
This is the option to provide :ref:`github_token` to application via command line. This option has higher priority than
**--c/---config***. It means that when the **--c/---config*** and **--t/---token** are called both, the application continues
working with the token that was set as **--t/---token**.

Commands
#########################

list_repos
----------------
The *list_repos* command is simple command, which will provide the list of user's repositories. In this command, there is/are made
a GET request(s) using the session. After receiving the response, the application parse it and print all the accessible repositories
to the user with GitHub token. The **token** may be set via command line option *--t/---token*, configuration file
or can stay named defaultly *config.cfg*. In any case the token must be set for proper proper functioning.

The way how to use list_repos::

    labelord [OPTIONS] list_repos

list_labels
----------------
The *list_labels* command is simple command, which will provide the list of labels from the certain repository. The user choose the name
of the repository and the application make GET request(s), parse the response and print the labels to the command line. The **token**
must be set, the same like in *list_repos*. The argument of this subcommand **repository** represents the name of repository, which
is chosen as the target of requests. After running this subcommand, its labels are listed in command line.

The way how to use list_repos::

    labelord [OPTIONS] list_labels REPOSITORY

run
----------------
The *list_labels* command is command, which includes the main logic of replication and actualising the labels. The user is able to choose
the template (repository or set of labels) and actualise target repositories with a couple of options. The user is able to set the
mode of actualising target repositories. The **replace** mode means that in all target repositories will stay only template labels.
The **update** mode is just adding the missing labels to the existing set of labels. **Verbose** means printing additional information
about the process of actualising the repositories. **Dry run** is running the acualisation without making any changes. **Quiet** is an
option to disable any printing of outputs.

Options for *run*
#########################

+----------------------------+-----------------------------------+
|   **Option for run**       |          **Meaning**              |
+============================+===================================+
|  --r/---template-repo TEXT | The name of the template repo     |
+----------------------------+-----------------------------------+
|  --v/---verbose            | Allows printing additional info   |
+----------------------------+-----------------------------------+
|   --d/---dry-run           | Runs without changes              |
+----------------------------+-----------------------------------+
|   --q/--quiet              | Disable printing any outputs      |
+----------------------------+-----------------------------------+
|   --a/--all-repos          | Actualise all repositories        |
+----------------------------+-----------------------------------+
|   --help                   | Show help message and exit.       |
+----------------------------+-----------------------------------+

The way how to use run::

    labelord [OPTIONS] run [RUN_OPTIONS] MODE

run_server
----------------
The *run_server* runs the Flask server, so the web part of application starts running. The user is able to run the web part of the application
using the *flask run* command and setting the *FLASK_APP* environmental variable to name of application. There is a possibility to use
some options. Option **debug** allows printing of debugging outputs while the application is running. The user is able to set the
**host** (IP adress,...) and the **port**.


Options for *run_server*
#########################

+----------------------------+-----------------------------------+
|   **Option for run_server**|          **Meaning**              |
+============================+===================================+
|  --h/--host TEXT           | The IP adress of server           |
+----------------------------+-----------------------------------+
|  --p/---port               | The port of server                |
+----------------------------+-----------------------------------+
|   --d/--debug              | Allows debugging information      |
+----------------------------+-----------------------------------+
|   --help                   | Show help message and exit.       |
+----------------------------+-----------------------------------+

The way how to use run_server::

    labelord [OPTIONS] run_server [RUN_SERVER_OPTIONS]


