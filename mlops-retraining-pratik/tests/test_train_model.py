from joblib import load

from training.train_model import (
    create_model,
    evaluate_model,
    load_dataset,
    split_dataset,
    train_and_save_model,
)


def test_dataset_is_loaded():
    features, target, target_names = load_dataset()

    assert features.shape == (150, 4)
    assert len(target) == 150
    assert len(target_names) == 3


def test_dataset_is_split():

    features, target, _ = load_dataset()

    train_features, test_features, train_target, test_target = split_dataset(
        features, target
    )

    assert len(train_features) == 120
    assert len(test_features) == 30


def test_model_can_be_trained():

    features, target, _ = load_dataset()

    train_features, test_features, train_target, test_target = split_dataset(
        features, target
    )

    # model oluştur ve eğit
    model = create_model()
    model.fit(train_features, train_target)

    # performans
    accuracy = evaluate_model(model, test_features, test_target)

    assert accuracy >= 0.8


def test_model_artifact_is_created(tmp_path):

    # test için geçici model yolu oluştur
    test_model_path = tmp_path / "iris_model.joblib"

    result = train_and_save_model(test_model_path)
    print(result)

    assert test_model_path.exists()

    # model paketini tekrar yükle
    model_bundle = load(test_model_path)

    assert "model" in model_bundle
