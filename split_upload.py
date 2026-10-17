import gzip
import subprocess
import sys

def upload_chunk(chunk_data, chunk_index):
    file_name = f"/project/input/reviews_part_{chunk_index:04d}.json"
    print(f"Uploading {file_name}...")
    
    # Use hdfs dfs -put - to stream data into HDFS
    proc = subprocess.Popen(['hdfs', 'dfs', '-put', '-', file_name], stdin=subprocess.PIPE)
    proc.communicate(input=chunk_data.encode('utf-8'))
    
    if proc.returncode != 0:
        print(f"Failed to upload {file_name}")
        sys.exit(1)

def main():
    input_gz = "/project/input/All_Amazon_Review.json.gz"
    
    # Read from HDFS using hdfs dfs -text
    print(f"Opening HDFS stream for {input_gz}...")
    hdfs_read = subprocess.Popen(['hdfs', 'dfs', '-text', input_gz], stdout=subprocess.PIPE, text=True)
    
    chunk_size_lines = 1000000  # 1 million lines per chunk (~ 1 GB)
    current_chunk = []
    chunk_index = 0
    
    for line in hdfs_read.stdout:
        current_chunk.append(line)
        if len(current_chunk) >= chunk_size_lines:
            upload_chunk("".join(current_chunk), chunk_index)
            current_chunk = []
            chunk_index += 1
            
    if current_chunk:
        upload_chunk("".join(current_chunk), chunk_index)
        
    print("Done splitting and uploading!")

if __name__ == "__main__":
    main()
