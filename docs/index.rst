.. Labelord documentation master file, created by
   sphinx-quickstart on Tue Nov 28 11:42:59 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Labelord's documentation
====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. toctree::
   :maxdepth: 2

   tutorial/install
   tutorial/usage
   auto/modules
   tutorial/examples

Intro
==================
Labelord is a simple application that provides automatic label replication which are used together with Issues on the Github.
The application is runable via command line after installing the Labelord module. The application includes showing the list of
user's repositories. The user is also able to see the list of all labels for the chosen respository. To achieve the unity of labels
used in repositories, the user can use special command to replicate all the labels from selected template to all the chosen repositories.
However this is not the only way. The user is able to run the server, which receives information about the label changes and
forward the to the other repositories. This server also provides the view of target repositories in the web browser.
