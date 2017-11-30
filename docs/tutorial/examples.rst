Examples
====================================
.. testsetup::

    from labelord import cli_support
    from labelord.cli_support import Label, is_named, print_version
    from labelord import cli
    from labelord import web
    from labelord.web import create_app, repo_link

**Here is the way how are the same labels compared**

.. testcode::

    a = Label('MyNameIs','#000000')
    b = Label('MyNameIs','#000000')
    if cli_support.cmp_labels(a, b):
        print("Labels are the same")

This would output:

.. testoutput::

   Labels are the same



**How to check if the label is named in template:**

.. testcode::

    first = Label('MyNameIs','#000000')
    second = Label('MyNameIs','#000000')
    template = []
    template.append( first )
    if cli_support.is_named(template, second):
        print("The label is named in template")

This would output:

.. testoutput::

   The label is named in template



**This is how the wep application can be created (with default configuration file):**

.. testcode::

    app = web.create_app()
    print( app.my_config )

This would output:

.. testoutput::

    config.cfg



**This is how the repository can be transofrmed to link:**

.. testcode::

    print( repo_link("ZaphodBeeblebrox/Marvin") )

This would output:

.. testoutput::

    https://github.com/ZaphodBeeblebrox/Marvin




