# input_metadata.json

Written by MOD001 for every upload, including a rejected one. A rejected upload has `stored_path: null` and no image file.

| Field | Type | Rule |
|---|---|---|
| input_id | string | `{case_id}-input-{seq}`, seq starting at 01. Never reused. |
| case_id | string | The case that owns the upload. |
| declared_filename | string | The name sent with the upload. |
| stored_path | string or null | Path of the stored image. Null when the upload was rejected. |
| byte_size | integer | Length of the uploaded bytes. |
| declared_format | string | Lowercase extension without the dot. |
| received_timestamp | string | ISO-8601. |
| status | string | `accepted` or `rejected`. |
| failure_id | string or null | MOD016 id when rejected. |
| limits | object | Present on accepted uploads: `min_edge`, `max_edge`, `max_bytes`. |

The image file is `original.{declared_format}` in the same directory. A later upload for the same case gets a new directory.
