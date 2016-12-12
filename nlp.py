import shelve
import logging
from nltk.tokenize import sent_tokenize, word_tokenize

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
oracle = shelve.open('oracle', writeback=True)


def masterdata():
    print('----------------------')
    print(list(oracle.keys()))
    for key in list(oracle.keys()):
        print(key + ':', oracle[key])
    print("----------------------")

def check_user_profile(username):
    if username in oracle['users']:
        print('User Found')
    else:
        print("User doesn't exist in the system. \n Do you want to add it?(yes/no)")
        yn = input()
        if yn == 'yes':
            create_user_profile(username)


def create_user_profile(username):
    print('Creating user profile')


def check_module_tokens(qn):
    l_match_module = 'UN IDENTIFIED'
    print('Checking module token match')
    for word in word_tokenize(qn):
        if word.lower() in oracle['common_tokens']:
            logging.debug(word + ': Common token')
            continue
        else:
            if username + '_modules' in oracle.keys():
                for user_module in oracle[username + '_modules']:
                    if word in oracle[user_module + '_tokens']:
                        print(word + ' found in ' + user_module)
                        l_match_module = user_module
        if l_match_module == 'UN IDENTIFIED':
            oracle['unid_tokens'].append(word)
        return l_match_module


masterdata()
print('Enter User Name:')
username = input()

check_user_profile(username)

# oracle.has_key
logging.debug('Context set for user: ' + username)
logging.debug('Get user modules assigned to user')
logging.debug(username + ' has the below responsibilities:')

## Display user assigned modules
if username+'_modules' in oracle.keys():
    logging.debug(oracle[username + '_modules'])

print('Ask your question in Natural Language')
qn = input()
oracle['qs'].append(qn)

#print(sent_tokenize(qn))

print('Qn Tokens:' , word_tokenize(qn))

logging.debug('Find the module related to question')
l_user_module = check_module_tokens(qn)

print('I see that your question belongs to ' + l_user_module.upper() + ' module. /n Is that right (Yes/No)?')
yn = input()

if yn.lower() == 'yes':
    print('Appreciate your feedback.')
else:
    print("Sorry I couldn't find the right module")

print('Find the action item')
print('Confirm action with user before performing')
print('Perform Action')
print('Store Question and Action item relation')

oracle.close()
