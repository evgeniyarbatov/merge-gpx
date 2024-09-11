import sys

import xml.dom.minidom
import xml.etree.ElementTree as ET

from datetime import datetime

GPX_NS = '{http://www.topografix.com/GPX/1/1}'
EXT_NS = '{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}'

def get_time(timestamp_str):
    return datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')

def parse_gpx(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = []
    
    for trkpt in root.findall(f".//{GPX_NS}trkpt"):
        time = trkpt.find(f"{GPX_NS}time")
        time = get_time(time.text)

        lat = float(trkpt.get('lat'))
        lon = float(trkpt.get('lon'))
        
        ele = trkpt.find(f"{GPX_NS}ele")
        ele_value = float(ele.text) if ele is not None else None

        extensions = trkpt.find(f"{GPX_NS}extensions")    
        cadence_value, power_value, hr_value = None, None, None
        
        if extensions is not None:
            power = extensions.find(f"{GPX_NS}power")
            power_value = int(power.text) if power is not None else None

            tpx = extensions.find(f"{EXT_NS}TrackPointExtension")
            if tpx is not None: 
                cadence = tpx.find(f"{EXT_NS}cad")
                cadence_value = int(cadence.text) if cadence is not None else None
        
                hr = tpx.find(f"{EXT_NS}hr")
                hr_value = int(hr.text) if hr is not None else None

        data.append({
            'time': time,
            'lat': lat,
            'lon': lon,
            'ele': ele_value,
            'cad': cadence_value,
            'power': power_value,
            'hr': hr_value,
        })
        
    return data

def merge(phone_gpx, watch_gpx):
    phone_data = parse_gpx(phone_gpx)
    watch_data = parse_gpx(watch_gpx)
    
    merged_data = []
    i, j = 0, 0
    
    while i < len(watch_data) and j < len(phone_data):        
        if watch_data[i]['time'] == phone_data[j]['time']:
            merged_data.append({
                'time': watch_data[i]['time'],
                'lat': phone_data[j]['lat'],
                'lon': phone_data[j]['lon'],
                'ele': phone_data[j]['ele'],
                'hr': watch_data[i]['hr'],
                'cad': watch_data[i]['cad'],
                'power': watch_data[i]['power'],
            })
            i += 1
            j += 1
        elif watch_data[i]['time'] < phone_data[j]['time']:
            i += 1
        else:
            j += 1
    
    return merged_data

def save(merged_data, output_file):
    namespaces = {
        'gpxtpx': 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1'
    }

    for prefix, uri in namespaces.items():
        ET.register_namespace(prefix, uri)

    gpx = ET.Element('gpx', {
        'creator': 'https://github.com/evgeniyarbatov/merge-gpx',
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xsi:schemaLocation': 'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd',
        'version': '1.1',
        'xmlns': 'http://www.topografix.com/GPX/1/1'
    })

    trk = ET.SubElement(gpx, "trk")
    trkseg = ET.SubElement(trk, "trkseg")

    for point in merged_data:
        trkpt = ET.SubElement(trkseg, 'trkpt', lat=str(point['lat']), lon=str(point['lon']))
        ET.SubElement(trkpt, 'ele').text = str(point['ele'])
        ET.SubElement(trkpt, 'time').text = point['time'].strftime('%Y-%m-%dT%H:%M:%SZ')
        
        extensions = ET.SubElement(trkpt, 'extensions')
        ET.SubElement(extensions, 'power').text = str(point['power'])
        
        tpe = ET.SubElement(extensions, '{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}TrackPointExtension')
        
        ET.SubElement(tpe, '{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}hr').text = str(point['hr']) 
        ET.SubElement(tpe, '{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}cad').text = str(point['cad']) 

    with open(output_file, "w") as f:
        gpx = xml.dom.minidom.parseString(
            ET.tostring(gpx, encoding="unicode")
        ).toprettyxml(
            indent='  '
        )
        
        f.write(gpx)

def main(
    phone_gpx, 
    watch_gpx, 
    output_gpx,
):
    merged_data = merge(phone_gpx, watch_gpx)
    save(merged_data, output_gpx)

if __name__ == "__main__":
    main(*sys.argv[1:])
