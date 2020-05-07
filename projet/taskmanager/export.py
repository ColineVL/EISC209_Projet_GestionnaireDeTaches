def create_file(file_type, fileneame, queryset, resource):
    file = open(fileneame, "wb")
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

