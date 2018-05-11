# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 17:42:55 2018
@author: 김동현
"""

import watson_developer_cloud
import csv
import re
import os.path


#CSV Data
def import_csv():
    BASE = os.path.dirname(os.path.abspath(__file__))
    chat_subject = []
    f = open(os.path.join(BASE, "chatbot.csv"), 'r', encoding='utf-8')
    #f = open('blog/chatbot.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        chat_subject.append(line[1])
    f.close()
    return chat_subject

#변수 초기화를 시켜준다

def initialize_watson():
    conversation = watson_developer_cloud.ConversationV1(
        username='6372fd90-10c7-4dbd-9f51-e98ab239c706',
        password='2dAeXBBVXDSl',
        version='2017-05-26'
    )
    response = conversation.message(workspace_id='7e437f5e-946b-43de-986e-4fc6968f9130')
    conversation_id = response['context']['conversation_id']
    outputs = response['output']['text']
    this_context = response['context']
    return (conversation,conversation_id,outputs,this_context)

def talk_watson(input_message,conversation,outputs,this_context):
    response = conversation.message(
        workspace_id='7e437f5e-946b-43de-986e-4fc6968f9130',
        input={
            'text': input_message
        },
        context=this_context
    )
    outputs = response['output']['text']
    this_context = response['context']
    return (outputs, this_context)

    
#두번째 대화
def __main__():
    chat_subject = import_csv()
    (conversation,conversation_id,outputs,this_context) = initialize_watson()
    print("출력 : ",end = "")
    print(outputs[0],end = "") #질문 출력
    
    while(1):
        input_message = input("입력 : ")
        if input_message == '종료':
            print('감사합니다. 프로그램을 종료합니다.')
            return
        
        (outputs, this_context) = talk_watson(input_message,conversation,outputs,this_context)

        if outputs[0][0]=='[': #List Up을 해주는 질문
            print("<다음 질문 중 골라주세요>")
            conv_lists = re.findall('\d+',outputs[0])
            for conv_list in conv_lists:
                print(chat_subject[int(conv_list)])
        else : # 일반적인 질문
            print("출력 : ",end = "")
            print(outputs[0]) #질문 출력

#__main__()