def test(query_wiz_api):
    # The variables sent along with the above query
    variables = {
        "first": 30,
        "filterBy": {
            "search": "36d7ac7f-4eb5-5586-8060-6636163f53ae",
            "severity": [
            "CRITICAL"
            ],
            "status": [
                "OPEN",
                "IN_PROGRESS"
            ],
            "relatedEntity": {}
        },
        "orderBy": {
            "field": "SEVERITY",
            "direction": "DESC"
        }
    }   

    # The GraphQL query that defines which data you wish to fetch.
    query = ("""
        query IssuesTable($filterBy: IssueFilters, $first: Int, $after: String, $orderBy: IssueOrder) {
            issues(filterBy: $filterBy, first: $first, after: $after, orderBy: $orderBy) {
            nodes {
                ...IssueDetails
            }
            pageInfo {
                hasNextPage
                endCursor
            }
            totalCount
            }
        }
        
            fragment IssueDetails on Issue {
            id
            control {
            id
            name
            query
            securitySubCategories {
                id
                category {
                id
                }
            }
            }
            createdAt
            updatedAt
            status
            severity
            entity {
            id
            name
            type
            }
            resolutionReason
            serviceTickets {
            id
            externalId
            name
            url
            }
        }
    """)

    
    #Look for critical/open issues on SB
    sb_issues_result = query_wiz_api(query,variables)

    # This is what we expect to see for issues on SB
    ## removing these temporaily
    # "Publicly exposed VM with a high/critical severity network vulnerability with a known exploit and sensitive data",
    # "Publicly facing VM instance with data access to sensitive data and high/critical severity network vulnerability with a known exploit",
    required_issues = [
        "Publicly exposed resource with high/critical severity network vulnerability with a known exploit and cleartext cloud keys with data access to sensitive data",
        "Publicly exposed VM instance with effective global admin permissions",
        "Publicly exposed VM with high privileges and high/critical severity network vulnerabilities with a known exploit",
        "Publicly exposed VM/serverless with a high/critical severity network vulnerability with a known exploit and data access to sensitive data"
    ]

    print("\n====Look for proper SB issues====\n")
    for required_issue in required_issues:
        matched_issue = False
        for issue in sb_issues_result['data']['issues']['nodes']:
            if issue['control']['name'] == required_issue:
                print("All Good - Found issue: " + required_issue)
                matched_issue = True 
                continue
        if matched_issue == False:
            message = "====Failed to find expected issue on SB instance:====\n" + required_issue
            print(message)
    
    try:
        return message
    except:
        return