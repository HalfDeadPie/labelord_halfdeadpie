README
====================================



The Labelord application is for the replication of GitHub labels. This application uses mainly requests,
 flask and click. You are able to use list_repos, list_labels, run and run_server commands.

Cassettes
---------------------

If you want to record new cassettes:

    - Write the real GitHub token to 'config.cfg' in tests_unit\fixtures\configs.
    - Set your parameters and outputs in tests_unit/conftest_unit.py
        •for example: REPOS, LABELS, RUN_DRY, TARGET_REPOS
    - Before recording cassettes you have to delete cassettes of mine

Documentation
---------------------

To generate documentation::

    docs\make html

To generate autodocs::

    python -m sphinx.apidoc -o docs\auto labelord

To run the documentation tests::

    docs\make doctest