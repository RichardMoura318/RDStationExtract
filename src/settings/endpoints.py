from datetime import datetime

def _default_period_params(start: datetime, end: datetime) -> dict:
    return {
        "start_date": start,
        "end_date": end
    }


ENDPOINTS_CONFIG = {
    "activities": {
        "sharepoint_list": "Activities",
        "paginated": True,
        "has_total": False,
        "period_params": _default_period_params
    },
    "campaigns": {
        "sharepoint_list": "Campaigns",
        "paginated": True,
        "has_total": True,
        "period_params": None
    },
    "contacts": {
        "sharepoint_list": "Contacts",
        "paginated": True,
        "has_total": True,
        "period_params": None
    },
    "custom_fields": {
        "sharepoint_list": "CustomFields",
        "paginated": False,
        "has_total": False,
        "period_params": None
    },
    "deal_lost_reasons": {
        "sharepoint_list": "DealLostReasons",
        "paginated": True,
        "has_total": True,
        "period_params": None
    },
    "deal_pipelines": {
        "sharepoint_list": "DealPipelines",
        "paginated": False,
        "has_total": False,
        "period_params": None
    },
    "deal_sources": {
        "sharepoint_list": "DealSources",
        "paginated": True,
        "has_total": True,
        "period_params": None
    },
    "deal_stages": {
        "sharepoint_list": "DealStages",
        "paginated": True,
        "has_total": True,
        "period_params": None
    },
    "deals": {
        "sharepoint_list": "Deals",
        "paginated": True,
        "has_total": True,
        "next_page": True,
        "period_params": lambda start, end: {
            "created_at_period": True,
            "start_date": start,
            "end_date": end
        }
    },
    "organizations": {
        "sharepoint_list": "Organizations",
        "paginated": True,
        "has_total": True,
        "period_params": None
    },
    "products": {
        "sharepoint_list": "Products",
        "paginated": True,
        "has_total": True,
        "period_params": None
    },
    "tasks": {
        "sharepoint_list": "Tasks",
        "paginated": True,
        "has_total": True,
        "period_params": lambda start, end: {
            "date_start": start,
            "date_end": end
        }
    },
    "teams": {
        "sharepoint_list": "Teams",
        "paginated": False,
        "has_total": True,
        "period_params": None
    },
    "users": {
        "sharepoint_list": "Users",
        "paginated": False,
        "has_total": False,
        "period_params": None
    }
}