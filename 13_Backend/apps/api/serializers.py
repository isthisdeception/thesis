"""DRF serializers for the canonical REST API contract (`13_Backend/api_spec/api_spec.md`)."""

from __future__ import annotations

import re

from rest_framework import serializers

MODEL_ID_PATTERN = re.compile(r"^MODEL\d{4}$")


class CaseCreateRequestSerializer(serializers.Serializer):
    model_id = serializers.CharField(required=False, allow_blank=False, max_length=32)
    configuration = serializers.CharField(
        required=False,
        allow_blank=False,
        max_length=128,
        default="rule_based/e4_calibrated_v1",
    )

    def validate_model_id(self, value: str) -> str:
        cleaned = value.strip()
        if not MODEL_ID_PATTERN.match(cleaned):
            raise serializers.ValidationError(f"model_id {cleaned!r} must match MODELxxxx")
        return cleaned


class CaseCreateResponseSerializer(serializers.Serializer):
    case_id = serializers.CharField()
    status = serializers.CharField()
    stage = serializers.CharField()
    model_id = serializers.CharField()
    configuration = serializers.CharField()
    created_timestamp = serializers.CharField()


class CaseDetailResponseSerializer(serializers.Serializer):
    case_id = serializers.CharField()
    status = serializers.CharField()
    stage = serializers.CharField()
    input_id = serializers.CharField(allow_null=True)
    evidence_ids = serializers.ListField(child=serializers.CharField())
    decision = serializers.CharField(allow_blank=True)
    model_id = serializers.CharField()
    version = serializers.CharField()
    configuration = serializers.CharField()
    execution_time_seconds = serializers.FloatField(allow_null=True)
    errors = serializers.ListField(child=serializers.CharField())
    warnings = serializers.ListField(child=serializers.CharField())
    timestamp = serializers.CharField()


class CaseUploadRequestSerializer(serializers.Serializer):
    file = serializers.FileField(required=True, allow_empty_file=True)


class CaseUploadResponseSerializer(serializers.Serializer):
    case_id = serializers.CharField()
    input_id = serializers.CharField(allow_null=True)
    intake = serializers.DictField()
    job_status = serializers.CharField()
    stage = serializers.CharField()


class CaseStatusResponseSerializer(serializers.Serializer):
    case_id = serializers.CharField()
    status = serializers.CharField()
    stage = serializers.CharField()
    stage_history = serializers.ListField(child=serializers.CharField())
    progress_percent = serializers.IntegerField()
    input_id = serializers.CharField(allow_null=True)
    failures = serializers.ListField(child=serializers.DictField())
    updated_timestamp = serializers.CharField()


class CaseEvidenceResponseSerializer(serializers.Serializer):
    case_id = serializers.CharField()
    evidence_ids = serializers.ListField(child=serializers.CharField())
    count = serializers.IntegerField()
    items = serializers.ListField(child=serializers.DictField())


class HealthResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    service = serializers.CharField()
    environment = serializers.CharField()
    checks = serializers.DictField(child=serializers.BooleanField())
    timestamp = serializers.CharField()


class VersionResponseSerializer(serializers.Serializer):
    system_version = serializers.CharField()
    api_version = serializers.CharField()
    model_id = serializers.CharField()
    model_version = serializers.CharField()
    dataset_id = serializers.CharField()
    experiment_id = serializers.CharField()
    git_commit = serializers.CharField()
    fusion_strategy_id = serializers.CharField()
    confidence_formula_id = serializers.CharField()
    timestamp = serializers.CharField()
