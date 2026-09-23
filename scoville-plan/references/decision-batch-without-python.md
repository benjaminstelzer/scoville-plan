# Decision batch without Python

Use an already installed byte-exact SHA-256 primitive. Validate the date,
unique IDs, authorized order, normalized root-contained relative paths, and
regular non-symlink files. Hash each file as raw bytes. Construct the UTF-8
payload specified in [native-decision-batches.md](native-decision-batches.md)
with one LF after every line, including the last, then hash that payload.
Record and compare ordered IDs and per-file hashes before using the result.
If no byte-exact primitive is available, stop instead of guessing a hash.
