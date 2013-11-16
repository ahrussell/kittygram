from SimpleCV import *
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
import numpy as np

# labels = ['accordion', 'airplanes', 'anchor', 'ant', 'BACKGROUND_Google', 'barrel', 'bass', 'beaver', 'binocular', 'bonsai', 'brain', 'brontosaurus', 'buddha', 'butterfly', 'camera', 'cannon', 'car_side', 'cats', 'ceiling_fan', 'cellphone', 'chair', 'chandelier', 'cougar_body', 'cougar_face', 'crab', 'crayfish', 'crocodile', 'crocodile_head', 'cup', 'dalmatian', 'dollar_bill', 'dolphin', 'dragonfly', 'electric_guitar', 'elephant', 'emu', 'euphonium', 'ewer', 'Faces', 'Faces_easy', 'ferry', 'flamingo', 'flamingo_head', 'garfield', 'gerenuk', 'gramophone', 'grand_piano', 'hawksbill', 'headphone', 'hedgehog', 'helicopter', 'ibis', 'inline_skate', 'joshua_tree', 'kangaroo', 'ketch', 'lamp', 'laptop', 'Leopards', 'llama', 'lobster', 'lotus', 'mandolin', 'mayfly', 'menorah', 'metronome', 'minaret', 'Motorbikes', 'nautilus', 'octopus', 'okapi', 'pagoda', 'panda', 'pigeon', 'pizza', 'platypus', 'pyramid', 'revolver', 'rhino', 'rooster', 'saxophone', 'schooner', 'scissors', 'scorpion', 'sea_horse', 'snoopy', 'soccer_ball', 'stapler', 'starfish', 'stegosaurus', 'stop_sign', 'strawberry', 'sunflower', 'tick', 'trilobite', 'umbrella', 'watch', 'water_lilly', 'wheelchair', 'wild_cat', 'windsor_chair', 'wrench', 'yin_yang']
# 
# labels = ["n","c"]
# paths = ["test/"+l for l in labels]
# 
# n = cv.ImageSet()
# n.load("test/n")
# 
# c = cv.ImageSet()
# t = c.load("test/c")
# 
# classifier = cv.TreeClassifier([cv.HaarLikeFeatureExtractor()])
# 
# classifier.train(paths,labels,-1,"trained")


target_names = ['noncats', 'cats']

print 'Loading Dogs for Training'
bolts = ImageSet('supervised/planes') #Load Bolts for training
bolt_blobs = [b.findBlobs()[0] for b in bolts] #exact the blobs for our features
tmp_data = [] #array to store data features
tmp_target = [] #array to store targets

for b in bolt_blobs: #Format Data for SVM
    tmp_data.append([b.area(), b.height(), b.width()])
    tmp_target.append(0)

print 'Loading Cats for Training'
nuts = ImageSet('supervised/cats')
nut_blobs = [n.invert().findBlobs()[0] for n in nuts]
for n in nut_blobs:
    tmp_data.append([n.area(), n.height(), n.width()])
    tmp_target.append(1)

dataset = np.array(tmp_data)
targets = np.array(tmp_target)

print 'Training Machine Learning'
clf = LinearSVC()
clf = clf.fit(dataset, targets)
clf2 = LogisticRegression().fit(dataset, targets)

a_d = 0
a_c = 0

print 'Running prediction on dogs now'
untrained_bolts = ImageSet('unsupervised/planes')
unbolt_blobs = [b.findBlobs()[0] for b in untrained_bolts]
for b in unbolt_blobs:
    ary = [b.area(), b.height(), b.width()]
    name = target_names[clf.predict(ary)[0]]
    probability = clf2.predict_proba(ary)[0]
    img = b.image
    img.drawText(name)
    print "Predicted:",name,", Guess:",probability[0], target_names[0],",", probability[1], target_names[1]

print
print
print 'Running prediction on cats now'
untrained_nuts = ImageSet('unsupervised/cats')
unnut_blobs = [n.invert().findBlobs()[0] for n in untrained_nuts]
for n in unnut_blobs:
    ary = [n.area(), n.height(), n.width()]
    name = target_names[clf.predict(ary)[0]]
    probability = clf2.predict_proba(ary)[0]
    img = n.image
    img.drawText(name)
    print "Predicted:",name,", Guess:",probability[0], target_names[0],",", probability[1], target_names[1]



