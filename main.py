import grpc
import time
import vector_service_pb2, vector_service_pb2_grpc
from datasets import load_dataset
import numpy as np
import matplotlib.pyplot as plt


def create_stub():
    channel = grpc.insecure_channel('localhost:50051')
    return vector_service_pb2_grpc.VectorServiceStub(channel), channel


def send_get_embedding_request(stub, text):
    request = vector_service_pb2.GetEmbeddingRequest(input_text=text)
    response = stub.GetEmbedding(request)
    # print("Received embedding response:", response.resulting_embedding.values[:5], "...")

    return response.resulting_embedding


def send_get_similarity_request(stub, embedding):
    request = vector_service_pb2.GetSimilarityRequest(input_embedding=embedding)
    response = stub.GetSimilarity(request)
    # print("Received similarity response.")

    return response.matches, response.scores


def send_load_queries_request(stub, queries, thresholds):
    request = vector_service_pb2.LoadQueryRequest(queries=queries, thresholds=thresholds)
    response = stub.LoadQueries(request)
    # print("Received load queries response.")


if __name__ == '__main__':
    dataset = load_dataset("tweet_eval", "emoji")
    texts = dataset['train'][:]['text']

    test_nums = [10, 100, 500, 1000, 2500, 5000]

    query_load_times = []

    for num_queries in test_nums:
        queries = texts[:num_queries]
        # thresholds = [0.8 + np.random.rand() * 0.2 for _ in range(len(queries))]
        thresholds = [0.8 for _ in range(len(queries))]
        input_stream = texts[num_queries:]

        request_times = []
        embed_request_times = []
        sim_request_times = []
        num_matches = []

        try:
            rpc_stub, channel = create_stub()
            # print("Loading %d queries." % len(queries))
            # print("Sending load queries request...")
            query_load_time = time.time()
            send_load_queries_request(rpc_stub, queries, thresholds)
            query_load_end_time = time.time()
            # print("Query load time:", query_load_end_time - query_load_time)
            query_load_times.append(query_load_end_time - query_load_time)

            while input_stream:
                current_input = input_stream.pop()

                # print("Sending get embedding request...")
                embedding_time = time.time()
                embedding = send_get_embedding_request(rpc_stub, current_input)
                embedding_end_time = time.time()
                # print("Embedding time:", embedding_end_time - embedding_time)

                # print("Sending get similarity request...")
                similarity_time = time.time()
                matches, scores = send_get_similarity_request(rpc_stub, embedding)
                similarity_end_time = time.time()
                # print("Similarity time:", similarity_end_time - similarity_time)
                # print("Input:", current_input)
                # print("Matches:", matches)
                # print("Scores:", scores)
                # print("Number of matches:", len(matches))
                # print("Total request time:", similarity_end_time - embedding_time)
                request_times.append(similarity_end_time - embedding_time)
                embed_request_times.append(embedding_end_time - embedding_time)
                sim_request_times.append(similarity_end_time - embedding_end_time)
                num_matches.append(len(matches))

                # time.sleep(2 - (embedding_end_time - embedding_time) - (similarity_end_time - similarity_time))
                if len(request_times) == num_queries:
                    break

            channel.close()
            # print("Average request time:", np.mean(request_times))
            # print("Number of requests:", len(request_times))
            # plot request times, embedding time, sim time
            plt.plot(request_times, label="Total request time")
            plt.plot(embed_request_times, label="Embedding time")
            plt.plot(sim_request_times, label="Similarity time")
            plt.title("Request times for %d queries" % len(queries))
            # show average request time
            plt.axhline(y=np.mean(request_times), color='r', linestyle='-', label="Average request time")
            # show average embedding time
            plt.axhline(y=np.mean(embed_request_times), color='g', linestyle='-', label="Average embedding time")
            # show average similarity time
            plt.axhline(y=np.mean(sim_request_times), color='b', linestyle='-', label="Average similarity time")
            plt.legend()
            plt.xlabel("Request number")
            plt.ylabel("Request time")
            plt.show()
            # plot how number of matches affects request time
            plt.plot(num_matches, request_times, 'o')
            plt.title("Request time vs number of matches")
            plt.xlabel("Number of matches")
            plt.ylabel("Request time")
            plt.show()
            # length of input vs embedding time
            plt.plot([len(text) for text in input_stream[:len(request_times)]], embed_request_times, 'o')
            plt.title("Embedding time vs length of input")
            plt.xlabel("Length of input")
            plt.ylabel("Embedding time")
            plt.show()

            print("finished %d queries" % num_queries)

        except KeyboardInterrupt:
            print("Average request time:", np.mean(request_times))
            print("Number of requests:", len(request_times))
            print("Script terminated by user.")

    # plot query load times
    plt.plot(test_nums, query_load_times)
    plt.xlabel("Number of queries")
    plt.ylabel("Query load time")
    plt.show()