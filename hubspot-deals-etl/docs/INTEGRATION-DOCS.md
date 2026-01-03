# 📋 hubspot-deals-etl - Integration with HubSpot API

This document explains the HubSpot REST API endpoints required by the hubspot-deals-etl service to extract deal data from HubSpot instances.

---

## 📋 Overview

The hubspot-deals-etl service integrates with HubSpot REST API endpoints to extract deal information. Below are the required and optional endpoints:

### ✅ **Required Endpoint (Essential)**
| **API Endpoint**              | **Purpose**                 | **Version** | **Required Permissions**       | **Usage**    |
|------------------------------|-----------------------------|-------------|--------------------------------|--------------|
| `/crm/v3/objects/deals`      | Search and list deals       | v3          | crm.objects.deals.read         | **Required** |

### 🔧 **Optional Endpoints (Advanced Features)**
| **API Endpoint**                          | **Purpose**                       | **Version** | **Required Permissions**       | **Usage**  |
|------------------------------------------|-----------------------------------|-------------|--------------------------------|------------|
| `/crm/v3/objects/deals/{dealId}`          | Get detailed deal information     | v3          | crm.objects.deals.read         | Optional   |

### 🎯 **Recommendation**
**Start with only the required endpoint.** The `/crm/v3/objects/deals` endpoint provides all essential deal data needed for basic deal analytics and extraction.

---

## 🔐 Authentication Requirements

### **Private App Access Token Authentication**
```http
Authorization: Bearer <HUBSPOT_PRIVATE_APP_ACCESS_TOKEN>
Content-Type: application/json
```

### **Required Permissions**
- **crm.objects.deals.read**: Allows read access to HubSpot deal records
- **crm.schemas.deals.read**: Allows reading deal schema metadata (optional but safe)

---

## 🌐 HubSpot API Endpoints

### 🎯 **PRIMARY ENDPOINT (Required for Basic Deal Extraction)**

### 1. **Search Deals** - `/crm/v3/objects/deals` ✅ **REQUIRED**

**Purpose**: Get paginated list of all deals – **THIS IS ALL YOU NEED FOR BASIC DEAL EXTRACTION**

**Method**: `GET`

**URL**: `https://api.hubapi.com/crm/v3/objects/deals`

**Query Parameters**:
```
?limit=100&after=<cursor>&properties=<comma_separated_properties>
```

**Request Example**:

**Request Example**:
```http
GET https://api.hubapi.com/crm/v3/objects/deals?limit=100
Authorization: Bearer <HUBSPOT_PRIVATE_APP_ACCESS_TOKEN>
Content-Type: application/json
```

**Response Structure** (Contains ALL essential deal data):
```json
{
  "pagination_start": 0,
  "pagination_size": 50,
  "pagination_total": 75,
  "pagination_last": false,
  "data_array": [
    {
      "deal_id": "123456",
      "deal_url": "https://app.hubspot.com/contacts/deal/123456",
      "deal_name": "Enterprise Deal",
      "deal_stage": "closedwon",
      "deal_properties": {
        "dealname": "Enterprise Deal",
        "amount": "50000",
        "pipeline": "default",
        "closedate": "2024-06-30",
        "createdate": "2024-06-01T10:00:00Z"
      }
    },
    {
      "deal_id": "789012",
      "deal_url": "https://app.hubspot.com/contacts/deal/789012",
      "deal_name": "Mid-Market Deal",
      "deal_stage": "presentationscheduled",
      "deal_properties": {
        "dealname": "Mid-Market Deal",
        "amount": "25000",
        "pipeline": "default",
        "closedate": "2024-07-15",
        "createdate": "2024-06-05T09:30:00Z"
      }
    }
  ]
}
```

**✅ This endpoint provides ALL the default deal fields:**
- Deal name, amount, deal stage
- Deal URL
- Deal properties with pipeline, close date, and owner
- Creation and update timestamps
- Deal ID for referencing related CRM data

**Rate Limit**: 150 requests per 10 seconds

---

## 🔧 **OPTIONAL ENDPOINTS (Advanced Features Only)**

> **⚠️ Note**: These endpoints are NOT required for basic deal extraction. Only implement if you need advanced deal analytics like pipeline analysis, stage history tracking, or deal enrichment.

### 2. **Get Deal Details** - `/crm/v3/objects/deals/{dealId}` 🔧 **OPTIONAL**

**Purpose**: Get detailed information for a specific deal

**When to use**: Only if you need additional deal metadata not available in search

**Method**: `GET`

**URL**: `https://api.hubapi.com/crm/v3/objects/deals/{dealId}`

**Request Example**:
```http
GET https://api.hubapi.com/crm/v3/objects/deals/123456
Authorization: Bearer <HUBSPOT_PRIVATE_APP_ACCESS_TOKEN>
Content-Type: application/json
```

**Response Structure**:
```json
{
  "deal_id": "123456",
  "deal_url": "https://app.hubspot.com/contacts/deal/123456",
  "deal_name": "Enterprise Deal",
  "deal_type": "sales_deal",
  "associations": {
    "contacts": [
      {
        "contact_id": "98765",
        "contact_email": "john.doe@example.com",
        "primary": true
      }
    ],
    "companies": [
      {
        "company_id": "54321",
        "company_name": "Example Corp"
      }
    ]
  },
  "deal_properties": {
    "dealname": "Enterprise Deal",
    "amount": "50000",
    "dealstage": "closedwon",
    "pipeline": "default",
    "closedate": "2024-06-30"
  },
  "archived": false,
  "deleted": false,
  "is_active": true
}
```

---

### 3. **Get Deal Related Data** - `/crm/v3/objects/deals/{dealId}/associations` 🔧 **OPTIONAL**

**Purpose**: Get related data associated with a deal

**When to use**: Only if you need related data analysis and specific CRM metrics

**Method**: `GET`

**URL**: `https://api.hubapi.com/crm/v3/objects/deals/{dealId}/associations`

**Query Parameters**:
```
?limit=100&after=<cursor>&associationType=<type>
```

**Request Example**:
```http
GET https://api.hubapi.com/crm/v3/objects/deals/123456/associations?limit=100
Authorization: Bearer <HUBSPOT_PRIVATE_APP_ACCESS_TOKEN>
Content-Type: application/json
```

**Response Structure**:
```json
{
  "pagination_start": 0,
  "pagination_size": 50,
  "pagination_total": 25,
  "pagination_last": false,
  "data_array": [
    {
      "related_id": "98765",
      "related_url": "https://app.hubspot.com/contacts/contact/98765",
      "related_status": "associated",
      "related_name": "John Doe",
      "date_start": "2024-06-01T10:00:00Z",
      "date_end": "2024-06-30T23:59:59Z",
      "date_complete": "2024-06-15T12:00:00Z",
      "date_created": "2024-06-01T10:00:00Z",
      "origin_field": "123456",
      "description_field": "Primary contact associated with the deal"
    },
    {
      "related_id": "54321",
      "related_url": "https://app.hubspot.com/contacts/company/54321",
      "related_status": "associated",
      "related_name": "Example Corp",
      "date_start": "2024-06-01T10:00:00Z",
      "date_end": "2024-07-01T23:59:59Z",
      "date_created": "2024-06-01T10:05:00Z",
      "origin_field": "123456",
      "description_field": "Company associated with the deal"
    }
  ]
}
```

---

### 4. **Get Deal Configuration** - `/crm/v3/pipelines/deals/{pipelineId}` 🔧 **OPTIONAL**

**Purpose**: Get deal configuration details (pipelines, stages, and stage properties)

**When to use**: Only if you need pipeline workflow and deal setup analysis

**Method**: `GET`

**URL**: `https://api.hubapi.com/crm/v3/pipelines/deals/{pipelineId}`

**Request Example**:
```http
GET https://api.hubapi.com/crm/v3/pipelines/deals/123456
Authorization: Bearer <HUBSPOT_PRIVATE_APP_ACCESS_TOKEN>
Content-Type: application/json
```

**Response Structure**:
```json
{
  "pipeline_id": "123456",
  "pipeline_name": "Sales Pipeline",
  "pipeline_type": "deal_pipeline",
  "pipeline_url": "https://app.hubspot.com/settings/pipelines/deals/123456",
  "pipeline_location": {
    "location_type": "account",
    "location_identifier": "hubspot_account"
  },
  "pipeline_filter": {
    "filter_id": "active",
    "filter_url": "https://api.hubapi.com/crm/v3/pipelines/deals?archived=false"
  },
  "pipeline_configuration": {
    "stages": [
      {
        "stage_name": "Qualified",
        "stage_values": [
          {
            "stage_id": "qualified",
            "stage_url": "https://api.hubapi.com/crm/v3/pipelines/deals/stages/qualified"
          }
        ]
      },
      {
        "stage_name": "Presentation Scheduled",
        "stage_values": [
          {
            "stage_id": "presentationscheduled",
            "stage_url": "https://api.hubapi.com/crm/v3/pipelines/deals/stages/presentationscheduled"
          }
        ]
      },
      {
        "stage_name": "Closed Won",
        "stage_values": [
          {
            "stage_id": "closedwon",
            "stage_url": "https://api.hubapi.com/crm/v3/pipelines/deals/stages/closedwon"
          }
        ]
      }
    ],
    "constraint_type": "sequential_stages"
  },
  "pipeline_estimation": {
    "estimation_type": "probability_based",
    "estimation_details": {
      "detail_id": "win_probability",
      "detail_name": "Deal Stage Win Probability"
    }
  }
}
```

---

### 5. **Get Deal Additional Data** - `/crm/v3/objects/deals/{dealId}/associations/{objectType}` 🔧 **OPTIONAL**

**Purpose**: Get additional data for a deal

**When to use**: Only if you need additional data analysis and specific CRM functionality

**Method**: `GET`

**URL**: `https://api.hubapi.com/crm/v3/objects/deals/{dealId}/associations/{objectType}`

**Query Parameters**:
```
?limit=100&after=<cursor>&archived=false&fields=hs_object_id,createdAt,updatedAt,archived
```

**Request Example**:
```http
GET https://api.hubapi.com/crm/v3/objects/deals/123456/associations/contacts?limit=100
Authorization: Bearer <HUBSPOT_PRIVATE_APP_ACCESS_TOKEN>
Content-Type: application/json
```

**Response Structure**:
```json
{
  "pagination_start": 0,
  "pagination_size": 50,
  "pagination_total": 120,
  "data_key": [
    {
      "item_id": "98765",
      "item_key": "CONTACT-98765",
      "item_url": "https://app.hubspot.com/contacts/contact/98765",
      "item_fields": {
        "summary_field": "Primary contact associated with the deal",
        "status_field": {
          "status_id": "associated",
          "status_name": "Associated",
          "status_category": {
            "category_id": 1,
            "category_key": "active",
            "category_color": "green"
          }
        },
        "assignee_field": {
          "assignee_id": "112233",
          "assignee_name": "Sales Owner"
        },
        "priority_field": {
          "priority_id": "high",
          "priority_name": "High"
        }
      }
    }
  ]
}
```

---

## 📊 Data Extraction Flow

### 🎯 **SIMPLE FLOW (Recommended - Using Only Required Endpoint)**

### **Single Endpoint Approach - `/crm/v3/objects/deals` Only**
```python
def extract_all_deals_simple():
    """Extract all deals using only the /crm/v3/objects/deals endpoint"""
    after = None
    batch_size = 100
    all_deals = []
    
    while True:
        response = requests.get(
            f"{base_url}/crm/v3/objects/deals",
            params={
                "after": after,
                "limit": batch_size
            },
            headers=auth_headers
        )
        
        data = response.json()
        deals = data.get("results", [])
        
        if not deals:  # No more deals
            break
            
        all_deals.extend(deals)
        
        # Check if this is the last page
        paging = data.get("paging")
        if not paging:
            break
            
        after = paging["next"]["after"]
    
    return all_deals

# This gives you ALL essential deal data:
# - deal ID, deal name, deal stage
# - deal properties such as amount, pipeline, closedate
# - deal URL for reference
```

---

### 🔧 **ADVANCED FLOW (Optional - Multiple Endpoints)**

> **⚠️ Only use this if you need related data, configuration, or additional data**

### **Step 1: Batch Deal Retrieval**
```python
# Get deals in batches
for _ in range(total_deals):
    response = requests.get(
        f"{base_url}/crm/v3/objects/deals",
        params={
            "limit": 100,
            "after": after
        },
        headers=auth_headers
    )
    deals_data = response.json()
    deals = deals_data.get("results", [])
```

### **Step 2: Enhanced Deal Details (Optional)**
```python
# Get detailed information for each deal
for deal in deals:
    response = requests.get(
        f"{base_url}/crm/v3/objects/deals/{deal['id']}",
        headers=auth_headers
    )
    detailed_deal = response.json()
```

### **Step 3: Deal Related Data (Optional)**
```python
# Get related data for each deal
for deal in deals:
    if deal.get("id"):
        response = requests.get(
            f"{base_url}/crm/v3/objects/deals/{deal['id']}/associations",
            params={"limit": 50},
            headers=auth_headers
        )
        deal_related_data = response.json()
```

### **Step 4: Deal Configuration (Optional)**
```python
# Get configuration for each deal
for deal in deals:
    response = requests.get(
        f"{base_url}/crm/v3/pipelines/deals/{deal['properties']['pipeline']}",
        headers=auth_headers
    )
    deal_config = response.json()
```

---

## ⚡ Performance Considerations

### **Rate Limiting**
- **Default Limit**: 150 requests per 10 seconds per API token
- **Burst Limit**: 150 requests per 10 seconds (short duration)
- **Best Practice**: Implement exponential backoff on HTTP 429 responses

### **Batch Processing**
- **Recommended Batch Size**: 100 deals per request
- **Concurrent Requests**: Max 1 parallel request (deals are complex objects)
- **Request Interval**: 100ms between requests to stay under rate limits

### **Error Handling**
```http
# Rate limit exceeded
HTTP/429 Too Many Requests
Retry-After: <retry_seconds>

# Authentication failed  
HTTP/401 Unauthorized

# Insufficient permissions
HTTP/403 Forbidden

# Deal not found
HTTP/404 Not Found
```

---

## 🔒 Security Requirements

### **API Token Permissions**

#### ✅ **Required (Minimum Permissions)**
```
Required Scopes:
- crm.objects.deals.read (for basic deal information)
```

#### 🔧 **Optional (Advanced Features)**
```
Additional Scopes (only if using optional endpoints):
- crm.objects.companies.read (for related data information)
- crm.schemas.deals.read (for deal configuration)
```

### **User Permissions**

#### ✅ **Required (Minimum)**
The API token user must have:
- **CRM Object Read** global permission
- **Deals Access** permission

#### 🔧 **Optional (Advanced Features)**
Additional permissions (only if using optional endpoints):
- **Pipeline Configuration Access** permission (for deal configuration details)
- **Associations Access** (for additional data access)

---

## 📈 Monitoring & Debugging

### **Request Headers for Debugging**
```http
Authorization: Bearer <HUBSPOT_PRIVATE_APP_ACCESS_TOKEN>
Content-Type: application/json
User-Agent: hubspot-deals-etl/1.0
X-Request-ID: deal-scan-001-batch-1
```

### **Response Validation**
```python
def validate_object_response(object_data):
    required_fields = ["deal_id", "deal_name", "deal_stage", "deal_properties"]
    for field in required_fields:
        if field not in object_data:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate deal type
    if object_data["deal_stage"] not in ["open", "closedwon", "closedlost"]:
        raise ValueError(f"Invalid deal stage: {object_data['deal_stage']}")
```

### **API Usage Metrics**
- Track requests per 10 seconds
- Monitor response times
- Log rate limit headers
- Track authentication failures

---

## 🧪 Testing API Integration

### **Test Authentication**
```bash
curl -X GET \
  "https://api.hubapi.com/crm/v3/objects/deals?limit=1" \
  -H "Authorization: Bearer <HUBSPOT_PRIVATE_APP_ACCESS_TOKEN>" \
  -H "Content-Type: application/json"
```

### **Test Deal Search**
```bash
curl -X GET \
  "https://api.hubapi.com/crm/v3/objects/deals?limit=5" \
  -H "Authorization: Bearer <HUBSPOT_PRIVATE_APP_ACCESS_TOKEN>" \
  -H "Content-Type: application/json"
```

### **Test Deal Details**
```bash
curl -X GET \
  "https://api.hubapi.com/crm/v3/objects/deals/123456" \
  -H "Authorization: Bearer <HUBSPOT_PRIVATE_APP_ACCESS_TOKEN>" \
  -H "Content-Type: application/json"
```

---

## 🚨 Common Issues & Solutions

### **Issue**: 401 Unauthorized
**Solution**: Verify Bearer token authentication and private app access token
```bash
curl -X GET "https://api.hubapi.com/crm/v3/objects/deals?limit=1" \
  -H "Authorization: Bearer <HUBSPOT_PRIVATE_APP_ACCESS_TOKEN>"
```

### **Issue**: 403 Forbidden
**Solution**: Check user has "CRM Object Read" and "Deals Access" permissions

### **Issue**: 429 Rate Limited
**Solution**: Implement retry with exponential backoff
```python
import time
import random

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)
    raise Exception("Max retries exceeded")
```

### **Issue**: Empty Deal List
**Solution**: Check if user has access to CRM pipelines with deal records

### **Issue**: Need Related Data/Configuration But Want to Keep It Simple**
**Solution**: Start with `/crm/v3/objects/deals` only. Add optional endpoints later if needed for advanced deal analytics

---

## 💡 **Implementation Recommendations**

### 🎯 **Phase 1: Start Simple (Recommended)**
1. Implement only `/crm/v3/objects/deals`
2. Extract basic deal data (deal_id, deal_name, deal_stage, deal_properties info)
3. This covers 90% of deal analytics needs

### 🔧 **Phase 2: Add Advanced Features (If Needed)**
1. Add `/crm/v3/objects/deals/{dealId}` for detailed deal information
2. Add `/crm/v3/objects/deals/{dealId}/associations` for related data analysis  
3. Add `/crm/v3/pipelines/deals/{pipelineId}` for pipeline workflow analysis
4. Add `/crm/v3/objects/deals/{dealId}/associations/{objectType}` for additional functionality

### ⚡ **Performance Tip**
- **Simple approach**: 1 API call per batch of deals
- **Advanced approach**: 1 + N API calls (N = number of deals for details)
- Start simple to minimize API usage and complexity!

---

## 📞 Support Resources

- **HubSpot API Documentation**: https://developers.hubspot.com/docs/api/crm/deals
- **Rate Limiting Guide**: https://developers.hubspot.com/docs/api/usage-details
- **Authentication Guide**: https://developers.hubspot.com/docs/api/private-apps
- **Deal Permissions Reference**: https://developers.hubspot.com/docs/api/crm/understanding-the-crm