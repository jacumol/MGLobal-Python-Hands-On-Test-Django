from typing import List, Dict
import requests


DATA_API_EMPLOYEES_URL = "http://masglobaltestapi.azurewebsites.net/api/Employees/"


class EmployeeDataGetter(object):
    """This class is a helper to get the data from the source
    separating the communication logic from the other processes.
    """

    @classmethod
    def get_api_data(cls) -> List[Dict]:
        try:
            response = requests.get(DATA_API_EMPLOYEES_URL)
        except requests.exceptions.Timeout as e:
            # Maybe set up for a retry, or continue in a retry loop
            return {"message": "Timeout error"}
        except requests.exceptions.TooManyRedirects as e:
            # Tell the user their URL was bad and try a different one
            return {"message": "Too many redirects error"}
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            return {"message": "Request exception error"}
        except:
            return {"message": "Unknown error"}

        return response.json()
