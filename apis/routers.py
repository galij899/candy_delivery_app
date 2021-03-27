from rest_framework import routers

class CourierRouter(routers.SimpleRouter):
    routes = [
        routers.Route(
            url=r'^{prefix}/{lookup}$',
            mapping={'get': 'retrieve',
                     'patch': 'partial_update'}, # todo: validate only correct fields
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'} # todo: what is a detail
        ),
        routers.Route(
            url=r'^{prefix}$',
            mapping={'post': 'create'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
    ]

class OrdersRouter(routers.SimpleRouter):
    routes = [
        routers.DynamicRoute(
            url=r'^{prefix}/{url_path}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
        routers.Route(
            url=r'^{prefix}$',
            mapping={'post': 'create'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        )
    ]
