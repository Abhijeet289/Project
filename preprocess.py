import pandas as pd
import dict
import numpy as np
import dbPointer
import json
from collections import OrderedDict
from tqdm import tqdm
import operator

# GLOBAL VARIABLES
DICT_SIZE = 3500
MAX_LENGTH = 50

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def read_data():
    google_sheet_id = "1Osl3p1MVKL7NAF3TAr4V3EoUmn-GTTUXTz1yP8vF99E"
    sheet_name = "CombinedSheet"
    google_sheet_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(google_sheet_id, sheet_name)
    df = pd.read_csv(google_sheet_url)
    return df

def fill_standard_slots():
    dict_mobile = {}
    dict_laptop = {}
    dict_camera = {}

    dict_mobile["ram"] = "Not mentioned"
    dict_mobile["camera"] = "Not mentioned"
    dict_mobile["cost"] = "Not mentioned"
    dict_mobile["battery"] = "Not mentioned"
    dict_mobile["model"] = "Not mentioned"
    dict_mobile["color"] = "Not mentioned"
    dict_mobile["brand"] = "Not mentioned"

    dict_laptop["brand"] = "Not mentioned"
    dict_laptop["cost"] = "Not mentioned"

    dict_camera["brand"] = "Not mentioned"
    dict_camera["cost"] = "Not mentioned"

    dict_combined = {"smartphone_tablet": dict_mobile, "laptop": dict_laptop, "camera": dict_camera}
    return dict_combined


def addDBPointer(agent_metadata):
    """Create database pointer for all related domains."""
    domains = ['smartphone_tablet', 'laptop', 'camera']
    pointer_vector = np.zeros(6 * len(domains))
    for domain in domains:
        num_entities = dbPointer.queryResult(domain, agent_metadata)
        pointer_vector = dbPointer.oneHotVector(num_entities, domain, pointer_vector)

    return pointer_vector

def create_data(df):
    """"
        Creating the dictionary for delexicalizing the data
    """
    delex_data = {}
    dialogue = []
    dialogue_number = 1
    current_domain = "No Domain"
    user_log = {}
    agent_log = {}
    mobile_tags = []
    laptop_tags = []
    camera_tags = []
    ids = []
    agent_metadata = fill_standard_slots()

    for i in df.index:
        print(dialogue_number)
        user_utterance = df["USER"][i]
        agent_utterance = df["AGENT"][i]
        if user_utterance == (str)(dialogue_number):
            if dialogue_number != 1:
                delex_data[dialogue_number-1] = dialogue
            dialogue = []
            current_domain = "No Domain"
            # if dialogue_number != 1:
                # print("hello")
            dialogue_number += 1
            agent_metadata = fill_standard_slots()
            continue

        slot_tags = df["Tag"][i]
        if current_domain == "No Domain":
            tmp = df["Task Info"][i]
            if tmp == tmp:
                arr = tmp.split(',')
                if len(arr) == 1:
                    current_domain = arr[0]
                if len(arr) > 1:
                    current_domain = "MultiDomain"
                    ids.append(dialogue_number-1)
        if current_domain == "MultiDomain":
            continue

        user_log["text"] = user_utterance

        agent_log["text"] = agent_utterance
        agent_log["metadata"] = agent_metadata

        # print(slot_tags)
        if slot_tags != slot_tags:
            pointer_vector = addDBPointer(agent_metadata)
            user_log["db_pointer"] = pointer_vector.tolist()
            dialogue.append(user_log.copy())
            dialogue.append(agent_log.copy())
            continue
        slots = slot_tags.split(',')
        # print(slots)
        for slot in slots:
            arr = slot.split('-')
            if len(arr) >= 2:
                slot_name = arr[0].strip().lower()
                slot_val = arr[1].strip()
                if current_domain == "Smartphone" or current_domain == "Tablet":
                    # mobile_tags.append(slot_name)
                    if agent_metadata["smartphone_tablet"].__contains__(slot_name):
                        agent_metadata["smartphone_tablet"][slot_name] = slot_val
                elif current_domain == "Laptop":
                    # laptop_tags.append(slot_name)
                    if agent_metadata["laptop"].__contains__(slot_name):
                        agent_metadata["laptop"][slot_name] = slot_val
                elif current_domain == "Camera":
                    # camera_tags.append(slot_name)
                    if agent_metadata["camera"].__contains__(slot_name):
                        agent_metadata["camera"][slot_name] = slot_val

        pointer_vector = addDBPointer(agent_metadata)
        user_log["db_pointer"] = pointer_vector.tolist()
        dialogue.append(user_log.copy())
        dialogue.append(agent_log.copy())


    # mobile_set = list(set(mobile_tags))
    # print(mobile_set)
    # laptop_set = list(set(laptop_tags))
    # print(laptop_set)
    # camera_set = list(set(camera_tags))
    # print(camera_set)
    with open('data/btpData.json', 'w') as f:
        json.dump(delex_data, f)

    return delex_data

def get_summary_bstate(bstate):
    domains = ['smartphone_tablet', 'laptop', 'camera']
    summary_bstate = []
    for domain in domains:
        domain_active = False

        for slot in bstate[domain]:
            if bstate[domain][slot] == "Not mentioned":
                summary_bstate.append(0)
            else:
                domain_active = True
                summary_bstate.append(1)

        # quasi domain-tracker
        if domain_active:
            summary_bstate += [1]
        else:
            summary_bstate += [0]

    print(len(summary_bstate))
    assert len(summary_bstate) == 14
    return summary_bstate

def analyze_dialogue(dialogue, max_len):
    """Cleaning procedure for all kinds of errors in text and annotation."""
    d = dialogue
    # do all the necessary postprocessing
    if len(d) % 2 != 0:
        # print path
        print('odd # of turns')
        return None  # odd number of turns, wrong dialogue

    if len(d) == 0:
        # print path
        print('Empty Dialogue')
        return None

    d_pp = {}
    usr_turns = []
    sys_turns = []
    for i in range(len(d)):
        if len(d[i]['text'].split()) > max_len:
            print("too long")
            return None
        if i % 2 == 0: #user turn
            if 'db_pointer' not in d[i]:
                print("No DB")
                return None
            text = d[i]['text']
            if not is_ascii(text):
                print("Not ASCII")
                return None
            usr_turns.append(d[i])
        else:
            text = d[i]['text']
            if not is_ascii(text):
                print("Not ASCII")
                return None
            belief_summary = get_summary_bstate(d[i]['metadata'])
            d[i]['belief_summary'] = belief_summary
            sys_turns.append(d[i])

    d_pp['usr_log'] = usr_turns
    d_pp['sys_log'] = sys_turns

    return d_pp


def get_dial(dialogue):
    """Extract a dialogue from the file"""
    dial = []
    d_orig = analyze_dialogue(dialogue, MAX_LENGTH)
    if d_orig is None:
        return None

    usr = [t['text'] for t in d_orig['usr_log']]
    db = [t['db_pointer'] for t in d_orig['usr_log']]
    bs = [t['belief_summary'] for t in d_orig['sys_log']]
    sys = [t['text'] for t in d_orig['sys_log']]
    for u, d, s, b in zip(usr, db, sys, bs):
        dial.append((u, s, d, b))

    return dial

def divideData(data):
    train_dials = {}
    val_dials = {}

    # dictionaries
    word_freqs_usr = OrderedDict()
    word_freqs_sys = OrderedDict()

    dialogue_number = 1

    for dialogue_name in tqdm(data):
        dial = get_dial(data[dialogue_name])
        print("dialogue number : ", dialogue_number)
        if dial:
            dialogue= {}
            dialogue['usr'] = []
            dialogue['sys'] = []
            dialogue['db'] = []
            dialogue['bs'] = []
            for turn in dial:
                dialogue['usr'].append(turn[0])
                dialogue['sys'].append(turn[1])
                dialogue['db'].append(turn[2])
                dialogue['bs'].append(turn[3])
            train_dials[dialogue_name] = dialogue
            if dialogue_number > 430:
                val_dials[dialogue_name] = dialogue

            for turn in dial:
                line = turn[0]
                words_in = line.strip().split(' ')
                for w in words_in:
                    if w not in word_freqs_usr:
                        word_freqs_usr[w] = 0
                    word_freqs_usr[w] += 1

                line = turn[1]
                words_in = line.strip().split(' ')
                for w in words_in:
                    if w not in word_freqs_sys:
                        word_freqs_sys[w] = 0
                    word_freqs_sys[w] += 1
            dialogue_number += 1

    with open('data/val_dials.json', 'w') as f:
        json.dump(val_dials, f, indent=4)

    with open('data/train_dials.json', 'w') as f:
        json.dump(train_dials, f, indent=4)

    return word_freqs_usr, word_freqs_sys

def createDict(word_freqs):

    word_freqs = sorted(word_freqs.items(), key=operator.itemgetter(1), reverse=True)
    sorted_words = []
    for i in word_freqs:
        sorted_words.append(i[0])
    # for key, val in word_freqs.items():
    #     print(key)
    #     print(val)
    #
    # words = word_freqs.keys()
    # freqs = word_freqs.values()
    #
    # sorted_idx = np.argsort(freqs)
    # sorted_words = []
    # for ii in sorted_idx[::-1]:
    #     sorted_words.append(words[ii])
    # sorted_words = [words[ii] for ii in sorted_idx[::-1]]

    # Extra vocabulary symbols
    _GO = '_GO'
    EOS = '_EOS'
    UNK = '_UNK'
    PAD = '_PAD'
    extra_tokens = [_GO, EOS, UNK, PAD]

    worddict = OrderedDict()
    for ii, ww in enumerate(extra_tokens):
        worddict[ww] = ii
    for ii, ww in enumerate(sorted_words):
        worddict[ww] = ii + len(extra_tokens)



    delete_keys = [key for key, idx in worddict.items() if idx >= DICT_SIZE]

    for key in delete_keys:
        del worddict[key]

    vocab_len = len(worddict)
    print("vocab length : ", vocab_len)

    # for key, idx in worddict.items():
    #     if idx >= DICT_SIZE:
    #         del worddict[key]

    return worddict

def buildDictionaries(word_freqs_usr, word_freqs_sys):
    """Build dictionaries for both user and system sides.
    You can specify the size of the dictionary through DICT_SIZE variable."""
    dicts = []
    worddict_usr = createDict(word_freqs_usr)
    dicts.append(worddict_usr)
    worddict_sys = createDict(word_freqs_sys)
    dicts.append(worddict_sys)

    # reverse dictionaries
    idx2words = []
    for dictionary in dicts:
        dic = {}
        for k,v in dictionary.items():
            dic[v] = k
        idx2words.append(dic)

    with open('data/input_lang.index2word.json', 'w') as f:
        json.dump(idx2words[0], f, indent=2)
    with open('data/input_lang.word2index.json', 'w') as f:
        json.dump(dicts[0], f,indent=2)
    with open('data/output_lang.index2word.json', 'w') as f:
        json.dump(idx2words[1], f,indent=2)
    with open('data/output_lang.word2index.json', 'w') as f:
        json.dump(dicts[1], f,indent=2)

def main():
    """"
    Reading the data from Google Sheet in a data-frame
    """
    df = read_data()

    delex_data = create_data(df)

    print('Divide dialogues for separate bits - usr, sys, db, bs')
    word_freqs_usr, word_freqs_sys = divideData(delex_data)

    print('Building dictionaries')
    buildDictionaries(word_freqs_usr, word_freqs_sys)


if __name__ == "__main__":
    main()