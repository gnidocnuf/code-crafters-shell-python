import sys
import os
import zlib

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    #Uncomment this block to pass the first stage
    
    command = sys.argv[1]
    # print(f"Commands: {sys.argv}")
    # for i in enumerate(sys.argv):
    #     print(f"Command {i}")

    # object_id = ""
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    # elif command == "hash-object":  
    #     if len(sys.argv) < 3:
    #         print("Usage: hash-object <file>")
    #         return
    #     file_path = sys.argv[2]
    #     if not os.path.exists(file_path):
    #         print(f"File {file_path} not found")
    #         return
    #     with open(file_path, "rb") as f:
    #         data = f.read()
    #     object_id = hash(data)
    #     object_path = os.path.join(".git", "objects", str(object_id))
    #     with open(object_path, "wb") as f:
    #         f.write(data)
    #     print(f"Object {object_id} created at {object_path}")
    #     print(f"{object_id} created at path:  {object_path}")
    
    elif command == "cat-file":
        if len(sys.argv) < 4:
            print("Usage: cat-file <object-id>")
            return
        object_id = sys.argv[3]

        object_path = os.path.join(".git", "objects", object_id[:2], object_id[2:])
        if not os.path.exists(object_path):
            print(f"Object {object_id} not found")
            return
        with open(object_path, "rb") as f:
            data = f.read()

        # Decompress the data
        decompressed_data = zlib.decompress(data)
        # Split the decompressed data into header and content
        # header, content = decompressed_data.split(b'\0', 1)
        _, content = decompressed_data.split(b'\0', 1)
      
        sys.stdout.buffer.write(content)
    
    elif command == "hash-object":
        if len(sys.argv) < 4:
            print("Usage: hash-object <file>")
            return
        for i in range(1, len(sys.argv)):
            print(f"Command {i}: {sys.argv[i]}")
        # file_path = sys.argv[2]
        # if not os.path.exists(file_path):
        #     print(f"File {file_path} not found")
        #     return
        # with open(file_path, "rb") as f:
        #     data = f.read()
        # object_id = hash(data)
        # object_path = os.path.join(".git", "objects", str(object_id))
        # with open(object_path, "wb") as f:
        #     f.write(data)
        # print(object_id)
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
