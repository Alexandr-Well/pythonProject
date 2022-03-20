import shutil
from pandas import read_excel, DataFrame
import os
from typing import List, Dict

markers: Dict[str, tuple] = {'blu': (50, 65), 'ltgrn': (65, 75), 'grn': (75, 85), 'ylw': (85, 95), 'org': (95, 105),
                           'red': (105, 120), 'brn': (120, 150)}
sorted_point: Dict[str, list] = {'blu': [], 'ltgrn': [], 'grn': [], 'ylw': [], 'org': [],
                                                         'red': [],
                                                         'brn': []}

begin = '<?xml version="1.0" encoding="utf-8" ?>\n' \
             '<kml xmlns="http://www.opengis.net/kml/2.2">\n' \
             '<Document id="root_doc">\n' \
             '<Schema name="File_2088" id="File_2088">\n' \
             '  <SimpleField name = "tessellate" type = "int" > </SimpleField >\n' \
             '</Schema > \n' \
             '  <Style id="blu">\n' \
             '    <IconStyle>\n' \
             '      <Icon>\n' \
             '        <href>blu.png</href>\n' \
             '      </Icon>\n' \
             '    </IconStyle>\n' \
             '  </Style>\n' \
             '  <Style id="brn">\n' \
             '    <IconStyle>\n' \
             '      <Icon>\n' \
             '        <href>brn.png</href>\n' \
             '      </Icon>\n' \
             '    </IconStyle>\n' \
             '  </Style>\n' \
             '  <Style id="grn">\n' \
             '    <IconStyle>\n' \
             '      <Icon>\n' \
             '        <href>grn.png</href>\n' \
             '      </Icon>\n' \
             '    </IconStyle>\n' \
             '  </Style>\n' \
             '  <Style id="ltgrn">\n' \
             '    <IconStyle>\n' \
             '      <Icon>\n' \
             '        <href>ltgrn.png</href>\n' \
             '      </Icon>\n' \
             '    </IconStyle>\n' \
             '  </Style>\n' \
             '  <Style id="org">\n' \
             '    <IconStyle>\n' \
             '      <Icon>\n' \
             '        <href>org.png</href>\n' \
             '      </Icon>\n' \
             '    </IconStyle>\n' \
             '  </Style>\n' \
             '  <Style id="red">\n' \
             '    <IconStyle>\n' \
             '      <Icon>\n' \
             '        <href>red.png</href>\n' \
             '      </Icon>\n' \
             '    </IconStyle>\n' \
             '  </Style>\n' \
             '  <Style id="ylw">\n' \
             '    <IconStyle>\n' \
             '      <Icon>\n' \
             '        <href>ylw.png</href>\n' \
             '      </Icon>\n' \
             '    </IconStyle>\n' \
             '  </Style>\n'


def get_folder_kml(var1: int, var2: int) -> str:
    """
    :param var1: int(from markers[key][value]):
    :param var2: int(from markers[key][value])
    :return:
    """
    return '<Folder>\n' \
           f'<name><![CDATA[-{var2} to -{var1}]]></name>\n' \
           '<visibility>0</visibility>\n' \
           '<open>0</open>'


def get_folder_end_kml(key: str) -> str:
    """
    :param key: str (sorted_point key)
    :return: str
    """
    return '    <Icon>\n' \
           f'        <href>{key}.png</href>\n' \
           '    </Icon>\n' \
           '</Folder>'


def get_placemark_kml(key: str, item: List) -> str:
    """
    :param key: str (sorted_point key)
    :param item: array (list, str, iterable)
    :return: str
    """
    return '\n' \
           '  <Placemark>\n' \
           f'     <description>Longitude: {item[2]}br&gt;' \
           f'Latitude: {item[1]}br&gt; ' \
           f'Time: {item[3]}&lt;br&gt;' \
           f'RS_RP: {item[4]}&lt;br&gt;</description>\n' \
           f'    <styleUrl>#{key}</styleUrl>\n' \
           '    <ExtendedData><SchemaData schemaUrl="#_105_to__95">\n' \
           '    <SimpleData name="altitudeMode">relativeToGround</SimpleData>\n' \
           '    </SchemaData></ExtendedData>\n' \
           f'      <Point><coordinates>{item[2]},{item[1]}</coordinates></Point>\n' \
           '  </Placemark>'


def make_file_clear_system(dir_path: str, file_name: str, user: str) -> str:
    """
    function make kmz file and destroy temp files
    :param dir_path: str (path to temp directory)
    :param file_name: str
    :param user: str
    :return: str
    """
    for file in os.listdir(os.path.join("static", "lte")):
        shutil.copy(os.path.join("static", "lte", file), dir_path)
    shutil.make_archive(dir_path, 'zip', dir_path)
    os.rename(f'{dir_path}.zip', dir_path + ".kmz")
    for file in os.listdir(dir_path):
        if not file.endswith('.kmz'):
            os.remove(os.path.join(dir_path, file))
    return os.path.join(user, file_name[:-5])


def kml_file_maker(dir_path: str, file_name: str, name: str, user: str, sorted_point: dict, markers: dict) -> str:
    """
    function create file kml
    :param dir_path: str (path to temp directory)
    :param file_name: str
    :param markers: dict
    :param name: str
    :param sorted_point: dict
    :param user: str
    :return: str (path)
    """
    with open(f'{name}.kml', 'w') as file:
        file.write(begin)
        for key in sorted_point:
            file.write(get_folder_kml(markers[key][0], markers[key][1]))
            file.write('\n')
            for item in sorted_point[key]:
                file.write(get_placemark_kml(key, item))
                file.write('\n')
            file.write(get_folder_end_kml(key))
            file.write('\n')
        file.write('\n</Document>\n</kml>')
    return make_file_clear_system(dir_path, file_name, user)


def xlsx_get_file(file: str, compression: float, user: str, file_name: str) -> str:
    """
    function got file, compression, user, file_name and calculate (depend on compression calculate values)
    data in dataframe pandas, also create temp directory
    :param file: str (path)
    :param compression: float
    :param user: str
    :param file_name: str
    :return: str (path)
    """

    distance = int(compression) * 0.000035
    dir_path = os.path.join("temp", user, file_name[:-5])
    name = os.path.join(dir_path, file_name[:-5])
    os.makedirs(dir_path)
    excel_data = read_excel(file)
    data = DataFrame(excel_data, columns=['UniqueId', 'Lat', 'Lon', 'Time', 'RSRP'])
    current_cords: List[str] = []
    for index, point in enumerate(data.values):
        if not current_cords:
            current_cords = [point[1], point[2]]
            for key in markers:
                if abs(markers[key][0]) <= abs(int(point[4])) < abs(markers[key][1]):
                    sorted_point[key].append(point)
                    break
        else:
            current_distance = (((float(current_cords[0]) - float(point[1])) ** 2) + (
                    ((float(current_cords[1]) - float(point[2])) * 0.61) ** 2)) ** 0.5
            if current_distance >= distance:
                current_cords = [point[1], point[2]]
                for key in markers:
                    if abs(markers[key][0]) <= abs(int(point[4])) < abs(markers[key][1]):
                        sorted_point[key].append(point)
                        break
            else:
                continue

    return kml_file_maker(dir_path, file_name, name, user, sorted_point, markers)


def remove_temp_dir(path: str) -> None:
    """
    function destroy temp directory
    :param path: str
    :return: None
    """
    shutil.rmtree(os.path.join('temp', path, ''))


if __name__ == "__main__":
    pass
