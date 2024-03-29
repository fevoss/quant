import pandas as pd
import requests
import json
from enum import Enum
from dataclasses import dataclass
from typing import Any


class Codes(Enum):
    SP500 = 'SP500'
    US_TBOND_1OY = 'DGS10'
    US_TBOND_3OY = 'DGS30'


@dataclass
class Api:

    api_key: str

    verify: bool = True
    _END_POINT = 'https://api.stlouisfed.org/fred'

    def _requisitar(self, url) -> Any | None:
        resposta = requests.get(url, verify=self.verify)
        if resposta.status_code == 200:
            return json.loads(resposta.text)
        return None

    def obter_serie(self, codigo: Codes):
        url = f'{self._END_POINT}/series/observations?api_key={self.api_key}&series_id={codigo.value}&file_type=json'
        r = self._requisitar(url)
        if r is not None:
            dict_ = r['observations']
            dias, valores = [], []
            for item in dict_:
                dias.append(item['date']), valores.append(item['value'])

            serie = pd.Series(pd.to_numeric(valores, errors='coerce'), index=pd.to_datetime(dias))
            serie.index.name = 'Data'
            serie.name = codigo.name
            return serie
