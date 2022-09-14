from apis import lambert
from rest_framework.views import APIView
from rest_framework.response import Response
import requests


class Query(APIView):
    def get(self, request):
        """
        Simple API View making external calls to governmental API
        Returns Response object
        """
        response = {}
        variable = self.request.GET.get('q')
        r = requests.get(f'https://api-adresse.data.gouv.fr/search/?q={variable}')
        r_status = r.status_code
        data = r.json()

        if r_status == 200:
            # Checks if datas received by external API is empty (wrong request)
            if not data['features']:
                return Response("Error ")
            # Get Lambert coordinates
            x, y = lambert.retrieve_lambert_from_json(data)
            # Creates KD Tree to find the nearest points easily
            tree = lambert.create_coordinates_tree()
            indexes_list = lambert.find_nearest_points(x, y, tree)
            # Get the CSV rows of the nearest points
            nearest_points_list = lambert.create_list_rows(indexes_list)
            # Format the row in a dictionary
            format_dict = lambert.format_coverage_dict(nearest_points_list)
            # Returns the dictionary as a HTTP Response
            return Response(format_dict)
        else:
            response['status'] = r.status_code
            response['message'] = 'error'
            return Response("Error")

