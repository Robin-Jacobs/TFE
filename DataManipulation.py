import json
with open('annotations/captions_val2017.json') as json_data:
    data_coco = json.load(json_data);
with open('image_data.json') as json_data:
    data_image_visual = json.load(json_data);
with open('objects.json') as json_data:
    objects_visual = json.load(json_data);
coco_annotations = data_coco.get("annotations");
with open('annotations/captions_train2017.json') as json_data:
    data_train_coco = json.load(json_data);
coco_train_annotations = data_train_coco.get("annotations");

#output format:
#result = [{"id_coco": ,
#         "id_visual": ,
#         "height: ,
#         "width: ,
#         "mycaption:[
#             {"description": ,
#              "captions:[
#                 {"word": ,
#                  "x": ,
#                  "y": ,
#                  "w": ,
#                  "h":}]}],
#         "split": }]

result = [];
count = 0; # is used to see the progression
size_max = 24999 #maximum size of the database (-1) 
for element_visual in data_image_visual:
    if count > size_max:
        break
    descrip = []
    test_found = 0;
    for element_coco in coco_annotations:
        if element_visual.get("coco_id") == element_coco.get("image_id"):
            test_found = 1;
            descrip.append({"description":element_coco.get("caption"),"caption":None})
            new_result = {
                "id_coco": element_coco.get("image_id"),
                "id_visual": element_visual.get("image_id"),
                "width": element_visual.get("width"),
                "height": element_visual.get("height"),
                "mycaption":None,
                "split": None #will be defined later
            }         
    if test_found == 1:
        result.append(new_result);
        count = count+1;
        if count % 100 == 0:
            print("part 1 : ",count," elements")
        result[-1]['mycaption'] = descrip;
for element_visual in data_image_visual:
    if count > size_max:
        break
    descrip = []
    test_found = 0;
    for element_coco in coco_train_annotations:
        if element_visual.get("coco_id") == element_coco.get("image_id"):
            test_found = 1;
            descrip.append({"description":element_coco.get("caption"),"caption":None})
            new_result = {
                "id_coco": element_coco.get("image_id"),
                "id_visual": element_visual.get("image_id"),
                "width": element_visual.get("width"),
                "height": element_visual.get("height"),
                "mycaption":None,
                "split": None #will be defined later
            }
    if test_found == 1:
        count = count+1;
        if count % 250 == 0:
            print("part2 : ",count, " elements")
        result.append(new_result);
        result[-1]['mycaption'] = descrip;


#we will now compare each word of the caption with attributes in Visual Genome and record the position if there is a match
count2 = 0;
count3 = 0;
mult_check = 0;
for element in result:
    count2 = count2+1;
    
    if count2 < (count/20):
        element["split"] = "val"
    elif count2 < (count/10):
        element["split"] = "test"
    else:
        element["split"] = "train"
    for objects_element in objects_visual:
        if objects_element.get("image_id") == element.get("id_visual"):
            objects_in_element = objects_element.get("objects");
            for element_mycaption in element.get("mycaption"):
                new_caption = [];
                sentence = element_mycaption.get("description").split();
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
                                if mult_check ==0:
                                    count3 = count3 +1;
                                    new_caption.append({"word":full_word,
                                                       "x":objects_in_image.get("x"),
                                                       "y":objects_in_image.get("y"),
                                                       "w":objects_in_image.get("w"),
                                                       "h":objects_in_image.get("h")
                                                       });
                                mult_check = 1;
                            position = position +1;
                    if mult_check == 0:
                        new_caption.append({"word": full_word,
                                            "x": 0,
                                            "y": 0,
                                            "w": 0,
                                            "h": 0
                                            });
                if count2 % 500 == 0:
                    print(count2,"/",count," elements and ",count3," results found")
                element_mycaption["caption"] = new_caption 
            
        

            

#we will now save the results as a json file
with open('drive/My Drive/mydatabase.json', 'w') as f:
    json.dump(result, f, indent=4)