import grpc
import src.proto.booker_pb2 as booker_pb2
import src.proto.booker_pb2_grpc as booker_pb2_grpc

def test_grpc_client():
    channel = grpc.insecure_channel("localhost:50051")
    stub = booker_pb2_grpc.BookerServiceStub(channel)

    # Test availability check via gRPC
    request = booker_pb2.BookerRequest(
        user_id="usr_991823",
        message="Are there any available slots on 2026-09-10?"
    )

    print("Sending gRPC request to BookerService...")
    response = stub.ProcessUserMessage(request)

    print("\n--- gRPC Response ---")
    print(f"Tool Executed: {response.tool_executed}")
    print(f"Reply:\n{response.reply}")

if __name__ == "__main__":
    test_grpc_client()