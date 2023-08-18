import datetime

from app.models import ClusterStatus, RequestCount


def test_create_request_count():
    request_count = RequestCount(
        count=1000, cluster="test_cluster", time=datetime.datetime.now()
    )
    assert request_count.count == 1000
    assert request_count.cluster == "test_cluster"


def test_create_cluster_status():
    cluster_status = ClusterStatus(
        cluster="test_cluster", status=1, time=datetime.datetime.now()
    )

    assert cluster_status.cluster == "test_cluster"
    assert cluster_status.status == 1
