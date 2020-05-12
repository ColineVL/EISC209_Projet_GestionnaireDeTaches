import os
import csv
import json
import xml.etree.ElementTree as ET
import xlsxwriter as xlsx
import yaml


def create_file(file_type, filename, queryset, fields, zipObj):
    """
    This function create a file to the specified format wich contained a table, write it in the zip object. We only want
    to modify the zip object so we destroy the created file at the end
    :param file_type: the type of the file to generate ('csv','xls','json','html' or 'yaml')
    :param filename: the name of the file to generate
    :param queryset: the table contained in the file
    :param resource: the resource assiated with the queryset
    :param zipObj: the zip object in wich we want to write
    :return: nothing
    """

    if file_type == 'csv':
        queryset_to_csv(queryset, fields, filename)
    elif file_type == 'json':
        queryset_to_json(queryset, fields, filename)
    elif file_type == 'html':
        queryset_to_xml(queryset, fields, filename)
    elif file_type == 'xlsx':
        queryset_to_xlsx(queryset, fields, filename)
    elif file_type == 'yaml':
        queryset_to_yaml(queryset, fields, filename)

    zipObj.write(filename)
    os.remove(filename)


def queryset_to_csv(queryset, fields, filename):
    """
    This function create a csv file with a given queryset
    :param queryset: the queryset that we want to export in a file
    :param fields: the fields that we want in our table (it must be the same names as those in the models
    :param filename: the name of the future file
    :return: nothing
    """
    file = open(filename, 'w')  # we create an empty file
    writer = csv.writer(file)  # we create a writer linked to the file
    writer.writerow([field for field in fields])  # we write the fields
    for row in queryset:
        line = []
        for field in fields:
            # if the field is a ManyToManyField, we must save a list, in this case a list of username
            if field == 'members':
                line.append([member.username for member in row.__getattribute__(field).all()])
            else:
                line.append(row.__getattribute__(field))
        writer.writerow(line)
    file.close()


def queryset_to_json(queryset, fields, filename):
    """
    This function does the same thing that queryset_to_csv but for json file
    :param queryset:
    :param fields:
    :param filename:
    :return:
    """
    file = open(filename, "w")
    result = dict()  # we create a dictionnary that contains dictionnaries for each items
    for row in queryset:
        row_dict = dict()
        for field in fields:
            if field == 'members':
                row_dict[field] = [member.username for member in row.__getattribute__(field).all()]
            else:
                row_dict[field] = row.__getattribute__(field).__str__()
        result[row.id] = row_dict
    file.write(json.dumps(result))  # we save this dictionnary
    file.close()


def queryset_to_xml(queryset, fields, filename):
    """
    This function does the same thing that queryset_to_csv but for xml/html file
    :param queryset:
    :param fields:
    :param filename:
    :return:
    """
    file = open(filename, "wb")
    table = ET.Element('table')
    head = ET.SubElement(table, 'tr')
    for field in fields:
        head_field = ET.SubElement(head, 'th')
        head_field.text = field

    for row in queryset:
        table_row = ET.SubElement(table, 'tr')
        for field in fields:
            item = ET.SubElement(table_row, 'td')
            if field == 'members':
                item.text = [member.username for member in row.__getattribute__(field).all()].__str__()
            else:
                item.text = row.__getattribute__(field).__str__()

    file.write(ET.tostring(table))
    file.close()


def queryset_to_xlsx(queryset, fields, filename):
    """
    This function does the same thing that queryset_to_csv but for xlsx file
    :param queryset:
    :param fields:
    :param filename:
    :return:
    """
    file = xlsx.Workbook(filename)  # we create an xlsx file
    worksheet = file.add_worksheet()  # we create a sheet inside this file
    bold = file.add_format({'bold': True})  # we create a bold format for the header
    count = 0
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for field in fields:
        worksheet.write(alphabet[count] + (1).__str__(), field, bold)  # we write a field in a cell with bold format
        count += 1
    row_number = 2
    for row in queryset:
        col_number = 0
        for field in fields:
            if field == 'members':
                worksheet.write(alphabet[col_number] + row_number.__str__(),
                                [member.username for member in row.__getattribute__(field).all()].__str__())
            else:
                worksheet.write(alphabet[col_number] + row_number.__str__(), row.__getattribute__(field).__str__())
                col_number += 1
        row_number += 1

    file.close()


def queryset_to_yaml(queryset, fields, filename):
    """
    This function does the same thing that queryset_to_csv but for yaml file
    :param queryset:
    :param fields:
    :param filename:
    :return:
    """
    file = open(filename, "w")
    result = []  # we create an empty list
    for row in queryset:
        row_dict = dict()
        for field in fields:
            if field == 'members':
                row_dict[field] = [member.username for member in row.__getattribute__(field).all()]
            else:
                row_dict[field] = row.__getattribute__(field).__str__()
        result.append(row_dict)  # we add a dictionnary to this list for each rows
    file.write(yaml.dump(result))
    file.close()
