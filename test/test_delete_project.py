from model.project import Project
import random

def test_delete_random_project(app):

    old_projects_list = app.project.get_project_list()
    print("OLD ", old_projects_list)
    random_project = random.choice(old_projects_list)
    app.project.delete_project(random_project)
    new_projects_list = app.project.get_project_list()
    print("NEW ", new_projects_list)
    assert len(new_projects_list) == len(old_projects_list)-1
    old_projects_list.remove(random_project)
    assert sorted(old_projects_list, key=Project.id_or_max) == sorted(new_projects_list, key=Project.id_or_max)