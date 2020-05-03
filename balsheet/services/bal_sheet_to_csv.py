import os
import tabula
import pandas as pd


class PdfFileReader:
    def __init__(self, directory, file_name):
        """Input: directory and pdf file
        OutPut: File content in raw form"""
        self.directory = directory
        self.file_name = file_name

    def get_file_path(self):
        file_path = "{dir}/{file}".format(
            dir=self.directory,
            file=self.file_name)
        if os.path.exists(file_path):
            return file_path
        else:
            print("file path does not exists")
            return False

    def read_pdf_file(self):
        file_path = self.get_file_path()
        content = tabula.read_pdf(
            file_path,
            multiple_tables=True
            )
        return content

    def get_pdf_file_table_content(self):
        content = self.read_pdf_file()
        return content[0].values


class CreateBalSheetDataFrame:
    def __init__(self, bal_sheet):
        self.bal_sheet = bal_sheet
        self.data_list = {}

    def header_data_to_data_list(self):
        header = self.bal_sheet[0]
        self.data_list[header[0]] = []
        self.data_list[header[1]] = []
        self.data_list[header[2]] = []
        self.data_list[header[3] + ' '] = []
        self.data_list[header[4] + ' '] = []
        self.data_list[header[5] + ' '] = []
        return

    def body_first_content_to_data_list(self):
        header = self.bal_sheet[0]
        first_content = self.bal_sheet[1]
        particulars1 = first_content[0].split("\r")
        self.data_list[header[0]] += particulars1
        first_year1 = first_content[1].split("\r")
        self.data_list[header[1]] += first_year1
        second_year1 = first_content[2].split("\r")
        self.data_list[header[2]] += second_year1
        particulars2 = first_content[3].split("\r")
        self.data_list[header[3] + ' '] += particulars2
        first_year2 = first_content[4].split("\r")
        self.data_list[header[4] + ' '] += first_year2
        second_year2 = first_content[5].split("\r")
        self.data_list[header[5] + ' '] += second_year2
        return

    def first_bal_sheet_summary_total(self):
        header = self.bal_sheet[0]
        summary = self.bal_sheet[2]
        self.data_list[header[1]].append(summary[1])
        self.data_list[header[2]].append(summary[2])
        self.data_list[header[4] + ' '].append(summary[3])
        self.data_list[header[5] + ' '].append(summary[4])
        return

    def body_second_content_to_data_list(self):
        header = self.bal_sheet[0]
        second_content = self.bal_sheet[3]
        first_year1 = second_content[1].split("\r")
        self.data_list[header[1]] += first_year1
        second_year1 = second_content[2].split("\r")
        self.data_list[header[2]] += second_year1
        first_year2 = second_content[3].split("\r")
        self.data_list[header[4] + ' '] += first_year2
        second_year2 = second_content[4].split("\r")
        self.data_list[header[5] + ' '] += second_year2
        return

    def manage_empty_row(self):
        header = self.bal_sheet[0]
        max_rows = len(self.data_list[header[0]])
        min_rows = len(self.data_list[header[3] + ' '])
        empty_rows = max_rows - min_rows
        empty_space_list = [''] * empty_rows
        self.data_list[header[3] + ' '] += empty_space_list
        self.data_list[header[4] + ' '] += empty_space_list
        self.data_list[header[5] + ' '] += empty_space_list
        return

    def fooler_data_to_data_list(self):
        header = self.bal_sheet[0]
        fooler = self.bal_sheet[-1]
        self.data_list[header[0]].append(fooler[0])
        self.data_list[header[1]].append(fooler[1])
        self.data_list[header[2]].append(fooler[2])
        self.data_list[header[3] + ' '].append(fooler[3])
        self.data_list[header[4] + ' '].append(fooler[4])
        self.data_list[header[5] + ' '].append(fooler[5])
        return

    def initialise_data_list(self):
        self.header_data_to_data_list()
        self.body_first_content_to_data_list()
        self.first_bal_sheet_summary_total()
        self.body_second_content_to_data_list()
        self.manage_empty_row()
        self.fooler_data_to_data_list()
        return self.data_list


class ConvertandWriteCSV:
    def __init__(self, data_list, directory, file_name):
        self.data_list = data_list
        self.directory = directory
        self.file_name = file_name

    def data_list_to_data_frame(self):
        data_frame = pd.DataFrame(self.data_list)
        return data_frame

    def write_csv(self):
        data_frame = self.data_list_to_data_frame()
        file_loc = "{directory}/{file_name}".format(
            directory=self.directory,
            file_name=self.file_name)
        data_frame.to_csv(file_loc, index=False)


class PdfToCsvBalSheet:
    def __init__(self, in_file_name, in_dir, out_dir):
        self.in_file_name = in_file_name
        self.out_file_name = self.in_file_name.split(".")[0] + ".csv"
        self.in_dir = in_dir
        self.out_dir = out_dir

    def pdf_to_csv_balsheet(self):
        pdf_file_reader = PdfFileReader(self.in_dir, self.in_file_name)
        content = pdf_file_reader.get_pdf_file_table_content()
        bal_sheet_data_frame = CreateBalSheetDataFrame(content)
        data_list = bal_sheet_data_frame.initialise_data_list()
        csv_writer = ConvertandWriteCSV(data_list, self.out_dir, self.out_file_name)
        csv_writer.write_csv()
        return
