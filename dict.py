import exceltojson
import csv, json
import logging
import numpy
import pandas as pd
import simplejson as json
import re
# from nlp import normalize
# from argparse import ArgumentParser
# from transformers import cached_path

# logger = logging.getLogger(__file__)

def createDict():
    dic = []

    excel_file_path = 'Electronics Database (Old).xlsx'
    f1 = pd.read_excel(excel_file_path, sheet_name='Smartphone and Tablet Database')
    # print(f1.columns)
    limit = len(f1)
    i = 0

    brand_container = []
    model_container = []
    battery_container = []
    mem_container = []
    cam_container= []
    color_container = []
    weight_container = []
    price_container = []
    display_container = []
    processor_container = []
    graphics_container = []
    disk_container = []

    while i < limit:
        # print("i : ", i)
        if f1.brand[i] == f1.brand[i] and brand_container.__contains__(f1.brand[i]) == False:
            dic.append((str(f1.brand[i]), '[brand_name]'))
            brand_container.append(f1.brand[i])

        if f1.model[i] == f1.model[i] and model_container.__contains__(f1.model[i]) == False:
            dic.append((str(f1.model[i]), '[model_name]'))
            model_container.append(f1.model[i])

        if f1.Battery[i] == f1.Battery[i] and battery_container.__contains__((str)((int)(f1.Battery[i]))) == False:
            dic.append(((str)((int)(f1.Battery[i])) + ' mAh', '[battery_size]'))
            battery_container.append((str)((int)(f1.Battery[i])))

        if f1.RAM[i] == f1.RAM[i] and mem_container.__contains__((str)((int)(f1.RAM[i]))) == False:
            dic.append(((str)((int)(f1.RAM[i])) + ' GB','[memory_size]'))
            mem_container.append((str)((int)(f1.RAM[i])))

        if f1.Internal_RAM[i] == f1.Internal_RAM[i] and mem_container.__contains__((str)((int)(f1.Internal_RAM[i]))) == False:
            dic.append(((str)((int)(f1.Internal_RAM[i])) + ' GB','[memory_size]'))
            mem_container.append((str)((int)(f1.Internal_RAM[i])))

        if f1.P_Camera[i] == f1.P_Camera[i] and f1.P_Camera[i] != "Dual" and f1.P_Camera[i] != "Yes" and f1.P_Camera[i] != "No" and f1.P_Camera[i] != "VGA" and cam_container.__contains__((str)((int)(f1.P_Camera[i]))) == False:
            dic.append(((str)((int)(f1.P_Camera[i])) + ' MP','[camera_MP]'))
            cam_container.append((str)((int)(f1.P_Camera[i])))

        if f1.S_Camera[i] == f1.S_Camera[i] and f1.S_Camera[i] != "CIF" and f1.S_Camera[i] != "QCIF-15fps" and f1.S_Camera[i] != "Videocall" and f1.S_Camera[i] != "Dual" and f1.S_Camera[i] != "720p" and f1.S_Camera[i] != "Yes" and f1.S_Camera[i] != "No" and f1.S_Camera[i] != "VGA" and cam_container.__contains__((str)((int)(f1.S_Camera[i]))) == False:
            dic.append(((str)((int)(f1.S_Camera[i])) + ' MP','[camera_MP]'))
            cam_container.append((str)((int)(f1.S_Camera[i])))

        if f1.Color[i] == f1.Color[i] and color_container.__contains__(f1.Color[i]) == False:
            dic.append((str(f1.Color[i]), '[model_color]'))
            color_container.append(f1.Color[i])

        if f1.weight_g[i] == f1.weight_g[i] and weight_container.__contains__((str)((int)(f1.weight_g[i]))) == False:
            dic.append(((str)((int)(f1.weight_g[i])) + ' g', '[model_weight]'))
            weight_container.append((str)((int)(f1.weight_g[i])))

        if f1.approx_price_EUR[i] == f1.approx_price_EUR[i] and price_container.__contains__((str)((int)(f1.approx_price_EUR[i]))) == False:
            dic.append(((str)((int)(f1.approx_price_EUR[i])) + ' EUR', '[model_price]'))
            price_container.append((str)((int)(f1.approx_price_EUR[i])))
        i = i + 1
    # print(len(dic))

    f2 = pd.read_excel(excel_file_path, sheet_name='Laptop Database')
    # print(f2.columns)
    limit2 = len(f2)
    i = 0

    while i < limit2:
        # print("i : ", i)
        if f2.brand[i] == f2.brand[i] and brand_container.__contains__(f2.brand[i]) == False:
            dic.append((str(f2.brand[i]), '[brand_name]'))
            brand_container.append(f2.brand[i])

        if f2.laptop_name[i] == f2.laptop_name[i] and model_container.__contains__(f2.laptop_name[i]) == False:
            dic.append((str(f2.laptop_name[i]), '[model_name]'))
            brand_container.append(f2.laptop_name[i])

        if f2.display_size[i] == f2.display_size[i] and display_container.__contains__((str)((int)(f2.display_size[i]))) == False:
            dic.append(((str)((int)(f2.display_size[i])) + ' inch', '[display_size]'))
            display_container.append((str)((int)(f2.display_size[i])))

        if f2.processor_type[i] == f2.processor_type[i] and processor_container.__contains__(f2.processor_type[i]) == False:
            dic.append((str(f2.processor_type[i]), '[processor_name]'))
            processor_container.append(f2.processor_type[i])

        if f2.graphics_card[i] == f2.graphics_card[i] and graphics_container.__contains__(f2.graphics_card[i]) == False:
            dic.append((str(f2.graphics_card[i]), '[graphics_name]'))
            graphics_container.append(f2.graphics_card[i])

        if f2.disk_space[i] == f2.disk_space[i] and disk_container.__contains__(f2.disk_space[i]) == False:
            dic.append((str(f2.disk_space[i]), '[disk_type_size]'))
            disk_container.append(f2.disk_space[i])

        if f2.discount_price[i] == f2.discount_price[i] and price_container.__contains__((str)((int)(f2.discount_price[i]))) == False:
            dic.append(((str)((int)(f2.discount_price[i])) + ' EUR', '[model_price]'))
            price_container.append((str)((int)(f2.discount_price[i])))

        if f2.old_price[i] == f2.old_price[i] and price_container.__contains__((str)((int)(f2.old_price[i]))) == False:
            dic.append(((str)((int)(f2.old_price[i])) + ' EUR', '[model_price]'))
            price_container.append((str)((int)(f2.old_price[i])))

        i = i + 1

    # print(len(dic))

    f3 = pd.read_excel(excel_file_path, sheet_name='Camera Database')
    # print(f3.columns)
    limit3 = len(f3)
    i = 0

    while i < limit3:
        # print("i : ", i)
        if f3.Model[i] == f3.Model[i] and model_container.__contains__(f3.Model[i]) == False:
            dic.append((str(f3.Model[i]), '[model_name]'))
            model_container.append(f3.Model[i])

        if f3.Price[i] == f3.Price[i] and price_container.__contains__((str)((int)(f3.Price[i]))) == False:
            dic.append(((str)((int)(f3.Price[i])) + ' EUR', '[model_price]'))
            price_container.append((str)((int)(f3.Price[i])))

        i = i + 1

    # print(len(dic))
    print("Dictionary Created with length = ", len(dic))
    return dic

def delexicalise(utt, dictionary):
    for key, val in dictionary:
        utt = (' ' + utt + ' ').replace(' ' + key + ' ', ' ' + val + ' ')
        utt = utt[1:-1]  # why this?

        utt = (' ' + utt + ' ').replace(' ' + key + '.', ' ' + val + '.')
        utt = utt[1:-1]

    return utt

def main():
    dic = createDict()

    new_data = {}

    # fin1 = file('data/multi-woz/data.json')
    file_path = 'data/test.json'
    with open(file_path, "r", encoding="utf-8") as f:
        dataset = json.loads(f.read())

    cnt = 0
    for dataset_name in dataset:
        new_data_name = []
        for dialogue in dataset[dataset_name]:
            print("cnt : ", cnt)
            cnt = cnt + 1
            new_dialogue = {}
            new_dialogue["personality"] = dialogue["personality"]
            new_utterances = []
            for utterance in dialogue["utterances"]:
                # print(utterance)
                new_utterance = {}
                new_candidates = []
                new_history = []
                for sent in utterance["candidate"]:
                    # print(sent)
                    words = sent.split()
                    delex_sent = delexicalise(' '.join(words), dic)
                    new_candidates.append(delex_sent)

                for sent in utterance["history"]:
                    words = sent.split()
                    delex_sent = delexicalise(' '.join(words), dic)
                    new_history.append(delex_sent)
                new_utterance["candidate"] = new_candidates
                new_utterance["history"] = new_history
                new_utterances.append(new_utterance)

            new_dialogue["utterances"] = new_utterances
            new_data_name.append(new_dialogue)
        new_data["train"] = new_data_name

    with open('valid_delex.json', 'w') as f:
        json.dump(new_data, f)
    print('Creating delexicalized dialogues....')

if __name__ == "__main__":
    main()