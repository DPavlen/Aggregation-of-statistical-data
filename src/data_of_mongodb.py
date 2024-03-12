import json
import pymongo
import datetime as dt
from dateutil.relativedelta import relativedelta

client = pymongo.MongoClient("mongodb://127.0.0.1:2717")
db = client.mymongo
collection = db.admin.collect
# db = client.newdb
# coll = db.newcol


def init_dict(gte, lte, group):
    # def init_dict(st, fn, group):
    """
    gte: ISODate("2022-09-01T00:00:00") - начальная дата
    lte: ISODate("2022-12-31T23:59:00") - конечная дата
    group - строка для указания временной группировки по месяцам, дням или часам.
    Функция принимает начальную (st)
    и конечную (fn) даты,
    а также строку gr для указания временной группировки по месяцам, дням или часам."""
    tmp_aggregate = {}
    if group == "month":
        n = gte.month - lte.month + 1
        for i in range(n):
            tmp_aggregate[gte.strftime("%Y-%m-%dT%H:%M:%S")] = 0
            gte += relativedelta(months=+1)
        return tmp_aggregate

    elif group == "day":
        n = (lte - gte).days + 1
        for i in range(n):
            tmp_aggregate[gte.strftime("%Y-%m-%dT%H:%M:%S")] = 0
            gte += relativedelta(days=+1)

        return tmp_aggregate

    elif group == "hour" and gte.day != lte.day:
        for i in range(25):
            tmp_aggregate[gte.strftime("%Y-%m-%dT%H:%M:%S")] = 0
            gte += relativedelta(hours=+1)
        return tmp_aggregate

    elif group == "hour" and gte.day == lte.day:
        for i in range(24):
            tmp_aggregate[gte.strftime("%Y-%m-%dT%H:%M:%S")] = 0
            gte += relativedelta(hours=+1)
        return tmp_aggregate


def get_key(dt_data, grouping_unit):
    """Возвращает ключ словаря в зависимости от группировки единицы:
    month - месяц;
    day - день;
    hour - час;
    """
    if grouping_unit == "month":
        return dt_data.strftime("%Y-%m") + "-01T00:00:00"
    elif grouping_unit == "day":
        return dt_data.strftime("%Y-%m-%d") + "T00:00:00"
    elif grouping_unit == "hour":
        return dt_data.strftime("%Y-%m-%dT%H") + ":00:00"


def main_app(dt_from, dt_upto, group_type):
    """
    dt_from - начальная дата в формате %Y-%m-%dT%H:%M:%S ;
    dt_upto - конечная дата в формате %Y-%m-%dT%H:%M:%S ;
    group_type - группировка по времени ;
    dictionary_time - временной словарь, куда происходит агрегация ;
    ."""
    dt_from = dt.datetime.strptime(dt_from, "%Y-%m-%dT%H:%M:%S")
    dt_upto = dt.datetime.strptime(dt_upto, "%Y-%m-%dT%H:%M:%S")
    dictionary_time = init_dict(dt_from, dt_upto, group_type)
    if dictionary_time is None:
        return "Такого запроса нет"

    for val in collection.find({"dt": {"$gte": dt_from, "$lte": dt_upto}}, {"_id": 0}):
        k = get_key(val["dt"], group_type)
        dictionary_time[k] = dictionary_time.get(k, 0) + val["value"]

    result = {
        "dataset": [],
        "labels": []
    }

    for key, val in dictionary_time.items():
        result["dataset"].append(val)
        result["labels"].append(key)

    return json.dumps(result)