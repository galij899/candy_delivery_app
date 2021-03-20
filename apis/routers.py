from rest_framework import routers

class CourierRouter(routers.SimpleRouter):
    routes = [
        routers.Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={'get': 'retrieve',
                     'patch': 'partial_update'}, # todo: validate only correct fields
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
        routers.Route(
            url=r'^{prefix}$',
            mapping={'post': 'create'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
    ]

