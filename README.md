This is the model of Image Captioning and the database manipulation code implemented for the Master Thesis "Improving Image Captioning with Dense Annotation".
The model in based on the existing model:
https://github.com/sgrvinod/a-PyTorch-Tutorial-to-Image-Captioning

The required files are to run this model are:
From the MS COCO library:
- captions_train2017.json
- captions_val2017.json

From the Visual Genome library:
- objects.json
- image_data.json

These files can be found on their website:
http://cocodataset.org/#download
https://visualgenome.org/api/v0/api_home.html


Since it uses its own database, DatabaseManipulation.py must be run at first. Then, createInputFiles.py will prepare the data for the training.
After these 2 codes, you can run train.py. Some checkpoints are saved during the training so it can be resume from them.

When the training is completed, you can caption an image with the following command:

python caption.py --img='path/to/image.jpeg' --model='path/to/BEST_checkpoint_coco_5_cap_per_img_5_min_word_freq.pth.tar' --word_map='path/to/WORDMAP_coco_5_cap_per_img_5_min_word_freq.json' --beam_size=5
