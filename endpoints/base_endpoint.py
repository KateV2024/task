from conftest import backend_url


class Endpoint:
    response = None
    response_json = None
    schema = {}


    def check_response_is_201(self):
        assert self.response.status_code == 201,\
            f'Expected 201, got {self.response.status_code}'

    def check_response_is_200(self):
        return self.response.status_code == 200,\
            f'Expected 200, got {self.response.status_code}'

    def check_response_is_400(self):
        assert self.response.status_code == 400,\
            f'Expected 400, got {self.response.status_code}'

    def check_response_is_404(self):
        assert self.response.status_code == 404,\
            f'Expected 404, got {self.response.status_code}'
