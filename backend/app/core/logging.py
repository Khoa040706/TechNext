import logging
import sys

def setup_logging():
    log_format = "%(asctime)s [%(levelname)s] %(name)s (req_id=%(request_id)s): %(message)s"
    
    # Custom record factory to always have request_id
    old_factory = logging.getLogRecordFactory()
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        if not hasattr(record, "request_id"):
            record.request_id = "-"
        return record
    logging.setLogRecordFactory(record_factory)

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)],
    )

logger = logging.getLogger("nexttech")
