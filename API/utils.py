import pickle


def load_model(model_file):
    with open(model_file, 'rb') as file:
        model = pickle.load(file)
    return model
