from utils import create_input_files

if __name__ == '__main__':
    # Create input files (along with word map)
    create_input_files(dataset='coco',
                       karpathy_json_path='drive/My Drive/mydatabase.json',#mettre la nouvelle database
                       image_folder='VG_100K/',
                       captions_per_image=5,
                       min_word_freq=5,
                       output_folder='drive/My Drive',
                       max_len=50)
