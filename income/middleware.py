from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class TokenValidator:

    def __init__(self, get_response):
        self.get_response = get_response
        self.num_request = 0
        self.num_exception = 0
        self.context_response = {
            "msg": {"warning": "There is a template to print"},
        }

    def __call__(self, request):

        # if request.META.get('HTTP_AUTHORIZATION', False):
        # try:
        #     auth = JWTAuthentication()
        #     user, payload = auth.authenticate(request)
        #     request.user = user
        #     request.auth = auth
        # except AuthenticationFailed as e:
        #     print(e)
        #     # todo
        #     #  change to logger
        request.user
        response = self.get_response(request)

        return response
    # middleware hooks

    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     print(f'view name: {view_func.__name__}')

    def process_exception(self, request, exception):
        self.num_exception += 1
        print(f"Exception count: {exception}, {self.num_exception}")

    # def process_template_response(self, request, response):
    #     response.context_data['new_data'] = self.context_response