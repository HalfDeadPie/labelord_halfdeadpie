Installation
===========================
The Labelord module is easy to setup::

    python -m pip install --extra-index-url https://test.pypi.org/pypi labelord-halfdeadpie

Configuration
===========================
The main purpose of the Labelord is the replication of GitHub labels. Because of the security and correct working
there is need to be done some configuration settings. The application needs the user's :ref:`github_token` to communicate
via Github API. The user have to set also the template, according which the set of labels will be modified.
To make the web part working properly, there is need to create the :ref:`webhook_secret` secret for the the all
target repositories. Target repository means the repository, which is influenced by the changes done in other repositories.
There are few ways how to set theese settings. One of them is the usage of :ref:`config`

.. _github_token:

GitHub Token
###########################
The GitHub API personal token is the user's secret string that is used for identification and authentication during the
communication using the API of GitHub. One way how to generate the token is this:

- on GitHub homepage, click on your profile and choose the **Settings**
- click on the **Developer settings** in the left navigation panel
- click on the **Personal access tokens**
- click on the **Generate new token**
- choose your settings (nothing is needed) and click on **Generate token**

.. _webhook_secret:

Webhook Secret
###########################
The Webhook secret is the user's secret string that is used for identification and authentication during the communication
using the **webhooks**. A webhook in web development is a method of augmenting or altering the behavior of a web page,
or web application, with custom callbacks. It's necessary to set up webhook for every repository that you want to mark as the
target of label replication.

- click on the **Settings** on the repository page
- choose the **Webhooks** in the left navigation panel
- click on the **Add webhook**
- set the **Payload URL** (the adress on which your application will be running)
- select *aplication/json* **Content type**
- choose your personal **Secret** (use one for all repositories)
- select **Let me select individual events.** and mark the *Label* option
- click on the **Add webhook**

.. _config:

Configuration file
###########################
Configuration file is the file, where the user is able to store the configuration settings. It's not recommended to share
this file with anybody. You can store in this file:

- GitHub token
- Webhook secret
- Repository, which is used as a template
- Set of label names and colors which are used as a template
- Target repositories

The default name of the configuration file is set *config.cfg* but the user is able to change it including the *PATH* to the file.
To change the file may be done using the option **-c/--config**.

The example of the configuration file *config.cfg*::

    [github]
    webhook_secret = ThisIsNoRealSecret
    token = ThisIsNotTheRealToken

    [labels]
    label1 = FFAA00
    label2 = CCAAFF
    label3 = 00FF00

    [others]
    template-repo = HalfDeadPie/MusicAppForEma

    [repos]
    HalfDeadPie/Software-router = yes
    HalfDeadPie/Software-bridge = yes
    HalfDeadPie/MusicAppForEma = no
    HalfDeadPie/LoRa-FIIT = yes