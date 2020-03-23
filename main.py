import shutil
import time
import yaml
import schedule
import os

def load_config(file):
    with open(file, "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.Loader)

class BackupManager:
    def __init__(self):
        self.configs = load_config("./config.yaml")
        self.backups = []
        schedule.every().day.at(self.configs["backup-at"]).do(self._backup)

    def _backup(self):
        # backing up
        backup_time = time.strftime('%Y-%m-%d-%H-%M')
        filename = f"{ self.configs.get('backup-path', '.') }/BACKUP-{backup_time}"
        # create the zipfile and return its name
        backup_name = shutil._make_zipfile(filename, self.configs["world-path"])
        
        # add the file to the queue
        self.backups.append(f"{filename}.zip")
        if len(self.backups) > self.configs["backups-count"]:
            to_remove = self.backups.pop(0)
            os.remove(to_remove)

        log_message = f"Backed up world at {backup_time}\n"
        
        # logging
        with open(self.configs["log-file"], "a", encoding="utf-8") as f:
            f.write(log_message)
            print(log_message, end='')
    
    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

def main():
    backer = BackupManager()
    backer.run()

if __name__ == "__main__":    
    main()
