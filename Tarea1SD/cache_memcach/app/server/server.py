import socket
import memcache
import argparse

class CacheService:
    def __init__(self, host="localhost", port=11211):
        self.cache = memcache.Client([f"{host}:{port}"], debug=0)

    def get(self, key):
        value = self.cache.get(key)
        if value:
            return value.decode()
        else:
            return None

    def put(self, key, value):
        self.cache.set(key, value)

    def remove(self, key):
        self.cache.delete(key)

def serve(port=11211):
    cache_service = CacheService(port=port)
    print(f"Cache server started on port {port}")

    while True:
        try:
            key = input("Enter key (or 'exit' to quit): ")
            if key == "exit":
                break

            operation = input("Enter operation (get/put/remove): ")
            if operation == "get":
                value = cache_service.get(key)
                if value is not None:
                    print(f"Value: {value}")
                else:
                    print("Key not found in cache.")
            elif operation == "put":
                value = input("Enter value: ")
                cache_service.put(key, value)
                print("Value inserted into cache.")
            elif operation == "remove":
                cache_service.remove(key)
                print("Key removed from cache.")
            else:
                print("Invalid operation. Use 'get', 'put', or 'remove'.")
        except KeyboardInterrupt:
            print("\nServer terminated.")
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Memcached Cache Server")
    parser.add_argument("port", type=int, default=11211, help="Port number to start the cache server on")

    args = parser.parse_args()
    serve(port=args.port)
