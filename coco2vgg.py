"""
Script de conversion des annotations au format COCO en annotations au format VGG Image Annotator (VIA).

Ce script prend un fichier d'annotations COCO JSON en entrée et génère un fichier d'annotations VIA JSON en sortie.
Les annotations VIA sont formatées pour représenter les polygones des boîtes englobantes.

Utilisation:
1. Assurez-vous d'avoir le fichier COCO JSON d'annotations à convertir.
2. Modifiez les chemins d'accès aux fichiers en remplaçant les valeurs des variables coco_json_path et vgg_json_path.
3. Exécutez le script.

Le fichier VIA résultant peut être utilisé avec le logiciel VIA (https://www.robots.ox.ac.uk/~vgg/software/via/) pour l'annotation d'images.

Auteur: Ikram MESBAH
Date: 05/02/2024
"""

import os
import json

def coco_to_vgg(coco_data):
    vgg_data = {}

    for image_info in coco_data["images"]:
        image_id = image_info["id"]
        image_width = image_info["width"]
        image_height = image_info["height"]
        image_file_name = image_info["file_name"]
        
        vgg_data[image_file_name] = {
            "filename": image_file_name,
            "size": image_width * image_height,
            "regions": [],
            "file_attributes": {}
        }

        for annotation in coco_data["annotations"]:
            if annotation["image_id"] == image_id:
                category_id = annotation["category_id"]
                segmentations = annotation["segmentation"]

                for segmentation in segmentations:
                    all_points_x = segmentation[::2]
                    all_points_y = segmentation[1::2]

                    vgg_data[image_file_name]["regions"].append({
                        "shape_attributes": {
                            "name": "polygon",
                            "all_points_x": all_points_x,
                            "all_points_y": all_points_y
                        },
                        "region_attributes": {"class": category_id}
                    })

    return vgg_data

def convert_coco_to_vgg(coco_json_path, vgg_json_path):
    with open(coco_json_path, 'r') as coco_file:
        coco_data = json.load(coco_file)

    vgg_data = coco_to_vgg(coco_data)

    with open(vgg_json_path, 'w') as vgg_file:
        json.dump(vgg_data, vgg_file, indent=2)

    print(f"Conversion terminée. Les données Vgg sont enregistrées dans {vgg_json_path}")



if __name__ == "__main__":
    coco_json_path = r"C:\Users\mesbahi\Documents\APA\datasets\valid\labels\output_valid.json"
    vgg_json_path = r"C:\Users\mesbahi\Documents\APA\datasets\valid\labels\vgg_annotations.json"

    convert_coco_to_vgg(coco_json_path, vgg_json_path)
