from model.project import Project


def test_add_project(app):
    base_name = "Project"
    unique_name = app.project.generate_project_name(base_name)
    new_project = Project(name=unique_name)
    old_projects_list = app.project.get_project_list()
    print("OLD", old_projects_list)
    app.project.create_new_project(new_project)
    old_projects_list.append(new_project)
    new_projects_list = app.soap.get_projects_list()
    print("NEW", new_projects_list)
    assert old_projects_list == new_projects_list







