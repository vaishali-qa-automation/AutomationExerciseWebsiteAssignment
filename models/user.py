from dataclasses import dataclass, field


@dataclass
class DateOfBirth:
    day: str = "2"
    month: str = "April"
    year: str = "1990"


@dataclass
class Address:
    first_name: str = "TestUser"
    last_name: str = "LastName"
    company: str = "Test Company"
    address: str = "T10 567"
    address_2: str = ""
    country: str = "India"
    state: str = "Uttar Pradesh"
    city: str = "Greater Noida"
    zipcode: str = "201306"
    mobile_number: str = "9876767343"


@dataclass
class User:
    name: str
    email: str
    password: str
    date_of_birth: DateOfBirth = field(default_factory=DateOfBirth)
    address: Address = field(default_factory=Address)
    title: str = "Mr"
    subscribe_newsletter: bool = False
    receive_special_offers: bool = False
