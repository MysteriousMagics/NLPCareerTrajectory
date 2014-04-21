import os
import nltk
import pickle
from career_trajectory_svm_new_0416 import unigram_features, bigram_features, tfidftransform


def feature_consolidation(resume_text, top_unigram_list, top_bigram_list):
    """
    Function to consolidate all the featuresets for the training data

    Args:
        top_unigram_list -- list of top unigrams from the training dataset
        top_bigram_list -- list of top bigrams from the training dataset

    Returns:
        consolidated_features -- list of consolidated features
    """
    uni_feats = [" ".join(unigram_features(resume_text, top_unigram_list))]
    bi_feats = [" ".join(bigram_features(resume_text, top_bigram_list))]
    consolidated_features = []
    ind = 0
    while ind < len(uni_feats):
        consolidated_features.append(uni_feats[ind] + bi_feats[ind])
        ind += 1
    return consolidated_features


def main():
    """
    Test the heldout dataset using the trained classifier and features
    """

    # Get the pickled classifier model and features
    with open('svmclassifier_new_0418_h_new.pkl', 'rb') as infile:
        model = pickle.load(infile)

    with open('features_0418_h_new.pkl', 'rb') as f:
        features = pickle.load(f)

    with open('label_names_0418_h_new.pkl', 'rb') as lab_names:
        labels_names = pickle.load(lab_names)

    with open('count_vect_0418_h_new.pkl', 'rb') as count_v:
        count_vect = pickle.load(count_v)

    top_unigrams = features['top_unigrams']
    top_bigrams = features['top_bigrams']

    resume_text = open('Grap.txt').read()

    # Create a featureset for the heldout data
    resume_featureset = feature_consolidation(resume_text, top_unigrams, top_bigrams)

    # predicted_score = model.predict(resume_featureset)
    # predicted_decision = model.decision_function(resume_featureset)

    resume_counts = count_vect.transform(resume_featureset)
    tfidf_test = tfidftransform(resume_counts)
    predicted_score = model.predict(tfidf_test)
    predicted_decision = model.decision_function(tfidf_test)

    predicted = []

    for i in range(1):
        predicted_dec_dup = predicted_decision[i]
        predicted_dec_dup_sorted = sorted(predicted_dec_dup, reverse=True)
        top_five_predictions = []
        predicted.append(labels_names[predicted_decision[i].tolist().index(predicted_dec_dup_sorted[0])])
        for j in range(5):
            top_five_predictions.append(labels_names[predicted_decision[i].tolist().index(predicted_dec_dup_sorted[j])])

        print "Predicted top5: " + ", ".join(top_five_predictions)



if __name__ == '__main__':
    main()