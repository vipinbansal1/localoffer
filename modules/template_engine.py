from jinja2 import Template
import pandas as pd

DEFAULT_TEMPLATE = "Hi {{name}}, today's special offer is: {{offer}}"

def render_messages(df: pd.DataFrame, template_str: str = DEFAULT_TEMPLATE):
    """
    Render personalized messages for each customer.
    Args:
        df: DataFrame with customer data (must have 'name', 'offer', etc.)
        template_str: Jinja2 template string
    Returns:
        List of dicts with phone and message
    """
    template = Template(template_str)
    messages = []

    for _, row in df.iterrows():
        msg = template.render(
            name=row["name"],
            offer=row["offer"],
            phone=row["phone"]
        )
        messages.append({"phone": row["phone"], "message": msg})

    return messages
