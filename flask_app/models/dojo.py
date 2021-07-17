from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models.ninja import Ninja

class Dojo():

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ninjas = []

    @classmethod
    def create_dojo(cls, data):
        query = "INSERT INTO dojos (name, location) VALUES (%(dojo_name)s, %(dojo_location)s);"

        new_dojo_id = connectToMySQL('dojos_and_ninjas_schema').query_db(query, data)

        return new_dojo_id

    @classmethod
    def get_all_dojos(cls):

        query = "SELECT * FROM dojos;"

        results = connectToMySQL('dojos_and_ninjas_schema').query_db(query)

        dojos = []

        for item in results:
            # new_dojo = Dojo(item)
            dojos.append(cls(item))

        return dojos

    @classmethod
    def delete_dojo(cls, data):

        query = "DELETE FROM dojos WHERE id = %(id)s;"

        connectToMySQL('dojos_and_ninjas_schema').query_db(query, data)

    @classmethod
    def get_dojo_by_id(cls, data):

        query = "SELECT * FROM dojos JOIN ninjas ON dojos.id = ninjas.dojo_id WHERE dojos.id = %(id)s;"

        results = connectToMySQL('dojos_and_ninjas_schema').query_db(query, data)

        dojo = Dojo(results[0])

        for item in results:
            ninja_data = {
                'id': item['ninjas.id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'age': item['age'],
                'created_at': item['created_at'],
                'updated_at': item['updated_at'],
                'dojo_id': item['dojo_id'],
            }
            ninja = Ninja(ninja_data)
            ninja.dojo = dojo
            dojo.ninjas.append(ninja)

        return dojo

    @classmethod
    def update_dojo(cls, data):

        query = "UPDATE dojos SET name = %(name)s, location = %(location)s WHERE id = %(id)s;"

        connectToMySQL('dojos_and_ninjas_schema').query_db(query, data)

