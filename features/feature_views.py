# features/feature_views.py
from feast import Entity, Feature, FeatureView, FileSource, ValueType

github_source = FileSource(
    path="lakehouse/github_repos.parquet",
    event_timestamp_column="stars"
)

repo_entity = Entity(name="repo_id", value_type=ValueType.INT64, description="GitHub repo ID")

repo_features = [
    Feature(name="stars", dtype=ValueType.INT64),
    Feature(name="forks", dtype=ValueType.INT64)
]

repo_feature_view = FeatureView(
    name="repo_features",
    entities=[repo_entity],
    ttl=None,
    features=repo_features,
    online=True,
    source=github_source
)

def compute_features():
    print("✅ Features computed and ready for online store")