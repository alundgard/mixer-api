import json
import random
import sys

# Form a new dialog using paraphrases according to the given index (specify dialogs)
def formDialog(index):
  dialog = flexData[index]
  newDialog = []
  for sen in dialog[1]:
    numPara = len(sen[2])
    newSen = sen[4]
    if numPara > 0:
      ranSenInx = random.sample(xrange(0, numPara - 1), 1)[0]
      newSen = sen[2][ranSenInx]
    newDialog.append([sen[3], sen[0], sen[1], newSen])
  newDialogs.append(newDialog)

inputName = "AllFlexData_ProfileID.json"    # The input file name
numWantDialog = (int)(sys.argv[1])         # How many new dialogs do you want to generate
flexData = []
# Read input json file
with open(inputName) as json_file:
    allData = json.load(json_file)
    for ad in allData:    # for each dataset
      for data in ad["data"]:    # for each dialog
        flexData.append([data["dialogName"], []])
        for sen in data["content"]:     # for each sentence in that dialog
          paras = [sen["role"], sen["dialogAct"], [], 0, sen["oriSen"]]
          sql = "N"
          if "sql_annotation" in sen:
            if len(sen["sql_annotation"]) > 0:
              sql = "Y"
          for para in sen["paraphrases"]:       # for each paraphrase of this sentence
            paras[2].append(para)
          paras[3] = sql
          index = len(flexData) - 1
          flexData[index][1].append(paras)
                     
numDialogs = len(flexData)
divide = numWantDialog / numDialogs
remainder = numWantDialog % numDialogs
newDialogs = []

# randomly select remainder number of dialogs
remDialogs = random.sample(xrange(0, numDialogs), remainder)
for index in remDialogs:
  formDialog(index)

# if # of wanted paraphrasing-dialogs > # of original dialogs, then every original dialog will be reformed accordingly
for i in range(0, divide):
  for j in range(0, numDialogs):
    formDialog(j)

# output new dialogs
dic = []
for i in range(0, len(newDialogs)):
  newDialog = {}
  dialogId = "dialog" + str(i)
  newDialog["dialogId"] = dialogId
  newDialog["dialog"] = []
  for sen in newDialogs[i]:
    newDialog["dialog"].append({"sql" : sen[0], "role" : sen[1], "dialogAct" : sen[2], "sen" : sen[3]})
  dic.append(newDialog)

# Write to output json file
# file = open("NewDialogs.json", "w")
# file.write(json.dumps(dic, sort_keys=True, indent=2))

# Send data back to node
dataToSendBack = json.dumps(dic, sort_keys=True, indent=2)
print(dataToSendBack)
sys.stdout.flush()