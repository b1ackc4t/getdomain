# pip install -U symspellpy

import pkg_resources
from symspellpy.symspellpy import SymSpell

sym_spell = SymSpell(max_dictionary_edit_distance=0, prefix_length=7)
dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")

sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

# a sentence without any spaces
input_term = "thequickbrownfoxjumpsoverthelazydog"
result = sym_spell.word_segmentation(input_term)
print("{}, {}, {}".format(result.corrected_string, result.distance_sum,result.log_prob_sum))
string1 = result.corrected_string
list1 = string1.split(' ')
print([list1[i][0] for i in range(len(list1))])
print(''.join(list1))

