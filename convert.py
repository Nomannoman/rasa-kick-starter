import pandas as pd
inputfile='Solutiondevelopment.csv'

df = pd.read_csv(inputfile)

df.columns=['questions','answers']
df=df.sort_values(by='answers', ascending= True)

questions = df.iloc[:,0]
answers=df.iloc[:,1]

print(answers)
q = questions.tolist()
a = answers.tolist()
print(len(q))
print(len(a))

#Merge dataframes

# length=len(q)
# i=0
# c=1

# with open("bot_rasa/data/nlu.yml","w") as f2:
#     f2.write('version: "2.0" ' +"\n\n")
#     f2.write("nlu: \n")
#     while i<length:
#          f2.write("  - intent: q"+str(c)+"\n    "+"examples: |"+"\n")
#          f2.write("      - ")
#          j=i+1
#          f2.write(str(q[i])+"\n")
#          while j<length and a[j]==a[i]:
#              f2.write("      - "+str(q[j])+"\n")
#              j=j+1
#          i=j
#          c=c+1
#     responses=c
# f2.close()

res = []
[res.append(x) for x in a if x not in res]
a=res

i=0
with open("help", "w") as f1:
    f1.write('version: "2.0" ' +"\n\n"+"intents:\n")
    while i<len(a):
        f1.write("  - q"+str(i+1)+"\n")
        i=i+1
    f1.write("\n\n"+"responses: \n")
    i=0
    while(i<len(a)):
        a[i]=str(a[i])
        a[i]=a[i].replace('"',"'")
        f1.write("  utter_a"+str(i+1)+":\n"+"  - text : "+'"'+a[i]+'  {emoji}"\n')
        i=i+1

# t1 = 1
# t2 = 1
# n = 1
# with open("help", "w") as file:
#   file.write('version: "2.0" ' + "\n\n")
#   file.write("stories:\n\n")
#   for i in range(0, 2 * (375)):
#     if i % 2 == 0:
#       file.write("- story: path" + str(n) + "\n" + "  " + "steps:\n")
#       file.write("  " + "- ")
#       file.write("intent: " + "q" + str(t1) + "\n")
#       t1 = t1 + 1
#       n = n + 1
#     elif i % 2 == 1:
#       file.write("  - action: action_sentiment_analysis" + "\n")
#       t2 = t2 + 1
# file.close()
