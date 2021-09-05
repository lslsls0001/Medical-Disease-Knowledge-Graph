'''

list1=["1","2","3"]
list2=[3,4,5]
stop_wds=[]

for wd1 in list1:
    for wd2 in list1:
        if wd1 in wd2 and wd1 != wd2:
            print(wd1 + "---" + wd2 + "\n")
            stop_wds.append(wd1)

print(stop_wds)
'''

wd_dict={"录雷他定":"producer", "发烧":"symptom", "美食":"food"}
final_wds = ["录雷他定","美食"]
final_dict = {i: wd_dict.get(i) for i in final_wds}
print(final_dict)