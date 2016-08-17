# This script builds a bootstrapper for the worker role
import io
import json
import os
import shutil

def reset_sln(sln_location, to_remove):
    with io.open(sln_location) as context:
        sln_data = context.readlines()
    clean = []
    for line in sln_data:
        for guid in to_remove:
            if guid in line:
                break
        else:
            clean.append(line)

    clean_sln = "".join(clean).replace("EndProject\nEndProject\n", "EndProject\n")
    with io.open(sln_location, 'w') as context:
        context.write(clean_sln)

def copy_compiled_code(directory):
    print(directory)
    for project in os.listdir(directory):
        project_path = os.path.join(directory, project)
        print(project)
        print(os.listdir(project_path))

def main(worker, solution, current_path, zip_package_name):
    # print(json.dumps(worker, indent=2))
    solution['parent']['name'] = solution['parent']['folder'].split("\\")[-1]
    projects = [worker] + [project for project in solution['projects'] if not project.get('role_type')]
    to_remove = [project['guid'] for project in solution['projects'] if project not in projects] + [solution['parent']['guid']]
    project_dest = os.path.join(current_path, '__save', worker['guid'], "projects")

    for project in projects[::-1]:
        shutil.copytree(project['folder'], os.path.join(project_dest, project['name']))

    packaged_worker_sln = os.path.join(project_dest, solution['parent']['name'])
    shutil.copy(solution['sln'], packaged_worker_sln)
    reset_sln(packaged_worker_sln, to_remove)
    os.system("C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\MSBuild.exe \"%s\"" % packaged_worker_sln)
    copy_compiled_code(project_dest)


    return solution
