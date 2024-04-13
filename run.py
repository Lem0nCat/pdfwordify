#!/usr/bin/env python

import os

from Tools.config import TESSDATA_PATH

# Экспортируем переменную среды TESSDATA_PREFIX
if TESSDATA_PATH.strip():
    os.environ['TESSDATA_PREFIX'] = TESSDATA_PATH

# Запускаем основной скрипт
import src.main
if __name__ == '__main__':
    src.main.main()
