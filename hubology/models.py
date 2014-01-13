import boto
import os


sdb = boto.connect_sdb(os.environ.get('AWS_KEY'), os.environ.get('AWS_SECRET'))

class HubUser(object):
    #["twitter", "facebook", "linkedin"]
#    socnet = None
#    userid = None
#    hubid = None
#    username = None
#    name = None
#    location = None #Lat/Lng from browser/device
#    location_name = None
#    town = None  #Name of town where they live/want to support
#    email = None
#    link = None
#    url = None
#    gender = None
#    profile_image_url = None
#    #list of mentor, educator, developer, designer
#    classification = None
#    original_insert_date = None
#    last_modified_date = None

    def __init__(self, simpledb_item):
        """
            Initialize a HubUser
        """
        self.db_item = simpledb_item

    def is_authenticated(self):
        """ Is this user authenticated?
            We'll just say True for now.
            If we've got a HubUser object, they had to 
            come from Twitter, Facebook, or LinkedIn
        """
        return True
        
    def is_active(self):
        """ Is this an active user?
            For now, all users are considered 'Active'
        """
        return True       
        
    def is_anonymous(self):
        """ Is this an anonymous user?
            No HubUsers are anonymous so it's always False
        """ 
        return False
        
    def is_member_type(self, member_type):
        """ Is this user of the specified member type?
        """
        classification = self.get('classification')
        if classification is not None:
            return member_type in classification
        else:
            return False
        
    
    def is_developer(self):
        """ Is this user a software developer?
        """
        return self.is_member_type(u'developer')

    def is_educator(self):
        """ Is this user an educator?
        """
        return self.is_member_type(u'educator')
    
    def is_designer(self):
        """ Is this user a designer?
        """
        return self.is_member_type(u'designer')
    
    def is_mentor(self):
        """ Is this user a mentor?
        """
        return self.is_member_type(u'mentor')
        
    def get_id(self):
        return self.get('hubid')

    def get(self, key, default=None):
        return self.db_item.get(key, default)

    def __getitem__(self, key):
        return self.db_item[key]

    def __getattribute__(self, attr):
        return self.db_item.attr

    def put(self):
        """
            Update information for this user.
        """
        self.db_item.save()


    def set_location(self, location_dict):
        """ Sets the user's location (lat, lng) based on the supplied dictionary
        """
        if location_dict is not None:
            geo_point = [str(location_dict.get('lat', 0.0)), str(location_dict.get('lng', 0.0))]
            self['location'] = geo_point

    @staticmethod
    def find(hubid):
        if hubid in ('', None):
            return None
        domain = sdb.get_domain('hubology_users')
        query = domain.select('select * from hubology_users where hubid = "%s"' % hubid)
        user = None
        for item in query:
            user = HubUser(item)
        return user
    
    @staticmethod
    def all():
        domain = sdb.get_domain('hubology_users')
        query = domain.select('select * from hubology_users')
        users = []
        for item in query:
           users.append(item)
        return users

    @staticmethod
    def all_with_location():
        domain = sdb.get_domain('hubology_users')
        query = domain.select('select * from hubology_users')
        users = []
        for item in query:
            users.append(HubUser(item))
        return users

    @staticmethod
    def delete(user_item_name):
        domain = sdb.get_domain('hubology_users')
        item = domain.get_item(user_item_name)
        item.delete()
