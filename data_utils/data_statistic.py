#!/usr/bin/env python3

'''
@Time   : 2018-11-29 22:11:22
@Author : su.zhu
@Desc   : 
'''

import sys
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--data_path', required=True, help='data path')
opt = parser.parse_args()

def get_vocab(file_path):
    slot_vocab = {}
    intent_vocab = {}
    with open(file_path) as in_file:
        data = json.load(in_file)
        print(list(data))
        for domain_name in data:
            support_sample_number = 0
            query_sample_number = 0
            for batch in data[domain_name]:
                #print(list(batch['support'])) # ['seq_ins', 'labels', 'seq_outs', 'word_piece_marks', 'tokenized_texts', 'word_piece_labels']
                #print(list(batch['batch'])) # ['seq_ins', 'labels', 'seq_outs', 'word_piece_marks', 'tokenized_texts', 'word_piece_labels']
                support_sample_number += len(batch['support']['labels'])
                query_sample_number += len(batch['batch']['labels'])
                for data_type in ['support', 'batch']:
                    for slots in batch[data_type]['seq_outs']:
                        for slot in slots:
                            if slot != 'O':
                                slot = slot.split('-', 1)[1]
                            slot_vocab[slot] = 1
                    for intent in batch[data_type]['labels']:
                        intent_vocab[intent] = 1
            print(domain_name, len(data[domain_name]), support_sample_number, query_sample_number)
    return slot_vocab, intent_vocab

train_slot_vocab, train_intent_vocab = get_vocab(opt.data_path + '/train.json')
valid_slot_vocab, valid_intent_vocab = get_vocab(opt.data_path + '/valid.json')
test_slot_vocab, test_intent_vocab = get_vocab(opt.data_path + '/test.json')

unseen_slot_number = 0
for slot in test_slot_vocab:
    if slot not in train_slot_vocab:
        unseen_slot_number += 1
print("Test set: unseen slots %d of all slots %d ." % (unseen_slot_number, len(test_slot_vocab)))
