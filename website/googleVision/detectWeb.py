import os
from google.cloud import vision


'''
This script gets "Best guess label", and "10 entities" from web that is similar to our input.
Based on this result, we will try to extract the artwork title.
'''

def detect_web(path):
    client = vision.ImageAnnotatorClient()

    best_guesses = set()
    descrptions = set()
    filter_words = {"Gallery", "Museum", "Painting", "Art"}


    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.web_detection(image=image)
    annotations = response.web_detection

    if annotations.best_guess_labels:
        for label in annotations.best_guess_labels:
            best_guesses.add(label.label)
            # print(f"\nBest guess label: {label.label}")

    # if annotations.pages_with_matching_images:
    #     print(
    #         "\n{} Pages with matching images found:".format(
    #             len(annotations.pages_with_matching_images)
    #         )
    #     )

    #     for page in annotations.pages_with_matching_images:
    #         print(f"\n\tPage url   : {page.url}")

    #         if page.full_matching_images:
    #             print(
    #                 "\t{} Full Matches found: ".format(len(page.full_matching_images))
    #             )

    #             for image in page.full_matching_images:
    #                 print(f"\t\tImage url  : {image.url}")

    #         if page.partial_matching_images:
    #             print(
    #                 "\t{} Partial Matches found: ".format(
    #                     len(page.partial_matching_images)
    #                 )
    #             )

    #             for image in page.partial_matching_images:
    #                 print(f"\t\tImage url  : {image.url}")

    if annotations.web_entities:
        print("\n{} Web entities found: ".format(len(annotations.web_entities)))

        for entity in annotations.web_entities:
            if not any(filter_word in entity.description for filter_word in filter_words):
                descrptions.add(entity.description)

            # print(f"\n\tScore      : {entity.score}")
            # print(f"\tDescription: {entity.description}")

    # if annotations.visually_similar_images:
    #     print(
    #         "\n{} visually similar images found:\n".format(
    #             len(annotations.visually_similar_images)
    #         )
    #     )

    #     for image in annotations.visually_similar_images:
    #         print(f"\tImage url    : {image.url}")

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    # print(best_guesses)    
    # print(descrptions)

    return best_guesses, descrptions

    


if __name__ == "__main__":
    test_images = {"./images/marc_chagall/barber_shop.jpg", "./images/pablo_picasso/Pablo_Picasso_29.jpg", "./images/van_gogh/portrait.jpg", "./images/michelangelo/Michelangelo_1.jpg", "./images/van_gogh/Vincent_van_Gogh_63.jpg"}
    for img in test_images:
        detect_web(img)