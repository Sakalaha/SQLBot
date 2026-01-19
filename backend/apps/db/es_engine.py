# Author: Junjun
# Date: 2025/9/9

import json
from base64 import b64encode

import requests
from elasticsearch import Elasticsearch

from apps.datasource.models.datasource import DatasourceConf
from apps.mock.es.mock_es import get_mock_indices, get_mock_mapping
from common.error import SingleMessageError


def get_es_auth(conf: DatasourceConf):
    username = f"{conf.username}"
    password = f"{conf.password}"

    credentials = f"{username}:{password}"
    encoded_credentials = b64encode(credentials.encode()).decode()

    return {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_credentials}"
    }


def get_es_connect(conf: DatasourceConf):
    """!!! deprecated 弃用的 ES 连接过程，生产环境没有集群权限: monitor权限"""
    es_client = Elasticsearch(
        [conf.host],  # ES address
        basic_auth=(conf.username, conf.password),
        verify_certs=False,
        compatibility_mode=True,
        headers=get_es_auth(conf)
    )
    return es_client


# def get_mock_indices():
#     """模拟 es_client.cat.indices 返回的索引列表，生产环境没有集群权限：monitor, indice 权限"""
#     # wa_annotator_db_t_api_access_log
#     # wa_annotator_db_t_web_login_log
#     # wa_annotator_db_t_web_operation_log
#     # wa_annotator_db_t_ip_base_info
#     # wa_annotator_db_t_ip_ioc
#     # wa_annotator_db_t_domain_icp
#     # wa_annotator_db_t_domain_whois
#     # wa_annotator_db_t_domain_ioc
#     # wa_annotator_db_t_unit_baseinfo
#     # wa_annotator_db_t_unit_iplist
#     # wa_annotator_db_t_unit_domaincertlist
#     # wa_annotator_db_t_x509certinfo
#     # wa_annotator_db_t_app_baseinfo
#     # wa_annotator_db_t_app_sdomain_list
#     # wa_annotator_db_t_app_sip_list
#     # wa_annotator_db_t_app_cert_list
#     # wa_annotator_db_t_app_userid_list
#     return [
#         {"index": "wa_annotator_db_t_api_access_log"},
#         {"index": "wa_annotator_db_t_web_login_log"},
#         {"index": "wa_annotator_db_t_web_operation_log"},
#         {"index": "wa_annotator_db_t_ip_base_info"},
#         {"index": "wa_annotator_db_t_ip_ioc"},
#         {"index": "wa_annotator_db_t_domain_icp"},
#         {"index": "wa_annotator_db_t_domain_whois"},
#         {"index": "wa_annotator_db_t_domain_ioc"},
#         {"index": "wa_annotator_db_t_unit_baseinfo"},
#         {"index": "wa_annotator_db_t_unit_iplist"},
#         {"index": "wa_annotator_db_t_unit_domaincertlist"},
#         {"index": "wa_annotator_db_t_x509certinfo"},
#         {"index": "wa_annotator_db_t_app_baseinfo"},
#         {"index": "wa_annotator_db_t_app_sdomain_list"},
#         {"index": "wa_annotator_db_t_app_sip_list"},
#         {"index": "wa_annotator_db_t_app_cert_list"},
#         {"index": "wa_annotator_db_t_app_userid_list"}
#     ]
#
#
# def get_mock_mapping(table_name: str):
#     """模拟 mapping = es_client.indices.get_mapping(index=index_name) 返回的 properties 列表，生产环境没有集群权限: monitor 权限"""
#     match table_name:
#         case "wa_annotator_db_t_api_access_log":
#             return {
#                 table_name: {
#                     "mappings": {
#                         "_meta": {
#                             "description": "API 访问日志"
#                         },
#                         "properties": {
#                             "authenticated_entity": {"type": "object"},
#                             "client_ip": {"type": "keyword"},
#                             "consumer": {"type": "object"},
#                             "latencies": {"type": "object"},
#                             "request": {"type": "object"},
#                             "response": {"type": "object"},
#                             "route": {"type": "object"},
#                             "service": {"type": "object"},
#                             "started_at": {"type": "long"},
#                             "tries": {"type": "object"},
#                             "upstream_uri": {"type": "keyword"}
#                         }
#                     }
#                 }
#             }
#         case "wa_annotator_db_t_web_login_log":
#             return {
#                 table_name: {
#                     "mappings": {
#                         "_meta": {
#                             "description": "界面登录日志"
#                         },
#                         "properties": {
#                             "id": {"type": "long"},
#                             "logTime": {"type": "keyword"},
#                             "appId": {"type": "keyword"},
#                             "clientIp": {"type": "keyword"},
#                             "hostIp": {"type": "keyword"},
#                             "sysURL": {"type": "keyword"},
#                             "statusCode": {"type": "integer"},
#                             "accountId": {"type": "keyword"},
#                             "accountName": {"type": "keyword"},
#                             "accountStatus": {"type": "keyword"},
#                             "type": {"type": "keyword"},
#                             "result": {"type": "keyword"},
#                             "details": {"type": "text"},
#                             "dep": {"type": "keyword"}
#                         }
#                     }
#                 }
#             }
#         case "wa_annotator_db_t_web_operation_log":
#             return {
#                 table_name: {
#                     "mappings": {
#                         "_meta": {
#                             "description": "界面操作日志"
#                         },
#                         "properties": {
#                             "id": {"type": "long"},
#                             "logTime": {"type": "keyword"},
#                             "appId": {"type": "keyword"},
#                             "clientIp": {"type": "keyword"},
#                             "hostIp": {"type": "keyword"},
#                             "sysURL": {"type": "keyword"},
#                             "statusCode": {"type": "integer"},
#                             "accountId": {"type": "keyword"},
#                             "accountName": {"type": "keyword"},
#                             "accountStatus": {"type": "keyword"},
#                             "entityTypeId": {"type": "keyword"},
#                             "entityType": {"type": "keyword"},
#                             "entityName": {"type": "keyword"},
#                             "menu": {"type": "keyword"},
#                             "details": {"type": "text"},
#                             "success": {"type": "keyword"},
#                             "signature": {"type": "text"},
#                             "dep": {"type": "keyword"},
#                         }
#                     }
#                 }
#             }
#         case "wa_annotator_db_t_ip_base_info":
#             return {
#                 table_name: {
#                     "mappings": {
#                         "_meta": {
#                             "description": "IP 基本信息"
#                         },
#                         "properties": {
#                             "c_uuid": {"type": "keyword"},
#                             "c_ip": {"type": "keyword"},
#                             "c_operator": {"type": "keyword"},
#                             "c_asn": {"type": "keyword"},
#                             "c_as": {"type": "keyword"},
#                             "c_unit": {"type": "keyword"},
#                             "c_uniticp": {"type": "keyword"},
#                             "c_unitnature": {"type": "keyword"},
#                             "c_unitindustry": {"type": "keyword"},
#                             "c_country": {"type": "keyword"},
#                             "c_privince": {"type": "keyword"},
#                             "c_city": {"type": "keyword"},
#                             "c_distinct": {"type": "keyword"},
#                             "c_address": {"type": "keyword"},
#                             "c_longitude": {"type": "keyword"},
#                             "c_latitude": {"type": "keyword"},
#                             "c_radius": {"type": "keyword"},
#                             "c_reserve1": {"type": "keyword"},
#                             "c_reserve2": {"type": "keyword"},
#                             "c_reserve3": {"type": "keyword"},
#                             "c_reserve4": {"type": "keyword"},
#                             "c_reserve5": {"type": "keyword"},
#                             "c_source": {"type": "keyword"},
#                             "c_day": {"type": "date"}
#                         }
#                     }
#                 }
#             }
#         case "wa_annotator_db_t_ip_ioc":
#             return {
#                 table_name: {
#                     "mappings": {
#                         "_meta": {
#                             "description": "IP 信誉信息表"
#                         },
#                         "properties": {
#                             "c_ip": {"type": "keyword"},
#                             "c_type": {"type": "keyword"},
#                             "c_level": {"type": "keyword"},
#                             "c_confidence": {"type": "keyword"},
#                             "c_phases": {"type": "keyword"},
#                             "c_compromise": {"type": "keyword"},
#                             "c_tags": {"type": "keyword"},
#                             "c_revoked": {"type": "keyword"},
#                             "c_modified": {"type": "keyword"},
#                             "c_validuntil": {"type": "keyword"},
#                             "c_source": {"type": "keyword"},
#                             "c_day": {"type": "integer"}
#                         }
#                     }
#                 }
#             }
#         case "wa_annotator_db_t_domain_icp":
#             return {
#                 table_name: {
#                     "mappings": {
#                         "_meta": {
#                             "description": "域名备案信息表"
#                         },
#                         "properties": {
#                             "c_domain": {"type": "keyword"},
#                             "c_index": {"type": "keyword"},
#                             "c_sitename": {"type": "keyword"},
#                             "c_siteicp": {"type": "keyword"},
#                             "c_orgNature": {"type": "keyword"},
#                             "c_orgIndustry": {"type": "keyword"},
#                             "c_unit": {"type": "keyword"},
#                             "c_uniticp": {"type": "keyword"},
#                             "c_province": {"type": "keyword"},
#                             "c_city": {"type": "keyword"},
#                             "c_country": {"type": "keyword"},
#                             "c_addr": {"type": "keyword"},
#                             "c_serviceicp": {"type": "keyword"},
#                             "c_maintype": {"type": "keyword"},
#                             "c_source": {"type": "keyword"},
#                             "c_update": {"type": "keyword"},
#                             "c_credentialtype": {"type": "keyword"},
#                             "c_credentialnumber": {"type": "keyword"},
#                             "c_credential_untiltime": {"type": "keyword"},
#                             "c_credentialaddr": {"type": "keyword"},
#                             "c_day": {"type": "integer"}
#                         }
#                     }
#                 }
#             }
#         case "wa_annotator_db_t_domain_whois":
#             return {
#                 table_name: {
#                     "mappings": {
#                         "_meta": {
#                             "description": "域名 WHOIS 信息表"
#                         },
#                         "properties": {
#                             "c_uuid": {"type": "keyword"},
#                             "c_domain": {"type": "keyword"},
#                             "c_base_whois_server": {"type": "keyword"},
#                             "c_base_dnsserver": {"type": "keyword"},
#                             "c_base_stats": {"type": "keyword"},
#                             "c_base_update": {"type": "keyword"},
#                             "c_base_expire": {"type": "keyword"},
#                             "c_registrar_name": {"type": "keyword"},
#                             "c_registrar_phone": {"type": "keyword"},
#                             "c_registrar_mail": {"type": "keyword"},
#                             "c_registrar_site": {"type": "keyword"},
#                             "c_registrar_abusemail": {"type": "keyword"},
#                             "c_registrar_inna": {"type": "keyword"},
#                             "c_registrant_name": {"type": "keyword"},
#                             "c_registrant_country": {"type": "keyword"},
#                             "c_registrant_province": {"type": "keyword"},
#                             "c_registrant_city": {"type": "keyword"},
#                             "c_registrant_mail": {"type": "keyword"},
#                             "c_administrative_name": {"type": "keyword"},
#                             "c_administrative_country": {"type": "keyword"},
#                             "c_administrative_province": {"type": "keyword"},
#                             "c_technical_mail": {"type": "keyword"},
#                             "c_source": {"type": "keyword"},
#                             "c_reserve1": {"type": "keyword"},
#                             "c_reserve2": {"type": "keyword"},
#                             "c_reserve3": {"type": "keyword"},
#                             "c_reserve4": {"type": "keyword"},
#                             "c_reserve5": {"type": "keyword"},
#                             "c_day": {"type": "integer"}
#                         }
#                     }
#                 }
#             }
#         case "wa_annotator_db_t_domain_ioc":
#             return {
#                 table_name: {
#                     "mappings": {
#                         "_meta": {
#                             "description": "域名信誉信息表"
#                         },
#                         "properties": {
#                             "c_domain": {"type": "keyword"},
#                             "c_type": {"type": "keyword"},
#                             "c_level": {"type": "keyword"},
#                             "c_confidence": {"type": "keyword"},
#                             "c_phases": {"type": "keyword"},
#                             "c_compromise": {"type": "keyword"},
#                             "c_tags": {"type": "keyword"},
#                             "c_revoked": {"type": "keyword"},
#                             "c_modified": {"type": "keyword"},
#                             "c_validuntil": {"type": "keyword"},
#                             "c_source": {"type": "keyword"},
#                             "c_day": {"type": "integer"}
#                         }
#                     }
#                 }
#             }
#         case "wa_annotator_db_t_unit_baseinfo":
#             return {
#                 table_name: {
#                     "mappings": {
#                         "_meta": {
#                             "description": "单位基本信息"
#                         },
#                         "properties": {
#                             "c_uuid": {"type": "keyword"},
#                             "c_id": {"type": "keyword"},
#                             "c_name": {"type": "keyword"},
#                             "c_ename": {"type": "keyword"},
#                             "c_aname": {"type": "keyword"},
#                             "c_groupid": {"type": "keyword"},
#                             "c_groupname": {"type": "keyword"},
#                             "c_category": {"type": "keyword"},
#                             "c_industry": {"type": "keyword"},
#                             "c_registrar_mail": {"type": "keyword"},
#                             "c_registrar_site": {"type": "keyword"},
#                             "c_registrar_abusemail": {"type": "keyword"},
#                             "c_registrar_inna": {"type": "keyword"},
#                             "c_registrant_name": {"type": "keyword"},
#                             "c_registrant_country": {"type": "keyword"},
#                             "c_registrant_province": {"type": "keyword"},
#                             "c_registrant_city": {"type": "keyword"},
#                             "c_registrant_mail": {"type": "keyword"},
#                             "c_administrative_name": {"type": "keyword"},
#                             "c_administrative_country": {"type": "keyword"},
#                             "c_administrative_province": {"type": "keyword"},
#                             "c_technical_mail": {"type": "keyword"},
#                             "c_source": {"type": "keyword"},
#                             "c_reserve1": {"type": "keyword"},
#                             "c_reserve2": {"type": "keyword"},
#                             "c_reserve3": {"type": "keyword"},
#                             "c_reserve4": {"type": "keyword"},
#                             "c_reserve5": {"type": "keyword"},
#                             "c_day": {"type": "integer"}
#                         }
#                     }
#                 }
#             }
#         case "wa_annotator_db_t_unit_iplist":
#             return {
#                 table_name: {
#                     "mappings": {
#                         "_meta": {
#                             "description": "API 访问日志"
#                         },
#                         "properties": {
#                             "authenticated_entity": {"type": "object"},
#                             "client_ip": {"type": "keyword"},
#                             "consumer": {"type": "object"},
#                             "latencies": {"type": "object"},
#                             "request": {"type": "object"},
#                             "response": {"type": "object"},
#                             "route": {"type": "object"},
#                             "service": {"type": "object"},
#                             "started_at": {"type": "long"},
#                             "tries": {"type": "object"},
#                             "upstream_uri": {"type": "keyword"}
#                         }
#                     }
#                 }
#             }
#         case "wa_annotator_db_t_unit_domaincertlist":
#             return {
#                 table_name: {
#                     "mappings": {
#                         "_meta": {
#                             "description": "API 访问日志"
#                         },
#                         "properties": {
#                             "authenticated_entity": {"type": "object"},
#                             "client_ip": {"type": "keyword"},
#                             "consumer": {"type": "object"},
#                             "latencies": {"type": "object"},
#                             "request": {"type": "object"},
#                             "response": {"type": "object"},
#                             "route": {"type": "object"},
#                             "service": {"type": "object"},
#                             "started_at": {"type": "long"},
#                             "tries": {"type": "object"},
#                             "upstream_uri": {"type": "keyword"}
#                         }
#                     }
#                 }
#             }
#         case "wa_annotator_db_t_x509certinfo":
#             return {
#                 table_name: {
#                     "mappings": {
#                         "_meta": {
#                             "description": "API 访问日志"
#                         },
#                         "properties": {
#                             "authenticated_entity": {"type": "object"},
#                             "client_ip": {"type": "keyword"},
#                             "consumer": {"type": "object"},
#                             "latencies": {"type": "object"},
#                             "request": {"type": "object"},
#                             "response": {"type": "object"},
#                             "route": {"type": "object"},
#                             "service": {"type": "object"},
#                             "started_at": {"type": "long"},
#                             "tries": {"type": "object"},
#                             "upstream_uri": {"type": "keyword"}
#                         }
#                     }
#                 }
#             }
#         case "wa_annotator_db_t_app_baseinfo":
#             return {
#                 table_name: {
#                     "mappings": {
#                         "_meta": {
#                             "description": "API 访问日志"
#                         },
#                         "properties": {
#                             "authenticated_entity": {"type": "object"},
#                             "client_ip": {"type": "keyword"},
#                             "consumer": {"type": "object"},
#                             "latencies": {"type": "object"},
#                             "request": {"type": "object"},
#                             "response": {"type": "object"},
#                             "route": {"type": "object"},
#                             "service": {"type": "object"},
#                             "started_at": {"type": "long"},
#                             "tries": {"type": "object"},
#                             "upstream_uri": {"type": "keyword"}
#                         }
#                     }
#                 }
#             }
#         case "wa_annotator_db_t_app_sdomain_list":
#             return {
#                 table_name: {
#                     "mappings": {
#                         "_meta": {
#                             "description": "API 访问日志"
#                         },
#                         "properties": {
#                             "authenticated_entity": {"type": "object"},
#                             "client_ip": {"type": "keyword"},
#                             "consumer": {"type": "object"},
#                             "latencies": {"type": "object"},
#                             "request": {"type": "object"},
#                             "response": {"type": "object"},
#                             "route": {"type": "object"},
#                             "service": {"type": "object"},
#                             "started_at": {"type": "long"},
#                             "tries": {"type": "object"},
#                             "upstream_uri": {"type": "keyword"}
#                         }
#                     }
#                 }
#             }
#         case "wa_annotator_db_t_app_sip_list":
#             return {
#                 table_name: {
#                     "mappings": {
#                         "_meta": {
#                             "description": "API 访问日志"
#                         },
#                         "properties": {
#                             "authenticated_entity": {"type": "object"},
#                             "client_ip": {"type": "keyword"},
#                             "consumer": {"type": "object"},
#                             "latencies": {"type": "object"},
#                             "request": {"type": "object"},
#                             "response": {"type": "object"},
#                             "route": {"type": "object"},
#                             "service": {"type": "object"},
#                             "started_at": {"type": "long"},
#                             "tries": {"type": "object"},
#                             "upstream_uri": {"type": "keyword"}
#                         }
#                     }
#                 }
#             }
#         case "wa_annotator_db_t_app_cert_list":
#             return {
#                 table_name: {
#                     "mappings": {
#                         "_meta": {
#                             "description": "API 访问日志"
#                         },
#                         "properties": {
#                             "authenticated_entity": {"type": "object"},
#                             "client_ip": {"type": "keyword"},
#                             "consumer": {"type": "object"},
#                             "latencies": {"type": "object"},
#                             "request": {"type": "object"},
#                             "response": {"type": "object"},
#                             "route": {"type": "object"},
#                             "service": {"type": "object"},
#                             "started_at": {"type": "long"},
#                             "tries": {"type": "object"},
#                             "upstream_uri": {"type": "keyword"}
#                         }
#                     }
#                 }
#             }
#         case "wa_annotator_db_t_app_userid_list":
#             return {
#                 table_name: {
#                     "mappings": {
#                         "_meta": {
#                             "description": "API 访问日志"
#                         },
#                         "properties": {
#                             "authenticated_entity": {"type": "object"},
#                             "client_ip": {"type": "keyword"},
#                             "consumer": {"type": "object"},
#                             "latencies": {"type": "object"},
#                             "request": {"type": "object"},
#                             "response": {"type": "object"},
#                             "route": {"type": "object"},
#                             "service": {"type": "object"},
#                             "started_at": {"type": "long"},
#                             "tries": {"type": "object"},
#                             "upstream_uri": {"type": "keyword"}
#                         }
#                     }
#                 }
#             }
#         case _:
#             raise ValueError(f"Unknown table: {table_name}")
#

# get tables
def get_es_index(conf: DatasourceConf):
    # es_client = get_es_connect(conf)
    # indices = es_client.cat.indices(format="json")
    indices = get_mock_indices()
    res = []
    if indices is not None:
        for idx in indices:
            index_name = idx.get('index')
            desc = ''
            # get mapping
            # mapping = es_client.indices.get_mapping(index=index_name)
            mapping = get_mock_mapping(index_name)
            mappings = mapping.get(index_name).get("mappings")
            if mappings.get('_meta'):
                desc = mappings.get('_meta').get('description') or ''
            res.append((index_name, desc))
    return res


# get fields
def get_es_fields(conf: DatasourceConf, table_name: str):
    # es_client = get_es_connect(conf)
    index_name = table_name
    # mapping = es_client.indices.get_mapping(index=index_name)
    # properties = mapping.get(index_name).get("mappings").get("properties")
    mapping = get_mock_mapping(index_name)
    properties = mapping.get(table_name).get("mappings").get("properties")

    res = []
    if properties is not None:
        for field, config in properties.items():
            field_type = config.get("type")
            desc = ''
            if config.get("_meta"):
                desc = config.get("_meta").get('description')

            if field_type:
                res.append((field, field_type, desc))
            else:
                # object、nested...
                res.append((field, ','.join(list(config.keys())), desc))
    return res


# def get_es_data(conf: DatasourceConf, sql: str, table_name: str):
#     r = requests.post(f"{conf.host}/_sql/translate", json={"query": sql})
#     if r.json().get('error'):
#         print(json.dumps(r.json()))
#
#     es_client = get_es_connect(conf)
#     response = es_client.search(
#         index=table_name,
#         body=json.dumps(r.json())
#     )
#
#     # print(response)
#     fields = get_es_fields(conf, table_name)
#     res = []
#     for hit in response.get('hits').get('hits'):
#         item = []
#         if 'fields' in hit:
#             result = hit.get('fields')  # {'title': ['Python'], 'age': [30]}
#             for field in fields:
#                 v = result.get(field[0])
#                 item.append(v[0]) if v else item.append(None)
#             res.append(tuple(item))
#             # print(hit['fields']['title'][0])
#         # elif '_source' in hit:
#         #     print(hit.get('_source'))
#     return res, fields


def get_es_data_by_http(conf: DatasourceConf, sql: str):
    url = conf.host
    while url.endswith('/'):
        url = url[:-1]

    host = f'{url}/_sql?format=json'

    response = requests.post(
        host,
        data=json.dumps({"timeout": 60, "query": sql}),
        headers=get_es_auth(conf),
        timeout=conf.timeout,
        verify=False
    )

    # print(response.json())
    res = response.json()
    if res.get('error'):
        raise SingleMessageError(json.dumps(res))
    fields = res.get('columns')
    result = res.get('rows')
    return result, fields


# 测试方法
if __name__ == '__main__':
    print(get_es_index(None))
    print(get_es_fields(None, "wa_annotator_db_t_app_userid_list"))
