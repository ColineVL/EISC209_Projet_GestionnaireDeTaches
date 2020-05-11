import os
import io
import csv
import json
import xml.etree.ElementTree as ET

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
    if file_type == 'json':
        file.write(queryset_to_json(queryset, fields))
    if file_type == 'html':
        file.write(queryset_to_xml(queryset, fields))

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

def queryset_to_json(queryset, fields):
    result = dict()
    for row in queryset:
        row_dict = dict()
        for field in fields:
            if field == 'members':
                row_dict[field]=[member.username for member in row.__getattribute__(field).all()]
            else:
                row_dict[field] = row.__getattribute__(field).__str__()
        result[row.id] = row_dict
    return json.dumps(result)

def queryset_to_xml(queryset, fields):
    table = ET.Element('table')
    head = ET.SubElement(table,'tr')
    for field in fields:
        head_field = ET.SubElement(head,'th')
        head_field.text = field

    for row in queryset:
        table_row = ET.SubElement(table,'tr')
        for field in fields:
            item = ET.SubElement(table_row,'td')
            if field == 'members':
                item.text= [member.username for member in row.__getattribute__(field).all()].__str__()
            else:
                item.text = row.__getattribute__(field).__str__()

    return ET.tostring(table).decode()