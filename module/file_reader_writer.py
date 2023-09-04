import os
import pandas as pd

class FileReaderWriter:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.file_list = []
        self.dataframes = []

    def _get_file_list(self):
        self.file_list = [file for file in os.listdir(self.folder_path) if file.startswith('Spare part catalog') and file.endswith('.txt')]

    def read_files(self):
        self._get_file_list()
        for file in self.file_list:
            file_path = os.path.join(self.folder_path, file)
            df = pd.read_csv(file_path, delimiter='\t', encoding='utf-16', skiprows=0)
            
            # Spaltennamen anpassen, falls erforderlich
            if 'Toc element name' in df.columns:
                df.rename(columns={'Toc element name': 'Hauptknoten Name'}, inplace=True)
            
            self.dataframes.append(df)

    def _find_common_columns(self):
        reference_columns = self.dataframes[0].columns.tolist()
        common_columns = []
        for col in reference_columns:
            if all(col in df.columns for df in self.dataframes):
                common_columns.append(col)
        return common_columns
    
    def process_data(self):
        for i, df in enumerate(self.dataframes):
            # Gemeinsame Spaltennamen finden
            common_columns = self._find_common_columns()
            
            # Struktur auf gemeinsame Spalten reduzieren
            relevant_df = df[common_columns]
            
            # Hier können Sie Ihre Datenverarbeitungslogik auf relevant_df anwenden
            relevant_df['Code'] = relevant_df['Code'].astype(str)
            relevant_df = relevant_df[~relevant_df['Code'].str.contains('SOTTO_PRODOTTO')]

            # Überschreiben Sie das ursprüngliche DataFrame in der Liste mit dem reduzierten relevant_df
            self.dataframes[i] = relevant_df

    def write_file(self, output_file):
        combined_df = pd.concat(self.dataframes, ignore_index=True)
        combined_df.to_csv(output_file, index=False, sep='\t', encoding='utf-16')