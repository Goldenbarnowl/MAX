from aiomax import ContactAttachment, User


def fixed_from_json(data: dict) -> "ContactAttachment | None":
    if not data:
        return None
    payload = data.get("payload") or {}
    return ContactAttachment(
        name=payload.get("name"),
        contact_id=payload.get("contact_id"),
        vcf_info=payload.get("vcf_info"),
        vcf_phone=payload.get("vcf_phone"),
        max_info=User.from_json(payload.get("max_info")),
    )