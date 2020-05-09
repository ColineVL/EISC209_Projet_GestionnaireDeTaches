import os


def create_file(file_type, filename, queryset, resource, zipObj):
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

