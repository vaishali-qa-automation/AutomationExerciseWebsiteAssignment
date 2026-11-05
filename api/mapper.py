import logging
from dataclasses import asdict

#  This maps the dataclass attributes with what actually need to be pass in signup user
#  This is just for mapping and nothing else

logger = logging.getLogger(__name__)

def user_dataclass_to_payload(user_obj) -> dict:

    #  asdict converts the entire datclass into nested dictionary structure
    raw_dict = asdict(user_obj)

    # Extracting nested dictionary to flatten
    dob = raw_dict.pop("date_of_birth")
    address = raw_dict.pop("address")

    flat_payload = {
        # Core user details
        "name": raw_dict.get("name"),
        "email": raw_dict.get("email"),
        "password": raw_dict.get("password"),
        "title": raw_dict.get("title"),
        # Flattened Date parameters
        "birth_date": dob.get("day"),
        "birth_month": dob.get("month"),
        "birth_year": dob.get("year"),
        # Flattened Address parameters
        "firstname": address.get("first_name"),
        "lastname": address.get("last_name"),
        "company": address.get("company"),
        "address1": address.get("address"),
        "address2": address.get("address_2"),
        "country": address.get("country"),
        "zipcode": address.get("zipcode"),
        "state": address.get("state"),
        "city": address.get("city"),
        "mobile_number": address.get("mobile_number"),
    }
    logger.debug(f"Creating payload: {flat_payload}")
    return flat_payload
