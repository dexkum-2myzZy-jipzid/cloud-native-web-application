from flask import Blueprint, jsonify
import requests

metadata_bp = Blueprint("metadata", __name__, url_prefix="/v2")


def get_metadata_v1(path):
    url = f"http://169.254.169.254/latest/meta-data/{path}"
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"failed to fetch metadata IMDSv1 {e}")
        return None


instance_id = get_metadata_v1("instance-id")
az_id = get_metadata_v1("placement/availability-zone-id")


@metadata_bp.route("/metadata", methods=["GET"])
def metadata():
    return jsonify(
        {
            "aws_instance_id": instance_id,
            "aws_availability_zone_id": az_id,
        }
    )
