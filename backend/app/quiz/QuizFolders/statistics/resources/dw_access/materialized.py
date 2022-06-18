
from bson.json_util import dumps, loads

from datetime import datetime, date, timedelta
from .domains import getOldRecord_Domain
from .system import getRecentAndOldRecordLogins, getRecentAndOldRecord
# materialied = {
#     Domain:xxx,
#     Start_date:yyy,
#     end_date:zzz
# }

def getMaterializedDates(domain,mongoDW):
    l_dates=[]

    try:
        dates = mongoDW.db.materialized.find({"Domain":domain})

        l_dates = list(dates)

        if l_dates==[] or l_dates[0].get('Start_Date') is None:
            list_dates = getOldRecord_Domain(domain,mongoDW)
            if list_dates!=[]:
                start = list_dates[0]['Dim_Calendar']['Date']
                end = list_dates[len(list_dates)-1]['Dim_Calendar']['Date']
                dates = {
                    'Domain': domain,
                    'Start_Date': start,
                    'End_Date': end
                }
                mongoDW.db.materialized.update_one({'Domain':domain},{'$set':dates},upsert=True)
                print('datesNotFound', dates)
                l_dates=[dates]
    except:
        print("Can't get materialized dates from db")
    return l_dates

# materialied = {
#     URL:xxx,
#     Method:POST
#     Start_date:yyy,
#     end_date:zzz
# }
def getMaterializedDatesLogin(mongoDW):
    l_dates=[]
    try:
        dates = mongoDW.db.materialized.find({"URL":"/","Method":"POST"})

        l_dates = list(dates)

        if l_dates==[] or l_dates[0].get('Start_Date') is None:
            list_dates = getRecentAndOldRecordLogins(mongoDW)
            if list_dates is not None:
                start = list_dates['old']
                end = list_dates['recent']
                dates = {
                    'URL': "/",
                    "Method": "POST",
                    'Start_Date': start,
                    'End_Date': end
                }
                mongoDW.db.materialized.update_one({"URL":"/","Method":"POST"},{'$set':dates},upsert=True)
                print('datesNotFound', dates)
                l_dates=[dates]
    except:
        print("Can't get login mterialized dates from db")
    return l_dates

# materialied = {
#     URL:xxx,
#     Method:POST
#     Start_date:yyy,
#     end_date:zzz
# }
def getMaterializedDatesSystem(mongoDW):
    l_dates=[]
    try:
        dates = mongoDW.db.materialized.find({"URL":"all"})

        l_dates = list(dates)

        if l_dates==[] or l_dates[0].get('Start_Date') is None:
            list_dates = getRecentAndOldRecord(mongoDW)
            if list_dates is not None:
                start = list_dates['old']
                end = list_dates['recent']
                dates = {
                    'URL': "all",
                    'Start_Date': start,
                    'End_Date': end
                }
                mongoDW.db.materialized.update_one({"URL":"all"},{'$set':dates},upsert=True)
                print('datesNotFound', dates)
                l_dates=[dates]
    except:
        print("Can't get system materialized dates from db")
    return l_dates