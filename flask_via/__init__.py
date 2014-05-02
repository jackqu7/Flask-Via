# -*- coding: utf-8 -*-

"""
flask_via
---------
"""

from importlib import import_module


class Via(object):
    """ The core class which kicks off the whole registration processes.

    Example
    -------
    .. sourcecode:: python

        from flask import Flask
        from flask.ext.via import Via
        from flask.ext.via.routers.flask import Basic

        app = Flask(__name__)

        def foo(bar=None):
            return 'Foo View!'

        routes = [
            Basic('/foo', foo),
            Basic('/foo/<bar>', foo, endpoint='foo2'),
        ]

        via = Via()
        via.init_app(app, routes_module='path.to.here')

        if __name__ == "__main__":
            app.run(debug=True)
    """

    def init_app(
            self,
            app,
            routes_module=None,
            routes_variable='routes',
            **kwargs):
        """ Initialises Flask extension. Bootstraps the automatic route
        registration process.

        Arguments
        ---------
        app : flask.app.Flask
            Flask application instance

        Keyword Arguments
        -----------------
        route_module : str, optional
            Python dotted path to where routes are defined, defaults
            to ``None``
        routes_variable : str, optional
            Within the routes module look for a variable of this name,
            defaults to ``routes``
        \*\*kwargs
            Arbitrary keyword arguments passed to ``add_url_rule``

        Raises
        ------
        ImportError
            If the route module cannot be imported
        AttributeError
            If routes do not exist in the moduke
        NotImplementedError
            If ``VIA_ROUTE_MODULE`` is not configured in appluication config
            and ``route_module`` keyword argument has not been provided.
        """

        if not routes_module:
            routes_module = app.config.get('VIA_ROUTES_MODULE')

        if not routes_module:
            raise NotImplementedError(
                'VIA_ROUTES_MODULE is not defined in application '
                'configuration.')

        # Import the moduke
        module = import_module(routes_module)

        # Get the routes from the module
        routes = getattr(module, routes_variable)

        # Process Routes
        for route in routes:
            route.add_to_app(app, **kwargs)
