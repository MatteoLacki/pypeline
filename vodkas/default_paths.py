apex3Dpath = "C:/SYMPHONY_VODKAS/plgs/Apex3D64.exe"
peptide3Dpath = "C:/SYMPHONY_VODKAS/plgs/Peptide3D.exe"
iadbspath = "C:/SYMPHONY_VODKAS/plgs/iaDBs.exe"
wx2csvpath = "C:/SYMPHONY_VODKAS/bin/wx2csv.jar"
logs_folder = 'C:/SYMPHONY_VODKAS/temp_logs'
logs_server_folder = 'X:/SYMPHONY_VODKAS/temp_logs'

# for docs only:
logs_folder_dict = dict(default=logs_folder,
    help="Path to the folder storing locally the logs. [default = {}]".format(logs_folder)
)
logs_server_folder_dict = dict(
    default=logs_server_folder,
    help="Path to the folder storing locally the logs. [default = {}]".format(logs_server_folder)
)