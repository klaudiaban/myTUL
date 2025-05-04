from datetime import datetime
import calendar
from flet import *
import flet_easy as fs
from constants import *

calen = fs.AddPagesy()
@calen.page('/calen', title='Calendar')
def calendar_view(data: fs.Datasy):
    return 