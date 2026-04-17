"""Allow `python -m maithili_dsl <file.dmai>` invocation."""
from maithili_dsl.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
