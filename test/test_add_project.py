from model.project import Project


def test_add_project(app):
    base_project_name = "Project"
    unique_number = app.project.generate_project_name(base_project_name)
    new_project = Project(name=unique_number)

    old_projects_list = app.project.get_project_list()
    app.project.create_new_project(new_project)
    new_projects_list = app.project.get_project_list()
    assert len(new_projects_list) == len(old_projects_list)+1
    old_projects_list.append(new_project)
    assert sorted(old_projects_list, key=Project.id_or_max) == sorted(new_projects_list, key=Project.id_or_max)






