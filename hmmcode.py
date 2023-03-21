
import sys
import json

hmm_model_file=open("hmmmodel.txt")
hmm_output_file=open("hmmoutput.txt", mode='w')
hmm_model=json.load(hmm_model_file)
tag_count,emission_count,transition_count,most_probable_count=hmm_model['tag_count'],hmm_model['emission_count'],hmm_model['transition_count'],hmm_model['most_probable_count'][0:5]

def get_lines_dev_data(file_path):
    dev_data_lines=[]
    with open(file_path) as hmm_dev_file:
        for lines in hmm_dev_file.readlines():
            dev_data_lines.append(lines.rstrip())
    return dev_data_lines

test_dev_data_file=sys.argv[1]
test_dev_lines=get_lines_dev_data(test_dev_data_file)

start_tag='<s>'
end_tag='<e>'

for line in test_dev_lines:
    word_exists_flag,tags=0,[]
    hmm_probabilities,hmm_backpointers=[{}],[{}]
    words_to_tagged=line.split(" ")
    word_exists_flag,word_index=0,0
    word_to_tag=words_to_tagged[word_index]
    if word_to_tag in emission_count.keys():
        word_exists_flag=1
        word_tags=emission_count[word_to_tag].keys()
    else:
        word_tags=most_probable_count
    for word_tag in word_tags:
        if word_exists_flag:
            hmm_probabilities[word_index][word_tag]=transition_count[start_tag][word_tag]*emission_count[word_to_tag][word_tag]
        else:
            hmm_probabilities[word_index][word_tag]=transition_count[start_tag][word_tag]
        hmm_backpointers[word_index][word_tag]=start_tag
    for word_index in range(1,len(words_to_tagged)):
        word_to_tag=words_to_tagged[word_index]
        word_exists_flag=0
        hmm_probabilities.append({})
        hmm_backpointers.append({})
        if word_to_tag in emission_count.keys():
            word_exists_flag=1
            word_tags=emission_count[word_to_tag].keys()
        else:
            word_tags=most_probable_count
        for word_tag in word_tags:
            if word_tag==start_tag or word_tag==end_tag:
                continue
            max_probability,max_state=-1,''
            for tag_new in hmm_probabilities[word_index-1]:
                if word_exists_flag:
                    current_probability=transition_count[tag_new][word_tag] * emission_count[word_to_tag][word_tag] * hmm_probabilities[word_index-1][tag_new]
                else:
                    current_probability=transition_count[tag_new][word_tag] * hmm_probabilities[word_index-1][tag_new]
                if max_probability<current_probability:
                    max_probability=current_probability
                    max_state=tag_new  
            hmm_backpointers[word_index][word_tag]=max_state
            hmm_probabilities[word_index][word_tag]=max_probability
    
    max_probability,max_state=-1,''
    hmm_probabilities.append({})
    hmm_backpointers.append({})
    for word_tag in hmm_probabilities[len(words_to_tagged)-1]:
        current_probability=transition_count[word_tag][end_tag]*hmm_probabilities[len(words_to_tagged)-1][word_tag]
        if max_probability<current_probability:
            max_probability=current_probability
            max_state=word_tag
    hmm_backpointers[len(words_to_tagged)][end_tag]=max_state
    hmm_probabilities[len(words_to_tagged)][end_tag]=max_probability
    
    l = len(hmm_probabilities)
    start = end_tag
    taggings = words_to_tagged[l-2] + "/" + hmm_backpointers[l-1][start]
    start = hmm_backpointers[l-1][start]
    hmm_probabilities.pop()
    l -= 1

    while len(hmm_probabilities)-1:
        taggings = words_to_tagged[l-2] + "/" + hmm_backpointers[l-1][start] + " "+ taggings
        start = hmm_backpointers[l-1][start]
        l -= 1
        hmm_probabilities.pop()

    hmm_output_file.write(taggings)
    hmm_output_file.write('\n')
hmm_output_file.close()


# In[ ]:




