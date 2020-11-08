# Std Libs
from contextlib import closing
import io
import os

# 3rd Party Libs
import dropbox
import pandas as pd

token = os.environ.get('DROPBOX')
dbx = dropbox.Dropbox(token)

# --------------------------------------------------------------------------------


def read_file(_path):

    def stream_dropbox_file(_path):
        _,res=dbx.files_download(_path)
        with closing(res) as result:
            byte_data=result.content
            return io.BytesIO(byte_data)
    
    file_stream=stream_dropbox_file(_path)
    d = pd.read_csv(file_stream)

    return d

# --------------------------------------------------------------------------------

def write_file(df,path):

        dbx.files_upload(df.to_csv(index=False).encode(),path,mode=dropbox.files.WriteMode.overwrite)

# --------------------------------------------------------------------------------