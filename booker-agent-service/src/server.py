import os
import concurrent.futures
import grpc
from dotenv import load_dotenv

import src.proto.booker_pb2 as booker_pb2
import src.proto.booker_pb2_grpc as booker_pb2_grpc
from src.agent.core import run_booker

load_dotenv()

class BookerServicer(booker_pb2_grpc.BookerServiceServicer):
    def ProcessUserMessage(self, request, context):
        print(f"\n[gRPC Inbound] User ID: {request.user_id} | Msg: {request.message}")
        
        try:
            raw_reply = run_booker(request.message, user_id=str(request.user_id))
            
            clean_reply = str(raw_reply) if raw_reply is not None else ""
            
            return booker_pb2.BookerResponse(
                reply=clean_reply,
                tool_executed=True
            )
        except Exception as e:
            print(f"[gRPC Error] Execution failed: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return booker_pb2.BookerResponse()

def serve():
    port = os.getenv("GRPC_PORT", "50051")
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    
    booker_pb2_grpc.add_BookerServiceServicer_to_server(BookerServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    
    print(f"🚀 Booker gRPC Service active on port {port}...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()