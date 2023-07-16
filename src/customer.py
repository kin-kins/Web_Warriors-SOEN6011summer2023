class Customer:

    def __init__(self,name, password1,password2, email, firstname, lastname, street, city, state, country, zipcode):
        self.name=name
        self.password1=password1
        self.password2=password2
        self.firstname= firstname
        self.lastname=lastname
        self.email=email
        self.street=street
        self.street_no=None
        self.city=city
        self.state=state
        self.country=country
        self.zipcode=zipcode

    def validate_data(self):
        if self.name == '' or self.password1 == '' or self.password2 == '' or self.firstname == '' or self.firstname == '' or self.lastname == '' or self.email == '' or self.street == '' or self.city == '' or self.state == '' or self.country == '' or self.zipcode == '':
            error = 'Please fill out all the fields.'
            return error

        # Check that passwords match
        if self.password1 != self.password2:
            error = 'Passwords do not match.'
            return error

        # Parse street_no from street
        street_no = -1

        # Check that address is valid format
        if len(self.street.split(" ")) < 3 or not self.street.split(" ")[0].isdigit():
            error = 'Street Address format not recognized. Please re-enter.'
            return error

        self.street_no = str(self.street.split(" ")[0])
        self.street = self.street[self.street.index(" ") + 1:]
        return 0
    
    def validate_data_for_update(self):
        if self.name == '' or self.firstname == '' or self.lastname == '' or self.email == '' or self.street == '' or self.city == '' or self.state == '' or self.country == '' or self.zipcode == '':
            error = 'Please fill out all the fields.'
            return error

        # Parse street_no from street
        street_no = -1

        # Check that address is valid format
        if len(self.street.split(" ")) < 3 or not self.street.split(" ")[0].isdigit():
            error = 'Street Address format not recognized. Please re-enter.'
            return error

        self.street_no = str(self.street.split(" ")[0])
        self.street = self.street[self.street.index(" ") + 1:]
        return 0


    def create_query(self):
        insert_address_query = ("insert into address (street_no, street_name, city, state, country, zip) values ("
			+ self.street_no + ", '" + self.street + "', '" + self.city + "', '" + self.state + "', '" + self.country + "', '" + self.zipcode + "');")
        insert_username_query = ("insert into user (username, password, email, is_admin, first_name, last_name, address_id, suspended) values ('"
	        + self.name + "', '" + self.password1 + "', '" + self.email + "', false, '" + self.firstname + "', '" + self.lastname + "', (select max(address_id) from address), 0);")
        return insert_address_query, insert_username_query
	
    def update(self, address_id):
        # Update address data in the address table
        address_query = "UPDATE address SET street_no = %s, street_name = %s, city = %s, state = %s, country = %s, zip = %s WHERE address_id = %s"
        address_values = (self.street_no, self.street, self.city, self.state, self.country, self.zipcode, address_id)

        # Update user data in the user table
        user_query = "UPDATE user SET  email = %s, first_name = %s, last_name = %s WHERE username = %s"
        user_values = (self.email, self.firstname, self.lastname, self.name)
        return address_query, address_values, user_query, user_values