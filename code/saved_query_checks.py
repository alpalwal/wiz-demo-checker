def test(query_wiz_api):
    
    # The GraphQL query that defines which data you wish to fetch.
    query = ("""
        query SavedGraphQuery($id: ID!) {
        savedGraphQuery(id: $id) {
            id
            name
            description
            query
            project {
            id
            }
            securitySubCategories {
            id
            }
        }
        }
    """)

    # Look for each saved query to make sure it's there
    search_list = [
        { 
            "query_name": "Sree - Azure CDR demo - lateral movement + Security Event (Defender for Cloud)",
            "query_variable": {"id": "4c00dedf-4685-46e6-b154-4f7211884efb"},
            "query_link": "https://demo.wiz.io/graph#~(query~(relationships~(~(type~(~(reverse~true~type~'ALERTED_ON))~with~(select~true~type~(~'LATERAL_MOVEMENT_FINDING)))~(type~(~(reverse~true~type~'ALERTED_ON))~with~(select~true~type~(~'SECURITY_EVENT_FINDING)))~(type~(~(reverse~true~type~'ALERTED_ON))~with~(blockExpanded~false~blockName~'Has*20vulnerabilities~relationships~(~(type~(~(reverse~true~type~'CAUSES))~with~(type~(~'VULNERABILITY))))~select~true~type~(~'SECURITY_TOOL_FINDING)~where~(severity~(EQUALS~(~'VulnerabilitySeverityCritical~'VulnerabilitySeverityHigh~'VulnerabilitySeverityMedium~'VulnerabilitySeverityLow))))))~select~true~type~(~'VIRTUAL_MACHINE)~where~(_vertexID~(EQUALS~(~'9cba02bb-808c-520e-a2fa-e272952d08fe))~cloudPlatform~(EQUALS~(~'Azure)))))"
        },
        { 
            "query_name": "Sree - Azure DSPM demo",
            "query_variable": {"id": "624d0010-4786-4b6f-b8de-3ab0f2886018"},
            "query_link": "https://demo.wiz.io/graph#~(query~(as~'scoped_entity~relationships~(~(type~(~(type~'SERVES))~with~(select~true~type~(~'ENDPOINT)~where~(portValidationResult~(NOT_EQUALS~(~'Closed)))))~(type~(~(type~'ACTING_AS))~with~(relationships~(~(type~(~(reverse~true~type~'ENTITLES))~with~(blockExpanded~true~blockName~'Data*20Access~relationships~(~(type~(~(type~'ALLOWS_ACCESS_TO))~with~(select~true~type~(~'DATABASE~'DB_SERVER~'BUCKET))))~type~(~'IAM_BINDING)~where~(accessTypes~(EQUALS~(~'Data))))))~select~true~type~(~'SERVICE_ACCOUNT)))~(type~(~(reverse~true~type~'ALERTED_ON))~with~(select~true~type~(~'SECURITY_TOOL_FINDING))))~select~true~type~(~'VIRTUAL_MACHINE)~where~(accessibleFrom.internet~(EQUALS~true)~cloudPlatform~(EQUALS~(~'Azure))~status~(EQUALS~(~'Active)))))"
        },        
        { 
            "query_name": "Sree - Kubernetes Cluster Arch",
            "query_variable": {"id": "20af74ad-048a-4597-be31-f6ed6f035497"},
            "query_link": "https://demo.wiz.io/graph#~(query~(relationships~(~(type~(~(type~'CONTAINS))~with~(relationships~(~(type~(~(type~'CONTAINS))~with~(relationships~(~(type~(~(type~'OWNS))~with~(relationships~(~(type~(~(type~'OWNS))~with~(relationships~(~(optional~true~type~(~(type~'CONTAINS))~with~(relationships~(~(optional~true~type~(~(type~'INSTANCE_OF))~with~(relationships~(~(optional~true~type~(~(reverse~true~type~'ALERTED_ON))~with~(blockExpanded~true~blockName~'Has*20vulnerabilities~relationships~(~(optional~true~type~(~(reverse~true~type~'CAUSES))~with~(type~(~'VULNERABILITY))))~select~true~type~(~'SECURITY_TOOL_FINDING)~where~(severity~(EQUALS~(~'VulnerabilitySeverityCritical))))))~select~true~type~(~'CONTAINER_IMAGE)))~(optional~true~type~(~(type~'ACTING_AS))~with~(relationships~(~(optional~true~type~(~(reverse~true~type~'ENTITLES))~with~(blockExpanded~true~blockName~'Has*20High*20Permissions~relationships~(~(optional~true~type~(~(type~'ALLOWS))~with~(select~true~type~(~'ACCESS_ROLE_PERMISSION)~where~(accessTypes~(EQUALS~(~'HighPrivilege))))))~type~(~'IAM_BINDING)~where~(accessTypes~(EQUALS~(~'HighPrivilege)))))~(optional~true~type~(~(reverse~true~type~'ENTITLES))~with~(blockExpanded~true~blockName~'Data*20Access~relationships~(~(optional~true~type~(~(type~'ALLOWS_ACCESS_TO))~with~(select~true~type~(~'DATABASE~'DB_SERVER~'BUCKET))))~type~(~'IAM_BINDING)~where~(accessTypes~(EQUALS~(~'Data))))))~select~true~type~(~'SERVICE_ACCOUNT)~where~(hasHighPrivileges~(EQUALS~true)))))~select~true~type~(~'CONTAINER)))~(type~(~(reverse~true~type~'RUNS))~with~(relationships~(~(optional~true~type~(~(reverse~true~type~'SERVES))~with~(select~true~type~(~'VIRTUAL_MACHINE))))~select~true~type~(~'KUBERNETES_NODE))))~select~true~type~(~'POD))))~type~(~'REPLICA_SET))))~select~true~type~(~'DEPLOYMENT))))~select~true~type~(~'NAMESPACE))))~select~true~type~(~'KUBERNETES_CLUSTER)~where~(_vertexID~(EQUALS~'8cb8ba17-97f5-56f9-a68f-45d1f3c14ff6))))"
        }  
    ]


    print("\n====Checking for saved queries====\n")
    for saved_query in search_list:
        result = query_wiz_api(query,saved_query['query_variable'])
        # print(result)
        try:
            if result['data']['savedGraphQuery']['name']:
                print("Found saved query: " + saved_query['query_name'] + ". All is well. Continuing")
            else:
                print("Something went wrong with saved query check.\n" + result)

        except Exception as e:
            message = "====================\nQuery not found or unhandled exception. \nQuery name: " + saved_query['query_name'] + "\n Link to recreate: " + saved_query["query_link"] + "\n===================="
            print(message)

    try:
        return message
    except:
        return

