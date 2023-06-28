import pandas as pd
import heapq


def calculate_distance(lat1, lon1, lat2, lon2):
    """This Function is used to calculate the score based on distance"""
    distance = ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5
    return distance


def convert_to_json():
    """This function converts the TSV file to a list of dictionaries"""
    tsv_file = 'data/cities_canada-usa.tsv'  # Path to the TSV file

    # Read the TSV file using pandas
    df = pd.read_csv(tsv_file, delimiter='\t', dtype=str)

    # Convert the DataFrame to a list of dictionaries
    cities = df.to_dict(orient='records')

    return cities


class GetCity:
    @staticmethod
    def get_suggest_city(data_dict):
        """This Method is used to Get All The Suggested Cities from Query Params"""
        try:
            query = data_dict.get("city")  # Get city name
            latitude = data_dict.get("lat")  # Get Latitude
            longitude = data_dict.get("long")  # Get Longitude

            if query is None or latitude is None or longitude is None:
                response = {
                    "data": {},
                    "success": False,
                    "status_code": 400,
                    "message": 'Please Provide Proper Attributes',
                }
                return response

            cities = convert_to_json()

            suggestions = [
                {
                    "name": f"{city['name']}, {city['tz'].split('/')[1]}, {city['country']}",
                    "latitude": city['lat'],
                    "longitude": city['long'],
                    "score": calculate_distance(float(latitude), float(longitude), float(city['lat']),
                                                float(city['long']))
                }
                for city in cities if query.lower() in city['name'].lower()
            ]

            suggestions = heapq.nlargest(len(suggestions), suggestions, key=lambda x: x['score'])

            response = {
                "data": suggestions,
                "success": True,
                "status_code": 200,
                "message": 'Get All The Suggested Cities',
            }
            return response

        except Exception as e:
            return e
