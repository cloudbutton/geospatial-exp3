"""

AUTHOR: Juanjo

DATE: 11/02/2019

"""

import requests

from bs4 import BeautifulSoup

# 1.
#
# url = 'http://centrodedescargas.cnig.es/CentroDescargas/catalogo.do'
# querystring = {"Serie": 'LIDAR'}
# headers = {}
# response = requests.get(url, headers=headers, params=querystring)
#
# if response.status_code != 200:
#     print('****************ERROR: ' + response.text)
# data = response.text
# cookies = response.cookies
# print(data)
# for c in cookies:
#     print(c.name + '=' + c.value)


# 2.
# url = 'http://centrodedescargas.cnig.es/CentroDescargas/buscadorOL'
# headers = {
#     'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
# }
# data = {
#     'codSerieBA': 'LIDA2',
#     'activaPunto': 'N'
# }
# response = requests.post(url, data=data)
# print(response.text)
# Host: centrodedescargas.cnig.es
# Origin: http: // centrodedescargas.cnig.es
# Referer: http: // centrodedescargas.cnig.es / CentroDescargas / catalogo.do?Serie = LIDAR


# 3.
# url = 'http://centrodedescargas.cnig.es/CentroDescargas/resultadosSeries'
# # headers = {
# #     'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
# # }
# data = {
#     'todaEsp': 'N',
#     'series': 'LIDA2',
#     'codProvAv': '30',
#     'tipoBusqueda': 'AV'
# }
# response = requests.post(url, data=data)
# print(response.text)
# # TODO: Recuperar campo oculto "numResultados"


# 4. LISTAR LOS IDs DE LOS DOCUMENTOS (BUENO)
# url = 'http://centrodedescargas.cnig.es/CentroDescargas/resultadosArchivos'
# next_page = 1
# doc_list = []
# while next_page:
#     data = {
#         'numPagina': next_page,
#         'codSerie': 'LIDA2',
#         'series': 'LIDA2',
#         'codProvAv': '30',
#         'todaEsp': 'N',
#         'tipoBusqueda': 'AV',
#     }
#     response = requests.post(url, data=data)
#     if response.status_code != 200:
#         print(response.text)
#         break
#     data = response.text
#     soup = BeautifulSoup(data, 'lxml')
#     next_link = soup.find("a", {"title": "Siguiente"})
#     next_page = next_page + 1 if next_link else None
#     file_list_div = soup.find("div", {"id": "blqListaArchivos"})
#     file_list_tb = file_list_div.find('table').find('tbody')
#     trs = file_list_tb.find_all('tr')
#     for tr in trs:
#         ihidden = tr.find_all("input", {'type': 'hidden'})
#         file_link_id = None
#         for input in ihidden:
#             if input['id'].startswith('secGeo_'):
#                 file_link_id = input['value']
#         file_name = tr.find('td', {'data-th': 'Nombre'}).text
#         doc_list.append((file_name, file_link_id))
# print("Número de docs: {}".format(len(doc_list)))
# with open('lidar_doc_ids.txt', 'w') as lidar_docs_file:
#     for doc in doc_list:
#         lidar_docs_file.write('{},{}\n'.format(doc[0], doc[1]))


# if table is None:
#     logger.error('Unable to find the <table> node for sensor {}'.format(self.sensor_name))
#     raise ParseResponseError('Unable to find the <table> node for sensor {}'.format(self.sensor_name))
# trs = table.find_all('tr')
# if len(trs) < 3:
#     logger.error('Unable to find the <tr> node for sensor {}'.format(self.sensor_name))
#     raise ParseResponseError('Unable to find the <tr> node for sensor {}'.format(self.sensor_name))
# td = trs[2].find("td", {"class", "celda10"})
# if td is None:
#     logger.error('Unable to find the <td> node for sensor {}'.format(self.sensor_name))
#     raise ParseResponseError('Unable to find the <td> node for sensor {}'.format(self.sensor_name))
# value = td.text
# TODO: Recuperar página actual. Comprobar si es la última. Si no, obtener los resultados de la página siguiente
# TODO: Recuperar cada uno de los documentos del listados


# 5.
# url = 'http://centrodedescargas.cnig.es/CentroDescargas/initDescargaDir'
# data = {
#     'secuencial': '9640119'
# }
# response = requests.post(url, data=data)
# print(response.json())


# 6.
# url = 'http://centrodedescargas.cnig.es/CentroDescargas/loadLicsDescDir'
# data = {
#     'secuencial': '9640119'
# }
# response = requests.post(url, data=data)
# print(response.content)


# 7.
# url = 'http://centrodedescargas.cnig.es/CentroDescargas/descargaDir'
# data = {
#     'secuencialDescDir': '9640119',
#     'aceptCodsLicsDD_0': '15'
# }
# response = requests.post(url, data=data)
# print(response.content)


# 8.
url = 'http://centrodedescargas.cnig.es/CentroDescargas/descargaDir'
data = {
    'codSerieMD': 'LIDA2',
    'codSerieSel': 'LIDA2'
}
with open('lidar_doc_ids.txt', 'r') as f:
    flines = f.readlines()
    for f_line in flines:
        file_name, sec_desc_dir_la = f_line.rstrip().split(',')
        data['secDescDirLA'] = sec_desc_dir_la
        response = requests.post(url, data=data)
        with open('lidar_files/' + file_name, 'wb') as lidar_file:
            lidar_file.write(response.content)
