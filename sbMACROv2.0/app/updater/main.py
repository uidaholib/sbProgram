"""Main module from which all Science Base data gathering branches."""
import os
import re
import time
import json
import pickle
import pandas as pd
import sciencebasepy
import app.updater.gl
from datetime import datetime
from app.updater import db_save
from app.updater import projects
from app.updater import fiscal_years
from difflib import SequenceMatcher
from textblob import TextBlob
from textblob.np_extractors import ConllExtractor
from textblob.np_extractors import FastNPExtractor

sb = sciencebasepy.SbSession()
chars_to_exclude = ",:;()&-–.’'`=<>/"

file_path = os.getcwd() + '/app/main/templates/static/'
conll = ConllExtractor()
fastext = FastNPExtractor()


def load_details_from_file(file_location):

    # a list of dicts
    details = []

    try:
        with open(file_location, 'rb') as details_file:
            details = pickle.load(details_file)
    except Exception as e:
        print('error: ' + str(e))

    return details


def update_graphs():

    cascs = ['Alaska', 'North Central',
             'Northeast', 'Northwest',
             'Pacific', 'South Central',
             'Southeast', 'Southwest', 'National']

    processed = set()

    start = time.time()
    for casc1 in cascs:
        for casc2 in cascs:
            if casc1 == casc2 or casc2 in processed:
                continue
            create_graph(casc1, casc2)

        processed.add(casc1)
    print('Graph updates completed!')

    end = time.time()

    duration = end - start
    mins = int(duration/60)
    secs = duration % 60

    print('\nProject comparison graphs updated \
         in {} minutes and {} seconds'.format(mins, secs))


def create_graph(casc1, casc2):

    proj_details1 = {}
    proj_details2 = {}
    graph = {'nodes': [], 'links': [], 'num_sources': 0, 'num_targets': 0}

    # destination file
    graph_name = casc1.lower().replace(' ', '_') + '_' + casc2.lower().replace(' ', '_') + '_' + 'proj_graph'
    print('Building {}...'.format(graph_name))
    graph_file_name = file_path + 'project_graphs/' + graph_name + '.json'

    # source files
    with open(file_path + 'proj_dict.json') as input_file:
        proj_dict = json.load(input_file)

    with open(file_path + 'item_dict.json') as input_file:
        item_dict = json.load(input_file)

    with open(file_path + 'proj_dataset_matches.json') as input_file:
        proj_dataset_matches = json.load(input_file)

    # build project details
    for proj_id in proj_dict:
        if proj_dict[proj_id]['casc'] == casc1 + ' CASC':
            proj_details1[proj_id] = {'title': proj_dict[proj_id]['title'], 'summary': proj_dict[proj_id]['summary'], 'casc': proj_dict[proj_id]['casc'], 'fy': proj_dict[proj_id]['fy'], 'url': proj_dict[proj_id]['url']}
            graph['num_sources'] += 1
        if proj_dict[proj_id]['casc'] == casc2 + ' CASC':
            proj_details2[proj_id] = {'title': proj_dict[proj_id]['title'], 'summary': proj_dict[proj_id]['summary'], 'casc': proj_dict[proj_id]['casc'], 'fy': proj_dict[proj_id]['fy'], 'url': proj_dict[proj_id]['url']}
            graph['num_targets'] += 1

    print('{} sources, {} targets'.format(graph['num_sources'],
          graph['num_targets']))

    # build node details
    print('collecting node details...')
    n = 0
    for proj_id in proj_details1:
        name = proj_details1[proj_id]['title']
        casc = proj_details1[proj_id]['casc']
        fy = proj_details1[proj_id]['fy']
        url = proj_details1[proj_id]['url']
        summary = proj_details1[proj_id]['summary']
        num_items = proj_dataset_matches[proj_id]['num_items']
        proj_items = proj_dataset_matches[proj_id]['proj_items']
        items = {}
        for item_id in proj_items:
            items[item_id] = {'title': item_dict[item_id]['title'],
                              'url': item_dict[item_id]['url']}
        graph['nodes'].append({'node': n, 'name': name, 'casc': casc,
                               'fy': fy, 'url': url, 'num_items': num_items,
                               'items': items, 'summary': summary})
        proj_details1[proj_id]['node'] = n
        n += 1
    for proj_id in proj_details2:
        name = proj_details2[proj_id]['title']
        casc = proj_details2[proj_id]['casc']
        fy = proj_details2[proj_id]['fy']
        url = proj_details2[proj_id]['url']
        summary = proj_details2[proj_id]['summary']
        num_items = proj_dataset_matches[proj_id]['num_items']
        proj_items = proj_dataset_matches[proj_id]['proj_items']
        items = {}
        for item_id in proj_items:
            items[item_id] = {'title': item_dict[item_id]['title'],
                              'url': item_dict[item_id]['url']}
        graph['nodes'].append({'node': n, 'name': name, 'casc': casc,
                               'fy': fy, 'url': url,
                               'num_items': num_items,
                               'items': items, 'summary': summary
                               })
        proj_details2[proj_id]['node'] = n
        n += 1

    # create graph links
    graph_links = create_graph_links(proj_details1, proj_details2)

    # build link details
    print('compiling link details...')
    scale_factor = 100
    for link in graph_links:
        source = link['source']
        target = link['target']
        value = link['value'] * scale_factor
        matches = link['matches']
        graph['links'].append({'source': source,
                               'target': target, 'value': value,
                               'matches': matches})

    # write graph to file
    with open(graph_file_name, 'w') as output_file:
        json.dump(graph, output_file)
    print('{} written to file\n'.format(graph_name))


def create_graph_links(proj_details1, proj_details2):
    graph_links = []

    for id1 in proj_details1:
        node1 = proj_details1[id1]['node']
        text1 = proj_details1[id1]['summary']
        # remove odd characters
        for ch in chars_to_exclude:
            if ch in text1:
                text1 = text1.replace(ch, ' ')
        # exclude single-letter words
        text1 = ' '.join([word for word in text1.split() if len(word) > 1])
        for id2 in proj_details2:
            node2 = proj_details2[id2]['node']
            text2 = proj_details2[id2]['summary']
            # remove odd characters
            for ch in chars_to_exclude:
                if ch in text2:
                    text2 = text2.replace(ch, ' ')
            # exclude single-letter words
            text2 = ' '.join([word for word in text2.split() if len(word) > 1])
            sim, matches = get_similarity(text1, text2)
            graph_links.append({'source': node1, 'target': node2,
                                'value': sim, 'matches': matches})

    return graph_links


def get_similarity(text1, text2):

    sim_threshold = 0.5

    # grab the general topics/ideas of interest from the project summary
    text1_blob1 = TextBlob(text1, np_extractor=conll)
    text1_blob2 = TextBlob(text1, np_extractor=fastext)
    text1_phrases = set(text1_blob1.noun_phrases + text1_blob2.noun_phrases)

    # grab the general topics/ideas of interest from the item summary
    text2_blob1 = TextBlob(text2, np_extractor=conll)
    text2_blob2 = TextBlob(text2, np_extractor=fastext)
    text2_phrases = set(text2_blob1.noun_phrases + text2_blob2.noun_phrases)

    # compute and store item similarity with project
    matches = []
    similarities = []

    for i in text2_phrases:
        for p in text1_phrases:
            match = SequenceMatcher(None, i, p)
            similarity = match.ratio()
            if similarity > sim_threshold:
                matches.append(similarity)
                similarities.append([i, p, round(similarity, 4)])

    match_sum = sum(matches)
    match_len = len(matches)
    phrases_len = len(text1_phrases)
    if match_len == 0:
        avg_sim = 0
        weighted_sim = 0
    else:
        inv_match_ratio = phrases_len/match_len
        scaled_inv_ratio = rescale(inv_match_ratio, 0, phrases_len, 0, 2)
        weight = 0.5**(scaled_inv_ratio)

        avg_sim = round(match_sum/match_len, 4)
        weighted_sim = round(weight * avg_sim, 4)

    return weighted_sim, similarities


def rescale(num, old_min, old_max, new_min, new_max):
    """
    Rescale num from range [old_min, old_max] to range [new_min, new_max]
    """
    old_range = old_max - old_min
    new_range = new_max - new_min
    new_val = new_min + (((num - old_min) * new_range)/old_range)

    return new_val


def update_search_table(app, source):

    # load or collect details
    # if source == 'file':
    #     items_file_path = file_path + 'master_details_full.pkl'
    #     projs_file_path = file_path + 'proj_dict.pkl'
    #     item_details = load_details_from_file(items_file_path)
    #     proj_details = load_details_from_file(projs_file_path)
    # elif source == 'sciencebase':
    item_details, proj_details = get_details(source)

    # write details to database
    db_save.save_master_details(app, item_details)
    db_save.save_project_details(app, proj_details)

    print('===== Master table update completed =====')


def get_details(source):

    msg = 'Collecting details'
    msg += '...' if source == 'file' else ' from sciencebase...'

    print(msg)

    casc_ids = {
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

    proj_details_list = []
    item_details_list = []

    # create empty dictionaries to save sb json files
    # (to avoid having to go back to sciencebase for trivial updates)
    proj_jsons = {}
    item_jsons = {}

    if source == 'file':
        # read from files instead - no need
        # to save from sciencebase along the way
        with open(file_path + 'proj_jsons.json') as input_file:
            proj_jsons = json.load(input_file)
        with open(file_path + 'item_jsons.json') as input_file:
            item_jsons = json.load(input_file)

    pause_duration = 2  # duration in seconds

    start = time.time()
    total_items = process_casc_ids(source, casc_ids,
                                   proj_details_list, item_details_list,
                                   proj_jsons, item_jsons, pause_duration)
    end = time.time()

    duration = end - start
    mins = int(duration/60)
    secs = duration % 60

    print('\n===== {} total items collected in {} minutes and {} seconds =====\n\n'.format(total_items, mins, secs))

    # ========== Save data ==========
    print('===== Saving data =====')

    # build and save dictionary of project and item details
    html_tags = re.compile('<.*?>')
    print('Building proj_dict...')
    proj_dict = {}
    for proj_detail in proj_details_list:
        proj_dict[proj_detail['id']] = {'title': proj_detail['title'],
                                        'size': proj_detail['size'],
                                        'casc': proj_detail['casc'],
                                        'fy': proj_detail['fy'],
                                        'summary': re.sub(html_tags,
                                        '', proj_detail['summary']).replace('\n', ' ').replace('&nbsp;', ' '), 'url': proj_detail['url']}
    # save proj_dict to file
    with open(file_path + 'proj_dict.json', 'w') as output_file:
        json.dump(proj_dict, output_file)
    print('proj_dict written to proj_dict.json')

    print('Building item_dict...')
    item_dict = {}
    for item_detail in item_details_list:
        item_dict[item_detail['id']] = {'title': item_detail['title'], 'contacts': item_detail['contacts'], 'casc': item_detail['casc'], 'fy': item_detail['FY'], 'summary': re.sub(html_tags, '', item_detail['summary']).replace('\n', ' ').replace('&nbsp;', ' '), 'url': item_detail['url'], 'parentId': item_detail['parentId'], 'proj_id': item_detail['proj_id'], 'purpose': item_detail['purpose'], 'relatedItemsUrl': item_detail['relatedItemsUrl']}
    # save item_dict to file
    with open(file_path + 'item_dict.json', 'w') as output_file:
        json.dump(item_dict, output_file)
    print('item_dict written to item_dict.json')

    # we have created new proj and item jsons
    if source == 'sciencebase':
        # write proj and item jsons to file
        with open(file_path + 'proj_jsons.json', 'w') as output_file:
            json.dump(proj_jsons, output_file)
        print('proj_jsons written to proj_jsons.json')
        with open(file_path + 'item_jsons.json', 'w') as output_file:
            json.dump(item_jsons, output_file)
        print('item_jsons written to item_jsons.json')

    # write proj_details_list and item_details_list to file
    with open(file_path + 'proj_dict.pkl', 'wb') as output_file:
        pickle.dump(proj_details_list, output_file)
    print('proj_details_list written to proj_dict.pkl')
    with open(file_path + 'master_details_full.pkl', 'wb') as output_file:
        pickle.dump(item_details_list, output_file)
    print('item_details_list \
        written to master_details_full.pkl')

    print()

    return item_details_list, proj_details_list


def process_casc_ids(source, casc_ids, proj_details_list,
                     item_details_list, proj_jsons,
                     item_jsons, pause_duration):

    total_items = 0
    for casc in casc_ids:
        num_items = 0
        casc_id = casc_ids[casc]
        casc += ' CASC'
        time.sleep(pause_duration)
        fy_ids = sb.get_child_ids(casc_id)
        num_items = process_proj_ids(source, casc,
                                     fy_ids, proj_details_list,
                                     item_details_list,
                                     proj_jsons, item_jsons, pause_duration)
        total_items += num_items
        print('{} processed ({} items)\n'.format(casc, num_items))

    return total_items


def process_proj_ids(source, casc, fy_ids, proj_details_list,
                     item_details_list, proj_jsons,
                     item_jsons, pause_duration):

    print('Processing: {}'.format(casc))

    num_items = 0
    for fy_id in fy_ids:
        try:
            time.sleep(pause_duration) # to ease pressure on sciencebase servers
            fy_json = sb.get_item(fy_id)
            fy = fy_json['title'].split()[1]
        except:
            continue
            
        if fy.isnumeric():
            proj_ids = sb.get_child_ids(fy_id)
            num_items += process_approved_ids(source, casc, fy, proj_ids,
                                              proj_details_list,
                                              item_details_list,
                                              proj_jsons, item_jsons,
                                              pause_duration)

    return num_items


def process_approved_ids(source, casc, fy,
                         proj_ids, proj_details_list,
                         item_details_list, proj_jsons, item_jsons,
                         pause_duration):
    num_items = 0
    for proj_id in proj_ids:
        # get project information
        if source == 'file':
            proj_json = proj_jsons[proj_id]
        else:
            try:
                time.sleep(pause_duration) # to ease pressure on sciencebase servers
                proj_json = sb.get_item(proj_id)
                proj_jsons[proj_id] = proj_json # save proj_json
            except:
                continue
                
        approved_dataset_items = []
        proj_details = {}

        proj_details['id'] = proj_id
        proj_details['casc'] = casc
        proj_details['fy'] = fy
        proj_details['title'] = proj_json['title']
        proj_details['size'] = 0
        try:
            proj_details['url'] = proj_json['link']['url']
        except Exception:
            proj_details['url'] = ''
        try:
            proj_files = proj_json['files']
            for proj_file in proj_files:
                proj_details['size'] += proj_file['size']
        # -------------------------------
        except Exception:
            pass
        try:
            proj_details['summary'] = proj_json['body']
        except Exception:
            try:
                proj_details['summary'] = proj_json['summary']
            except Exception:
                proj_details['summary'] = ''

        proj_title = proj_details['title']
        proj_size = proj_details['size']

        proj_details_list.append(proj_details)
 
        # build approved dataset list
        dataset_ids = sb.get_child_ids(proj_id)
        for dataset_id in dataset_ids:
            try:
                time.sleep(pause_duration) # to ease pressure on sciencebase servers
                dataset_json = sb.get_item(dataset_id)
                item_type = dataset_json['title'].lower()
                if item_type in ['approved datasets', 'approved products']:
                    approved_dataset_items = get_approved_items(dataset_id, item_type.split()[1][:-1])
                    num_items += collect_item_details(source, casc, fy, proj_id, proj_title, proj_size, approved_dataset_items, item_details_list, item_jsons, pause_duration)
            except:
                continue
        
    return num_items

def get_approved_items(dataset_id, item_type):
        
    approved_items = []
    
    def get_items(parent_id, item_type):
        child_id_list = sb.get_child_ids(parent_id)
        for child_id in child_id_list:
            try:
                child_json = sb.get_item(child_id)
                if child_json['hasChildren']:
                    get_items(child_id)
                else:
                    approved_items.append((child_id, item_type))
            except:
                pass
    
    get_items(dataset_id, item_type)

    return approved_items


def collect_item_details(source, casc, fy, proj_id, proj_title,
                         proj_size, approved_dataset_items,
                         item_details_list, item_jsons, pause_duration):

    num_items = 0

    for item_id, item_type in approved_dataset_items:

        # get item informatino
        if source == 'file':
            item_json = item_jsons[item_id]
        else:
            try:
                time.sleep(pause_duration) # to ease pressure on sciencebase servers
                item_json = sb.get_item(item_id)
                item_jsons[item_id] = item_json # save item_json
            except:
                continue

        #-----build item details-----

        item_details = {}

        item_details['id'] = item_id
        item_details['item_type'] = item_type
        item_details['casc'] = casc
        item_details['FY'] = fy
        item_details['proj_id'] = proj_id
        item_details['proj_title'] = proj_title
        item_details['proj_size'] = proj_size

        try:
            item_details['title'] = item_json['title']
        except Exception:
            item_details['title'] = ''
        try:
            item_details['url'] = item_json['link']['url']
        except Exception:
            item_details['url'] = ''
        try:
            item_details['relatedItemsUrl'] = \
                item_json['relatedItems']['link']['url']
        except Exception:
            item_details['relatedItemsUrl'] = ''
        try:
            item_details['summary'] = item_json['body']
        except Exception:
            try:
                item_details['summary'] = item_json['summary']
            except Exception:
                item_details['summary'] = ''
        try:
            item_details['purpose'] = item_json['purpose']
        except Exception:
            item_details['purpose'] = ''
        try:
            item_details['hasChildren'] = item_json['hasChildren']
        except Exception:
            item_details['hasChildren'] = ''
        try:
            item_details['parentId'] = item_json['parentId']
        except Exception:
            item_details['parentId'] = ''

        xml_urls = ''
        try:
            for item_file in item_json['files']:
                if 'xml' in item_file['contentType'] and \
                 'xml' in item_file['name']:
                    xml_urls += item_file['url'] + ','  # separate by commas
            xml_urls = xml_urls.strip(',')
        except Exception:
            pass
        item_details['xml_urls'] = xml_urls

        try:
            item_details['num_files'] = len(item_json['files'])
        except Exception:
            item_details['num_files'] = 0

        item_details['pub_date'] = ''
        item_details['start_date'] = ''
        item_details['end_date'] = ''
        try:
            for date_item in item_json['dates']:
                try:
                    if date_item['type'].lower() == 'publication' or\
                       date_item['label'] == 'publication date':
                        item_details['pub_date'] = date_item['dateString']
                except Exception:
                    item_details['pub_date'] = ''
                try:
                    if date_item['type'].lower() == 'start':
                        item_details['start_date'] = date_item['dateString']
                except Exception:
                    item_details['start_date'] = ''
                try:
                    if date_item['type'].lower() == 'end':
                        item_details['end_date'] = date_item['dateString']
                except Exception:
                    item_details['end_date'] = ''
        except Exception:
            pass

        item_details['contacts'] = []
        try:
            contacts = item_json['contacts']
            for contact in contacts:
                details = {}
                try:
                    details['name'] = contact['name']
                except Exception:
                    details['name'] = ''
                try:
                    details['type'] = contact['type']
                except Exception:
                    details['type'] = ''
                try:
                    details['email'] = contact['email']
                except Exception:
                    details['email'] = ''
                try:
                    details['jobTitle'] = contact['jobTitle']
                except Exception:
                    details['jobTitle'] = ''
                try:
                    details['orcId'] = contact['orcId']
                except Exception:
                    details['orcId'] = ''

                item_details['contacts'].append(details)
        # ----------------------------
        except Exception:
            pass

        item_details_list.append(item_details)
        num_items += 1

    return num_items


def update_proj_dataset_matches():
    proj_dataset_matches = {}
    sim_threshold = 0.5

    # read in item_details and proj_dict
    item_details = pd.DataFrame(pd.read_pickle(file_path +
                                'master_details_full.pkl'))
    with open(file_path + 'proj_dict.json') as input_file:
        proj_dict = json.load(input_file)
    with open(file_path + 'item_dict.json') as input_file:
        item_dict = json.load(input_file)

    print('Building proj_dataset_matches...')
    start = time.time()
    for pid in proj_dict:
        num_items = 0
        item_weighted_sims = []
        proj_dataset_matches[pid] = {}
        proj_dataset_matches[pid]['proj_url'] = proj_dict[pid]['url']
        proj_summary = proj_dict[pid]['summary']
        proj_dataset_matches[pid]['proj_summary'] = proj_summary

        # grab the general topics/ideas of interest from the project summary

        proj_blob1 = TextBlob(proj_summary, np_extractor=conll)
        proj_blob2 = TextBlob(proj_summary, np_extractor=fastext)
        proj_phrases = set(proj_blob1.noun_phrases + proj_blob2.noun_phrases)
        proj_dataset_matches[pid]['proj_phrases'] = list(proj_phrases)

        # compile details of all items for this project
        proj_dataset_matches[pid]['proj_items'] = {}
        items = item_details[item_details['proj_id'] == pid][['id']]
        for item_id in items['id'].values:
            num_items += 1
            proj_dataset_matches[pid]['proj_items'][item_id] = {}
            proj_dataset_matches[pid]['proj_items'][item_id]['item_url'] = \
                item_dict[item_id]['url']
            item_summary = \
                (item_dict[item_id]['summary'] + ' ' +
                    item_dict[item_id]['purpose']).strip()
            proj_dataset_matches[pid]['proj_items'][item_id]['item_summary'] =\
                item_summary

            # grab the general topics/ideas of interest from the item summary
            item_blob1 = TextBlob(item_summary, np_extractor=conll)
            item_blob2 = TextBlob(item_summary, np_extractor=fastext)
            item_phrases = set(item_blob1.noun_phrases +
                               item_blob2.noun_phrases)
            proj_dataset_matches[pid]['proj_items'][item_id]['item_phrases'] =\
                list(item_phrases)

            # compute and store item similarity with project
            matches = []
            similarities = []

            for i in item_phrases:
                for p in proj_phrases:
                    match = SequenceMatcher(None, i, p)
                    similarity = match.ratio()
                    if similarity > sim_threshold:
                        matches.append(similarity)
                        similarities.append([i, p, round(similarity, 4)])

            match_sum = sum(matches)
            match_len = len(matches)
            phrases_len = len(proj_phrases)
            if match_len == 0:
                avg_sim = 0
                weighted_sim = 0
            else:
                inv_match_ratio = phrases_len/match_len
                scaled_inv_ratio = rescale(inv_match_ratio,
                                           0, phrases_len, 0, 2)
                weight = 0.5**(scaled_inv_ratio)

                avg_sim = round(match_sum/match_len, 4)
                weighted_sim = round(weight * avg_sim, 4)

            proj_dataset_matches[pid]['proj_items'][item_id]['similarities'] =\
                similarities
            proj_dataset_matches[pid]['proj_items'][item_id]['avg_sim'] =\
                avg_sim
            proj_dataset_matches[pid]['proj_items'][item_id]['weighted_sim'] =\
                weighted_sim
            item_weighted_sims.append(weighted_sim)

        proj_dataset_matches[pid]['num_items'] = num_items
        proj_dataset_matches[pid]['avg_item_sim'] =\
            0 if len(item_weighted_sims) ==\
            0 else round(sum(item_weighted_sims)/len(item_weighted_sims), 4)

    print('proj_dataset_matches done, saving to file...')

    end = time.time()

    duration = end - start
    mins = int(duration/60)
    secs = duration % 60

    print('\nProject match dictionary update completed \
        in {} minutes and {} seconds'.format(mins, secs))

    # write proj_dataset_matches to file
    with open(file_path + 'proj_dataset_matches.json', 'w') as output_file:
        json.dump(proj_dataset_matches, output_file)
    print('proj_dataset_matches written to proj_dataset_matches.json')


def update_cascs(app, casc_list):
    """Perform hard search on any ids older than 1 day.

    This function calls get_cascs() to populate the fy_obj_list list with
    fiscal year objects for each of the fiscal years present in each CSC.
    It begins the parsing process by calling parse_fiscal_years(), which finds
    all projects in each fiscal year and each item in each project to create a
    comprehensive database for each fiscal year in each CSC. All CSCs, fiscal
    years, projects, items, etc are added to their respective relational
    database tables.

    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.
        casc_list -- List of CASCs to be updated

    Raises:
        Exception -- If something was wrong and fy_obj_list was not cleared by
                     the end of the process.

    """
    # To run this package from command line:
    # python -c 'from __init__ import start; start()'

    start = time.time()

    fy_obj_list = fiscal_years.get_cascs(casc_list)

    if __debug__:
        print("fy_obj_list:\n{0}".format(fy_obj_list))
    fy_obj_list = fiscal_years.parse_fiscal_years(app, fy_obj_list)
    update_casc_total_data(app)

    end = time.time()

    duration = end - start
    mins = int(duration/60)
    secs = duration % 60

    print('Total time: {} minutes and {} seconds'.format(mins, secs))

    if not fy_obj_list:
        print("""

    ===========================================================================

                    CASC update completed.\n""")
    #     exit(0)
    # print("WHY AM I HERE???")
    # assert False, "Should never get here!!!!"
    # raise Exception("Something went wrong in full_hard_search()")


def full_hard_search(app):
    """Perform hard search on any ids older than 1 day.

    This function calls get_all_cscs() to populate the fy_obj_list list with
    fiscal year objects for each of the fiscal years present in each CSC.
    It begins the parsing process by calling parse_fiscal_years(), which finds
    all projects in each fiscal year and each item in each project to create a
    comprehensive database for each fiscal year in each CSC. All CSCs, fiscal
    years, projects, items, etc are added to their respective relational
    database tables.

    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.

    Raises:
        Exception -- If something was wrong and fy_obj_list was not cleared by
                     the end of the process.

    """
    # To run this package from command line:
    # python -c 'from __init__ import start; start()'

    fy_obj_list = fiscal_years.get_all_cscs()

    if __debug__:
        print("fy_obj_list:\n{0}".format(fy_obj_list))
    fy_obj_list = fiscal_years.parse_fiscal_years(app, fy_obj_list)
    update_casc_total_data(app)
    if not fy_obj_list:
        print("""

    ===========================================================================

                    Hard Search is now finished.""")
        exit(0)
    print("WHY AM I HERE???")
    assert False, "Should never get here!!!!"
    raise Exception("Something went wrong in full_hard_search()")


def defined_hard_search(app):
    """Perform hard search on specific fiscal years via user-input.

    This hard search function collects fiscal years from a user that are
    parsed to find projects, which are parsed to find items. All CSCs, fiscal
    years, projects, items, etc are added to their respective relational
    database tables.

    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.

    Raises:
        Exception -- If something was wrong and fy_obj_list was not cleared by
                     the end of the process.

    """
    # To run this function from command line:
    # python -c 'from main import defined_hard_search; defined_hard_search()'

    fy_id_list = fiscal_years.get_user_input_fys()
    fy_obj_list = fiscal_years.create_fy_objs(fy_id_list)

    if __debug__:
        print("fy_obj_list:\n{0}".format(fy_obj_list))
    fiscal_years.parse_fiscal_years(app, fy_obj_list)
    update_casc_total_data(app)
    if not fy_obj_list:
        print("""

    ===========================================================================

                    Defined Hard Search is now finished.""")
        exit(0)
    print("WHY AM I HERE???")
    assert False, "Should never get here!!!!"
    raise Exception("Something went wrong in full_hard_search()")


def debug_projects():
    """For debugging/testing, find all items and calculate project size.

    The function can be given a fiscal year ID and CSC, or use a 'dummy'
    default (SWCSC FY 2011) if not important. It will then parse the project
    and its items as it normally would and print the results.
    """
    # To run this from the terminal, use the following:
    # python -c 'from main import debug_projects; debug_projects()'

    project_id = '1'
    while len(project_id) != 24:
        print("Please provide a Science Base Project ID.")
        project_id = input("Project ID: ")
    print("Provide a fiscal year ID and CSC, or use Dummy Fiscal Year?")
    preference = input("> ").lower()
    if "dum" in preference:
        # Dummy Fiscal Year:
        fiscal_year = gl.SbFiscalYear("50070504e4b0abf7ce733fd7", "SWCSC")
    else:
        fy_id = input("Fiscal Year ID: ")
        fy_csc = input("CSC: ")
        fiscal_year = gl.SbFiscalYear(fy_id, fy_csc)

    project = gl.SbProject(project_id, fiscal_year)
    projects.parse_project(project)
    print("\n\nAnother? (Y / N)")
    answer = input("> ").lower()
    if 'y' in answer:
        debug_projects()
    elif 'n' in answer:
        exit(0)
    else:
        print("Neither answer selected. Program ended.")


def id_in_list(obj_list, sb_object):
    """Check if a Science Base object exists in a list.

    Arguments:
        obj_list -- (list) a list of objects with an 'ID' attribute.
        sb_object -- (item_id, SbFiscalYear, SbProject, or SbItem)
                     Any item with an '.ID' field.

    Returns:
        True -- (boolean) returned if an item is encountered in obj_list with
                an .ID attribute that matches the .ID attribute of sb_object.
        False -- (boolean) returned if no such item is encountered after
                 iterating through obj_list.

    """
    if __debug__:
        print("Checking if sb_object in list...")
    for sb_objects in obj_list:
        if sb_object.ID == sb_objects.ID:
            if __debug__:
                print("Object in list.")
            return True
    if __debug__:
        print("Object not in list")
    return False


def get_date():
    """Return the current date as a string."""
    now = datetime.now()
    date = now.strftime("%Y%m%d")
    return date


def save_to_db(app, fiscal_year):
    """Save Fiscal Year data to database.

    Call functions from the module 'db_save.py' to save Fiscal Year, Projects,
    Items, etc to the database.

    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.
        fiscal_year -- (SbFiscalYear) A completed SbFiscalYear object (defined
                       in 'gl.py') to be parsed and saved to the database.

    """
    # Save casc to db and get db model for casc
    casc_model = db_save.save_casc(app, fiscal_year)

    fy_model = db_save.save_fy(app, fiscal_year, casc_model)

    for project in fiscal_year.projects:
        proj_model = db_save.save_proj(app, project, fy_model, casc_model)
        for item in project.project_items["Project_Item_List"]:
            item_model = db_save.save_item(app, item, proj_model, fy_model,
                                           casc_model)
            for file_json in item.file_list:
                db_save.save_file(app, file_json, item_model, proj_model,
                                  fy_model, casc_model)


def update_casc_total_data(app):
    print("""
------------------------------------------------------------------------------
          """)
    print("Updating all CASC `.total_data` fields...")
    cascs = app.db.session.query(app.casc).all()
    print("CASCs found:")
    num = 0
    for casc in cascs:
        num += 1
        total_data = 0
        print("\t{0}. {1}".format(num, casc.name))
        fys = casc.fiscal_years.all()
        for fy in fys:
            total_data += fy.total_data
            if (total_data - fy.total_data) == 0:
                print("{}".format(fy.total_data), end="")
            else:
                print(" + {}".format(fy.total_data), end="")
        print("\n")
        casc.total_data = total_data
        app.db.session.commit()
        print("Total Data in {0}:\n\t{1}\n\n"
              .format(casc.name, casc.total_data))

    print("""
------------------------------------------------------------------------------
          """)
