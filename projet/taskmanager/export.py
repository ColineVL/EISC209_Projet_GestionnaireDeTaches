import os
import io
import csv

def create_file(file_type, filename, queryset, fields, zipObj):
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
    file = open(filename, "w")

    if file_type == 'csv':
        file.write(queryset_to_csv(queryset, fields))

    file.close()
    zipObj.write(filename)
    os.remove(filename)

def queryset_to_csv(queryset, fields):
    result = io.StringIO()
    writer = csv.writer(result)
    writer.writerow([field for field in fields])
    for row in queryset:
        line = []
        for field in fields:
            if field == 'members':
                line.append([member.username for member in row.__getattribute__(field).all()])
            else:
                line.append(row.__getattribute__(field))
        writer.writerow(line)
    return result.getvalue()