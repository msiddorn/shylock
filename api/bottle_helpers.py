'''
Helper functions for the bottle server stuff
Mainly for setting up the routes
'''
import bottle

def router(method, route):
    '''Decorator to tag class methods for routing'''
    def outer(fn):
        setattr(
            fn,
            'route_{}'.format(method),
            route
        )
        return fn
    return outer


def init_routes(app):
    '''Initialise the bottle routes for an object'''
    for attr_name in dir(app):
        attr = getattr(app, attr_name)
        for method_name in ['GET', 'POST']:
            route = getattr(attr, 'route_{}'.format(method_name), None)
            if route is not None:
                print(method_name, route, attr)
                app._app.route(
                    route,
                    method=method_name,
                    callback=attr,
                )
