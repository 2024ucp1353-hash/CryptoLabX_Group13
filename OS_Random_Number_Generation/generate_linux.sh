
#!/bin/bash

# Create data folder if it does not exist
mkdir -p data

echo "Generating random data..."

# Generate 1 MiB using Linux /dev/urandom
dd if=/dev/urandom of=data/linux_urandom.bin bs=1M count=1 status=progress

# Generate 1 MiB using OpenSSL
openssl rand -out data/openssl_rand.bin 1048576

echo ""
echo "Random data generation completed!"

# Display file sizes
echo "Linux /dev/urandom:"
wc -c data/linux_urandom.bin

echo "OpenSSL:"
wc -c data/openssl_rand.bin
