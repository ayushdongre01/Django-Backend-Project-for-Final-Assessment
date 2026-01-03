def map_deal(deal):
    props = deal.get("properties", {})

    return {
        "deal_id": deal.get("id"),
        "deal_name": props.get("dealname"),
        "amount": props.get("amount"),
        "stage": props.get("dealstage"),
        "pipeline": props.get("pipeline"),
        "close_date": props.get("closedate"),
        "raw_payload": deal,
    }
