from model.project import Project
import random
import re



class ProjectHelper:

    def __init__(self, app):
        # Ссылка на главный файл фикстуры Application
        self.app = app

    def open_project_form(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/manage_proj_page.php")):
            self.open_projects_table()
        wd.find_element_by_css_selector("input[value='Create New Project']").click()


    #def return_to_project_table(self):
        #wd = self.app.wd

    def create_new_project(self, project):
        wd = self.app.wd
        self.open_project_form()
        self.fill_project_form(project)
        self.project_cache = None
        self.open_project_form()


    def fill_project_form(self, project):
        wd = self.app.wd
        self.change_field_value("name", project.name)
        self.change_list_value("status", project.status)
        #self.change_checkbox_value("enabled", project.enabled)
        #self.change_checkbox_value("inherit_global", project.inherit_global)
        self.change_list_value("view_state", project.view_status)
        self.change_field_value("description", project.description)
        wd.find_element_by_css_selector('input[value="Add Project"]').click()

    '''
    def change_checkbox_value(self, field_name):
        wd = self.app.wd
        wd.find_element_by_name(field_name, ":checked").click()
    '''

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)


    def change_list_value(self, list_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(list_name).click()
            wd.find_element_by_name(list_name).send_keys(text)


    def open_projects_table(self):
        wd = self.app.wd
        # Open Manage tab
        wd.find_element_by_link_text("Manage").click()
        wd.find_element_by_link_text("Manage Projects").click()


    def open_project_by_id(self, project_id):
        wd = self.app.wd
        #if not (wd.current_url.endswith("/manage_proj_page.php")):
            #self.open_projects_table()
        wd.find_element_by_css_selector('a[href="manage_proj_edit_page.php?project_id=%s"]' % project_id).click()


    def check_if_name_is_unique(self, project_name):
        wd = self.app.wd
        projects = self.get_project_list()
        return any(project.name == project_name for project in projects)


    def generate_project_name(self, project_name):
        return ("%s#%i" % (project_name, random.randint(1, 100)))

    def delete_project(self, project):
        wd = self.app.wd
        self.open_projects_table()
        self.open_project_by_id(project.id)
        wd.find_element_by_css_selector('input[value="Delete Project"]').click()
        # Confirm deleting
        wd.find_element_by_css_selector('input[value="Delete Project"]').click()
        self.open_projects_table()
        self.project_cache = None


    def extract_id(self, href):
        id = re.search("project_id=([0-9.]+)", href).group(1)
        return id

    def count(self):
        wd = self.app.wd
        self.open_projects_table()
        return len(wd.find_elements_by_name("tr.row-1")) + len(wd.find_elements_by_name("tr.row-2"))


    project_cache = None

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_projects_table()
            self.project_cache = []
            for element in wd.find_elements_by_css_selector("tr.row-1, tr.row-2"):
                columns = element.find_elements_by_css_selector("td")
                if len(columns) >= 5:
                    href = element.find_element_by_css_selector('td>a').get_attribute('href')
                    id = self.extract_id(href)
                    name = columns[0].text
                    status = columns[1].text
                    inherit_global = columns[2].text
                    view_status = columns[3].text
                    description = columns[4].text
                    self.project_cache.append(Project(id=id, name=name,
                                                      status=status,
                                                      inherit_global=inherit_global,
                                                      view_status=view_status,
                                                      description=description))
            return list(self.project_cache)

