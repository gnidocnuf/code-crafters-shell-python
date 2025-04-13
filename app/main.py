import sys
import os
import zlib
import hashlib

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    #Uncomment this block to pass the first stage
    
    command = sys.argv[1]

    # object_id = ""
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
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
        if not os.path.exists(sys.argv[3]): 
            print(f"File {sys.argv[3]} not found")
            return
        with open(sys.argv[3], "rb") as f:
            data = f.read()

        # create the header for git object
        header = f"blob {len(data)}\0".encode()
        # concatenate the header and data
        data = header + data
        upper_dir = os.path.join(".git", "objects", str(hashlib.sha1(data).hexdigest()[:2]))
        object_id = hashlib.sha1(data).hexdigest()
        object_path = os.path.join(".git", "objects", object_id[:2], object_id[2:])    
        # create the directory if it doesn't exist
        os.makedirs(os.path.dirname(object_path), exist_ok=True)
        # write the data to the object file
        with open(object_path, "wb") as f:
            data = zlib.compress(data)
            f.write(data)   
        print(object_id)
    elif command == "ls-tree":
        if len(sys.argv) < 4:
            print("Usage: ls-tree <object-id>")
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
        header, content = decompressed_data.split(b'\0', 1)

        # make sure the object is a tree
        if not header.startswith(b"tree"):
            print(f"Object {object_id} is not a tree")
            return
        
        # parse tree content
        index = 0 
        while index < len(content):
            # Extract the mode (e.g., "40000" for directories or "100644" for files)
            mode_end = content.find(b' ', index)
            mode = content[index:mode_end].decode()

            # Extract the file name
            name_end = content.find(b'\0', mode_end + 1)
            name = content[mode_end + 1:name_end].decode()

            # Extract the hash (20 bytes after the null terminator)
            sha = content[name_end + 1:name_end + 21]
            sha_hex = sha.hex()

            print(f"{name}")
            # Move to the next entry
            index = name_end + 21

    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
