def test(query_wiz_api):
    query = ("""
        query GraphSearch($query: GraphEntityQueryInput, $controlId: ID, $projectId: String!, $first: Int, $after: String, $fetchTotalCount: Boolean!, $quick: Boolean = true, $fetchPublicExposurePaths: Boolean = false, $fetchInternalExposurePaths: Boolean = false, $fetchIssueAnalytics: Boolean = false, $fetchLateralMovement: Boolean = false, $fetchKubernetes: Boolean = false) {
        graphSearch(
            query: $query
            controlId: $controlId
            projectId: $projectId
            first: $first
            after: $after
            quick: $quick
        ) {
            totalCount @include(if: $fetchTotalCount)
            maxCountReached @include(if: $fetchTotalCount)
            pageInfo {
            endCursor
            hasNextPage
            }
            nodes {
            entities {
                ...PathGraphEntityFragment
                userMetadata {
                isInWatchlist
                isIgnored
                note
                }
                technologies {
                id
                icon
                }
                publicExposures(first: 10) @include(if: $fetchPublicExposurePaths) {
                nodes {
                    ...NetworkExposureFragment
                }
                }
                otherSubscriptionExposures(first: 10) @include(if: $fetchInternalExposurePaths) {
                nodes {
                    ...NetworkExposureFragment
                }
                }
                otherVnetExposures(first: 10) @include(if: $fetchInternalExposurePaths) {
                nodes {
                    ...NetworkExposureFragment
                }
                }
                lateralMovementPaths(first: 10) @include(if: $fetchLateralMovement) {
                nodes {
                    id
                    pathEntities {
                    entity {
                        ...PathGraphEntityFragment
                    }
                    }
                }
                }
                kubernetesPaths(first: 10) @include(if: $fetchKubernetes) {
                nodes {
                    id
                    path {
                    ...PathGraphEntityFragment
                    }
                }
                }
            }
            aggregateCount
            }
        }
        }
        
            fragment PathGraphEntityFragment on GraphEntity {
        id
        name
        type
        properties
        issueAnalytics: issues(filterBy: {status: [IN_PROGRESS, OPEN]}) @include(if: $fetchIssueAnalytics) {
            highSeverityCount
            criticalSeverityCount
        }
        }
        

            fragment NetworkExposureFragment on NetworkExposure {
        id
        portRange
        sourceIpRange
        destinationIpRange
        path {
            ...PathGraphEntityFragment
        }
        applicationEndpoints {
            ...PathGraphEntityFragment
        }
        }
    """)

    # The variables sent along with the above query
    variables = {
        "quick": True,
        "fetchPublicExposurePaths": True,
        "fetchInternalExposurePaths": False,
        "fetchIssueAnalytics": False,
        "fetchLateralMovement": True,
        "fetchKubernetes": False,
        "first": 50,
        "query": {
            "type": [
            "VIRTUAL_MACHINE"
            ],
            "select": True,
            "where": {
            "name": {
                "CONTAINS": [
                "SB"
                ]
            }
            },
            "relationships": [
            {
                "type": [
                {
                    "type": "SERVES"
                }
                ],
                "with": {
                "type": [
                    "ENDPOINT"
                ],
                "select": True
                }
            }
            ]
        },
        "projectId": "*",
        "fetchTotalCount": False
    }

    #Look for at least 1 app endpoint on SB
    result = query_wiz_api(query,variables)

    print("\n====Does SB have an app endpoint?====\n")
    results_count = len(result['data']['graphSearch']['nodes'])

    if results_count == 0:
        message = ("\nCHECK FAILED: No app endpoints found on SB \nhttps://demo.wiz.io/graph#~(query~(type~(~'VIRTUAL_MACHINE)~select~true~where~(name~(CONTAINS~(~'SB)))~relationships~(~(type~(~(type~'SERVES))~with~(type~(~'ENDPOINT)~select~true)))))\n")    
        print(message) 
    else:           
        print("SB has mongo running, a lateral movement finding, and a guard duty finding")

    try:
        return message
    except:
        return