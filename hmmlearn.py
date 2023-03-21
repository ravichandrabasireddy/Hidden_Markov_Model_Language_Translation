import sys
import json
from collections import OrderedDict
def get_lines_training_data(file_path):
    training_data_lines=[]
    with open(file_path) as hmm_training_file:
        for lines in hmm_training_file.readlines():
            training_data_lines.append(lines.rstrip())
    return training_data_lines

def get_words_training_data(line):
    start_tag="/<s>"
    end_tag="/<e>"
    line=start_tag+" "+line+" "+end_tag
    return line.split(" ")

def check_new_tag(individual_word_tags,word):
    if tag in individual_word_tags.keys():
        return False
    return True

hmm_training_data_file_path=sys.argv[1]
lines_in_training_data=get_lines_training_data(hmm_training_data_file_path)
for index in range(len(lines_in_training_data)):
    lines_in_training_data[index]=get_words_training_data(lines_in_training_data[index])
unique_tags=set()
individual_word_tags={}
tag_count={}
emission_count={}
emission={}
transition_count={}
start_tag='<s>'
end_tag='<e>'
for line in lines_in_training_data:
    pre_tag=start_tag
    transition_count.setdefault(pre_tag,{})
    transition_count.setdefault(end_tag,{})
    for word_tag in line:
        word_tag_split=word_tag.rpartition("/")
        word,tag=word_tag_split[0],word_tag_split[2]
        unique_tags.add(tag)
        tag_count[tag]=tag_count.get(tag,0)+1
        if word=="":
            continue
        if tag!=start_tag and tag!=end_tag:
            if individual_word_tags.get(tag) is not None:
                individual_word_tags[tag].add(word)            
            else:
                individual_word_tags[tag]=individual_word_tags.setdefault(tag,set((word)))
        transition_count[pre_tag][tag]=transition_count[pre_tag].get(tag,0)+1
        transition_count.setdefault(tag,{})
        pre_tag=tag
        if pre_tag not in transition_count:
            transition_count[pre_tag]=transition_count.setdefault()
        if word not in emission_count:
            emission_count[word][tag]=emission_count.setdefault(word,{}).setdefault(tag,1)
        else:
            emission_count[word][tag]=emission_count[word].get(tag,0)+1

for tag_i in tag_count.keys():
    for tag_j in tag_count.keys():
        transition_count[tag_i][tag_j]=transition_count[tag_i].get(tag_j,0)+1
        tag_count[tag_j]+=1

for tag_i in transition_count:
    for tag_j in transition_count[tag_i]:
        transition_count[tag_i][tag_j]/=tag_count[tag_i]

for word in emission_count:
    for tag in emission_count[word]:
        emission_count[word][tag]/=tag_count[tag]

most_probable_count= sorted(individual_word_tags, key=lambda k: len(individual_word_tags[k]), reverse=True)

with open('hmmmodel.txt','w') as file:
    file.write(json.dumps({"tag_count":tag_count,"transition_count":transition_count,"emission_count":emission_count,"most_probable_count":most_probable_count}))

