import sqlite3
import os


class VideoDatabase():
    def __init__(self):
        super(VideoDatabase, self).__init__()
        # self.dbname = 'jcfgvd.dll'
        # libray FOR jbadonaiventures configuration file FOR video downloader
        self.dbname = 'libjcfvd.dll'

    def set_db_filename(self, filename):
        self.dbname = filename

    def create_video_database(self):
        ''' create video table in the database '''
        try:
            print('createing video data database...')
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()
            command = '''
            CREATE TABLE IF NOT EXISTS VideoData
            (
            id integer primary key AUTOINCREMENT,
            download_video BOOL,
            download_all BOOL,
            format TEXT,
            url TEXT,
            title TEXT,
            is_playlist BOOL,
            playlist_index TEXT NULL,
            playlist_title TEXT NULL,
            playlist_url TEXT NULL,
            thumbnail TEXT,
            status TEXT,
            download_location TEXT        
            )
            '''
            cursor.execute(command)
            connection.commit()
            connection.close()
        except Exception as e:
            print(f"An error occurred in database module ': {e}")

    def create_settings_database(self):
        ''' creates settings table in the database '''
        try:
            print("Creating settings database...")
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()
            command = '''
            CREATE TABLE IF NOT EXISTS Settings
            (
            id integer primary key AUTOINCREMENT,
            key TEXT,
            value TEXT      
            )
            '''
            cursor.execute(command)
            connection.commit()
            connection.close()
        except Exception as e:
            print(f"An error occurred in database module 'CREATE SETTINGS DATABASE' : {e}")

    def insert_into_video_database(self, data):
        ''' save input data into the video database '''

        downloadVideo = data['download_video']
        downloadAll = data['download_all']
        format = data['format']
        url = data['url']
        title = data['title']
        isPlaylist = data['is_playlist']
        playlistIndex = data['playlist_index']
        playlistTitle = data['playlist_title']
        playlistURL = data['playlist_url']
        thumbnail = data['thumbnail']
        status = data['status']
        downloadLocation = data['download_location']

        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()

            cursor.execute('INSERT INTO VideoData '
                           '(download_video, download_all, format, url, title, is_playlist, playlist_index, playlist_title, playlist_url, thumbnail, status, download_location) '
                           'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                           (downloadVideo, downloadAll, format, url, title, isPlaylist, playlistIndex, playlistTitle,
                            playlistURL, thumbnail, status, downloadLocation))
            connection.commit()

        except Exception as e:
            print(f"An error occurred in database module 'INSERT INTO VIDEO DATABASE' : {e}")

    def setup_create_settings(self, key, value):
        ''' set up required columns in the settings table '''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()
            cursor.execute("insert into Settings (key, value) values (?, ?)", (key, value))
            connection.commit()
            connection.close()
        except Exception as e:
            print(f"An error occurred in database module 'SETUP CREATE SETTINGS': {e}")

    def update_setting(self, key, value):
        ''' update the value of a setting using the key'''
        try:

            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()
            cursor.execute("update Settings set value = ? where key = ?", (value, key))
            connection.commit()
            connection.close()
        except Exception as e:
            print(f"An error occurred in database module 'UPDATE SETTING': {e}")

    def get_settings(self, key):
        ''' Reterieve a particular settings from the database using the key '''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()
            cursor.execute("select value from Settings where key = ?", (key,))
            ans = cursor.fetchall()
            return ans[0][0]
        except Exception as e:
            print(f"An error occurred in the database module 'GET SETTING' [{key}]:{e}")

    def is_setting_key_in_database(self, key):
        ''' check if a particular key exist in the settings table'''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()
            cursor.execute("select value from Settings where key = ?", (key,))
            ans = cursor.fetchall()
            if len(ans) == 0:
                return False
            else:
                return True

        except Exception as e:
            print(f"An error occurred in database moodule 'IS SETTING KEY IN DATABASE' : {e}")

    def get_all_video_data(self):
        ''' get all the video data in the database '''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()

            cursor.execute('select * from VideoData')
            data = cursor.fetchall()
            return data
        except Exception as e:
            print(f"An error occurred in database module ' GET ALL VIDEO DATA' : [e")

    def get_waiting_number(self):
        ''' get all data in database with status of waiting '''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()

            cursor.execute('select * from VideoData where status = "waiting"')
            data = cursor.fetchall()
            return len(data)
        except Exception as e:
            print(f"An error occurred in database module 'GET WAITING NUMBER': {e}")

    def get_completed_number(self):
        '''get all data in database with status of completed'''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()

            cursor.execute('select * from VideoData where status = "completed"')
            data = cursor.fetchall()
            return len(data)
        except Exception as e:
            print(f"An error occurred in database module 'GET COMPLETED NUMBER': {e}")

    def get_stopped_number(self):
        ''' get all data in database with status of stopped'''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()

            cursor.execute('select * from VideoData where status = "stopped"')
            data = cursor.fetchall()
            return len(data)
        except Exception as e:
            print(f"An error occurred in database module 'GET STOPPED NUMBER': {e}")

    def get_downloading_number(self):
        ''' Get all data in database with status of downloading'''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()

            cursor.execute('select * from VideoData where status = "downloading"')
            data = cursor.fetchall()
            return len(data)
        except Exception as e:
            print(f"An error occurred in database module 'GET DOWNLOADING NUMBER': {e}")

    def get_total_number(self):
        ''' This get the total number of data already stored in the database '''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()

            cursor.execute('select * from VideoData where status != ? ',('deleted',))
            data = cursor.fetchall()
            return len(data)
        except Exception as e:
            print(f"An error occurred in database module 'GET TOTAL NUMBER': {e}")

    def get_next_waiting_data(self):
        ''' This loop through the database and get the next item that has a status of waiting'''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()

            cursor.execute('select * from VideoData where status = "waiting"')
            data = cursor.fetchall()
            return data[0]
        except Exception as e:
            print(f"An error occurred in database module 'GET NEXT WAITING DATA' :{e}")

    def delete_by_url(self,url):
        connection = sqlite3.connect(self.dbname)
        cursor = connection.cursor()

        cursor.execute('DELETE FROM VideoData WHERE url=? ', (url,))
        connection.commit()

    def delete_by_title(self,title):
        connection = sqlite3.connect(self.dbname)
        cursor = connection.cursor()

        cursor.execute('DELETE FROM VideoData WHERE title=? ', (title,))
        connection.commit()

    def get_status(self, url):
        ''' gets status of the specified url '''
        # try:
        connection = sqlite3.connect(self.dbname)
        cursor = connection.cursor()

        cursor.execute('select status from VideoData where url = ? ', (url,))
        data = cursor.fetchall()

        return data[0][0]
        # except Exception as e:
        #     print(f"An error occurred in database module ' GET STATUS' : {e}")
        #     return 'e'

    def get_entry_by_url(self, url):
        ''' gets status of the specified url '''
        # try:
        connection = sqlite3.connect(self.dbname)
        cursor = connection.cursor()

        cursor.execute('select * from VideoData where url = ? ', (url,))
        data = cursor.fetchall()

        return data[0]
        # except Exception as e:
        #     print(f"An error occurred in database module ' GET STATUS' : {e}")
        #     return 'e'

    def get_download_location_by_url(self, url):
        ''' gets status of the specified url '''
        # try:
        connection = sqlite3.connect(self.dbname)
        cursor = connection.cursor()

        cursor.execute('select download_location from VideoData where url = ? ', (url,))
        data = cursor.fetchall()

        return data[0][0]
        # except Exception as e:
        #     print(f"An error occurred in database module ' GET STATUS' : {e}")
        #     return 'e'

    def get_entry_by_playlist_url(self, url):
        ''' gets status of the specified url '''
        # try:
        connection = sqlite3.connect(self.dbname)
        cursor = connection.cursor()

        cursor.execute('select * from VideoData where playlist_url = ? ', (url,))
        data = cursor.fetchall()

        return data[0]
        # except Exception as e:
        #     print(f"An error occurred in database module ' GET STATUS' : {e}")
        #     return 'e'

    def get_all_entries_by_title(self, title):
        ''' gets status of the specified url '''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()

            cursor.execute('select * from VideoData where title = ? ', (title,))
            data = cursor.fetchall()

            return data
        except Exception as e:
            print(f"An error occurred in database module ' GET all entries by title' : {e}")
            return 'e'

    def get_all_entries_by_playlist_title(self, playlist_title):
        ''' gets status of the specified url '''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()

            cursor.execute('select * from VideoData where playlist_title = ? ', (playlist_title,))
            data = cursor.fetchall()

            return data
        except Exception as e:
            print(f"An error occurred in database module ' GET all entries by playlist title' : {e}")
            return 'e'

    def get_all_entries_by_status(self, status):
        ''' gets status of the specified url '''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()

            cursor.execute('select * from VideoData where status = ? ', (status,))
            data = cursor.fetchall()

            return data
        except Exception as e:
            print(f"An error occurred in database module ' GET all entries by playlist title' : {e}")
            return 'e'

    def get_total_by_status(self, status):
        ''' gets status of the specified url '''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()

            cursor.execute('select * from VideoData where status = ? ', (status,))
            data = cursor.fetchall()

            return len(data)
        except Exception as e:
            print(f"An error occurred in database module ' get total by STATUS' : {e}")
            return 0

    def get_no_of_video_in_playlist(self, playlist_url):
        ''' gets status of the specified url '''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()

            cursor.execute('select * from VideoData where playlist_url = ? ', (playlist_url,))
            data = cursor.fetchall()

            return len(data)
        except Exception as e:
            print(f"An error occurred in database module ' get_no_of_video_in_playlist' : {e}")
            return 0

    def get_status_by_playlist_url(self, playlist_url):
        ''' gets status of the specified url '''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()

            cursor.execute('select status from VideoData where playlist_url = ? ', (playlist_url,))
            data = cursor.fetchall()

            return data[0][0]
        except Exception as e:
            print(f"An error occurred in database module ' GET STATUS' : {e}")

    def is_url_exists_in_database(self, url):
        '''
        checks if url (which is key identifier in vidoe database) exists to avoid duplicate
        '''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()

            cursor.execute("select * from VideoData where url =?", (url,))
            data = cursor.fetchall()
            if len(data) == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f"An error occurred in database module 'IS URL EXISTS IN DATABASE': {e}")

    def is_playlist_url_exists_in_database(self, url):
        '''
        checks if url (which is key identifier in vidoe database) exists to avoid duplicate
        '''
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()

            cursor.execute("select * from VideoData where playlist_url =?", (url,))
            data = cursor.fetchall()
            if len(data) == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f"An error occurred in database module 'IS URL EXISTS IN DATABASE': {e}")

    def set_status(self, url, status):
        '''
        set status for provided key (url)
        '''

        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()

            cursor.execute("update VideoData set status = ? where url = ?", (status, url))
            connection.commit()
            connection.close()
        except Exception as e:
            print(f"An error occurred in database module 'SET STATUS': ")

    def set_status_using_playlist_url(self, playlist_url, status):
        '''
        set status for provided key (url)
        '''

        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()

            cursor.execute("update VideoData set status = ? where url = ?", (status, playlist_url))
            connection.commit()
            connection.close()
        except Exception as e:
            print(f"An error occurred in database module 'SET STATUS': ")

    def reset_all_status_to(self, status):
        '''
        loop through all the download stores in the database and set all their status to new status provided
        '''

        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()
            cursor.execute("select * from VideoData")
            all = cursor.fetchall()
            for data in all:
                cursor.execute("update VideoData set status = ? where url = ? ", (status, data[4]))
                connection.commit()
            connection.close()
        except Exception as e:
            print(f"An error occurred in database module 'RESET ALL STATUS TO': {e}")

    def initialize_database(self):
        '''
        creates required tables for video and settings in the database
        checks for required settings key entry and create one if not available
        '''
        try:
            print("Initializing and checking the database...")
            # crates video table if it does not exists
            self.create_video_database()
            # crates settings table if it dow not exist.
            self.create_settings_database()

            # check for keys in setting stable and create one if it does not exist.
            if self.is_setting_key_in_database("max_download") is False:
                self.setup_create_settings("max_download", 1)

            if self.is_setting_key_in_database("trial_expired") is False:
                self.setup_create_settings("trial_expired", False)

            if self.is_setting_key_in_database("trial_activated") is False:
                self.setup_create_settings("trial_activated", False)

            if self.is_setting_key_in_database("fully_activated") is False:
                self.setup_create_settings("fully_activated", False)

            if self.is_setting_key_in_database("license_key") is False:
                self.setup_create_settings("license_key", "")

            if self.is_setting_key_in_database("trial_key") is False:
                self.setup_create_settings("trial_key", "")

            if self.is_setting_key_in_database("active") is False:
                self.setup_create_settings("active", False)

            if self.is_setting_key_in_database("message_sent_successfully") is False:
                self.setup_create_settings("message_sent_successfully", False)

            if self.is_setting_key_in_database("owner") is False:
                self.setup_create_settings("owner", "jbadonaiventures")

            if self.is_setting_key_in_database("temp_owner") is False:
                self.setup_create_settings("temp_owner", "")

            if self.is_setting_key_in_database("system_id") is False:
                self.setup_create_settings("system_id", None)

            if self.is_setting_key_in_database("system_key") is False:
                self.setup_create_settings("system_key", None)

            if self.is_setting_key_in_database("permanent_delete") is False:
                self.setup_create_settings("permanent_delete", True)

            if self.is_setting_key_in_database("max_retries") is False:
                self.setup_create_settings("max_retries", 5)

            if self.is_setting_key_in_database("server_list") is False:
                self.setup_create_settings("server_list", None)

            if self.is_setting_key_in_database("default_server") is False:
                self.setup_create_settings("default_server", b'gAAAAABjkzU6SloQLb0TU7BKTE3Of2Fr7R55NEy0cdgamyvvoEkp_Zfq7dS6XeymioKJJcBzhnYvGFT0Hmdo-gBBJE1MFqNEPRSK7qG1mKf3xRGQbA9uLB0=')

                # WORNG SERVER FOR TESTING
                # self.setup_create_settings("default_server", b'gAAAAABjkD-tJpew_5OC_DsY-YYjXgTrK95P8_IvhxaFEU6SIDVvEXUk2Bf9tcDtOb1b4uEbXwmCI3QcjiqscUa1XDTG3PBmiEaTgsFSyeJX-gwqePsPsCo=')

            # Theme
            if self.is_setting_key_in_database("theme") is False:
                self.setup_create_settings("theme", "dark")

            if self.is_setting_key_in_database("check_internet_speed") is False:
                self.setup_create_settings("check_internet_speed", False)

            # Auto start new download
            if self.is_setting_key_in_database("auto_start_new_download") is False:
                self.setup_create_settings("auto_start_new_download", True)

            # Auto add new download to the download list
            if self.is_setting_key_in_database("auto_add_new_download") is False:
                self.setup_create_settings("auto_add_new_download", True)

            # Auto start waiting download
            if self.is_setting_key_in_database("auto_start_waiting_download") is False:
                self.setup_create_settings("auto_start_waiting_download", True)

            if self.is_setting_key_in_database("default_download_location") is False:
                self.setup_create_settings("default_download_location",  "downloads")
                # self.setup_create_settings("default_download_location", os.path.join(os.getcwd(), "download"))

        except Exception as e:
            print(f"An error occurred in database module 'INITIALIZE DATABASE': {e}")
