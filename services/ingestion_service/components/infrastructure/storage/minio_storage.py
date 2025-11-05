from minio import Minio
from minio.error import S3Error


class MinioStorage:

    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket: str,
        secure: bool = False
    ):
        self._client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        self._bucket = bucket
        if not self._client.bucket_exists(bucket):
            self._client.make_bucket(bucket)

    def upload(self, local_path: str, object_key: str) -> str:
        self._client.fput_object(
            self._bucket, object_key, local_path, content_type="image/jpeg"
        )
        # For alpha: presign GET for 7 days
        url = self._client.get_presigned_url("GET", self._bucket, object_key)
        return url
