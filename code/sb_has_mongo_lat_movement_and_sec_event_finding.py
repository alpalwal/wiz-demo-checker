def test(query_wiz_api):
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
            "HOSTED_TECHNOLOGY"
            ],
            "select": True,
            "where": {
            "techId": {
                "EQUALS": "2021"
            }
            },
            "relationships": [
            {
                "type": [
                {
                    "type": "RUNS",
                    "reverse": True
                }
                ],
                "with": {
                "type": [
                    "VIRTUAL_MACHINE",
                ],
                "select": True,
                "relationships": [
                    {
                    "type": [
                        {
                        "type": "ALERTED_ON",
                        "reverse": True
                        }
                    ],
                    "with": {
                        "type": [
                        "LATERAL_MOVEMENT_FINDING"
                        ],
                        "select": True
                    }
                    },
                    {
                    "type": [
                        {
                        "type": "ALERTED_ON",
                        "reverse": True
                        }
                    ],
                    "with": {
                        "type": [
                        "SECURITY_EVENT_FINDING"
                        ],
                        "select": True
                    }
                    }
                ],
                "where": {
                    "_vertexID": {
                    "EQUALS": [
                        "36d7ac7f-4eb5-5586-8060-6636163f53ae"
                    ]
                    }
                }
                }
            }
            ]
        },
        "projectId": "*",
        "fetchTotalCount": False
        } 

    # The GraphQL query that defines which data you wish to fetch.
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


    #Look for critical/open issues on SB
    result = query_wiz_api(query,variables)

    print("\n====Does SB have mongo running, a lateral movement finding, and a guard duty finding?====\n")
    results_count = len(result['data']['graphSearch']['nodes'])

    if results_count != 1:
        message = "CHECK FAILED: Does SB have mongo running, a lateral movement finding, and a guard duty finding?\nThis query has an incorrect number of results. (1 expected)\nhttps://demo.wiz.io/graph#~(queryTitle~'Resources*20using*20MongoDB~query~(type~(~'HOSTED_TECHNOLOGY)~select~true~where~(techId~(EQUALS~'2021))~relationships~(~(type~(~(type~'RUNS~reverse~true))~with~(type~(~'CONTAINER_IMAGE~'VIRTUAL_MACHINE~'CONTAINER)~select~true~relationships~(~(type~(~(type~'ALERTED_ON~reverse~true))~with~(type~(~'LATERAL_MOVEMENT_FINDING)~select~true))~(type~(~(type~'ALERTED_ON~reverse~true))~with~(type~(~'SECURITY_EVENT_FINDING)~select~true)))~where~(_vertexID~(EQUALS~(~'36d7ac7f-4eb5-5586-8060-6636163f53ae))))))))"
        print(message)
    else:           
        print("All Good - SB has mongo running, a lateral movement finding, and a guard duty finding")

    try:
        return message
    except:
        return