def format_message_with_placeholders(template: str, name: str, company: str) -> str:
    return template.format(recipient_name=name, company_name=company)