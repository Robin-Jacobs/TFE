import json
with open('captions_val2017.json') as json_data:
    data_coco = json.load(json_data);
with open('image_data.json') as json_data:
    data_image_visual = json.load(json_data);
with open('objects.json') as json_data:
    objects_visual = json.load(json_data);
coco_annotations = data_coco.get("annotations");
with open('captions_train2017.json') as json_data:
    data_train_coco = json.load(json_data);
coco_train_annotations = data_train_coco.get("annotations");

#output format:
#result = [{"id_coco": ,
#         "id_visual": ,
#         "description": ,
#         "caption:[
#             {"word": ,
#              "x": ,
#              "y": ,
#              "w": ,
#              "h":]}]
result = [];
count = 0; # is used to see the progression
for element_visual in data_image_visual:
    for element_coco in coco_annotations:
        if element_visual.get("coco_id") == element_coco.get("image_id"):
            new_result = {
                "id_coco": element_coco.get("image_id"),
                "id_visual": element_visual.get("image_id"),
                "description": element_coco.get("caption"),
                "caption": None #will be defined later
            }
            result.append(new_result);
            count = count+1;
            print(count)
for element_visual in data_image_visual:
    for element_coco in coco_train_annotations:
        if element_visual.get("coco_id") == element_coco.get("image_id"):
            new_result = {
                "id_coco": element_coco.get("image_id"),
                "id_visual": element_visual.get("image_id"),
                "description": element_coco.get("caption"),
                "caption": None #will be defined later
            }
            result.append(new_result);
            #count = count+1;
            #print(count)


#we will now compare each word of the caption with attributes in Visual Genome and record the position if there is a match
count2 = 0;
count3 = 0;
mult_check = 0;
for element in result:
    count2 = count2+1;
    new_caption = [];
    for objects_element in objects_visual:
        if objects_element.get("image_id") == element.get("id_visual"):
            objects_in_element = objects_element.get("objects");
            sentence = element.get("description").split();
            position = 0;
            for word in sentence:
                mult_check = 0;
                for objects_in_image in objects_in_element:
                    object_names = objects_in_image.get("names");
                    full_word = word;
                    for name in object_names:
                        nb_words = len(name.split());
                        if (position+nb_words-1)<len(sentence):
                            for i in range(position, (position+nb_words-1)):
                                full_word = full_word + " " + sentence[i+1];
                        full_word = full_word.replace('.','');# necessary because there is a dot with the last word of the sentences
                        if full_word == name:
                            count3 = count3 +1;
                            mult_check = 1;
                            new_caption.append({"word":full_word,
                                               "x":objects_in_image.get("x"),
                                               "y":objects_in_image.get("y"),
                                               "w":objects_in_image.get("w"),
                                               "h":objects_in_image.get("h")
                                               });
                        position = position +1;
                if mult_check == 0:
                    new_caption.append({"word": full_word,
                                        "x": -1,
                                        "y": -1,
                                        "w": 0,
                                        "h": 0
                                        });
    print(count2,"/",count," elements and ",count3," results found")
    element["caption"] = new_caption 
            
        

            

#we will now save the results as a json file
with open('result.json', 'w') as f:
    json.dump(result, f, indent=4)