import json
import nltk
from rouge_score import rouge_scorer

with open('data/gen_dict.json') as f:
    gen_dict = json.load(f)
with open('data/gold_dict.json') as f:
    gold_dict = json.load(f)

scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)

cnt4 = 0
cnt3 = 0
cnt2 = 0
cnt1 = 0
cnt = 0

rg1_score = 0
rgl_score = 0

for key,val in gen_dict.items():
    scores = scorer.score(gold_dict[key], val)
    # cnt_scores += scores
    rg1 = scores['rouge1'].precision
    rg1_score += rg1
    rgl_score += scores['rougeL'].precision
    # print(rg1)
    # print(scores)
    expected = gold_dict[key].split(' ')
    actual = val.split(' ')
    print(expected)
    print(actual)
    BLEUscore4 = nltk.translate.bleu_score.sentence_bleu([expected], actual)
    BLEUscore3 = nltk.translate.bleu_score.sentence_bleu([expected], actual, weights=(0.4, 0.3, 0.3, 0))
    BLEUscore2 = nltk.translate.bleu_score.sentence_bleu([expected], actual, weights=(0.5, 0.5, 0, 0))
    BLEUscore1 = nltk.translate.bleu_score.sentence_bleu([expected], actual, weights=(1, 0, 0, 0))
    cnt1 += BLEUscore1
    cnt2 += BLEUscore2
    cnt3 += BLEUscore3
    cnt4 += BLEUscore4
    cnt += 1
    # print(BLEUscore4)

cnt1 /= cnt
cnt2 /= cnt
cnt3 /= cnt
cnt4 /= cnt
rg1_score /= cnt
rgl_score /= cnt
print("Bleu Score 1 : ", cnt1)
print("Bleu Score 2 : ", cnt2)
print("Bleu Score 3 : ", cnt3)
print("Bleu Score 4 : ", cnt4)
print("Rouge1 : ", rg1_score)
print("RougeL : ", rgl_score)

# print(cnt_scores)
