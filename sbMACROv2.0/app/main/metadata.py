import os
import sciencebasepy
from xml.dom import minidom
from urllib.request import urlopen
from nltk.corpus import stopwords
from pattern.en import singularize


my_root = os.path.dirname(os.path.abspath(__file__))
file_write_path = os.path.join(my_root, 'templates/static/tag_contents/')

chars_to_exclude = ",:;()&-.'`=<>/0123456789"

sb = sciencebasepy.SbSession()

casc_id = {
    'Alaska':        '4f831626e4b0e84f6086809b',
    'National':      '5050cb0ee4b0be20bb30eac0',
    'North Central': '4f83509de4b0e84f60868124',
    'Northeast':     '4f8c648de4b0546c0c397b43',
    'Northwest':     '4f8c64d2e4b0546c0c397b46',
    'Pacific':       '4f8c650ae4b0546c0c397b48',
    'South Central': '4f8c652fe4b0546c0c397b4a',
    'Southeast':     '4f8c6557e4b0546c0c397b4c',
    'Southwest':     '4f8c6580e4b0546c0c397b4e'
}

def get_item_ids(casc_name):
    
    print('Collecting item ids...')
    
    # root_ids will start with fiscal year ids
    root_ids = sb.get_child_ids(casc_id[casc_name])

    # id_level 1 => projects
    # id_level 2 => approved datasets
    # id_level 3 => items (approved items)

    id_level = 1
    child_id_lists = [] # a list of lists
    child_ids = [] # a list of strings

    proj_ids = []
    aprvd_ids = []
    item_ids = []

    while id_level < 4:

        for child_id in root_ids:
            try:
                result = sb.get_child_ids(child_id)
                if result:
                    child_id_lists.append(result)       
            except:
                pass

    #     # save child_id_lists to relevant list
    #     if id_level == 1:
    #         proj_ids = child_id_lists
    #     elif id_level == 2:
    #         aprvd_ids = child_id_lists
    #     else:
    #         item_ids = child_id_lists

        # expand list of lists into list of strings
        for id_list in child_id_lists:
            for child_id in id_list:
                child_ids.append(child_id)

        # save child_id_lists to relevant list
        if id_level == 1:
            proj_ids = child_ids
        elif id_level == 2:
            aprvd_ids = child_ids
        else:
            item_ids = child_ids

        # update variables and objects
        root_ids = child_ids
        child_ids = []
        child_id_lists = []
        id_level += 1
        
    print('{} item ids collected\n'.format(len(item_ids)))
        
    return item_ids

def get_metadata_urls(item_ids):
    
    print('Collecting urls...')
    
    metadata_urls = []

    for item_id in item_ids:
        item_json = sb.get_item(item_id)
        item_info = sb.get_item_file_info(item_json)

        for info in item_info:
            if 'xml' in info['contentType'] and 'xml' in info['name']:
                metadata_urls.append(info['url'])
                
    print('{} urls collected\n'.format(len(metadata_urls)))
                
    return metadata_urls

def applyNLP(metadata, chars_to_exclude, stop_words):
    print('Processing metadata')
    
    processed_list = []

    for line in metadata:
        for ch in chars_to_exclude:
            if ch in line:
                line = line.replace(ch, ' ')
        words = line.split()
        for w in [word for word in words if word.lower() not in stop_words]:
            if len(w) > 2:
                w = singularize(w) # collapse plurals into singulars
                processed_list.append(w.lower())
            
    return processed_list

def collectData(data_nodes):
    
    def getData(data_list, l, rel):
        if data_list.childNodes:
            for data in data_list.childNodes:
                if data.childNodes:
                    children.append(data.nodeName)
                    getData(data, l, children)
                else:
                    l.append(data)
    
    l = []
    children = []
    for data_list in data_nodes:
        getData(data_list, l, children)
        
    return l, children

def processNode(node, children, nodeNames, data):
    
    global tabValue
    
    tabValue = 0
    
    def processParentNode(node, children):
        global tabValue
        if node.parentNode.nodeName in children:
            processParentNode(node.parentNode, children)
        
        nodeName = node.parentNode.nodeName
        if nodeName not in nodeNames:
#             print(' '*tabValue, end = '')
#             print(nodeName)
            nodeNames.add(nodeName)
            
        tabValue += 1
    
    if node.nodeValue and node.nodeValue.split():
        processParentNode(node, children)
#         print(' '*tabValue, end = '')
        if node.parentNode.nodeName[-2:].lower() == 'kt':
            pass
#             print('[' + node.nodeValue.upper() + ']')
        else:
            data.append(node.nodeValue)
#             print(node.nodeValue)

def get_data(metadata_urls, tag_header, tag_to_search, chars_to_exclude, stop_words):
    
    print('Getting metadata...')
    
    data = []
    
    for url in metadata_urls:
        try:
            xml_content = minidom.parse(urlopen(url))

            data_nodes = xml_content.getElementsByTagName(tag_to_search)

            nodes, children = collectData(data_nodes)
            nodeNames = set()

            for node in nodes:
                processNode(node, children, nodeNames, data)
        except:
            pass

    metadata = [tag_header] + applyNLP(data, chars_to_exclude, stop_words)
            
    return metadata

def write_metadata(casc_name, tag_to_search, metadata_urls, stop_words):

    # check that required file does not already exist
    current_files = os.listdir(file_write_path)
    filename = casc_name + '_' + tag_to_search.replace(':', '_') + '.csv'
    if filename not in current_files:
        # create casc metadata file
        print('CASC: ' + casc_name)

        tag_header = '<' + tag_to_search + '>'

        metadata = get_data(metadata_urls, tag_header, tag_to_search, chars_to_exclude, stop_words)

        # write data to file
        print('Writing tag contents to ' + filename)
        with open(file_write_path + filename, 'w') as file:
            for data in metadata:
                file.write(data.replace(',', '') + '\n')
        print('-----------------')
