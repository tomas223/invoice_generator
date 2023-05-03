import os
import click
import datetime
from logging import getLogger

logger = getLogger(__name__)

# from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader


from settings import config


# Define the Jinja2 environment & output directory
APP_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# jinja2
TEMPLATES_DIR = os.path.join(APP_ROOT_DIR, "templates")
jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=True)
# ouput
OUTPUT_DIR = os.path.join(APP_ROOT_DIR, "output")
TEMPLATE_FILE_NAME = "invoice_cz.html"


def save_output(content: str, file_name: str):
    file_path = os.path.join(OUTPUT_DIR, file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def format_date(date: datetime.date):
    return date.strftime("%d.%m.%Y")


# Define the render function
def render_invoice(template_name: str) -> tuple[str, str]:
    # Calculate the dates
    today = datetime.date.today()
    last_day_of_previous_month = datetime.date(
        today.year, today.month, 1
    ) - datetime.timedelta(days=1)

    issue_date = today
    service_delivery_date = last_day_of_previous_month
    payment_due_date = datetime.date(today.year, today.month, 15)

    if issue_date > payment_due_date:
        logger.warning("issue-date is after payment-due-date")

    # Generate invoice_no
    invoice_no = (
        f"{last_day_of_previous_month.strftime('%Y%m')}{config.INVOICE_NO_SUFFIX}"
    )
    price_summary = sum(x[1] for x in config.PROJECTS)

    # Render the template
    template = jinja_env.get_template(template_name)
    html_content = template.render(
        **config.dict(),
        bank_payment_ref_no=config.BANK_PAYMENT_REF_NO or config.CUSTOMER_IC,
        invoice_no=invoice_no,
        # bank_payment_ref_no=invoice_no,
        price_sum=price_summary,
        issue_date=format_date(issue_date),
        service_delivery_date=format_date(service_delivery_date),
        payment_due_date=format_date(payment_due_date),
    )

    return html_content, invoice_no


# Define the CLI interface
@click.command()
# @click.confirmation_option(prompt="Are you sure you want to generate the invoice?")
def cli():
    invoice_html, invoice_no = render_invoice(TEMPLATE_FILE_NAME)

    invoice_file_name = f"{invoice_no}.html"
    save_output(invoice_html, invoice_file_name)

    click.echo(f"Invoice '{invoice_file_name}' generated.")


if __name__ == "__main__":
    cli()
