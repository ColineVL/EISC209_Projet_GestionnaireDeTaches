import os


def create_file(file_type, filename, queryset, resource, zipObj):
    """
    This function create a file to the specified format wich contained a table, write it in the zip object. We only want
    to modify the zip object so we destroy the created file at the end
    :param file_type: the type of the file to generate ('csv','xls','json','html' or 'yaml')
    :param filename: the name of the file to generate
    :param queryset: the table contained in the file
    :param resource: the resource assiated withe the queryset
    :param zipObj: the zip object in wich we want to write
    :return: nothing
    """
    file = open(filename, "wb")
    dataset = resource.export(queryset)
    if file_type == 'csv':
        file.write(dataset.csv.encode())
    elif file_type == 'xls':
        file.write(dataset.xls)
    elif file_type == 'json':
        file.write(dataset.json.encode())
    elif file_type == 'html':
        file.write(dataset.html.encode())
    elif file_type == 'yaml':
        file.write(dataset.yaml.encode())
    file.close()
    zipObj.write(filename)
    os.remove(filename)

