from re import S
import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np

class Face:
    def __init__(self, target_folder: str) -> None:
        self.cwd = os.getcwd()
        self.fpath = target_folder
        #self.encoded = self.get_encoded_faces()

    def get_encoded_faces(self):
        """
        looks through the faces folder and encodes all
        the faces

        :return: dict of (name, image encoded)
        """
        encoded = {}
        
        for fname in os.listdir(self.fpath):
            if fname.endswith(".jpg") or fname.endswith(".png"):
                face = fr.load_image_file(self.fpath + fname)
                encoding = fr.face_encodings(face)[0]
                encoded[fname.split(".")[0]] = encoding

        return encoded

    def classify_face(self, im):
        """
        will find all of the faces in a given image and label
        them if it knows what they are

        :param im: str of file path
        :return: list of face names
        """
        faces = self.get_encoded_faces()
        faces_encoded = list(faces.values())
        known_face_names = list(faces.keys())

        self.img = im
    
        self.face_locations = face_recognition.face_locations(self.img)
        unknown_face_encodings = face_recognition.face_encodings(self.img, self.face_locations)

        face_names = []
        for face_encoding in unknown_face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(faces_encoded, face_encoding)
            name = "Unknown"

            # use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

            for (top, right, bottom, left), name in zip(self.face_locations, face_names):
                # Draw a box around the face
                cv2.rectangle(self.img, (left-20, top-20), (right+20, bottom+20), (255, 0, 0), 2)

                # Draw a label with a name below the face
                cv2.rectangle(self.img, (left-20, bottom -15), (right+20, bottom+20), (255, 0, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(self.img, name, (left -20, bottom + 15), font, 1.0, (255, 255, 255), 2)

        if face_names != []:
            return self.img, face_names[0]
        else:
            return self.img, None

    def display_result(self):
        # Display the resulting image
        cv2.namedWindow("Result - press q to exit", cv2.WINDOW_NORMAL)
        img = cv2.resize(self.img, (0, 0), fx=0.4, fy=0.4)
        #img = img[:,:,::-1]
        
        while True:
            cv2.imshow("Result - press q to exit", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cv2.destroyAllWindows()


if __name__ == "__main__":
    path = os.getcwd() + "/main"
    classifier = Face(path)
    classifier.classify_face("main/students/Gitansh.jpg")
    classifier.display_result()

#print(classify_face("C:/Users/gitan/Desktop/Files/Programming/Face Recognition/face_rec/test.jpg"))