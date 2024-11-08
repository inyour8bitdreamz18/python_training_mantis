from suds.client import Client
from suds import WebFault
from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client(self.app.base_url + "api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True

        except WebFault as e:
            print(e)
            return False

    project_cache = None

    def get_projects_list(self):
        client = Client(self.app.base_url + "api/soap/mantisconnect.php?wsdl")
        self.project_cache = []
        try:
            projects = client.service.mc_projects_get_user_accessible(self.app.config["webadmin"]["username"],
                                                                  self.app.config["webadmin"]["password"])
            for project in projects:
                id = project["id"]
                name = project["name"]
                self.project_cache.append(Project(id=id, name=name))

            return self.project_cache

        except WebFault as e:
            print(e)
            return []


    '''
    def get_project_id_from_name(self):
        client = Client(self.app.base_url + "api/soap/mantisconnect.wsdl")
        try:
            rqst = client.service.mc_project_get_id_from_name(self.app.config["webadmin"]["username"],
                                                                  self.app.config["webadmin"]["password"], "Project#8")
            print("REQUEST", rqst)
            return rqst

        except WebFault as e:
            print(e)
            return None
    '''
