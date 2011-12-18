Treemap Debug Toolbar
=====================

This is a django-debug-toolbar panel that displays cProfile data as a
treemap. The area of each node corresponds to the time spent in that function,
and the colour shows how many calls were made (relative to other functions).

Left-clicking on a node with children will go down to that level in the hierarchy,
so you are able to visually browse through the call stack. Right-clicking will
go back up a level.

This is a proof of concept - suggestions and feedback to make it more useful
would be appreciated.

Getting started
---------------

 * Check out the project
 * Create a local_settings.py file containing::
    
    INTERNAL_IPS = ('1.2.3.4', )

 * ./manage.py runserver
 * Visit /demo/

What works
----------

Processing cProfile data to get a hierarchy of calls.
Rendering a treemap using Google's Treemap Visualization.

TODO
----

More flexible treemap using the `D3 library <http://mbostock.github.com/d3/ex/treemap.html>`_.
Display values for total calls, cumulative time in function.
More friendly/useful data browsing experience.
`Sunburst chart <http://mbostock.github.com/d3/ex/sunburst.html>`_
Flat display of data (i.e. without the call stack) for an overview of where
most time was spent (e.g. in views, performing SQL queries etc.)
