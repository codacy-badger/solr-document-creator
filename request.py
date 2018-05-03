import time
import requests

SOLR_HOST = "localhost"
SOLR_PORT = "8983"
SOLR_COLLECTION = "payloads"
BASIC_REQUEST_URL = "http://{0}:{1}/solr/{2}/select?".format(SOLR_HOST, SOLR_PORT, SOLR_COLLECTION)
EXECUTIONS_PER_QUERY = 100

QUERY_ALL = "q=*:*"
QUERY_PAYLOAD_ABOVE_THRESHOLD = "q={!frange%20l=0.7}payload(classifications_dpf,first_classifier:class_one)"
QUERY_AWESOME_NUMBER_ABOVE_THRESHOLD = "q=awesome_number:%5B0.7+TO+1.0%5D"
QUERY_BY_AWESOME_MULTI_FIELD = "q=awesome_multi_field:%22first_classifier:class_three%22"
FL_SINGLE_FIELD = "fl=id,class_one:payload(classifications_dpf,first_classifier:class_one)"
SORT_BY_AWESOME_STRING = "sort=awesome_string+desc"
SORT_BY_AWESOME_NUMBER = "sort=awesome_string+desc"
SORT_BY_ONE_PAYLOAD = "sort=payload(classifications_dpf,first_classifier:class_one)+desc"
SORT_BY_TWO_PAYLOADS = "sort=payload(classifications_dpf,first_classifier:class_one)+desc,payload(classifications_dpf,first_classifier:class_two)+asc"
RESPONSE_FORMAT = "wt=json"
INDENT_ON = "indent=on"

non_payload_queries = [
    "{0}&{1}&{2}".format(QUERY_ALL, RESPONSE_FORMAT, INDENT_ON),
    "{0}&{1}&{2}".format(QUERY_AWESOME_NUMBER_ABOVE_THRESHOLD, RESPONSE_FORMAT, INDENT_ON),
    "{0}&{1}&{2}".format(QUERY_BY_AWESOME_MULTI_FIELD, RESPONSE_FORMAT, INDENT_ON),
    "{0}&{1}&{2}&{3}".format(QUERY_ALL, SORT_BY_AWESOME_NUMBER, RESPONSE_FORMAT, INDENT_ON),
    "{0}&{1}&{2}&{3}".format(QUERY_AWESOME_NUMBER_ABOVE_THRESHOLD, SORT_BY_AWESOME_NUMBER, RESPONSE_FORMAT, INDENT_ON),
    "{0}&{1}&{2}&{3}".format(QUERY_ALL, SORT_BY_AWESOME_STRING, RESPONSE_FORMAT, INDENT_ON)
]

payload_queries = [
    "{0}&{1}&{2}".format(QUERY_PAYLOAD_ABOVE_THRESHOLD, RESPONSE_FORMAT, INDENT_ON),
    "{0}&{1}&{2}&{3}".format(QUERY_PAYLOAD_ABOVE_THRESHOLD, FL_SINGLE_FIELD, RESPONSE_FORMAT, INDENT_ON),
    "{0}&{1}&{2}&{3}".format(QUERY_ALL, SORT_BY_ONE_PAYLOAD, RESPONSE_FORMAT, INDENT_ON),
    "{0}&{1}&{2}&{3}".format(QUERY_ALL, SORT_BY_TWO_PAYLOADS, RESPONSE_FORMAT, INDENT_ON),
    "{0}&{1}&{2}&{3}".format(QUERY_PAYLOAD_ABOVE_THRESHOLD, SORT_BY_ONE_PAYLOAD, RESPONSE_FORMAT, INDENT_ON),
    "{0}&{1}&{2}&{3}".format(QUERY_PAYLOAD_ABOVE_THRESHOLD, SORT_BY_TWO_PAYLOADS, RESPONSE_FORMAT, INDENT_ON),
    "{0}&{1}&{2}&{3}&{4}".format(QUERY_ALL, SORT_BY_TWO_PAYLOADS, FL_SINGLE_FIELD, RESPONSE_FORMAT, INDENT_ON),
    "{0}&{1}&{2}&{3}&{4}".format(QUERY_PAYLOAD_ABOVE_THRESHOLD, SORT_BY_TWO_PAYLOADS, FL_SINGLE_FIELD, RESPONSE_FORMAT,
                                 INDENT_ON)
]


def measure(query, f):
    successful_queries = 0
    non_successful_queries = 0
    sum_of_times = 0.0
    first_time = 0.0
    full_request = "{0}{1}".format(BASIC_REQUEST_URL, query)
    for i in range(0, EXECUTIONS_PER_QUERY):
        start_time = time.time()
        response = requests.request("GET", full_request)
        if response.status_code is 200:
            successful_queries += 1
            execution_time = time.time() - start_time
            sum_of_times += execution_time
            if i == 0:
                first_time = execution_time
        else:
            non_successful_queries += 1
    print("{0} ({1} successful, {2} non-successful)\n".format(query, successful_queries, non_successful_queries))
    f.write("{0} ({1} successful, {2} non-successful)\n".format(query, successful_queries, non_successful_queries))
    f.write(
        "\t{0}\tseconds (first)\n\t{1}\tseconds (average)\n".format(first_time, sum_of_times / EXECUTIONS_PER_QUERY))


def run():
    with open('outfile', 'a') as f:
        f.write("Calculating the average execution times of {0} requests per query\n".format(EXECUTIONS_PER_QUERY))
        f.write("##### non-payload queries #####\n")
        for query in non_payload_queries:
            measure(query, f)
        f.write("\n##### payload queries #####\n")
        for query in payload_queries:
            measure(query, f)


if __name__ == '__main__':
    run()