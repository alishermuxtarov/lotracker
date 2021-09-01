from rest_framework.throttling import SimpleRateThrottle


class AntiPerMinuteThrottle(SimpleRateThrottle):
    def get_cache_key(self, request, view):
        return '{throttle_key}_minute_{scope}_{indent}'.format(
            throttle_key=view.throttle_key, scope=self.scope, indent=self.get_ident(request)
        )

    def get_rate(self):
        return '1/min'


class AntiPerDayThrottle(SimpleRateThrottle):
    def get_cache_key(self, request, view):
        return '{throttle_key}_day_{scope}_{indent}'.format(
            throttle_key=view.throttle_key, scope=self.scope, indent=self.get_ident(request)
        )

    def get_rate(self):
        return '10/day'
