import re
import io
import zipfile
import requests
from pathlib import Path

import pandas as pd


PROCESSING_LIBRARY_URL = 'http://download.processing.org/contribs'

PARAGRAPH_REGEX = re.compile('^paragraph=(.*?)^[a-z]*?=', re.DOTALL | re.MULTILINE)


class ProcessingLibraryInfo:

    def __init__(self):
        self._data = self._load_data()

    def _load_data(self):
        response = requests.get(PROCESSING_LIBRARY_URL)
        if response.status_code != 200:
            raise RuntimeError(f'could not download data file at {PROCESSING_LIBRARY_URL}')

        blocks = [b for b in response.text.split('\n\n') if b.startswith('library')]
        block_lines = [dict([line.split('=', 1)
                            for line in block.split('\n')
                            if line != "library"])
                       for block in blocks]
        df = pd.DataFrame.from_dict(block_lines, dtype="string")
        # lastUpdated is supposed to be the last column
        df = df.iloc[:, :(df.columns.get_loc('lastUpdated') + 1)]
        df.astype({'id': int, 'minRevision': int, 'maxRevision': int})
        df['id'] = df['id'].astype(int)
        df['minRevision'] = df['minRevision'].astype(int)
        df['maxRevision'] = df['maxRevision'].astype(int)
        df['categories'] = df['categories'].apply(lambda x: x.split(','))
        # get paragraph values from raw data because they could be on more than one
        # line or the paragraph could be missing
        df['paragraph'] = [PARAGRAPH_REGEX.findall(b) for b in blocks]
        df['paragraph'] = df['paragraph'].apply(lambda x: x[0] if x else '').astype('string')

        return df

    def get_library_info(self, library_name=None, library_id=None):
        if library_name:
            info = self._data[self._data['name'] == library_name]
        elif library_id:
            info = self._data[self._data['id'] == library_id]
        else:
            raise RuntimeError(f'no library {library_name} specified')

        if len(info) == 0:
            raise RuntimeError(f'library {library_name} not found')
        if len(info) > 1:
            raise RuntimeError(f'more than one library with name {library_name}???')

        return info.T.to_dict()[info.index[0]]

    def download_zip(self, dest, library_name=None, library_id=None):
        info = self.get_library_info(library_name=library_name, library_id=library_id)
        download_url = info['download']

        response = requests.get(download_url)
        if response.status_code != 200:
            raise RuntimeError(f'could not download library at {download_url}')

        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            jars = []
            for name in zf.namelist():
                path = Path(name)
                if len(path.parts) > 2 and path.parts[1] == 'library' and path.suffix == '.jar':
                    jars.append(name)
            zf.extractall(dest, jars)
