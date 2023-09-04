from module.file_reader_writer import FileReaderWriter

# Verwendung der Klasse FileReaderWriter
folder_path = 'data/'
output_file = 'combined_data.csv'

file_reader_writer = FileReaderWriter(folder_path)
file_reader_writer.read_files()
file_reader_writer.process_data()
file_reader_writer.write_file(output_file)