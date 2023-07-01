from typing import Any, Optional, List, Dict, Tuple
from pydantic import BaseSettings, validator


LINE_DELIMITER = "|"
NAME_PRICE_DELIMITER = ";"


class Settings(BaseSettings):
    """Application settings, cors, paths"""

    # supplier
    SUPPLIER_NAME: str
    SUPPLIER_ADDRESS_LINES: List[str]
    SUPPLIER_IC: str
    SUPPLIER_INFO_LINES: List[str]
    SUPPLIER_ISSUED_BY_LINES: List[str]

    # customer
    CUSTOMER_NAME: str
    CUSTOMER_ADDRESS_LINES: List[str]
    CUSTOMER_IC: str
    CUSTOMER_INFO_LINES: List[str]

    # naming
    INVOICE_NO_SUFFIX: Optional[str]

    @validator("INVOICE_NO_SUFFIX")
    @classmethod
    def default_invoice_no_suffix(cls, v: Optional[str], values: Dict[str, str]) -> str:
        if isinstance(v, str):
            return v
        return f"-{values.get('CUSTOMER_IC')}-01"

    # bank details
    BANK_CONNECTION_NAME: str
    BANK_ACCOUNT_NO: str
    BANK_PAYMENT_REF_NO: Optional[str]
    BANK_IBAN: Optional[str]
    BANK_SWIFT: Optional[str]

    # invoice details
    PROJECTS: List[Tuple[str, float]]

    class Config:
        env_file = ".env"

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            # converts `str` to `List[str]`
            if field_name.endswith("_LINES"):
                return raw_val.split(LINE_DELIMITER)

            # converts `str` to `List[tuple[str, float]]`
            if field_name == "PROJECTS":
                return [
                    (name, price)
                    for (name, price) in (
                        line.strip().split(NAME_PRICE_DELIMITER)
                        for line in raw_val.split(LINE_DELIMITER)
                    )
                ]

            return cls.json_loads(raw_val)


config = Settings()
