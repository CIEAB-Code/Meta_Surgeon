from exif import Image, DATETIME_STR_FORMAT
from os import scandir
import argparse

parser = argparse.ArgumentParser(description="Remove exif data from JPEG image files.")
parser.add_argument('--directory', '-d', type=str, metavar='',
                    help="Enter path with / separators to directory containing JPEG files.")
parser.add_argument('--verbose', '-v', action='store_true',
                    help="Print dictionary of exif data before and after it is removed.")
parser.add_argument('--All', '-A', action='store_true',
                    help="Remove ALL exif data from JPEG files.")
parser.add_argument('--remove_gps', '-rg', action='store_true',
                    help="Delete GPS information from JPEG files")
parser.add_argument('--change_date', '-cd', type=str, metavar='',
                    help="Change data information of exif data, replace with argument given.")
parser.add_argument('--remove_saturation', '-rs', nargs=argparse.OPTIONAL,
                    help="Remove saturation data from JPEG files.")
args = parser.parse_args()


# Default values for argparse options
verbose = False
clear_all = False
clear_gps = False
clear_sat = False

mod_sat = False


# GET DATA FUNCTIONS

def get_files(path):
    try:
        images_path = []
        images = [image.name for image in scandir(path) if '.JPG' in image.name]
        for each_image in images:
            image_full_path = f"{path}/{each_image}"
            images_path.append(image_full_path)
        return images_path

    except Exception as e:
        print(e)
        return None


def get_meta(image_path):
    image = None
    with open(image_path, 'rb') as picture_file:
        image_bytes = picture_file.read()
    image = Image(image_bytes)
    return image


# DELETE DATA FUNCTIONS

def del_all_meta(image):
    image.delete_all()
    return image


def del_gps(image):
    # TO DO: Delete '_gps_ifd_pointer' also?
    gps_tags = ['gps_altitude', 'gps_altitude_ref', 'gps_datestamp', 'gps_dest_bearing', 'gps_dest_bearing_ref',
                'gps_horizontal_positioning_error', 'gps_img_direction', 'gps_img_direction_ref', 'gps_latitude',
                'gps_latitude_ref', 'gps_longitude','gps_longitude_ref', 'gps_speed', 'gps_speed_ref', 'gps_timestamp',
                '_gps_ifd_pointer']
    for gps_tag in gps_tags:
        if image.get(gps_tag):
            print('HAS:', gps_tag)
            del image[gps_tag]
    return image


def del_sat(image):
    sat_tag = 'saturation'
    if image.get([sat_tag]):
        del image[sat_tag]
    return image


# MODIFY DATA FUNCTIONS

def mod_saturation(image, sat_num):
    sat_tag = 'saturation'
    if image.get(sat_tag):
        print('SAT:', image[sat_tag])
        image[sat_tag] = sat_num
        print('SAT:', image[sat_tag])
    return image


# WRITE DATA FUNCTION

def write_file(final_image, image_path):
    with open(image_path, 'wb') as new_image_file:
        new_image_file.write(final_image.get_file())


if __name__ == '__main__':

    sat_num = 0
    rounds = 0

    # if directory to files provided
    if args.directory:
        # checking arguments given by user
        if args.verbose:
            verbose = True
        if args.All:
            clear_all = True
        if args.remove_gps:
            clear_gps = True
        if args.remove_saturation:
            sat_num = args.remove_saturation
            if sat_num == 'No':
                clear_sat = True
            else:
                mod_sat = True

        # get list of image file paths
        folder_path = args.directory
        image_paths = get_files(folder_path)
        print('LENGTH LIST', len(image_paths))
        # Iterate through each image and modify exif data
        for each in image_paths:
            rounds += 1
            print(rounds)
            # get meta data
            mod_image = get_meta(each)
            if rounds == 1:
                print(dir(mod_image))
            if clear_all:
                mod_image = del_all_meta(mod_image)
            if clear_gps:
                mod_image = del_gps(mod_image)
            if clear_sat:
                mod_image = del_sat(mod_image)
            if mod_sat:
                mod_image = mod_saturation(mod_image, sat_num)

            write_file(mod_image, each)

    else:
        print("Please enter path to directory of JPEG images using : '--directory' or '-d' ")
